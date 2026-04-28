---
title: "AIエージェントを「道具」から「熟練のパートナー」へ。Matt Pocock氏が公開した『skills』の衝撃 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# From "Tool" to "Expert Partner": The Impact of Matt Pocock's "skills" for AI Agents

## Introduction: In 2026, Will We Still Be Writing Code Based on "Vibes"?

"I gave the AI instructions, but the code it returned wasn't what I expected." This remains one of the most universal challenges facing modern engineers. Currently, much of AI utilization stays within the realm of **"Vibe Coding"**—the uncertain process of throwing vague prompts at a model and praying for a lucky output.

A decisive solution to break this status quo is now drawing the attention of engineers worldwide. It is "**skills**," a collection of essential expertise for Claude directories (`.claude`) released by **Matt Pocock**, a renowned authority in the TypeScript community. This is not merely a collection of prompt fragments. It is an "OS for the development process" designed to transform AI agents from "passive tools waiting for instructions" into "autonomous senior engineers."

<div class="expert-opinion">
From a tech-watch perspective, the true value of this repository lies in "how to hand over initiative to the AI." While conventional AI tools are things you "make the AI do," Matt’s skills approach focuses on "educating the AI on the engineer's thought process." In particular, the concept of "/grill-me"—forcing the AI to point out omissions in requirements—represents a Copernican shift in prompt engineering.
</div>

## The Core of "skills": Why Your AI Usually Falls Short

The root of engineer frustration with AI lies in a **"lack of context"** and **"asymmetry in communication."** To bridge this gap, Matt Pocock introduced the highly sophisticated concept of "skills."

### 1. `/grill-me`: Realizing Socratic Questioning with AI
Before starting implementation, you run this command. The AI then stops being a submissive code generator and transforms into a rigorous reviewer. "What is the rationale behind choosing this library?" "How will you handle these edge cases?" "What are the performance constraints?" By having the AI "grill" you with relentless questions, you refine the design to the extreme before a single line of code is written. This process drastically reduces the risk of costly rework.

### 2. `/grill-with-docs`: Turning Domain-Driven Design (DDD) into Prompts
By aggregating project-specific terminology and architectural decisions into a `CONTEXT.md` file, you teach the AI the "Ubiquitous Language" of your project. This allows the AI to propose optimal solutions that respect the specific context of the project without requiring redundant explanations. This goes beyond mere efficiency; it contributes to both practical benefits—like reducing token consumption—and quality benefits, such as unifying naming conventions.

### 3. Composable Design Philosophy
These skills are designed to be independent and tool-agnostic. While they are optimized for use with Claude Code, they can easily be ported to other AI agents like Cursor. This extensibility—allowing professionals to "hack" functions to fit their workflow—is a prerequisite for any tool used by experts.

## Differentiation: Providing "Discipline" Rather Than Just Automation

The market is flooded with various AI agent frameworks. However, many of them tend to become "black boxes" that strip away human control in an attempt to "fully automate the process." In contrast, `skills` presents a thoroughly **engineering-first** stance.

- **Ensuring Transparency**: It is always clear what logic the AI is using to think and which documents it is referencing.
- **Emphasis on Design Intent**: Rather than just creating "working code," it pursues "intentional code" that considers maintainability and scalability.
- **Low-Friction Adoption**: It can be instantly integrated into existing projects via the `npx` command. The barrier to entry is extremely low.

## Logical Constraints and Considerations for Implementation

`skills` is not a magic wand. To maximize its potential, a certain level of discipline is required from the user.

- **Environmental Prerequisites**: Running it requires a Node.js environment, with setup standardized through `npx skills@latest`.
- **Continuous Documentation**: To reap the benefits of `/grill-with-docs`, an operational workflow to keep `CONTEXT.md` and ADRs (Architecture Decision Records) up to date is essential. One must understand that the tool doesn't solve the problem; rather, the AI accelerates your "good habits."

## FAQ: Core Questions for Adoption

**Q: Can this be used with LLMs other than Claude?**
**A:** While the prompt design philosophy is universal, it is currently optimized to deliver the best results in agent environments like Claude Code.

**Q: Are there integrations with external tools like Linear or GitHub?**
**A:** You can select an issue tracker during setup. This enables a consistent context across the entire workflow, from issue triaging to code implementation and PR creation.

**Q: How practical is it in non-English environments?**
**A:** While the command logic (system prompts) is written in English, the dialogue (the Q&A) with the AI can be conducted smoothly in other languages. In fact, by creating rigorous definition documents, you can eliminate the ambiguity inherent in natural language and achieve higher precision outputs.

## Conclusion: Arm Yourself for the AI-Native Era

Matt Pocock’s `skills` is a "manifesto" for every engineer who wishes to master AI. It moves us away from vague "Vibe Coding" and elevates the AI to a true pair-programming partner. The concrete methods for achieving this are concentrated right here.

Whether you view AI as a mere labor-saving tool or as a "cyborg part" that extends your own engineering capabilities is up to you. The moment you integrate this repository into your environment, your development process will enter a new dimension.

🚀 **[Check out mattpocock/skills on GitHub](https://github.com/mattpocock/skills)**
