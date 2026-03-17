"""
Persistent Memoization for Tool Calls.

Integrates with the Factory's Hybrid Memory Architecture.
"""

import json
import hashlib
import os
import time
import logging
from typing import Any, Callable, Dict, Optional, Union, TypeVar
from datetime import datetime
from functools import wraps

T = TypeVar("T")
logger = logging.getLogger(__name__)

DEFAULT_CACHE_PATH = ".agent/cache/tool-cache.json"


class Memoizer:
    """
    A persistent memoization system for deterministic utility functions.
    """

    def __init__(self, persistence_file: str = DEFAULT_CACHE_PATH):
        self.persistence_file = os.path.abspath(persistence_file)
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)
        if not os.path.exists(self.persistence_file):
            with open(self.persistence_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generates a stable unique hash for a call."""
        # Inclusion of func_name prevents collisions between different functions with same args
        payload = {"func": func_name, "args": list(args), "kwargs": kwargs}
        arg_str = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(arg_str.encode()).hexdigest()

    def get_cached_result(self, func_name: str, *args, **kwargs) -> Optional[Any]:
        """Retrieve a result from the local JSON cache if not expired."""
        key = self._generate_key(func_name, args, kwargs)

        try:
            with open(self.persistence_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
                if key in cache:
                    entry = cache[key]
                    expires_at = entry.get("expires_at")
                    if expires_at is None or expires_at > time.time():
                        return entry["result"]
        except Exception as e:
            logger.debug(f"Cache miss or error for {key}: {e}")

        return None

    def cache_result(
        self, func_name: str, result: Any, ttl: int = 86400, *args, **kwargs
    ):
        """Stores a result in the persistent cache."""
        key = self._generate_key(func_name, args, kwargs)
        expires_at = time.time() + ttl

        try:
            # Ensure directory exists right before write
            os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)

            cache = {}
            if os.path.exists(self.persistence_file):
                with open(self.persistence_file, "r", encoding="utf-8") as f:
                    cache = json.load(f)

            cache[key] = {
                "function": func_name,
                "args": list(args),
                "kwargs": kwargs,
                "result": result,
                "cached_at": datetime.now().isoformat(),
                "expires_at": expires_at,
            }

            with open(self.persistence_file, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to cache result for {func_name}: {e}")


def memoize_persistent(ttl: int = 86400, cache_path: str = DEFAULT_CACHE_PATH):
    """
    Decorator for functions to enable persistent memoization.
    """
    memoizer = Memoizer(persistence_file=cache_path)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            cached = memoizer.get_cached_result(func.__name__, *args, **kwargs)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            memoizer.cache_result(func.__name__, result, ttl, *args, **kwargs)
            return result

        return wrapper

    return decorator
