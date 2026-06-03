---
title: "LLM全盛期に『ゼロつく②』第6章を今こそ復習すべき理由：LSTMの構造をスクラッチで理解し、技術的優位性を築く (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# Why You Should Review Chapter 6 of "Deep Learning from Scratch ②" Right Now in the Age of LLMs: Master LSTM Architecture from Scratch and Build a Technical Edge

In today's landscape, where Large Language Models (LLMs) like ChatGPT and Claude have become standard in development, it is natural to wonder, "Why bother learning classic architectures like RNNs and LSTMs now?" However, to truly grasp the essence of "Attention" and "context windows" underlying state-of-the-art LLMs, and to gain deep insight into next-generation architectures emerging today, understanding the "Gated RNN" mechanisms covered in Chapter 6 of the masterpiece *"Deep Learning from Scratch ②: Natural Language Processing"* is an essential step.

In this post, using the "LSTM implementation" from Chapter 6 as our foundation, we will thoroughly analyze from a technical and practical perspective why gated RNNs were able to solve the vanishing gradient problem, and the true value of building them from scratch for modern engineers.

<div class="expert-opinion">
[Tech Watch Perspective]
To break away from being a mere "wrapper developer" who simply calls LLM APIs and instead build a unique edge as an AI engineer, you must precisely grasp tensor operations and gradient behaviors inside neural networks at the code level. In particular, the separation of the "Cell" and "Hidden State" in LSTMs, and the control of gradient flow via the "Hadamard product (element-wise product)" detailed in Chapter 6, are directly linked to the theoretical backbone of state-of-the-art State Space Models (such as Mamba) and Linear Attention. Bypassing these fundamentals could restrict your long-term growth as an engineer.
</div>

---

## 1. The Bottlenecks of Traditional RNNs and the Innovation of "Gates"

Traditional Recurrent Neural Networks (RNNs), which process sequential data recursively, are theoretically elegant and extremely simple in structure. However, when handling long sequential data in practice, developers inevitably face critical mathematical limitations: **"Vanishing Gradient"** and **"Exploding Gradient"**.

As backpropagation travels back through time steps, sequential matrix multiplications cause gradients to decay or explode exponentially. The architecture designed to fundamentally solve this issue is the **"Gated RNN"**, the main theme of Chapter 6, with **LSTM (Long Short-Term Memory)** being its most prominent representative.

Instead of simply propagating information forward, LSTMs introduce "gates" to dynamically control the flow of information. By allowing the network itself to learn the opening and closing state of gates designed with sigmoid functions (output range 0.0 to 1.0), a dynamic control system is established. Through this, the model adaptively determines "what past information to retain, what new information to absorb, and what information to output."

---

## 2. LSTM Architecture: The Synergy of Three Gates and the Memory Cell

At the core of LSTM is the interaction between three gates and a single "memory cell." By writing this from scratch (using only Python and NumPy) without relying on frameworks, you can vividly experience the process of mathematical equations transforming into working programs.

| Component | Key Role | Mathematical Dynamics |
| :--- | :--- | :--- |
| **forget gate** | Determines how much of the unnecessary information from the past memory cell $C_{t-1}$ should be discarded. | Multiplies the past memory by an element-wise coefficient of 0.0 to 1.0. |
| **input gate** | Estimates the importance of newly input information that should be written to the memory cell. | Multiplies the new candidate information (tanh output) by the activation value of the input gate. |
| **output gate** | Controls the hidden state $h_t$ to be output to the next time step or higher layers from the updated memory cell $C_t$. | Multiplies the memory cell value (normalized by tanh) by the activation value of the output gate. |
| **Memory Cell ($C_t$)** | The "context highway" of LSTM. Gradients flowing here propagate via addition, preventing vanishing gradients. | $C_t = f \odot C_{t-1} + i \odot g$ (* $\odot$ represents the element-wise Hadamard product; addition preserves backpropagation) |

The greatest breakthrough lies in the fact that **"backpropagation in the memory cell is executed via 'addition'."** Unlike the sequential matrix multiplications (multiplication) in a standard RNN, additive propagation prevents gradient decay, enabling long-distance information transmission (solving long-range dependencies). You can only truly appreciate the beauty and rationality of this elegant mathematical structure by implementing `backward` manually.

---

## 3. RNN, LSTM, and Onto Transformer: Unraveling the Evolutionary Tree

By organizing the lineage leading to the Transformer, which is today's de facto standard, the trade-offs of each architecture become crystal clear.

