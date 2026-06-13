---
title: "圏論的ディープラーニング入門：Compositional LearningとBackprop as Functorが導く「学習を組み立てる」未来 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# Introduction to Categorical Deep Learning: The Future of "Assembling Learning" Led by Compositional Learning and Backprop as Functor

While modern deep learning has made remarkable progress, much of its network architecture design still relies on ad-hoc trial and error based on "experimentation and intuition." Addressing the fundamental question, "Why does this specific combination work so well?" with mathematical beauty and rigor is an emerging paradigm called **"Categorical Deep Learning (CDL)"**, and the core philosophy driving it is **"Compositional Learning."**

In this article, moving beyond a simple listing of mathematical formulas, we will thoroughly explore the disruptive impact of "Backprop as Functor" on design paradigms from a perspective that bridges engineering and mathematics. By reading this article, you will gain insights that help transform "black-box AI" into a "designable, reliable, and precise machine."

---

## 💡 Why Rebuild Learning with "Category Theory" Now?

The standard approach in conventional deep learning has been to build massive, monolithic models and optimize them entirely end-to-end. However, as systems grow larger, this approach makes it extremely difficult to predict behavior beforehand or safely reuse modules individually.

Just as software engineering constructs complex systems by combining "functions" and "microservices," can we also build deep learning as a **"combination of guaranteed components"**? Compositional Learning is a powerful approach directly addressing this challenge.

<div class="expert-opinion">
<strong>Tech Watch Perspective:</strong><br>
Category Theory is the mathematical study of the "architecture of relationships." Applying this to machine learning is not about simply manipulating formulas. It is an attempt to bring "loosely coupled, highly cohesive" component-oriented design—common in system development—into the inner workings of deep learning (such as gradient propagation and parameter update dynamics) with mathematical guarantees. If realized in practice, it could allow us to safely connect previously trained "inference modules" or "control modules" like Lego blocks to execute new tasks without any retraining.
</div>

If we can mathematically guarantee that "the behavior of the entire system will not break" when combining models, we can achieve true modular AI, combining large-scale models without fine-tuning. Category theory provides that robust mathematical foundation.

---

## 🛠️ Core Concept: What is "Backprop as Functor"?

Proposed in a landmark 2017 paper by Brendan Fong, David Spivak, and Rémy Tuyéras, "**Backprop as Functor**" rigorously formulates the sequence of processes in deep learning—"forward propagation (Forward)," "backward propagation (Backward)," and "parameter update (Update)"—as a **"functor"** in category theory.

The key points of this mathematically organized structure lie in the following three layers:

1. **Category of Parameterized Morphisms (Para)**:
   A category that models not only the mapping from input $X$ to output $Y$, but also explicitly models the parameter space $P$ that controls it. Each "layer" or subnetwork in deep learning corresponds to a morphism in this category.
2. **Category of Learners (Learner)**:
   A category where the morphisms are abstract objects (learners) containing a set of three dynamics: "forward propagation," "backward propagation," and the "optimization step (gradient update)."
3. **Correspondence as a Functor**:
   The mapping from `Para` to `Learner` acts as a "functor" (a mapping that preserves morphism composition and identity morphisms). This implies a crucial fact: **"When two network modules are combined using the rules of forward propagation, the backward propagation process of the entire system matches exactly with the natural composition of the backward propagation processes of the individual modules."**

The software engineering ideal—that "the healthy composition of parts automatically guarantees the healthy behavior of the whole"—has been mathematically proven within the dynamic computational mechanism of backpropagation.

---

## 📊 Traditional Approach vs. Categorical Deep Learning

The shift in design philosophy brought about by this paradigm can be summarized as follows:

| Dimension | Traditional End-to-End (PyTorch/TensorFlow) | Categorical (Compositional) Deep Learning |
| :--- | :--- | :--- |
| **Design Philosophy** | Tightly coupled networks, a single massive black box | Loosely coupled components, mathematically rigorous "composability" |
| **Reusability** | Extracting or reusing parts requires retraining to prevent catastrophic forgetting | Pre-trained components (Learners) can be safely and directly combined without retraining |
| **Mathematical Guarantees** | Behaviors like local optima or vanishing gradients must be verified experimentally | Gradient dynamics during composition can be mathematically proven beforehand from constituent elements |
| **Implementation Process** | Can be written quickly and intuitively, but debugging and ensuring interpretability are extremely difficult | Requires theoretical design, but structurally eliminates room for bugs to creep in |

---

## ⚠️ Bottlenecks and Concerns for Practical Adoption

Despite how beautiful this theory is, there are several practical hurdles to fully adopting it in production environments at this stage.

- **Computational Efficiency and Hardware Optimization Barriers**:
  Current ecosystems like PyTorch, JAX, and GPUs/TPUs are optimized for batch parallel processing of massive tensor operations. Directly and naively serializing and implementing a categorically modularized system can sometimes result in inferior execution speeds and memory efficiency.
- **High Mathematical Barrier to Entry**:
  It demands extremely advanced knowledge of abstract algebra—such as "functors," "bicategories," "symmetric monoidal categories," and "lenses"—from the developer community, making the education and learning curve for engineers exceptionally steep.

As a result, while the theoretical framework is highly complete, the ecosystem is still in its infancy. However, in recent years, libraries and compilers like **Discopy** and **Catlab.jl**, which allow for building and visualizing categorical pipelines at the code level, have been evolving, rapidly bridging this gap.

---

## ❓ FAQ (Frequently Asked Questions)

**Q1: Should average AI engineers start studying category theory right away?**
**A:** There is no need to master the equations immediately. However, if you are involved in complex system integration, such as designing multi-agent systems or merging control theory with deep learning in robotics, exposing yourself to the basic concepts (especially monoidal categories and the philosophy of compositionality) will be a powerful weapon for the future.

**Q2: How can I experience "Backprop as Functor" through code?**
**A:** Python's `discopy` library is highly recommended. Tutorials are available that let you build and train quantum machine learning or natural language processing pipelines based on a diagrammatic representation called "string diagrams." Starting with visual comprehension is the fastest way to deepen your understanding.

**Q3: Will this lead to the creation of new optimization algorithms?**
**A:** Yes. In fact, by categorically abstracting and generalizing existing methods like Adam and SGD, new "update rules" with geometric consistency have been proposed. This is leading to the discovery of next-generation learning algorithms that are less prone to falling into local minima and possess better global convergence properties.

---

## 🚀 Conclusion: From "Writing" Learning to "Assembling" Learning

The era of relying on luck—"I don't know why it works, but the accuracy is high"—is coming to an end. Compositional Learning is the missing link to elevate deep learning from empirical "alchemy" into a predictable, highly reliable "true engineering."

Shifting from hand-coding development to assembling components with mathematical guarantees, category theory will play an increasingly prominent role as the common language for rigorously designing AI as a system.
