---
title: "最先端LLMでも意見が分かれる「不一致問題」——現実世界のファクトチェックにおける限界とエンジニアが取るべき解決策 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# The "Disagreement Problem" Where Even State-of-the-Art LLMs Divide: Limits of Real-World Fact-Checking and Solutions for Engineers

"If we integrate state-of-the-art LLMs like GPT-4, Claude, and Gemini, we can automate fact-checking in our products."

If you are designing your systems with this assumption, you may need to reconsider.

Currently, a major challenge is surfacing at the forefront of AI research. This is the phenomenon of **"LLM Disagreement,"** where state-of-the-art LLMs completely divide on opinions during real-world fact-checking. This is not merely a temporary glitch, but a structural issue that fundamentally shakes the reliability and decision-making processes of AI. For developers and product managers operating AI agents or RAG (Retrieval-Augmented Generation) systems in production, this behavioral uncertainty poses a significant risk.

In this article, we will unpack the background and mechanics behind this "disagreement problem" and present concrete engineering methods that can be applied in practice right away.

---

## Why Do AIs Draw Different Conclusions Over "Objective Facts"?

To understand the essence of this issue, we must clearly distinguish between traditional "hallucination" (false outputs not grounded in facts) and this new "disagreement."

Traditional hallucination occurs due to a lack of training data or probabilistic fluctuations in token generation. On the other hand, LLM disagreement is a divergence that occurs at the level of reasoning and semantic interpretation: **even when given the exact same evidence (source document), Model A outputs "True," Model B outputs "False," and Model C outputs "Unclear."**

<div class="expert-opinion">
<strong>Tech Watch Perspective: This is not just a technical bug, but a "bias in contextual interpretation"</strong><br>
Real-world news and claims have an extremely high volume of "gray areas" that cannot be clearly defined as black or white. LLMs do not simply cross-reference dictionary facts; they make judgments based on the "safety standards (safeguards)" and "contextual nuances" embedded during training. In other words, the current reality is that each model's "philosophy and tuning quirks" warp the conclusions of fact-checks that ought to be objective. Blindly trusting AI to drive automation is seriously high-risk.
</div>

---

## Three Structural Factors Behind "Disagreement" in Frontier LLMs

Why does this divergence in interpretation occur in cutting-edge commercial models (such as GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro)? The primary factors can be summarized into the following three points.

### 1. Differences in "Tolerance" Toward Nuance and Modifiers
Real-world claims often contain subjective adjectives and adverbs. For example, when verifying the claim "Company A has developed an innovative new technology," evaluation criteria differ across models.
*   **GPT-4o**: Tends to judge strictly, stating: "Since similar technology has existed in the past, the term 'innovative' is inappropriate (= False)."
*   **Claude 3.5 Sonnet**: Tends to interpret contextually, stating: "Since this is a first in terms of the scale of commercialization, the intent of the phrasing is reasonable (= True)."

As shown here, the "threshold" for how much exaggeration is tolerated in a claim is not standardized across models.

### 2. Divergence in Prioritizing Source Grounding
When external sources are provided using RAG or other methods, LLMs do not evaluate all information equally. Due to model training biases and RLHF (Reinforcement Learning from Human Feedback), the "definition" of what makes a document reliable differs. As a result, even though they are reading the exact same reference text, the priority of which parts they extract and use for evaluation becomes misaligned.

### 3. Differences in Characteristics When Comparing Structured Data

Summarizing the behavioral characteristics of each LLM in fact-checking yields the following:

| Model Characteristics | Fact-Checking Tendencies | Likely Risks |
| :--- | :--- | :--- |
| **GPT-4 Series** | Logically strict. Does not miss even slight contradictions. | Tends to reject "partially true" claims as entirely "False." |
| **Claude 3 Series** | Deep contextual understanding, grasping intent. | Judging criteria can be slightly too lenient, risking the acceptance of gray-area claims. |
| **Gemini Series** | Rapid access to search sources. | Strong with the latest information, but easily swayed by noise within the search results themselves. |

