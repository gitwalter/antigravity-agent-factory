---
description: Monitor ML model performance, data drift, LLM observability, and production
  metrics
name: ml-monitoring
type: skill
---
# Ml Monitoring

Monitor ML model performance, data drift, LLM observability, and production metrics

Monitor machine learning models in production for performance degradation, data drift, latency issues, and cost tracking.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Model Performance Monitoring

```python
# performance_monitoring.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class PredictionRecord:
    timestamp: datetime
    input: str
    prediction: str
    actual: str = None
    latency_ms: float = None
    model_version: str = None

class ModelPerformanceMonitor:
    """Monitor model performance metrics."""

    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.predictions: List[PredictionRecord] = []
        self.metrics_history = []

    def record_prediction(self, record: PredictionRecord):
        """Record a prediction."""
        self.predictions.append(record)

        # Keep only recent predictions
        if len(self.predictions) > self.window_size:
            self.predictions = self.predictions[-self.window_size:]

    def calculate_accuracy(self, window_minutes: int = 60) -> float:
        """Calculate accuracy over time window."""
        cutoff = datetime.now() - timedelta(minutes=window_minutes)
        recent = [
            p for p in self.predictions
            if p.timestamp >= cutoff and p.actual is not None
        ]

        if not recent:
            return None

        correct = sum(1 for p in recent if p.prediction == p.actual)
        return correct / len(recent)

    def detect_accuracy_drift(
        self,
        baseline_accuracy: float,
        threshold: float = 0.05,
    ) -> bool:
        """Detect if accuracy has drifted significantly."""
        current_accuracy = self.calculate_accuracy()

        if current_accuracy is None:
            return False

        drift = baseline_accuracy - current_accuracy
        return drift > threshold

    def get_latency_stats(self) -> Dict:
        """Get latency statistics."""
        latencies = [p.latency_ms for p in self.predictions if p.latency_ms]

        if not latencies:
            return {}

        return {
            "mean": np.mean(latencies),
            "median": np.median(latencies),
            "p95": np.percentile(latencies, 95),
            "p99": np.percentile(latencies, 99),
            "max": np.max(latencies),
        }

    def get_performance_report(self) -> Dict:
        """Generate performance report."""
        return {
            "total_predictions": len(self.predictions),
            "accuracy": self.calculate_accuracy(),
            "latency_stats": self.get_latency_stats(),
            "predictions_per_minute": self._calculate_throughput(),
        }

    def _calculate_throughput(self) -> float:
        """Calculate predictions per minute."""
        if len(self.predictions) < 2:
            return 0.0

        time_span = (
            self.predictions[-1].timestamp - self.predictions[0].timestamp
        ).total_seconds() / 60

        if time_span == 0:
            return 0.0

        return len(self.predictions) / time_span
```

### Step 2: Data Drift Detection with Evidently AI

```python
# data_drift_detection.py
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import (
    DataDriftTable,
    DatasetDriftMetric,
    ColumnDriftMetric,
)
import pandas as pd

class DataDriftMonitor:
    """Monitor data drift using Evidently AI."""

    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.column_mapping = ColumnMapping(
            target=None,
            prediction="prediction",
            numerical_features=list(reference_data.select_dtypes(include=[np.number]).columns),
            categorical_features=list(reference_data.select_dtypes(include=["object"]).columns),
        )

    def check_drift(
        self,
        current_data: pd.DataFrame,
        threshold: float = 0.1,
    ) -> Dict:
        """Check for data drift."""

        # Create drift report
        report = Report(metrics=[
            DatasetDriftMetric(),
            DataDriftTable(),
        ])

        report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping,
        )

        # Extract drift information
        result = report.as_dict()
        dataset_drift = result["metrics"][0]["result"]["dataset_drift"]
        drift_score = result["metrics"][0]["result"]["drift_score"]

        # Get column-level drift
        drifted_columns = []
        if len(result["metrics"]) > 1:
            for col_result in result["metrics"][1]["result"]["drift_by_columns"]:
                if col_result["drift_detected"]:
                    drifted_columns.append({
                        "column": col_result["column_name"],
                        "drift_score": col_result["drift_score"],
                    })

        return {
            "dataset_drift_detected": dataset_drift,
            "drift_score": drift_score,
            "drifted_columns": drifted_columns,
            "threshold": threshold,
            "action_required": drift_score > threshold,
        }

    def generate_drift_report_html(
        self,
        current_data: pd.DataFrame,
        output_path: str = "drift_report.html",
    ):
        """Generate HTML drift report."""
        report = Report(metrics=[
            DatasetDriftMetric(),
            DataDriftTable(),
            ColumnDriftMetric(column_name="feature_1"),
        ])

        report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping,
        )

        report.save_html(output_path)
        return output_path

# Usage
reference_data = pd.read_csv("reference_data.csv")
monitor = DataDriftMonitor(reference_data)

# Check drift periodically
current_data = pd.read_csv("current_data.csv")
drift_result = monitor.check_drift(current_data, threshold=0.15)

if drift_result["action_required"]:
    print(f"Drift detected! Score: {drift_result['drift_score']}")
    monitor.generate_drift_report_html(current_data)
```

