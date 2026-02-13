---
description: Structured logging with structlog, metrics collection, alerting patterns,
  and distributed tracing
name: logging-monitoring
type: skill
---
# Logging Monitoring

Structured logging with structlog, metrics collection, alerting patterns, and distributed tracing

Implement comprehensive logging, metrics collection, alerting, and distributed tracing for production agent systems.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Structured Logging with Structlog

```python
import structlog
from structlog.types import Processor

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

# Get logger
logger = structlog.get_logger()

# Usage
logger.info(
    "agent_request",
    user_id="user_123",
    query="What is Python?",
    model="gemini-2.5-flash"
)

logger.error(
    "agent_error",
    error="Rate limit exceeded",
    user_id="user_123",
    retry_count=3
)
```

### Step 2: Contextual Logging

```python
from structlog import contextvars

class AgentLogger:
    """Logger with request context."""
    
    def __init__(self):
        self.logger = structlog.get_logger()
    
    def bind_context(self, **kwargs):
        """Bind context variables."""
        contextvars.bind_contextvars(**kwargs)
        return self.logger
    
    def log_request(self, user_id: str, query: str, **kwargs):
        """Log agent request."""
        self.bind_context(user_id=user_id, request_id=kwargs.get("request_id"))
        self.logger.info(
            "agent_request",
            query=query,
            **kwargs
        )
    
    def log_response(self, response: str, latency: float, **kwargs):
        """Log agent response."""
        self.logger.info(
            "agent_response",
            response_length=len(response),
            latency_ms=latency * 1000,
            **kwargs
        )
    
    def log_error(self, error: Exception, **kwargs):
        """Log error with context."""
        self.logger.error(
            "agent_error",
            error_type=type(error).__name__,
            error_message=str(error),
            exc_info=True,
            **kwargs
        )

# Usage
agent_logger = AgentLogger()

agent_logger.log_request(
    user_id="user_123",
    query="Hello",
    request_id="req_456"
)

try:
    response = await agent.ainvoke("Hello")
    agent_logger.log_response(response, latency=1.2)
except Exception as e:
    agent_logger.log_error(e)
```

### Step 3: Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from typing import Optional
import time

# Define metrics
agent_requests_total = Counter(
    'agent_requests_total',
    'Total agent requests',
    ['model', 'status']
)

