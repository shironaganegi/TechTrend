---
title: "【ISSデバッグ】宇宙の極限環境に学ぶ、システム保守と可観測性（Observability）の真髄 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# [ISS Debugging] The Essence of System Maintenance and Observability Learned from the Extreme Environment of Space

The "air leak" trouble that occurred on the International Space Station (ISS)—an extreme system orbiting approximately 400 kilometers above the Earth—is still fresh in our memories. Despite having to take temporary evacuation measures, the astronauts identified and repaired the cause of the leak through a tenacious investigation, successfully returning the station to normal operations.

At first glance, this might seem like an incident limited to astrophysics or specialized hardware. However, when we abstract the troubleshooting process, the very **philosophy of "incident response" and "observability"** that we software and system infrastructure engineers confront daily comes into sharp relief.

In this article, we dissect the "physical debugging" actually performed on the ISS to share essential insights for improving error handling, resource monitoring, and system resilience in terrestrial system development.

<div class="expert-opinion">
<strong>Editor-in-Chief Tech Watch's Professional Perspective:</strong><br>
With terrestrial cloud systems, we can easily achieve "temporary error mitigation" through container restarts or Auto Scaling. However, in space (ISS), where replacement parts and resources are strictly limited, "system reboots" or "disposable" approaches are impossible. That is why ISS maintenance operations incorporate the ultimate fail-safe design that every engineer should learn: thorough "Localization of the cause," "Containment of the impact," and "Phased recovery." This "physical debugging" approach serves as the best textbook for designing observability when building terrestrial distributed systems.
</div>

---

## 1. The Full Picture of the "Multi-Layer Monitoring System" Operating on the Edge of Space

In the absolute death of a vacuum, how does the ISS detect minute air leaks? It utilizes a highly sophisticated, multi-layered monitoring architecture that shares an incredible affinity with modern terrestrial system monitoring.

*   **Trend Monitoring via Time-Series Metrics (Air Pressure and Temperature Sensors)**
    The modules of the ISS are filled with high-precision environmental sensors that collect tiny fluctuations in air pressure and temperature as telemetry data at millisecond intervals, constantly streaming it to ground control stations. Crucially, they do not just monitor the "current value" but the "rate of pressure drop (slope)" as a trend. This is exactly the same philosophy used to detect the gradual depletion of disk capacity or thread pools in software systems.
*   **Physical Profiling (Ultrasonic Leak Detector)**
    When a leak is minuscule, trend analysis of pressure drops alone cannot pinpoint the source. This is where ultrasonic sensors come into play. They capture high-frequency acoustic emissions (sound waves inaudible to humans) generated when high-pressure air rushes into a vacuum, isolating the "anomaly signal" from ambient noise to perform profiling. This is highly analogous to attaching a profiler to analyze thread dumps or CPU cycles to identify application bottlenecks.
*   **Fault Isolation via Bulkhead Patterns (Compartment Isolation Tests)**
    To identify the failing module, astronauts sequentially closed hatches (bulkheads) and measured pressure changes within each sealed compartment. This is the literal implementation of the **"Bulkhead Pattern"** in system architecture. It demonstrates the golden rule of logically isolating a failed segment (such as a microservice or database connection pool) to prevent total system failure (system down) while identifying the root cause.

---

## 2. The Uncanny Similarity Between Physical "Air Leaks" and Logical "Memory Leaks"

The bugs and resource leaks we encounter in our sea of code behave in ways surprisingly similar to air leaks on the ISS. The comparison table below highlights the essential commonalities between physical troubles in space and logical troubles on Earth.

| Monitored Target & Lifecycle | ISS Air Leak (Physical Space) | Application Memory Leak (Logical Space) |
| :--- | :--- | :--- |
| **Root Cause** | Aging of hatch seals (gaskets), micro-debris impacts, or microscopic cracks. | Unreleased resources, retaining references to unused objects (preventing garbage collection). |
| **Early System Symptoms** | An extremely slow but steady downward trend in air pressure (over weeks or months). | Gradual rise in heap memory usage, slight latency degradation in initial response times. |
| **Catastrophic Impact (Worst-Case)** | Complete loss of pressure containment in modules, oxygen depletion, and mission abortion. | Out of Memory (OOM) errors, sudden process crashes leading to total service disruption. |
| **Ad-hoc Mitigation in Production** | Closing the hatch of the affected module (isolating the service), patching with sealants or specialized tape. | Forced termination of specific sessions, explicit pointer deallocation, or applying a hotfix to the leak site. |

Since resources (whether air or memory) are finite, capturing early warning signs of a leak, isolating the failure, and removing the root cause before total depletion occurs remains an immutable principle across any infrastructure.

---

## 3. "Design for Failure" vs. "Survivability": Cloud and Space Design Philosophies

The cloud infrastructures we design daily, such as AWS or Google Cloud, and the infrastructure design of the ISS are based on fundamentally different philosophies. From this contrast, we can learn the essence of true redundancy (resilience).