### Step 3: LLM Observability with Langfuse

```python
# langfuse_monitoring.py
from langfuse import Langfuse
from langfuse.decorators import langfuse_context, observe
from typing import Optional
import os

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

class LLMMonitor:
    """Monitor LLM usage and performance."""

    @observe(name="llm_generation")
    def generate_with_monitoring(
        self,
        prompt: str,
        model: str,
        **kwargs,
    ) -> str:
        """Generate with Langfuse tracking."""

        # Set trace metadata
        langfuse_context.update_current_trace(
            name="llm_inference",
            user_id="user_123",
            session_id="session_456",
            metadata={
                "model": model,
                "environment": "production",
            },
        )

        # Set generation parameters
        langfuse_context.update_current_generation(
            model=model,
            model_parameters={
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 512),
            },
            input=prompt,
        )

        # Simulate LLM call
        response = self._call_llm(prompt, model, **kwargs)

        # Record output
        langfuse_context.update_current_generation(
            output=response,
            usage={
                "prompt_tokens": self._count_tokens(prompt),
                "completion_tokens": self._count_tokens(response),
                "total_tokens": self._count_tokens(prompt) + self._count_tokens(response),
            },
        )

        return response

    def _call_llm(self, prompt: str, model: str, **kwargs) -> str:
        """Call LLM (placeholder)."""
        # Replace with actual LLM call
        return f"Response to: {prompt}"

    def _count_tokens(self, text: str) -> int:
        """Count tokens (simplified)."""
        return len(text.split()) * 1.3  # Rough estimate

# Track custom events
def track_custom_event(event_name: str, metadata: dict):
    """Track custom event."""
    langfuse.event(
        name=event_name,
        metadata=metadata,
    )

# Score generations
def score_generation(
    trace_id: str,
    score_name: str,
    value: float,
    comment: Optional[str] = None,
):
    """Score a generation."""
    langfuse.score(
        trace_id=trace_id,
        name=score_name,
        value=value,
        comment=comment,
    )
```

### Step 4: A/B Testing Setup

```python
# ab_testing.py
import random
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ABTestResult:
    model_version: str
    prompt: str
    response: str
    latency_ms: float
    user_rating: float = None
    timestamp: datetime = None

class ABTestManager:
    """Manage A/B testing between model versions."""

    def __init__(self, variants: Dict[str, float]):
        """
        Args:
            variants: Dict mapping model version to traffic percentage
        """
        self.variants = variants
        self.results: List[ABTestResult] = []
        self._validate_traffic_split()

    def _validate_traffic_split(self):
        """Validate traffic split sums to 100%."""
        total = sum(self.variants.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Traffic split must sum to 1.0, got {total}")

    def select_variant(self) -> str:
        """Select model variant based on traffic split."""
        rand = random.random()
        cumulative = 0.0

        for variant, percentage in self.variants.items():
            cumulative += percentage
            if rand <= cumulative:
                return variant

        return list(self.variants.keys())[-1]

    def record_result(self, result: ABTestResult):
        """Record A/B test result."""
        result.timestamp = datetime.now()
        self.results.append(result)

    def get_variant_stats(self, variant: str) -> Dict:
        """Get statistics for a variant."""
        variant_results = [
            r for r in self.results if r.model_version == variant
        ]

        if not variant_results:
            return {}

        latencies = [r.latency_ms for r in variant_results]
        ratings = [r.user_rating for r in variant_results if r.user_rating]

        return {
            "count": len(variant_results),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "avg_rating": sum(ratings) / len(ratings) if ratings else None,
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
        }

    def compare_variants(self) -> Dict:
        """Compare all variants."""
        comparison = {}

        for variant in self.variants.keys():
            comparison[variant] = self.get_variant_stats(variant)

        return comparison

# Usage
ab_manager = ABTestManager({
    "model-v1": 0.5,
    "model-v2": 0.5,
})

variant = ab_manager.select_variant()
result = ABTestResult(
    model_version=variant,
    prompt="Hello",
    response="Hi there",
    latency_ms=150.0,
    user_rating=4.5,
)
ab_manager.record_result(result)
```

### Step 5: Token Usage and Cost Tracking