- **RNN**: Extremely simple in structure with low computational cost, but suffers from fatal flaws in retaining long-term context (vanishing gradients). Parallel processing is impossible due to sequential temporal dependencies.
- **LSTM**: Overcomes the long-term memory issue using a gate structure. However, the internal parameters become complex, and its sequential nature makes large-scale parallel training using GPUs difficult.
- **Transformer**: Adopts Self-Attention to achieve batch parallel processing independent of temporal order. While offering overwhelming expressiveness, its computational complexity grows quadratically with the sequence length $N$ ($O(N^2)$), heavily consuming computational resources (VRAM) as the context window scales up.

In recent years, to overcome the computational limit of Transformers (quadratic time complexity), **State Space Models (SSM, with Mamba being a prominent example), which function as "RNNs that can be parallelized during training while operating in constant time/memory during inference,"** have gained significant attention. The "fusion of dynamic state representation and selective gating" behind SSMs is a direct extension of the "gate-controlled" philosophy pioneered by LSTMs. In other words, understanding LSTMs is the ultimate shortcut to decoding next-generation architectures.

---

## 4. Three Implementation Pitfalls and Practical Debugging Approaches

When actually implementing the code from Chapter 6 of *Deep Learning from Scratch ②*, developers often fall into traps due to the gap between theory and implementation. Here are the typical pitfalls and how to address them:

1. **Proper Tuning of Gradient Clipping**
   Even with LSTMs, the risk of gradient explosion is not zero in extremely long sequences. To prevent this, implementing "Gradient Clipping"—which scales gradients down when the L2 norm of all parameter gradients exceeds a threshold—is essential. Without this, your loss function can suddenly output `NaN` during training, causing the model to collapse.
   
2. **The "1.0" Barrier in Forget Gate Bias Initialization**
   By convention, the bias of the LSTM hidden layers, especially the initial bias corresponding to the forget gate, is set to `1.0` (or a similar positive value). If you leave this at 0.0 or a random small decimal at initialization, the forget gate will tend to "block everything (near 0.0)" in the early stages of training, preventing long-range information from propagating. This practice is extremely important when building custom models in production.

3. **Balancing Truncated BPTT Context Length and Memory Constraints**
   Designing the window size for "Truncated BPTT," which cuts the backpropagation chain at a specific length, involves a trade-off between system resource constraints and learning capability. If you set the context length too long, you will easily deplete the VRAM (or main memory) required to hold the computation graph, resulting in an Out of Memory (OOM) error. In the early stages of development, it is highly recommended to start verification with a smaller size (e.g., 10 to 30 steps).

---

## 5. FAQ to Solidify Theory

### Q1. In the current golden age of Transformers, why spend time learning LSTM?
**A.** Because it teaches you the design philosophy of an extremely efficient dynamic system: "compressing and maintaining state within a fixed-size memory." Furthermore, in domains with strict resource and power constraints like edge AI or real-time time-series analysis (sensor data, embedded speech recognition, etc.), lightweight and computationally cheap architectures like LSTMs or GRUs are still frequently the optimal solution. Developing a foundational understanding is essential for cultivating the judgment needed to choose the right technology for the right job.

### Q2. What is the functional difference between GRU (Gated Recurrent Unit) and LSTM?
**A.** GRU is a lightweight variant that merges LSTM's three gates into two (reset gate and update gate) and consolidates the memory cell and hidden state into one, thereby reducing the parameter count. When the dataset is relatively small or when you want to minimize computational resources, GRUs tend to converge faster while preventing overfitting. In practice, the standard approach is to establish a baseline with the highly expressive LSTM first, and then explore GRU as an optimization step.

### Q3. What is the best way to verify the correctness of a model built from scratch?
**A.** As an initial test, we recommend performing an "overfitting test" using a tiny toy dataset (e.g., a short, fixed sentence made of a few words, or a simple sine wave). If forward propagation and backpropagation are mathematically linked correctly, the model should completely memorize the toy data within a few epochs, and the loss will converge close to zero. If you feed large-scale text data into the model without conducting this initial validation, debugging and isolating issues becomes extremely difficult.

---

## 6. Conclusion: Stripping Away Abstracted Libraries to Grasp the Essence

Simply repeating `model.fit()` or API calls on highly abstracted frameworks makes it difficult to survive in the rapidly evolving AI industry. The ability to mentally visualize tensor operations unfolding inside an architecture, and to identify and resolve bottlenecks in backpropagation, is what builds a solid barrier to entry (technical advantage) as an engineer.

Chapter 6 of *Deep Learning from Scratch ②* is a timeless gateway to reaching that core essence. Take this opportunity to open up a Jupyter Notebook and meticulously build an LSTM from scratch, step-by-step. Witnessing mathematical formulas come to life as autonomous code and extracting features from raw information is, after all, the greatest thrill of engineering. 🚀
