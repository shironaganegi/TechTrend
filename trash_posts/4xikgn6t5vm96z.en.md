+++
title = "AIエージェントとの協業を深化させる「skills」：Matt Pocock氏が提唱する「真のエンジニアリング」アプローチ (English)"
date = "2026-06-18T00:26:46.449148"
tags = ["AI", "Tools", "LLM", "RAG", "AI\u30a8\u30fc\u30b8\u30a7\u30f3\u30c8", "\u30d5\u30ed\u30f3\u30c8\u30a8\u30f3\u30c9"]
draft = false
description = "Introduction to AIエージェントとの協業を深化させる「skills」：Matt Pocock氏が提唱する「真のエンジニアリング」アプローチ (English)"
canonicalUrl = "https://techtrend-watch.com/posts/4xikgn6t5vm96z/"
+++


# Deepening Collaboration with AI Agents with `skills`: Matt Pocock's Proposed Approach to 'True Engineering'

Many developers face challenges such as "discrepancy from expectations" and "unstable output" when developing with AI agents. The cause may lie not only in the AI's performance but also in the human-side's collaboration approach. The open-source project "[skills](https://github.com/mattpocock/skills)", proposed by world-renowned TypeScript expert Matt Pocock, is a groundbreaking framework designed to elevate collaboration with AI agents from "vague coding" to "**real engineering**".

This article delves into the core of how `skills` can transform the future of AI-powered development. From the perspective of TechTrend Watch, we will explain concrete methods for maximizing AI capabilities and dramatically improving the development process, along with the benefits of their introduction.

## The Importance of 'Question Quality' in the AI Era: Why `skills` is Needed Now

In today's technology industry, "AI," "ChatGPT," and "engineer" are constantly drawing attention as hot keywords. However, behind the scenes, there's no end to voices saying, "I can't fully utilize AI" or "It's disappointing." Ultimately, this stems from the human side failing to establish a fundamental approach to "how to utilize AI" and "what to ask." This is because AI is not an omnipotent wizard; the quality of its output strictly depends on the "input" and "context" we provide.

As Matt Pocock points out, many developers unconsciously tend towards "vague coding" – giving AI ambiguous instructions and feeling frustrated when the expected results are not achieved. However, even in collaboration with AI, just as in human-to-human development, **"alignment"** and **"building shared understanding"** are essential.

<div class="expert-opinion">
  Many developers currently expect "perfect answers" too much from AI agents. However, AI is merely a tool, and the quality of its output directly depends on the "quality of the prompt." What `skills` offers is a framework for embedding "engineering thinking" into AI, delving into the essence of problems and building shared understanding through dialogue with the agent. TechTrend Watch asserts that this transcends mere prompt engineering, serving as a strategic communication method for involving AI from the initial stages of system design. This is an attempt to redefine the "operating system" of AI-powered development. While conventional AI tools offered "individual functions," `skills` optimizes the "collaboration process" with AI itself. This shift in perspective is precisely what is demanded of "Real Engineers."
</div>

## The Two Core Functions of `skills`: Preventing AI from 'Wandering Off Course'

`skills` is built to resolve two typical failure modes that AI agents often fall into.

### 1. Grilling Sessions to Resolve Mismatched Intentions: `/grill-me` and `/grill-with-docs`

AI doesn't act as requested – this is precisely "a gap in understanding," the most common failure mode in software development. As David Thomas & Andrew Hunt point out in 'The Pragmatic Programmer', the situation where "no one knows exactly what they want" also occurs when dealing with AI.

The solution provided by `skills` is a "**grilling session**" that makes the AI ask thorough questions. Specifically, the following skills are used:

*   `**/grill-me**`: For general use cases (non-code), it makes the AI ask detailed questions to delve deeper into the problem.
*   `**/grill-with-docs**`: In addition to the functionality of `/grill-me`, it supports the construction of a Shared Language, as described later.

These skills are designed for thorough alignment with the AI before starting development. Just as "requirements definition alignment" is crucial in human-to-human development, this process should not be omitted in collaboration with AI. On the contrary, a secondary effect can be expected: as the AI asks multi-faceted questions, our human thinking also deepens.

### 2. Controlling AI Redundancy through Shared Language

We often hear feedback like, "AI's output is convoluted and difficult to understand what it's trying to say." In the early stages of a project, similar to how developers and domain experts might speak different languages, AI often doesn't fully grasp project-specific terminology or context.

The solution of `skills` is the establishment of a "**Shared Language**". Specifically, you create a `CONTEXT.md` file that defines project-specific terminology, concepts, abbreviations, and more. This allows the AI to accurately understand project-specific jargon, omit unnecessary explanations, and provide **concise and precise output**.

<details>
<summary>Example of Shared Language (from mattpocock/course-video-manager)</summary>

*   **BEFORE**: "There's a problem when a lesson inside a section of a course is made 'real' (i.e. given a spot in the file system)"
*   **AFTER**: "There's a problem with the materialization cascade"

</details>