```python
# cost_tracking.py
from typing import Dict, List
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class TokenUsage:
    timestamp: datetime
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float

# Pricing per 1M tokens (example)
MODEL_PRICING = {
    "gpt-4": {"input": 30.0, "output": 60.0},
    "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    "claude-3-opus": {"input": 15.0, "output": 75.0},
    "claude-3-sonnet": {"input": 3.0, "output": 15.0},
}

class CostTracker:
    """Track token usage and costs."""

    def __init__(self):
        self.usage_history: List[TokenUsage] = []

    def record_usage(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ):
        """Record token usage."""
        total_tokens = prompt_tokens + completion_tokens

        # Calculate cost
        pricing = MODEL_PRICING.get(model, {"input": 0, "output": 0})
        cost = (
            (prompt_tokens / 1_000_000) * pricing["input"] +
            (completion_tokens / 1_000_000) * pricing["output"]
        )

        usage = TokenUsage(
            timestamp=datetime.now(),
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=cost,
        )

        self.usage_history.append(usage)

    def get_daily_cost(self, date: datetime = None) -> float:
        """Get total cost for a day."""
        if date is None:
            date = datetime.now()

        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        daily_usage = [
            u for u in self.usage_history
            if start <= u.timestamp < end
        ]

        return sum(u.cost_usd for u in daily_usage)

    def get_model_breakdown(self, days: int = 7) -> Dict:
        """Get cost breakdown by model."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [u for u in self.usage_history if u.timestamp >= cutoff]

        breakdown = {}
        for usage in recent:
            if usage.model not in breakdown:
                breakdown[usage.model] = {
                    "cost": 0.0,
                    "tokens": 0,
                    "requests": 0,
                }

            breakdown[usage.model]["cost"] += usage.cost_usd
            breakdown[usage.model]["tokens"] += usage.total_tokens
            breakdown[usage.model]["requests"] += 1

        return breakdown

    def check_budget_alert(self, daily_budget: float) -> bool:
        """Check if daily budget exceeded."""
        daily_cost = self.get_daily_cost()
        return daily_cost > daily_budget

# Usage
tracker = CostTracker()
tracker.record_usage("gpt-4", prompt_tokens=1000, completion_tokens=500)
daily_cost = tracker.get_daily_cost()
breakdown = tracker.get_model_breakdown(days=7)
```

### Step 6: Alerting Rules

```python
# alerting.py
from typing import Callable, Optional
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText

@dataclass
class AlertRule:
    name: str
    condition: Callable[[], bool]
    severity: str  # "critical", "warning", "info"
    message: str
    enabled: bool = True

class AlertManager:
    """Manage alerting rules."""

    def __init__(self):
        self.rules: List[AlertRule] = []
        self.alert_history = []

    def add_rule(self, rule: AlertRule):
        """Add alert rule."""
        self.rules.append(rule)

    def check_rules(self):
        """Check all alert rules."""
        triggered = []

        for rule in self.rules:
            if not rule.enabled:
                continue

            try:
                if rule.condition():
                    triggered.append(rule)
                    self._send_alert(rule)
            except Exception as e:
                print(f"Error checking rule {rule.name}: {e}")

        return triggered

    def _send_alert(self, rule: AlertRule):
        """Send alert (placeholder)."""
        # Implement email, Slack, PagerDuty, etc.
        print(f"ALERT [{rule.severity.upper()}]: {rule.name} - {rule.message}")
        self.alert_history.append({
            "rule": rule.name,
            "timestamp": datetime.now(),
            "severity": rule.severity,
        })

# Usage
alert_manager = AlertManager()

# Add rules
alert_manager.add_rule(AlertRule(
    name="accuracy_drift",
    condition=lambda: monitor.detect_accuracy_drift(0.85, threshold=0.1),
    severity="critical",
    message="Model accuracy has dropped below threshold",
))

alert_manager.add_rule(AlertRule(
    name="high_latency",
    condition=lambda: monitor.get_latency_stats().get("p95", 0) > 1000,
    severity="warning",
    message="P95 latency exceeds 1 second",
))

alert_manager.add_rule(AlertRule(
    name="budget_exceeded",
    condition=lambda: tracker.check_budget_alert(daily_budget=100.0),
    severity="critical",
    message="Daily budget exceeded",
))

# Check rules periodically
triggered = alert_manager.check_rules()
```

## Output

- Model performance dashboards
- Data drift detection reports
- LLM observability traces
- A/B test comparison results
- Cost tracking and budget alerts

## Best Practices

- Monitor accuracy, latency, and throughput continuously
- Set up data drift detection with Evidently
- Use Langfuse for LLM observability
- Track token usage and costs per model
- Set up alerting for critical metrics
- Run A/B tests before full rollout
- Keep reference datasets for drift comparison

## Related

- Skill: `model-serving`
- Skill: `ml-deployment`
- Skill: `ai-cost-optimization`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
