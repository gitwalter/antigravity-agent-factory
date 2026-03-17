import time
import os
import pytest
from scripts.ai.core.memoization import memoize_persistent


@memoize_persistent(ttl=2, cache_path=".tmp/test-cache.json")
def dummy_func(n):
    return n * 10


def test_memoization_logic():
    # Ensure .tmp directory exists
    os.makedirs(".tmp", exist_ok=True)

    # Clear cache file if exists
    cache_file = os.path.abspath(".tmp/test-cache.json")
    if os.path.exists(cache_file):
        os.remove(cache_file)

    # First call (miss)
    assert dummy_func(5) == 50
    assert os.path.exists(cache_file)

    # Second call (hit - should be faster/same result)
    assert dummy_func(5) == 50
