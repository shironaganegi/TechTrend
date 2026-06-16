---
title: "ログベンチマークの罠：「最速」の選択がシステムを崩壊させる理由と、真の選定基準 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# The Trap of Log Benchmarks: Why Choosing the "Fastest" Can Break Your System, and the Real Selection Criteria

How do you choose a logging library when starting a new project or optimizing the performance of an existing system? If you make your choice solely based on "high GitHub star counts" or because it "records the 'fastest' speeds in benchmarks," you are heading down a highly dangerous path.

In the worst-case scenario, this can trigger unexpected, large-scale outages in production, leaving you scrambling with late-night emergency responses.

In this article, we will thoroughly dissect the technical underpinnings behind why you should never take log library benchmark figures at face value—a common blind spot even among experienced engineers. Through this piece, we hope to help you cultivate the "true discernment" needed to push your production environment's reliability and robustness to the absolute limit.

---

## Why You Must Re-evaluate Your Log Library Selection Criteria Now

In modern development, where microservices and serverless architectures have become the standard, logs have completely evolved past simple "plain-text outputs for debugging." With the adoption of distributed tracing and structured logging (JSON format), the volume of data processed by logging libraries and the resulting load on CPU and memory have increased like never before.

Despite this, many developers uncritically accept benchmark results boasting the title of "fastest logger" and adopt these libraries. As a result, they find themselves facing severe production issues such as Out of Memory (OOM) errors and unexplained log loss. In reality, log benchmarks are riddled with "cleverly hidden traps" masquerading as measurement conditions.

<div class="expert-opinion">
<strong>Editor-in-Chief's Eye: Benchmarks are "Extreme-Condition Demos"</strong><br>
In most cases, benchmark scores are nothing more than the result of completely mocking disk I/O and performing buffering in memory under the most ideal conditions. In reality, production servers are exposed to poor network connectivity, congested storage, limited shared memory, and sudden traffic spikes. Buying the "fastest" logger based on benchmarks is like buying an F1 race car stripped down to the bare minimum for track use as your daily family car. What we really need to know is: "How stably can it drive on a bumpy road when packed to maximum capacity?"
</div>

---

## Three Fatal Traps Hidden Behind Benchmarks

When evaluating logging library benchmarks, there are key specifications hidden behind the numbers that you must verify. Let's break them down from three perspectives.

### 1. Speed Ratings That Ignore "Allocations" (Memory Allocation)
Even if a logger claims it can "write 10 million logs per second," if it frequently triggers dynamic memory allocation with every single log output, its real-world performance will degrade significantly.

In languages utilizing garbage collection (GC) like Go or Java, frequent memory allocation from creating temporary objects triggers **GC "Stop-The-World" (complete program pause)** phases. While such loggers might look fast during short-lived benchmark runs, running them in a production environment for days will cause overall application latency to spike due to high GC frequency.

*   **Metrics to Watch:** `B/op` (allocated bytes per operation) and `allocs/op` (number of allocations per operation). Loggers with values near zero (Zero-allocation loggers) are the ones that deliver true stability and speed over long-term operations.

### 2. The Time Bomb Called "Asynchronous Logging"
Many of the loggers recording astronomical throughput in benchmarks leverage "asynchronous logging" under the hood. Instead of writing log output to storage immediately, this mechanism temporarily queues logs in an in-memory buffer and batches them asynchronously on a background thread.

Because it avoids blocking the application threads, benchmark scores skyrocket. However, this introduces severe operational risks:

*   **Blocking or Dropping Due to Full Buffers:** If a sudden traffic spike causes log generation to outpace disk write speeds, the buffer will fill up. At this point, you are forced to choose between blocking the application thread (killing performance) or discarding (dropping) logs.
*   **Log Loss on Abnormal Process Termination:** If the application process crashes due to an OOM, segmentation fault, or panic, all the "most critical error logs right before the crash" residing in the in-memory buffer will be lost forever.

### 3. Loose Measurement Conditions for Serialization
In the context of modern observability, adopting "structured logging" (like JSON format) is essential to integrate with log monitoring platforms like CloudWatch or Datadog. However, some benchmarks only measure simple string outputs (plain text).

