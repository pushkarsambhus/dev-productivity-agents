# Python Basics

A collection of simple Python scripts covering core concepts — great for beginners and as a quick reference.

## Files

| File | Topic |
|------|-------|
| `variables_and_types.py` | int, float, string, bool, type casting |
| `strings.py` | String methods, slicing, f-strings |
| `lists.py` | List operations, slicing, list comprehension |
| `tuples.py` | Tuples, immutability, unpacking |
| `dictionaries.py` | Dict creation, access, methods, dict comprehension |
| `sets.py` | Set operations, union, intersection, difference |
| `conditionals.py` | if/elif/else, ternary operator |
| `loops.py` | for/while loops, break, continue, enumerate, zip |
| `functions.py` | Defining functions, args, kwargs, return values |
| `lambda_and_builtins.py` | lambda, map, filter, sorted, zip, enumerate |
| `classes.py` | Defining a class, attributes, methods, self |
| `class_constructor.py` | __init__, instance vs class variables, __str__, __repr__ |
| `inheritance.py` | Single and multiple inheritance, super() |
| `encapsulation.py` | Public, protected, private attributes, getters/setters |
| `polymorphism.py` | Method overriding, duck typing |
| `custom_exceptions.py` | Custom exception classes, raising, try/except/finally |
| `file_handling.py` | Reading and writing files, with statement |
| `modules_and_imports.py` | Standard library modules, imports |
| `decorators.py` | Function decorators, @property |
| `generators.py` | yield, generator functions, lazy evaluation |
| `list_comprehensions_advanced.py` | Nested and conditional comprehensions |
| `error_handling.py` | try/except/else/finally, multiple except blocks |

## AI & Data Science

| File | Topic |
|------|-------|
| `numpy_basics.py` | Arrays, matrix operations, dot product (NumPy) |
| `pandas_basics.py` | DataFrames, Series, filtering, groupby (Pandas) |
| `matplotlib_basics.py` | Line plot, bar chart, scatter plot (Matplotlib) |
| `ai_intro.py` | What is AI/ML, types of ML explained with plain-English analogies |
| `linear_regression.py` | Linear regression from scratch — pure math, no libraries |
| `sklearn_basics.py` | Train/test split, LinearRegression, MSE, R² (scikit-learn) |
| `neural_network_basics.py` | Input → weights → output, forward pass, backprop (NumPy only) |
| `tokenization_basics.py` | What tokenization is, word tokenizer, how LLMs think in tokens |
| `prompt_engineering.py` | Bad vs good prompts, few-shot prompting, chain-of-thought |

> **Note:** `numpy`, `pandas`, and `matplotlib` are required for the data science files.
> Install them with: `pip install numpy pandas matplotlib`
> For `sklearn_basics.py` you also need: `pip install scikit-learn`

## AI Agents

| File | Topic |
|------|-------|
| `agent_basics.py` | What is an agent? Perception → thinking → action loop, rule-based agent |
| `tool_use_agent.py` | Agents that call tools: calculator, weather, search, unit converter |
| `memory_agent.py` | Short-term (conversation) and long-term (persistent file) memory |
| `planning_agent.py` | Plan → Act → Observe loop; multi-step goal execution |
| `multi_agent.py` | Two agents conversing; orchestrator + specialist agents |
| `anthropic_agent.py` | Real agent using Anthropic SDK; tool use with Claude API |
| `langchain_agent_intro.py` | LangChain concepts: chains, agents, tools, memory, LCEL |
| `agentic_loop.py` | The raw agentic loop from scratch — mocked LLM, mirrors real agents exactly |

> **Note:** `anthropic_agent.py` requires `pip install anthropic` and an `ANTHROPIC_API_KEY`.
> `langchain_agent_intro.py` requires `pip install langchain langchain-anthropic`.
> All other agent files run with no extra dependencies.

## How to Run

Each file is self-contained and runnable:

```bash
python variables_and_types.py
python strings.py
# ... and so on
```

## Tips for Beginners

- Read the top comment in each file first — it explains the concept in plain English
- Run each file and observe the output
- Try changing values and see what happens
- The `if __name__ == "__main__":` block is where the examples run
