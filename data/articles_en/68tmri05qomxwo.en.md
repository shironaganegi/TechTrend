---
title: "LLM時代の新常識？Rust製Python実行環境「monty」が切り拓くセキュアなAIエージェント開発の衝撃 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---


### Introduction

The evolution of "AI Agents"—where LLMs write and execute their own code to solve problems—shows no signs of slowing down. However, developers consistently face a critical challenge: **"How can we execute LLM-generated code both securely and at high speed?"**

Conventional container-based sandboxes, such as Docker, offer high security but suffer from startup latencies of several hundred milliseconds and significant resource overhead. Enter [monty](https://github.com/pydantic/monty), a project currently under development by the Pydantic team. This minimalist Python interpreter, written in Rust, has the potential to rewrite the playbook for AI agent development.

### Key Features of monty

*   **Ultra-Fast Startup**: Takes less than 1 microsecond (μs) from startup to execution results. This speed is incomparable to traditional containers.
*   **Robust Security via Rust**: Access to the host environment (filesystem, network, etc.) is completely blocked by default. The interpreter can only call functions explicitly permitted by the developer.
*   **Snapshot Capabilities**: Execution states can be saved as byte sequences and resumed later. This is ideal for workflows where processes need to be saved to a database and continued asynchronously.
*   **Integrated Type Checking**: It features built-in support for [ty](https://docs.astral.sh/ty/), allowing for checks based on modern Python type hints before execution.


### An Engineer’s Perspective: Why Do We Need "monty" Now?

From a professional engineering standpoint, the true value of monty lies in the democratization of **"Programmatic Tool Calling."**

Traditionally, AI tool calling involves passing arguments in JSON format. However, for complex logic or loops, having the LLM write Python code directly is often far more accurate and flexible. The "Code-as-a-Tool" concept—advocated by Anthropic’s [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) and Hugging Face’s [smolagents](https://github.com/huggingface/smolagents)—becomes feasible at scale and speed thanks to monty.

Even within the Japanese development landscape, the ability to embed a "secure code execution environment" without building heavy-duty sandboxes provides an immense advantage for enterprise AI development where security requirements are stringent.

### Installation and Basic Usage

You can easily introduce it to your Python environment using `uv`.

```bash
uv add pydantic-monty
```

Usage Example (Python):

```python
import pydantic_monty

code = """
def sum_list(items):
    return sum(items)
"""

# Execute code in a secure environment
result = pydantic_monty.run(code, func="sum_list", args=[[1, 2, 3]])
print(result) # 6
```


#### Pros
*   **Performance**: Maintains execution speeds comparable to CPython while offering drastically lower latency.
*   **Portability**: Since it does not depend on CPython, it can run anywhere Rust runs (including JS/WASM environments).
*   **Resource Control**: Allows for strict limits on memory usage and execution time.

#### Cons (Current Limitations)
*   **Limited Standard Library**: Currently restricted to modules like `sys`, `typing`, and `asyncio`. Third-party libraries like Pydantic cannot be used within the environment yet.
*   **Development Phase**: Still in an experimental stage; features like class definitions and `match` statements are currently unimplemented.

### Summary

`monty` is the missing piece for giving AI agents a "secure brain." With integration into Pydantic AI planned, it is poised to become a standard in future AI development. If you find yourself in a situation where you don't need the full weight of Python but require a secure "execution environment" to augment LLM reasoning, you should "Star" the [official repository](https://github.com/pydantic/monty) and keep a close eye on its progress.

It also promises to be a powerful tool in the context of edge code execution, similar to [Cloudflare’s Code-mode](https://blog.cloudflare.com/code-mode/).
