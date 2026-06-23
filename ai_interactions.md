# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

Prompt(s) used:

```
Identify three edge-case inputs that might still break the guessing game,
then refactor parse_guess into logic_utils.py and write a suite of pytest
cases that verify the game handles those inputs gracefully. Run pytest and
show me the output.
```

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative number (`-7`) | (prompt above) | `test_negative_number_is_parsed` | ✅ Yes | A minus sign is valid int syntax, so the parser should accept it instead of erroring. |
| Decimal (`3.7`) | (prompt above) | `test_decimal_is_truncated_to_int` | ✅ Yes | Players may type decimals; the code should coerce to an int (truncating to 3), not crash. |
| Extremely large value (`10^20`) | (prompt above) | `test_extremely_large_number_is_parsed` | ✅ Yes | Python ints are arbitrary precision, so a huge value should parse without overflow. |
| Non-numeric text (`abc`) | (prompt above) | `test_non_numeric_input_is_rejected_gracefully` | ✅ Yes | Garbage input should return a friendly error message, not an unhandled exception. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
