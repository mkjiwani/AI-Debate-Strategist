"""Telemetry tracking for AI Debate Strategist.

Tracks input tokens, output tokens, total tokens, and latency per layer.
Provides aggregated metrics and optimization analysis.
"""

import time
from dataclasses import dataclass, field


@dataclass
class LayerMetrics:
    """Metrics for a single reasoning layer."""
    layer_name: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0

    @property
    def tokens_per_second(self) -> float:
        if self.latency_ms <= 0:
            return 0.0
        return (self.output_tokens / self.latency_ms) * 1000


@dataclass
class TelemetryTracker:
    """Aggregates telemetry across all reasoning layers."""
    layers: list = field(default_factory=list)

    def record_layer(self, layer_name: str, usage, latency_ms: float) -> LayerMetrics:
        """Record metrics for a completed layer."""
        metrics = LayerMetrics(
            layer_name=layer_name,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            latency_ms=latency_ms,
        )
        self.layers.append(metrics)
        return metrics

    @property
    def total_input_tokens(self) -> int:
        return sum(m.input_tokens for m in self.layers)

    @property
    def total_output_tokens(self) -> int:
        return sum(m.output_tokens for m in self.layers)

    @property
    def total_tokens(self) -> int:
        return sum(m.total_tokens for m in self.layers)

    @property
    def total_latency_ms(self) -> float:
        return sum(m.latency_ms for m in self.layers)

    @property
    def avg_latency_ms(self) -> float:
        if not self.layers:
            return 0.0
        return self.total_latency_ms / len(self.layers)

    @property
    def avg_tokens_per_second(self) -> float:
        speeds = [m.tokens_per_second for m in self.layers if m.tokens_per_second > 0]
        if not speeds:
            return 0.0
        return sum(speeds) / len(speeds)

    def get_optimization_insights(self) -> list:
        """Analyze token usage and provide optimization suggestions."""
        if not self.layers:
            return []

        insights = []

        # Find the most expensive layer
        most_tokens = max(self.layers, key=lambda m: m.total_tokens)
        insights.append(
            f"**Highest token usage:** {most_tokens.layer_name} "
            f"({most_tokens.total_tokens:,} tokens) — consider tightening "
            f"this prompt if budget is a concern."
        )

        # Find the slowest layer
        slowest = max(self.layers, key=lambda m: m.latency_ms)
        insights.append(
            f"**Slowest layer:** {slowest.layer_name} "
            f"({slowest.latency_ms:,.0f}ms) — latency correlates with "
            f"output length ({slowest.output_tokens:,} output tokens)."
        )

        # Input/output ratio analysis
        for m in self.layers:
            if m.input_tokens > 0:
                ratio = m.output_tokens / m.input_tokens
                if ratio < 0.1:
                    insights.append(
                        f"**Low output ratio:** {m.layer_name} has a "
                        f"{ratio:.2f} output/input ratio — large prompt "
                        f"relative to response. Consider trimming context."
                    )

        # Overall efficiency
        if self.total_latency_ms > 0:
            overall_tps = (self.total_output_tokens / self.total_latency_ms) * 1000
            insights.append(
                f"**Overall throughput:** {overall_tps:,.1f} output tokens/sec "
                f"across all layers."
            )

        return insights

    def reset(self):
        """Clear all tracked metrics."""
        self.layers.clear()
