---
title: "【削除済み】MSがハリー・ポッターでLLM学習？RAG開発で絶対に踏んではいけない「著作権」の地雷 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# [Deleted] Did Microsoft Train an LLM on Harry Potter? The "Copyright" Landmine You Must Avoid in RAG Development

"You've got to be kidding. Did Microsoft try to use magic in an official blog post and end up provoking the wrath of their legal department?"

Recently, the tech industry timeline was abuzz with a story that was, to put it mildly, less than flattering. It centers on an instructional article published on the official Azure SQL blog. In it, the author detailed a process—bold to the point of recklessness—that involved importing the full text of *Harry Potter and the Sorcerer's Stone* as data for LLM (Large Language Model) training and retrieval.

The result was, predictably, immediate deletion. Now, all that remains is a 404 void.

However, this isn't a story we can just shrug off as a "giant's simple oversight." For every engineer venturing into AI implementation, this incident visualizes a **"legal and ethical landmine"** that could just as easily be under their own feet. By reading this, you'll learn how to ensure the product you've poured your heart into doesn't one day get hit by a "Killing Curse" named copyright infringement.

## 💡 What Happened? Behind the Scenes of the Broken Spell

The post in question was a hands-on guide for building a RAG (Retrieval-Augmented Generation) system using LangChain, with Azure SQL serving as the vector database. The technology itself is fantastic. However, the choice of material was catastrophic.

- **Entering the "Forbidden Forest"**: The article included code that imported the text of *Harry Potter*—a massive lump of copyrighted intellectual property—directly as demo data.
- **Official Negligence**: Even Microsoft, a global leader in AI, tripped over the absolute basics of license management. This fact sent shivers down the spines of engineers everywhere.
- **Erased Evidence**: Following backlash online, the article vanished at the speed of light. Now, the "traces of magic" can only be found via web caches.

Even if you have the finest kitchen knife, cooking with stolen ingredients is still a crime. In engineering, "data selection" carries an equally heavy weight of responsibility.

## 🔧 The Technical Core: The Potential of Azure SQL × LangChain

While overshadowed by the controversy, the technology being introduced is actually extremely practical. The vector search capability in Azure SQL is a "magical" upgrade that allows you to repurpose the "foundation of trust" that is the existing SQL Server into a part of an AI's brain.

```python
# Conceptual implementation (Please, use clean data!)
from langchain_community.vectorstores import AzureSqlVectorStore
from langchain_openai import OpenAIEmbeddings

# Azure SQL connection settings
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:..."

# Vectorize and save (The data here should be the fruit of your own hard work)
vector_store = AzureSqlVectorStore.from_documents(
    documents=my_legal_docs, 
    embedding=OpenAIEmbeddings(),
    connection_string=connection_string
)
```

The real value here—which should have been the focus—is the "ease of use": being able to build RAG using familiar SQL skills without having to learn a specialized vector-only database from scratch.

## 🚀 3 Golden Rules to Keep RAG Development Out of the "Landmine Zone"

Using this incident as a lesson, let's redefine the rules for safe development.

1.  **Never test with "borrowed" data**: Always use public domain sources like "Project Gutenberg" or data your company specifically holds the rights to for sample data.
2.  **Trust the "Infrastructure Walls"**: To protect data rights and confidentiality, it is the right move to manage vector data in an enterprise-grade, closed environment like Azure SQL.
3.  **Output Censorship (Guardrails)**: What if the LLM tries to spit out a line that sounds suspiciously like copyrighted material? You should implement mechanisms to prevent this via system prompts or filtering layers.

## ✅ Pros & Cons

- **Pros**: Completing vector searches within Azure SQL alone is significantly easier in terms of operational overhead. Being able to leverage existing assets is a huge advantage.
- **Cons**: Even "official documentation," which should be a source of truth, can fall victim to legal errors. What we need is healthy skepticism, not blind faith.

<!-- AFFILIATE_START -->

### 👇 Recommended Services for Engineers 👇
[**🌐 Get your own domain at "Onamae.com." TechTrend Watch uses it too!**](https://www.onamae.com/)

<!-- AFFILIATE_END -->

## 💾 Summary: Data Selection is a Core Part of "Engineering"

It's easy to scoff and say, "I can't believe Microsoft made such a rookie mistake." However, what we should really be doing is raising our **awareness of data provenance** in AI development to the same level as code debugging.

No matter how beautiful the algorithm, it is a house of cards if built on inappropriate data. No matter how far technology evolves, the final safeguard for a product is the ethics and caution of the person who built it.

The next time you build a RAG system, stop for a moment and check if you're tempted to copy-paste a passage from your favorite novel as demo data.

I hope this article helps protect your product. If you found it insightful, please share it with your fellow engineers.
