# Control signals in frozen LLMs (a pragmatic view)

A “control signal” is any *input-side change* that reliably shifts a model’s behavior without changing the model’s weights.

## Why this matters

If you can steer behavior via inputs, you can:

- patch factual memory (weakly) without finetuning,
- induce a style/stance (helpful vs skeptical),
- create *modules* that compose (e.g., memory + safety + domain voice).

## Common control channels

- **Prompting:** instructions, exemplars, constraints.
- **Special tokens / learned embeddings:** adding tokens whose embeddings are optimized while keeping the model frozen.
- **Retrieval context:** injecting external text (RAG).
- **Tool use:** changing the action space (a different kind of control).

## A useful mental model

Think of the model as implementing a conditional distribution:

```text
P(next_token | prefix)
```

A control signal changes the *prefix* in a structured way so the conditional distribution shifts toward a target behavior.

## Failure modes

- Control becomes “soft”: it changes *style* more than truth.
- Strong steering can increase hallucination or refusal.
- Control may not generalize outside the training/prompt regime.

## A rule of thumb

When you claim control, always ask:

1. **What is being controlled?** (truth, verbosity, tone, refusal rate, calibration…)
2. **How stable is it across tasks?**
3. **What is the cost?** (accuracy, abstention, latency, brittleness)
