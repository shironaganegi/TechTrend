---
title: "フレームワークに依存しない、数式とコードからLLMを再構築する超硬派カリキュラム「AI Engineering from Scratch」 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# "AI Engineering from Scratch": A Hardcore, Framework-Independent Curriculum for Rebuilding LLMs from Math and Code

"I feel like I'm hitting a wall just writing wrapper code for LangChain and LlamaIndex."
"I built an AI agent, but I can't logically explain what kind of reasoning or control is happening under the hood."

In the midst of today's massive shift toward AI, many engineers share this exact anxiety about dealing with "black boxes."

The GitHub repository we are introducing today, "**ai-engineering-from-scratch**", is the ultimate prescription for this exact pain point.

This is a hardcore, open-source curriculum spanning 435 lessons, 20 phases, and an estimated 320 hours of study. It reconstructs the entire scope of AI engineering using only "mathematical equations" and "raw implementation from scratch" without relying on third-party frameworks. It presents a highly robust roadmap designed to take you from a mere "consumer" of existing libraries to a "creator" who truly understands the essence of the technology.

---

## 💡 Why This Project Matters Now (Editor's Eye)

<div class="expert-opinion">
<strong>Editor-in-Chief TechWatch's Take:</strong><br>
Currently, data shows that while 84% of students and young engineers worldwide use AI tools, only a mere 18% feel confident enough to master them as professionals. The reason is obvious. Most educational materials on the market stop at superficial demonstrations like "Look, a chatbot running on just a few lines of copy-pasted code!" With that approach, you cannot debug why a loss curve isn't converging or understand how the internal Attention mechanism actually functions. This roadmap perfectly bridges that gap by completely dismantling the "black box" behind these libraries and guiding you to rebuild it all from scratch with your own hands.
</div>

---

## 🛠️ The Full Curriculum of "AI Engineering from Scratch"

The greatest strength of this curriculum lies in its bottom-up approach: **"instantiating algorithms into raw code directly from mathematical protocols, and only then abstracting them using production-ready libraries like PyTorch."**

You aren't allowed to call overly convenient APIs right from the start. It is carefully structured so that you first interpret the underlying mathematical and physical mechanisms at the code level, and only then can you truly appreciate the benefits of existing frameworks and the value of abstraction.

The 20-phase roadmap builds up meticulously, step-by-step, as follows:

```
Phase 0: Environment Setup & Tools
  └── Phase 1: Math Foundations (Linear Algebra & Calculus)
        └── Phase 2: Basic Machine Learning Algorithms
              └── Phase 3: Deep Learning Core (Implementing Backpropagation from Scratch)
                    ├── Phase 4 & 5 & 6: Computer Vision, Natural Language Processing (NLP), & Audio
                    └── Phase 7: Transformers (Implementing Attention from Scratch)
                          ├── Phase 8 & 10: Generative AI & Building LLMs from Scratch
                          └── Phase 11 & 12: LLM Engineering & Multimodal
                                └── Phase 13 & 14 & 15: MCP Servers & Agent Construction
                                      └── Phase 16 & 17: Multi-Agents, Infrastructure & Production Deployment
```

What is particularly noteworthy is the sheer breadth of programming languages covered. In addition to the de facto standard **Python**, implementation examples are provided in three other languages: **TypeScript** (high production utility), **Rust** (ideal for low-level optimization), and **Julia** (strong in data science). From frontend integration to system programming and ultra-fast tensor operations, you can choose the language that matches your domain.

---

## ⚖️ Comparison with Other Learning Resources (Hugging Face / Coursera)

Where does this project stand when compared to existing learning resources? The table below highlights its unique characteristics.

| Feature | Standard AI Courses (e.g., Coursera) | Hugging Face Course | ai-engineering-from-scratch |
| :--- | :--- | :--- | :--- |
| **Learning Approach** | Theoretical lectures + API calling | Library explanations & practice | **Implementation from scratch + Production deployment** |
| **Time Commitment** | Relatively low (video-centric) | Moderate (hands-on coding) | **Extremely high (Estimated 320 hours)** |
| **Technical Opacity** | Often leaves black boxes | Partially covered, practical level | **Completely eliminated (translating equations to code)** |
| **Deliverables** | Quizzes & assignments | Demo app deployment | **Reusable custom MCPs & custom Agents** |
| **Supported Languages** | Python only | Primarily Python | **Python, TS, Rust, Julia** |

While most resources teach you "how to assemble a pre-made puzzle," this curriculum starts from "chopping down the tree, designing, and carving out the puzzle pieces yourself." The barrier to mastery is incredibly high, but the resulting "adaptability" and "debugging capability" will place you light-years ahead.

---

## ⚠️ Pitfalls and Countermeasures in Practice

To succeed in this challenge, you must face three realities from the outset:

1. **Demanding Time Commitment**
   Completing the entire curriculum is estimated to take around 320 hours. Even if you study for 2 hours every single day, that translates to over 5 months. To maintain motivation, a highly effective strategy is to pinpoint and target specific phases directly related to your current interests, such as "Phase 7 (Transformers)" or "Phase 14 (Building AI Agents)."
2. **Securing Hardware Resources**
   While the early phases will run smoothly on any standard laptop, the later phases—such as implementing "LLM Fine-Tuning" and "Multimodal Processing"—benefit greatly from a local machine equipped with an NVIDIA GPU or an Apple Silicon Mac with sufficient Unified Memory. This will drastically speed up your iteration cycles.
3. **A Strictly Active Learning Attitude**
   There are no hand-holding instructional videos here. Your "autonomy as a developer" will be constantly tested as you parse through specifications and math equations written in Markdown, writing the code yourself to make the test suite pass.

---


### Q1. I have a strong aversion to math. Can I still complete it?
**A.** While a basic understanding of high-school-level math (linear algebra and calculus) is desirable, you don't need to give up. Phase 1 focuses strictly on rebuilding the mathematical foundations "truly necessary for AI." Rather than memorizing equations, you will go through the process of "converting formulas into code and actually running them," making the design highly intuitive even for abstract concepts.

### Q2. Why does an AI engineer need to learn Rust or Julia?
**A.** In modern AI production environments, Python is increasingly serving as merely an interface. Rust is an incredibly powerful weapon for accelerating inference engines and resolving data pipeline bottlenecks. Meanwhile, TypeScript is perfect for implementing agents that integrate tightly with frontends. Learning multiple languages serves as a solid differentiator, helping you become an "irreplaceable engineer" in a fast-evolving landscape.

### Q3. Is this truly 100% free?
**A.** Yes. This project is entirely free and published under the **MIT License**. The custom MCP servers and agent frameworks you build throughout the curriculum can be added to your portfolio or even integrated directly into your company's commercial projects.

---

## 📝 Editor-in-Chief's Summary

If you don't want your career to end as a programmer who merely wraps APIs built by others (like ChatGPT), you should bookmark this repository immediately and dive into Phase 0's environment setup.

What lies beyond the "magic veil" of frameworks? Once you spend 320 hours mastering the underlying math and physical architecture, you will gain an overwhelming competitive edge. No matter what new technology emerges next, you will instantly grasp its essence and optimize it with your own custom implementations. Build AI from the ground up with your own hands. Take your first step into this intellectual pursuit today.