agent_request_duration = Histogram(
    'agent_request_duration_seconds',
    'Agent request duration',
    ['model'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

agent_tokens_generated = Counter(
    'agent_tokens_generated_total',
    'Total tokens generated',
    ['model']
)

agent_active_requests = Gauge(
    'agent_active_requests',
    'Currently active agent requests'
)

class MetricsCollector:
    """Collect agent metrics."""
    
    @staticmethod
    def record_request(model: str, status: str = "success"):
        """Record agent request."""
        agent_requests_total.labels(model=model, status=status).inc()
    
    @staticmethod
    def record_duration(model: str, duration: float):
        """Record request duration."""
        agent_request_duration.labels(model=model).observe(duration)
    
    @staticmethod
    def record_tokens(model: str, count: int):
        """Record tokens generated."""
        agent_tokens_generated.labels(model=model).inc(count)
    
    @staticmethod
    def increment_active():
        """Increment active requests."""
        agent_active_requests.inc()
    
    @staticmethod
    def decrement_active():
        """Decrement active requests."""
        agent_active_requests.dec()

# Usage
start_http_server(8000)  # Expose metrics on :8000/metrics

async def monitored_agent_call(query: str, model: str):
    """Agent call with metrics."""
    MetricsCollector.increment_active()
    start_time = time.time()
    
    try:
        response = await agent.ainvoke(query)
        
        # Record metrics
        MetricsCollector.record_request(model, "success")
        MetricsCollector.record_duration(model, time.time() - start_time)
        
        # Estimate tokens (rough)
        token_count = len(response.content.split()) * 1.3
        MetricsCollector.record_tokens(model, int(token_count))
        
        return response
    except Exception as e:
        MetricsCollector.record_request(model, "error")
        raise
    finally:
        MetricsCollector.decrement_active()
```

### Step 4: Custom Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

class AgentMetrics:
    """Custom agent metrics."""
    
    def __init__(self):
        self.tool_calls = Counter(
            'agent_tool_calls_total',
            'Total tool calls',
            ['tool_name', 'status']
        )
        
        self.cache_hits = Counter(
            'agent_cache_hits_total',
            'Cache hits',
            ['cache_type']
        )
        
        self.cache_misses = Counter(
            'agent_cache_misses_total',
            'Cache misses',
            ['cache_type']
        )
        
        self.queue_size = Gauge(
            'agent_queue_size',
            'Request queue size'
        )
        
        self.error_rate = Gauge(
            'agent_error_rate',
            'Error rate (errors per minute)'
        )
    
    def record_tool_call(self, tool_name: str, success: bool):
        """Record tool call."""
        status = "success" if success else "error"
        self.tool_calls.labels(tool_name=tool_name, status=status).inc()
    
    def record_cache_hit(self, cache_type: str):
        """Record cache hit."""
        self.cache_hits.labels(cache_type=cache_type).inc()
    
    def record_cache_miss(self, cache_type: str):
        """Record cache miss."""
        self.cache_misses.labels(cache_type=cache_type).inc()
    
    def set_queue_size(self, size: int):
        """Set queue size."""
        self.queue_size.set(size)
    
    def set_error_rate(self, rate: float):
        """Set error rate."""
        self.error_rate.set(rate)

# Usage
metrics = AgentMetrics()
metrics.record_tool_call("web_search", success=True)
metrics.record_cache_hit("semantic")
```

### Step 5: Alerting Patterns

```python
from typing import Callable, Optional
from datetime import datetime, timedelta
from collections import deque

class AlertManager:
    """Manage alerts based on metrics."""
    
    def __init__(self):
        self.alerts: dict[str, dict] = {}
        self.error_history: deque = deque(maxlen=100)
    
    def check_error_rate(self, threshold: float = 0.1) -> Optional[str]:
        """Check if error rate exceeds threshold."""
        if len(self.error_history) < 10:
            return None
        
        recent_errors = sum(
            1 for entry in list(self.error_history)[-10:]
            if entry.get("status") == "error"
        )
        
        error_rate = recent_errors / 10
        if error_rate > threshold:
            return f"High error rate: {error_rate:.1%} (threshold: {threshold:.1%})"
        
        return None
    
    def check_latency(self, recent_latencies: list[float], threshold: float = 5.0) -> Optional[str]:
        """Check if latency exceeds threshold."""
        if not recent_latencies:
            return None
        
        avg_latency = sum(recent_latencies) / len(recent_latencies)
        if avg_latency > threshold:
            return f"High latency: {avg_latency:.2f}s (threshold: {threshold}s)"
        
        return None
    
    def record_request(self, status: str, latency: float):
        """Record request for alerting."""
        self.error_history.append({
            "status": status,
            "latency": latency,
            "timestamp": datetime.now()
        })
    
    def check_alerts(self) -> list[str]:
        """Check all alert conditions."""
        alerts = []
        
        # Check error rate
        error_alert = self.check_error_rate()
        if error_alert:
            alerts.append(error_alert)
        
        # Check latency
        recent_latencies = [
            entry["latency"]
            for entry in list(self.error_history)[-10:]
        ]
        latency_alert = self.check_latency(recent_latencies)
        if latency_alert:
            alerts.append(latency_alert)
        
        return alerts

# Usage
alert_manager = AlertManager()

# Record requests
alert_manager.record_request("success", 1.2)
alert_manager.record_request("error", 0.5)
alert_manager.record_request("error", 0.6)

# Check alerts
alerts = alert_manager.check_alerts()
for alert in alerts:
    logger.warning("alert", message=alert)
    # Send to alerting system (PagerDuty, Slack, etc.)
```

### Step 6: Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.langchain import LangChainInstrumentor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export to OTLP (Jaeger, Tempo, etc.)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument LangChain
LangChainInstrumentor().instrument()

# Manual tracing
async def traced_agent_call(query: str):
    """Agent call with tracing."""
    with tracer.start_as_current_span("agent.request") as span:
        span.set_attribute("query", query)
        span.set_attribute("model", "gemini-2.5-flash")
        
        try:
            with tracer.start_as_current_span("agent.llm_call"):
                response = await llm.ainvoke(query)
            
            span.set_attribute("response_length", len(response.content))
            span.set_status(trace.Status(trace.StatusCode.OK))
            
            return response
        except Exception as e:
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            span.record_exception(e)
            raise
```

### Step 7: Health Checks

```python
from typing import Dict, Any
from datetime import datetime
import asyncio

class HealthChecker:
    """Check agent system health."""
    
    def __init__(self):
        self.checks: dict[str, Callable] = {}
    
    def register_check(self, name: str, check_func: Callable):
        """Register a health check."""
        self.checks[name] = check_func
    
    async def check_llm_health(self) -> dict[str, Any]:
        """Check LLM availability."""
        try:
            start = time.time()
            response = await llm.ainvoke("health check")
            latency = time.time() - start
            
            return {
                "status": "healthy",
                "latency_ms": latency * 1000,
                "response_received": True
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def check_cache_health(self) -> dict[str, Any]:
        """Check cache health."""
        try:
            # Test cache read/write
            test_key = "health_check"
            cache.set(test_key, "test")
            value = cache.get(test_key)
            
            return {
                "status": "healthy" if value == "test" else "unhealthy",
                "read_write_ok": value == "test"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def run_all_checks(self) -> dict[str, Any]:
        """Run all health checks."""
        results = {}
        
        for name, check_func in self.checks.items():
            try:
                if asyncio.iscoroutinefunction(check_func):
                    results[name] = await check_func()
                else:
                    results[name] = check_func()
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Overall status
        all_healthy = all(
            result.get("status") == "healthy"
            for result in results.values()
        )
        
        return {
            "status": "healthy" if all_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "checks": results
        }

# Usage
health_checker = HealthChecker()
health_checker.register_check("llm", health_checker.check_llm_health)
health_checker.register_check("cache", health_checker.check_cache_health)

# Health endpoint
@app.get("/health")
async def health():
    return await health_checker.run_all_checks()
```

### Step 8: Log Aggregation

```python
import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
import json

class StructuredFileHandler(RotatingFileHandler):
    """File handler that writes structured logs."""
    
    def emit(self, record):
        """Emit structured log record."""
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        
        # Add exception info
        if record.exc_info:
            log_entry["exception"] = self.format(record)
        
        self.stream.write(json.dumps(log_entry) + "\n")
        self.stream.flush()

# Setup logging
def setup_logging(log_file: str = "agent.log"):
    """Setup structured logging."""
    handler = StructuredFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        format="%(message)s"  # JSON format
    )
```

## Logging Levels

| Level | Use Case | Example |
|-------|----------|---------|
| DEBUG | Detailed debugging | Function entry/exit |
| INFO | Normal operations | Request received |
| WARNING | Recoverable issues | Rate limit approaching |
| ERROR | Errors that are handled | Retry after error |
| CRITICAL | System failures | Service unavailable |

## Metrics Types

| Type | Use Case | Example |
|------|----------|---------|
| Counter | Count events | Total requests |
| Gauge | Current value | Active requests |
| Histogram | Distribution | Request latency |
| Summary | Percentiles | Response time |

## Best Practices

- Use structured logging (JSON)
- Include request IDs for tracing
- Log at appropriate levels
- Don't log sensitive data
- Use metrics for monitoring
- Set up alerting thresholds
- Trace distributed requests
- Rotate log files

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Unstructured logs | Use structured logging |
| No request IDs | Add request IDs |
| Logging secrets | Filter sensitive data |
| Too verbose | Use appropriate log levels |
| No metrics | Add Prometheus metrics |
| No alerts | Set up alerting |
| No tracing | Use OpenTelemetry |
| Logging everything | Log selectively |

## Related

- Skill: `langsmith-tracing`
- Skill: `error-handling`
- Skill: `agent-testing`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