The construction of this shared language is integrated into the `/grill-with-docs` skill, allowing you to refine the shared language together with the AI through grilling sessions. The idea of applying the concept of a 'Ubiquitous Language' discussed in Eric Evans' 'Domain-Driven Design' to collaboration with AI is highly insightful. Once you experience this powerful feature, you will be amazed by its effects.

💡 **Other Benefits of Shared Language**
*   Variable names, function names, and file names become consistent across the entire project, improving code readability.
*   Onboarding new team members becomes smoother.
*   Communication among human developers is also streamlined.

## Comparison with Existing Approaches and the Uniqueness of `skills`

Traditional development processes and frameworks like GSD, BMAD, and Spec-Kit have, by attempting to "own" the entire process, ironically taken control away from developers and made bug resolution difficult in certain scenarios. `skills` distinguishes itself from these.

`skills`, designed by Matt Pocock, is characterized by being "**small, adaptable, and composable**". This offers engineers the freedom to flexibly customize AI to their own workflows and preferred AI models, without being bound by specific large frameworks. It embodies a philosophy akin to modern CLI tools or microservices architecture. Its versatility, not being dependent on a specific AI agent, will also be a significant advantage from a long-term perspective.

## Practical Guide: Introduction Pitfalls and Tips for Smooth Setup

To effectively utilize these benefits in practice, we will explain points to note during introduction and tips for a smooth setup.

### Pitfalls and Preparation

*   **Initial Effort Investment**: At first, you might feel, "Do I really need to put that much effort into AI?" However, this initial investment in 'alignment' dramatically reduces rework and wasted time later on. Especially the task of creating a shared language with `/grill-with-docs` may seem troublesome, but its utility will be demonstrated throughout the project's lifespan. Considering not just immediate efficiency but also long-term project health, this is undoubtedly a worthwhile investment.
*   **Hardware Requirements**: Installation is possible as long as you have an environment where Node.js/npm can run. No specific high-performance GPUs are required, making it appealing due to its low barrier to entry for many developers.

### 30-Second Quick Start

1.  **Run the installer**: Execute the following command in your terminal.
    ```bash
    npx skills@latest add mattpocock/skills
    ```
2.  **Select skills**: Choose the skills you want to install and the coding agent that will use them. **Make sure to select `/setup-matt-pocock-skills`**. This is crucial for the initial setup.
3.  **Execute setup script**: Run `/setup-matt-pocock-skills` within your agent. This will prompt you for the following settings interactively:
    *   Issue tracker to use (GitHub, Linear, or local file)
    *   Labels to apply during ticket triage (used by the `/triage` skill)
    *   Document storage location
4.  **Ready to go!**: Your AI agent is now ready to begin "real engineering". We recommend starting with `/grill-with-docs`.

## FAQ: Frequently Asked Questions

#### Q1: Which AI agents can I use it with?
`skills` is designed to be model-agnostic. It can be used with Claude Code, Codex, and other LLM-based coding agents. As long as the agent has skill execution capabilities, it can be widely utilized.

#### Q2: Is it difficult to set up?
As shown in the "30-Second Quick Start" above, installation can be done with a single CLI command, and subsequent settings proceed interactively, making it very easy. If you have an environment where npm can be used, you should be able to try it immediately.

#### Q3: I'm still not clear on the benefits of creating a Shared Language.
For example, imagine you instruct the AI with the concept of "user information **materialization**". Without a shared language, the AI might repeatedly ask questions like, "Do you mean to make it into a physical form?" However, if you define "Materialization: The process of constructing a user object from the database and storing it in the cache" in `CONTEXT.md`, the AI will immediately understand your intent and generate precise code. In the long run, this extra step dramatically reduces communication costs.

#### Q4: Specifically, which tasks are streamlined by using this skill?
Significant effects can be expected mainly in the following tasks:
*   **Improved Requirements Definition Accuracy**: By deeply exploring requirements with the AI using `/grill-with-docs`, misunderstandings at the initial stage are eliminated.
*   **New Feature Development**: Using a shared language makes it easier to generate consistent code.
*   **Refactoring Existing Code**: Since the AI understands project-specific terminology, more accurate suggestions and modifications become possible.
*   **Documentation**: The process of building a shared language itself becomes a high-quality documentation asset.

## Conclusion: `skills` for Building the Strongest Team with AI

TechTrend Watch evaluates Matt Pocock's `skills` as an absolutely **essential tool** for elevating collaboration with AI agents from "vague coding" to "real engineering". This project strongly suggests that "quality of questioning" and "shared understanding" from the human side are indispensable for maximizing AI capabilities.

Developers who felt that "AI is smart but often fails to deliver expected results" are precisely the ones who should try `skills`. By improving the quality of communication with the agent and eliminating inefficiencies, you will ultimately be able to produce high-quality code. TechTrend Watch is confident that this has the potential to become the standard for future AI development. If you haven't adopted it yet, why not take this opportunity to try `skills`? Build the strongest team with AI and gain overwhelming development efficiency and high-quality output.


---

> This article is also available in [Japanese](https://techtrend-watch.com/posts/4xikgn6t5vm96z/).