---

## Workarounds to Overcome "LLM Disagreement" in Production

If verification systems are automated while ignoring this disagreement issue, it will trigger system failures such as presenting misinformation to users or unjustly rejecting legitimate information due to misjudgment. There are two primary approaches engineers should take at the implementation phase.

### Solution 1: Implementing a Consensus (Ensemble Majority) Architecture
Relying on a single LLM instance for verification is risky. A highly effective method is to implement a consensus layer that aggregates individual judgments from multiple different language models (from different model families).

Below is an implementation concept for a verification evaluation incorporating majority voting logic in Python.

```python
import openai
import anthropic

def check_fact_consensus(claim, source_context):
    # Evaluation by GPT-4o
    gpt_opinion = call_gpt4o(claim, source_context) # "True", "False", "Unclear"
    
    # Evaluation by Claude 3.5
    claude_opinion = call_claude35(claim, source_context) 
    
    # Evaluation by Gemini
    gemini_opinion = call_gemini(claim, source_context)
    
    opinions = [gpt_opinion, claude_opinion, gemini_opinion]
    
    # Majority vote logic
    most_common = max(set(opinions), key=opinions.count)
    is_consensus = opinions.count(most_common) >= 2
    
    return {
        "final_verdict": most_common,
        "consensus_reached": is_consensus,
        "details": {"gpt": gpt_opinion, "claude": claude_opinion, "gemini": gemini_opinion}
    }
```

### Solution 2: "Strict Structuring of Judgment Criteria" via System Prompts
Asking an LLM open-ended questions like "Is this claim correct?" easily invites model-specific bias. You must break down the judgment, explicitly define the Chain-of-Thought, and apply evaluation criteria that are closer to a rule-based system.

```text
[Instructions]
Evaluate the given claim based strictly on the following three criteria only.
1. Does the "numerical value" in the claim match the source? (Yes/No)
2. Is the "relationship between subject and object" in the claim correct? (Yes/No)
3. When excluding exaggerations, is the essential fact stated in the source? (Yes/No)
Judge as "True" only if all items are Yes.
```

---

## FAQ: Technical Questions Regarding Fact-Checking with LLMs

**Q1: Doesn't implementing RAG (Retrieval-Augmented Generation) solve the disagreement problem?**

**A1:** No, it does not. RAG is a technology used to "inject the correct primary source information into the context." Disagreements still occur because variances arise in how each model interprets whether the claim is logically correct based on that injected primary information during the reasoning stage.

**Q2: Which LLM is currently the most reliable for fact-checking?**

**A2:** Choosing a single model is not the optimal solution. While GPT-4o is suited for strict logical structures and scrutinizing numerical data, Claude 3.5 Sonnet has the upper hand when it comes to reading between the lines of context and interpreting metaphors or sarcasm. It is essential to design your system to use different models—or combine them—depending on the nature of the target data.

**Q3: Constantly calling multiple models will cause API costs to spike. Are there countermeasures?**

**A3:** We recommend a design that divides the judgment process into stages (cascading). Run lightweight, fast models (such as GPT-4o-mini or Claude 3.5 Haiku) for primary screening. Only escalate boundary cases—where judgments diverge or the "Confidence Score" falls below a certain threshold—to an ensemble of high-performance models or human review. This allows you to optimize the trade-off between cost and accuracy.

---

## Conclusion: Moving Toward a Distributed, Collaborative Architecture Not Reliant on a Single "Intelligence"

LLM disagreement in fact-checking reveals the limitations of AI while simultaneously providing new guidelines for system design. We must move away from seeking a single answer—"selecting the single best model"—and shift toward a multi-angled architectural design that **"cooperates multiple models with different characteristics to ensure objectivity."**

Precisely because we are dealing with a technology like AI that can possess "subjectivity," its system design demands robust "objectivity." Let us build resilient evaluation systems and advance product development that earns unwavering trust from users.