The most CPU-intensive part of log processing is "serialization (encoding)"—converting objects into JSON format. Libraries that dynamically parse key-value pairs are exponentially slower than statically typed ones. You must strictly scrutinize what kind of data structures were actually used in the benchmark measurements.

---

## Feature Comparison of Representative Log Libraries (Go Language Example)

Taking the Go language as an example, let's compare the design philosophies and trade-offs of major loggers.

| Library Name | Performance Philosophy | Key Features and Considerations |
| :--- | :--- | :--- |
| **zap** (by Uber) | Structured, fast, low allocation | Designed to eliminate allocations as much as possible by using strong typing (e.g., `zap.String`). While configuration is somewhat complex, it offers an exceptionally high balance of reliability and performance in production environments. |
| **zerolog** | Strict zero-allocation orientation | Specialized in JSON output, thoroughly suppressing memory allocations. It provides an intuitive chained-method interface for a great developer experience, but you must be careful about log loss risks when enabling asynchronous buffering. |
| **slog** (Go standard) | Standardization, high extensibility | Introduced to the standard library in Go 1.21. While not the fastest, the benefit of eliminating external dependencies is huge. Can be flexibly customized by pairing with third-party handlers. |
| **logrus** | Legacy, feature-rich | The former de facto standard. Its design is outdated and triggers frequent allocations, making it not recommended for new projects requiring high performance. |

---

## A "Logger Selection Checklist" to Prevent Failures in the Field

Before entering the implementation phase of your system, we recommend using the following checklist to establish alignment within your team.

1.  [ ] **How much log loss risk can you tolerate?**
    *   For systems where losing even a single log entry is unacceptable—such as payment transactions or audit logs—"synchronous logging" (Sync) is mandatory. On the other hand, if you prioritize application latency over losing a few access logs, consider "asynchronous logging" (Async).
2.  [ ] **Have you accounted for stdout (standard output) transfer performance in container environments?**
    *   In containerized environments like Kubernetes, logs are typically collected by container runtimes via standard output. The overall performance depends not just on the logger's standalone throughput, but also on whether proper buffering is working when writing to stdout.
3.  [ ] **Is it easy to change or extend the schema of structured logs (JSON)?**
    *   Does it conform to the ingestion specifications of log analysis platforms like Datadog, Splunk, or Elasticsearch for seamless parsing?

---

## FAQ: Common Questions in Log Design

### Q1. What if I still want to adopt the logger with the fastest benchmark?
**A.** Adopting it is not inherently wrong, but you must run load tests that simulate hardware limits and sudden traffic spikes. Particularly when introducing asynchronous logging, you must strictly ensure via code review that buffer sizes are properly configured, and that a `Flush()` (or `Sync()`) operation is reliably executed to force-flush logs from memory when the application terminates.

### Q2. Are standard loggers (like Go's slog or Node.js's console) insufficient?
**A.** For small-to-medium-sized services or systems that do not handle extreme high traffic, modern standard loggers (e.g., Go's `slog`) are perfectly adequate for production. Considering the overhead of depending on third-party libraries (security vulnerability risks and version management costs), a highly pragmatic architectural approach is to start with the standard logger and incrementally migrate to `zap` or `zerolog` only when performance bottlenecks are explicitly detected.

### Q3. There are too many logs in production, which is putting pressure on disk space and costs.
**A.** This is a matter of proper "log level design" and "rotation/retention policies" rather than logger performance. Restrict the default production output level to `INFO` or `WARN` and eliminate unnecessary `DEBUG` logs. Additionally, adopting a logger with "rate-limiting" capabilities that automatically throttles log volume under specific high-load conditions is a highly effective solution.

---

## Conclusion: Choose the "Most Predictable" Logger, Not the Fastest

What truly matters in logging library selection is not how much instantaneous processing speed it can deliver at its peak (maximum throughput), but rather **how well it maintains predictable behavior without squeezing application resources when the system is under extreme load (predictability)**.

Instead of getting bedazzled by flashy benchmark charts, we encourage you to properly understand memory allocation behaviors, error-handling robustness, and synchronous/asynchronous mechanisms to design a truly resilient system architecture.
