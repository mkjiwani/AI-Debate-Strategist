"""Multi-layer reasoning engine for the AI Debate Strategist.

Orchestrates 5 reasoning layers through the OpenAI API, chaining
outputs so each layer builds on the previous one's analysis.
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI

from prompts import LAYER_PROMPTS
from telemetry import TelemetryTracker

load_dotenv()


def run_layer(client, model: str, layer_name: str,
              system_prompt: str, user_prompt: str,
              tracker: TelemetryTracker) -> str:
    """Execute a single reasoning layer and record telemetry.

    Args:
        client: OpenAI client instance.
        model: Model name to use.
        layer_name: Name of the current reasoning layer.
        system_prompt: System message for the AI.
        user_prompt: User message for the AI.
        tracker: TelemetryTracker to record metrics.
    """
    temperature = float(os.getenv("TEMPERATURE", "0.7"))
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    start = time.perf_counter()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    tracker.record_layer(layer_name, response.usage, elapsed_ms)
    return response.choices[0].message.content


def run_debate_analysis(client, model: str, topic: str,
                        tracker: TelemetryTracker,
                        progress_callback=None) -> dict:
    """Run all 5 reasoning layers sequentially.

    Args:
        client: OpenAI client instance.
        model: Model name to use.
        topic: The debate topic string.
        tracker: TelemetryTracker to record metrics.
        progress_callback: Optional callable(layer_name, layer_number) for UI updates.

    Returns:
        Dict mapping layer names to their output text.
    """
    tracker.reset()
    results = {}
    layers = list(LAYER_PROMPTS.items())

    for i, (layer_name, prompts) in enumerate(layers, 1):
        if progress_callback:
            progress_callback(layer_name, i)

        system = prompts["system"]
        user_template = prompts["user"]

        # Build the user prompt with context from prior layers
        if layer_name == "Layer 1: Context Analysis":
            user_prompt = user_template.format(topic=topic)

        elif layer_name == "Layer 2: Argument Builder":
            user_prompt = user_template.format(
                topic=topic,
                previous_output=results["Layer 1: Context Analysis"],
            )

        elif layer_name == "Layer 3: Counter Argument":
            user_prompt = user_template.format(
                topic=topic,
                previous_output=results["Layer 2: Argument Builder"],
            )

        elif layer_name == "Layer 4: Self-Critique":
            user_prompt = user_template.format(
                topic=topic,
                argument=results["Layer 2: Argument Builder"],
                previous_output=results["Layer 3: Counter Argument"],
            )

        elif layer_name == "Layer 5: Final Strategy":
            user_prompt = user_template.format(
                topic=topic,
                context_analysis=results["Layer 1: Context Analysis"],
                argument=results["Layer 2: Argument Builder"],
                counter_argument=results["Layer 3: Counter Argument"],
                previous_output=results["Layer 4: Self-Critique"],
            )

        output = run_layer(client, model, layer_name, system, user_prompt,
                           tracker)
        results[layer_name] = output

    return results
