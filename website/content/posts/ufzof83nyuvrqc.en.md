+++
title = "【AIセキュリティの深淵】IBM Bobへの機密流出を未然に防ぐ――MCPとカスタムルールが描く「攻めの防御」 (English)"
date = "2026-03-13T04:50:47.118466"
tags = ["AI", "Tools", "Python"]
draft = false
description = "Introduction to 【AIセキュリティの深淵】IBM Bobへの機密流出を未然に防ぐ――MCPとカスタムルールが描く「攻めの防御」 (English)"
canonicalUrl = "https://techtrend-watch.com/posts/ufzof83nyuvrqc/"
+++


# The Depths of AI Security: Preventing Data Leaks to IBM Bob—Building "Proactive Defense" with MCP and Custom Rules

"Wait, did that prompt just contain confidential information...?"

For an engineer immersed in development, this is a spine-chilling moment. AI assistants like ChatGPT and IBM Bob have become indispensable partners that expand a developer's cognitive reach. However, the flip side of this convenience is the risk of unintended information leakage. In an era where powerful AI agents have deep access to local environments and internal documentation, security measures that rely solely on "human caution" have reached their limit.

This article details advanced defensive measures to prevent "accidental" slips when utilizing IBM Bob. Specifically, we will explore the construction of systemic guardrails by combining the **Model Context Protocol (MCP)** with **Custom Rules**.

## 1. Why "Guidelines" Alone Can't Prevent Leaks to AI

The evolution of AI agents has made it possible to seamlessly provide context—such as source code, error logs, and configuration files—to the AI. While this "context sharing" is the key to unlocking AI intelligence, it is also the primary source of risk.

When using sophisticated tools like IBM Bob, users easily fall into the psychological illusion that they are conversing with a "trusted colleague." As a result, they may unconsciously include highly confidential information—such as private API keys, authentication tokens, or codenames for unannounced projects—into their prompts.

Traditional countermeasures have centered on "mindset-based" approaches, such as establishing usage policies or literacy education. However, engineering problems should be solved with engineering. What we need now is a mechanism where **"the system physically intervenes at the very moment information is being passed."**

<div class="expert-opinion">
**Tech Watch Perspective:**
Until now, AI security has been a form of analog perimeter defense where humans performed censorship "outside" the model. However, the emergence of MCP (Model Context Protocol), proposed by Anthropic, is fundamentally shifting this power balance. MCP is not merely a standard for data integration; it allows for the insertion of a "protocol-based censorship layer" between the AI and local resources. By dynamically embedding security into the AI's context understanding itself, the concept of an "Intelligent Gatekeeper" is set to become the standard for enterprise AI utilization from 2026 onwards.
</div>

## 2. Automating Censorship via MCP (Model Context Protocol)

MCP is an open standard that allows AI models to communicate safely with external tools and data sources. By leveraging this, you can intervene with an "MCP Server" that enforces specific security policies before IBM Bob accesses files or processes a prompt.

### Three Steps to Building Robust Guardrails:

1.  **Deployment of a Security-Specialized MCP Server**: Using Python or TypeScript, build a proprietary MCP server equipped with sensitive information detection logic using regular expressions or lightweight LLMs.
2.  **Prompt Pre-scanning**: Immediately before IBM Bob sends a request, the MCP tool scrutinizes the content. It checks for patterns like `BEGIN PRIVATE KEY` or specific internal identifiers in milliseconds.
3.  **Interception and Alerting**: If the inclusion of confidential information is detected, the communication is immediately severed, and a warning is displayed to the user. This creates an environment where a "transmission error" is physically impossible.

## 3. Utilizing IBM Bob's "Custom Rules" as a Second Line of Defense

In addition to systemic blocking via MCP, the thorough use of IBM Bob’s own "Custom Instructions (Custom Rules)" is highly effective for immediate results. By defining the AI's behavior at the system prompt level, you can establish a double layer of defense.

*   **Defining Keyword Blacklists**: Explicitly register specific secret project names or internal server hostnames as information the AI should not process.
*   **Constraints on Context Extraction**: Formulate detailed instructions such as "Ignore authentication info contained in TODO comments within the code" or "Do not read the contents of environment variable files."

By doing so, even if a piece of information manages to bypass the MCP layer, the probability that the AI will autonomously decide "I cannot accept that information" is significantly increased.

## 4. Comparison with Other Approaches: Why Stop It "At the Edge"?

Many AI tools, such as GitHub Copilot or ChatGPT Enterprise, claim privacy protections stating they "do not use input data for training." However, from a compliance standpoint, that is merely a conversation about "what happens after the data is sent."

The advantage of a self-built guardrail using MCP lies in edge-side defense: **"preventing the information from being sent to the external (model's) server in the first place."** The stricter a company's legal and security requirements, the more this "pre-transmission censorship" approach becomes the only viable solution for AI adoption.

## 5. Challenges and Workarounds in Implementation

In the process of building this ironclad defensive line, several technical trade-offs must be considered.

*   **The Issue of Over-blocking**: If security is too strict, even legitimate source code may be blocked, significantly reducing development efficiency. To prevent this, it is effective to deploy a small LLM (such as Llama 3) on the MCP server side to perform flexible, context-aware judgments rather than relying solely on simple regex.
*   **Response Latency**: The overhead of filtering can degrade the developer experience. It is crucial to select a lightweight runtime that operates in the local environment and appropriately combine asynchronous processing.
*   **Dynamic Rule Updates**: As projects progress, the keywords that need to be kept secret constantly change. You should establish an operational flow where the MCP configuration files are managed via Git (Infrastructure as Code) to ensure the latest defense policies are shared across the team.

## FAQ: Frequently Asked Questions

**Q: Is building a custom MCP server difficult for an average engineer?**
**A:** With the availability of comprehensive official SDKs, anyone with basic knowledge of Python or Node.js can build a prototype in a few hours. We recommend starting small with simple string matching rather than jumping straight into complex AI detection.

**Q: Are these measures necessary for individual developers?**
**A:** We strongly recommend them for individual developers as well. An accidental leak of an AWS key can directly impact personal assets and reputation. A system that "assumes mistakes will happen and covers for them" increases psychological safety and ultimately contributes to faster development speeds.

**Q: Can this mechanism be used with tools other than IBM Bob?**
**A:** Yes. Since MCP is an open standard, it can be applied across the rapidly expanding ecosystem, including Claude Desktop and MCP-compatible IDE extensions.

## Summary: Don't "Blindly Trust" AI—Arm Yourself with Technology

AI dramatically improves our productivity, but those benefits can only be fully enjoyed under appropriate control. "Preemptive" defensive measures combining IBM Bob and MCP will likely become an essential practice for engineers in the AI-native era.

Mitigating risks created by technology with even more advanced technology—this healthy tension is the true engine that accelerates innovation.


---

> This article is also available in [Japanese](https://techtrend-watch.com/posts/ufzof83nyuvrqc/).