### Terrestrial Cloud Infrastructure: "Design for Failure"
Terrestrial systems are built on the assumption that "servers will eventually fail."
*   **Approach**: Instead of clinging to a single instance, the moment an error is detected, an Auto Scaling group automatically provisions replacement containers or VMs in a different Availability Zone (AZ), and a load balancer instantly reroutes traffic (a disposable, throw-away design).

### ISS Infrastructure (Space): "Survivability"
In space, it is impossible to instantly provision a new module, and the hardware replacement cost is astronomical.
*   **Approach**: The system must "prevent catastrophic failure even when broken, and keep running by being repaired on-site (Fault Tolerance)." When an error occurs, crew members immediately evacuate to a safe zone (the docked spacecraft acting as a "cold standby" safe house) while maintaining the infrastructure's minimal operating environment (life support systems). Then, they repeat precise, on-site debugging—both manual and remote—to patch the affected area and recover from degradation back to normal operations.

For teams operating legacy monolithic systems that cannot be easily disposed of, or on-premises systems tightly coupled with physical infrastructure, the ISS "Survivability" design offers far more practical lessons than modern cloud-native approaches.

---

## 4. The Pitfalls of Observability: Signal Design to Avoid "Alert Fatigue"

From ISS monitoring operations, we can learn how to combat a trap that operations managers frequently fall into: **"Alert Fatigue."**

In an incredibly complex system like the ISS, minor temperature fluctuations and pressure deviations occur daily. If alarms blared for every single fluctuation, the attention of the crew and ground controllers would degrade, leading them to overlook real, catastrophic leak signals. This is the exact same mistake development teams make when they flood Slack channels with notifications just because "CPU usage temporarily exceeded 80%."

### Two Defenses to Guarantee Reliability:

1.  **Symptom-Based Alerting Based on SLAs/SLOs**
    Instead of panicking over minor internal system "causes," define alerts based on whether the "survivability zone is objectively threatened (symptoms)." For the ISS, this means that rather than alerting on "momentary pressure drops," they set an SLO (Service Level Objective) on the "Time-to-Live (TTL)"—the time remaining before air pressure drops below the human-breathable limit—and dynamically predict and evaluate this value to trigger warnings.
2.  **Standardization of Runbooks and Seamless Evacuation Procedures**
    When an alert occurs, if the operator hesitates over "what to look at first" or "where to isolate," that monitoring system has already failed. On the ISS, depending on the warning level, the priority of hatches to close and evacuation routes to the rescue spacecraft are fully documented down to millisecond-level tasks in Runbooks (operations manuals). In terrestrial systems as well, procedures (playbooks) for taking diagnostic dumps or decoupling services should be automated or made immediately executable upon anomaly detection.

---


### Q1. How do you apply a "patch" to a leak in space?
**A1.** For physical micro-cracks, they apply high-performance films like Kapton tape or special epoxy-based sealants that can cure in a vacuum and withstand extreme temperature ranges (from below -100°C to over +100°C).
This is a perfect metaphor for applying a **"Hotfix"** in software operations. It is a technology that allows them to dynamically apply a patch and repair the infrastructure online while maintaining the system's (ISS) state, without having to shut down or depressurize the entire station.

### Q2. What are the spacecraft that act as safe houses?
**A2.** The "SpaceX Crew Dragon" or "Soyuz" spacecraft, which are always docked to the ISS, serve this purpose.
In system architecture, these represent **"Cold Standby / Passive Failover destinations in multi-region deployments."** The moment the main system (the ISS itself) is deemed unviable, they can immediately migrate the state (crew and critical data) to the safe house, ensuring a safe rollback (return) route back to Earth (the local development environment).

### Q3. Why can't repairs be fully automated using robots or AI?
**A3.** Because "fuzzy exploration and decision-making" under unexpected, compounding errors—such as feeling for minute airflow, routing flexible piping in tight spaces, or understanding context—still relies heavily on the cognitive abilities of human engineers (astronauts).
No matter how advanced automation (AI/autonomic operations) becomes, in the final stages of debugging and critical decision-making, manual intervention by skilled engineers remains the ultimate safety valve (fail-safe).

---

## 5. Conclusion: Bringing Back Lessons for "Resilient Systems" from the Extremes of Space

The successful identification and repair of the air leak on the ISS is more than just an achievement in space exploration. It is a grand proof-of-concept that validates the golden rules of operations and maintenance: "detect anomalies early at millisecond scale, evacuate safely, isolate the system, and reliably patch the root cause."

As we write code and build infrastructure on Earth, we cannot turn a blind eye to the "production memory leaks and resource depletions" that will inevitably occur.

Take another look at the dashboards (Datadog, Grafana, etc.) of the systems you manage. Are your metrics capable of catching the precursors of a "microscopic leak"? When an anomaly is detected, can your system survive locally using bulkhead patterns? Let us breathe the wisdom of space-grade system maintenance, built to survive the harshest environments, into our daily deployments.
