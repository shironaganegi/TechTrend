---
title: "オプティカルフローが紡ぐ数理の美――鳴門の渦潮から宇宙の超新星まで、森羅万象の「動き」を定量化する技術 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# The Mathematical Beauty of Optical Flow: Quantifying "Movement" in All Things, From Naruto's Whirlpools to Cosmic Supernovae

In recent years, with the rise of generative AI and Large Multimodal Models (LMMs), image and video analysis technologies have undergone rapid evolution. However, beneath the surface of this spectacular trend, a classical yet critically important image processing technique is once again playing a decisive role. This is **"Optical Flow."**

This article shines a spotlight on a highly suggestive approach that has generated significant buzz on Qiita: "Reading the Flow with Optical Flow: From Naruto's Whirlpools to Supernovae." This technology visualizes all "dynamic flows" regardless of scale—from micro-level viewpoints to terrestrial natural phenomena (Naruto's whirlpools) and even cosmic-scale hyper-phenomena (supernova explosions). In this post, we will delve deep into its essential potential and explain from a highly technical standpoint why modern engineers should learn this mathematical model today.

---

## 1. The True Value of Optical Flow in Modern Video Analysis

<div class="expert-opinion">
<strong>[Professional Tech Watch Perspective]</strong><br>
Even today, as AI and deep learning have evolved to make object detection models like YOLO mainstream, the value of optical flow has not diminished in the slightest. On the contrary, its mathematical models have become increasingly critical: serving as a guide to guarantee temporal consistency in video-generating AI, and playing a vital role in Physics-Informed Neural Networks (PINNs) that merge physical simulations with neural networks. The ability to capture continuous pixel-level movement is the "last bastion" of image analysis—something that coarse bounding-box detection by deep learning can never replace.
</div>

While object detection using deep learning is excellent at determining *what* is there, it struggles to quantify with pixel-level precision *how* objects with ambiguous boundaries—such as fluids or deformable bodies—are moving. Optical flow is the indispensable piece that bridges this gap.

---

## 2. Two Mathematical Approaches to Scientific Movement Analysis

Optical flow is a technique that describes where and how fast each pixel in an image has moved across consecutive time frames as a two-dimensional vector field. This technology is broadly classified into two approaches, strictly selected based on the specific application.

### ① Sparse Optical Flow
*   **Representative Method**: Lucas-Kanade Method
*   **Key Characteristics**: Tracks only salient points, such as "corners" (feature points), extracted from the image.
*   **Metaphor**: Like tracking only the trajectories of the brightest stars in a constellation across the night sky.
*   **Advantages**: Highly computationally efficient, making it ideal for resource-constrained edge devices, drone self-localization (Visual Odometry), and real-time eye-gaze tracking.

### ② Dense Optical Flow
*   **Representative Methods**: Farneback Method, HS (Horn-Schunck) Method
*   **Key Characteristics**: Calculates motion vectors for "every single pixel" across the entire image based on intensity changes.
*   **Metaphor**: An approach like mapping the entire swell of incoming waves or the subtle diffusion of smoke without leaving any gaps, down to the millimeter.
*   **Advantages**: Allows complete visualization of the dynamics of fluids, smoke, or objects with vague boundaries. This is precisely the method of choice for analyzing the "whirlpools" and "supernovae" featured in this theme.

```
[Lucas-Kanade Method (Sparse)]
 [・] ───→ [・]      (Tracks only specific feature points at high speed)

[Farneback Method (Dense)]
 [→][→][↗][↑]
 [→][↗][↑][↖]      (Recreates continuous flow of all pixels as a vector field)
 [↗][↑][↖][←]
```

### The Universality of Mathematics Across Scales
The real beauty of this project lies in the fact that **"by using a common mathematical model, we can quantify everything from terrestrial fluid phenomena to cosmic thermodynamic phenomena under the exact same logic."**

Fluid motion at a "geophysical scale" like Naruto's whirlpools, and energy diffusion at an "astrophysical scale" like a supernova explosion (the expansion of supernova remnants). Though seemingly completely different events, in terms of image representation, they both reduce to the same mathematical problem: "temporal and spatial changes in pixel intensity." Optical flow presents us with rigorous numerical data, revealing the origin of minute vortices invisible to the naked eye and the propagation vectors of shockwaves.

---

## 3. Positioning Motion Detection Technologies: A Comparison

There are multiple approaches to capturing the "motion" of objects in image analysis. Understanding the technical characteristics of each and selecting the appropriate architecture is critical to the success of a project.

| Technique / Method | Target of Detection | Advantages | Disadvantages / Challenges |
| :--- | :--- | :--- | :--- |
| **Frame Differencing** | Regions of moving objects | Extremely simple implementation, fast | Cannot determine the "direction" or "speed" of motion |
| **Object Tracking (YOLO, etc.)** | Defined objects (people, cars, etc.) | Robust to occlusion | Cannot track "fluids" like smoke or whirlpools |
| **Optical Flow** | Movement of all pixels | Can quantify fluids and amorphous movements | Sensitive to illumination changes and noise, high computational cost |

These are not mutually exclusive but rather complementary. For example, a hybrid system that applies dense optical flow inside a rough bounding box identified by YOLO to analyze the "detailed behavior" (gestures or suspicious movements) of an object is frequently used in production environments.

---

## 4. Three Technical Obstacles Faced in Production and How to Overcome Them

When implementing optical flow using Python or C++ (OpenCV), there are mathematical and physical pitfalls that engineers inevitably encounter. Knowing how to avoid these traps is the key to professional system development.

### Obstacle 1: The Aperture Problem
This is a phenomenon where, if only a portion of an edge (boundary) is observed, the motion is falsely perceived as moving in a direction different from its actual trajectory.
*   **Solution**: Introduce a multi-scale image pyramid. By creating a pyramid of progressively downscaled images, you can compute and propagate flow step-by-step from coarse resolutions (global motion) to fine resolutions (local motion). This drastically reduces false detections caused by large displacements or edge ambiguity.

### Obstacle 2: Violation of the Brightness Constancy Assumption
Optical flow relies on the assumption that "the brightness of a target pixel does not change before and after motion" (brightness constancy constraint). However, the real world is filled with light reflections, moving shadows, and flicker.
*   **Solution**: Rigorous preprocessing. Beyond converting images to grayscale, it is highly effective to apply **CLAHE (Contrast Limited Adaptive Histogram Equalization)**, **Gaussian filtering** to eliminate high-frequency noise, or to compute flow in the gradient domain using texture gradients (such as Sobel filters) which are less susceptible to illumination changes.

### Obstacle 3: Computational Cost in Real-Time Processing
Dense optical flow, which computes vectors for every single pixel, requires a massive amount of computation, easily leading to CPU bottlenecks during the real-time processing of high-resolution video.
*   **Solution**: Introduce GPU (CUDA)-accelerated functions like `cv2.cuda.calcOpticalFlowFarneback`. Alternatively, as a modern approach, you can consider swapping the legacy methods for deep-learning-based, ultra-lightweight optical flow inference models (such as lightweight versions of FastFlow or RAFT) to achieve both high accuracy and real-time performance.

---

## 5. Practical FAQ (Frequently Asked Questions & Answers)

**Q1: When applying OpenCV's Farneback method, what are some tips for parameter tuning?**
**A:** The parameters with the greatest impact are `pyr_scale` (the scale image pyramid reduction factor, usually 0.5), `levels` (number of pyramid layers), and `winsize` (averaging window size). If motion is fast and large, set a larger `winsize` (e.g., 15 to 21). If you want to suppress noise and capture subtle movements, set it smaller. A common best practice is to build a quick GUI slider to dynamically adjust these parameters, allowing you to tune them interactively for your target video.

**Q2: Where is the dividing line between traditional mathematical models (like Farneback) and modern deep learning models (like RAFT)?**
**A:** 
*   **When mathematical models are better suited**: Strict reproduction of physical phenomena, implementation on edge devices (like Raspberry Pi), and academic or industrial applications where computational "explainability" is required.
*   **When AI models (like RAFT) are better suited**: Scenes with complex occlusions, tracking areas with extremely poor texture, or environments where abundant GPU resources are available.

**Q3: Can 3D depth movement (approach/recession) be inferred from 2D optical flow?**
**A:** Mathematically and theoretically, yes. When an object approaches the camera, its vectors radiate outward (divergence). Conversely, as it moves away, the vectors converge toward the center. By calculating the degree of divergence or convergence of these vectors, you can back-calculate 3D distance changes from a 2D plane to estimate metrics like Time-to-Collision (TTC).

---

## 6. Conclusion: Becoming an Engineer Who Masters Dynamics

Optical flow is by no means a legacy technology of the past. It remains a foundational technology underpinning all modern "dynamic vision" applications—from self-localization in autonomous driving, robot vision, and drone collision avoidance to ensuring temporal consistency in state-of-the-art AI video generation.

We are shifting from the era of AI that understands static images to an era of AI that predicts and controls dynamic "flows."

To start, try experiencing this "mathematical beauty" with just a few lines of OpenCV code in your own local development environment. The moment those countless vectors drawn on the screen faithfully mirror the physical laws of the real world, your perspective as an image analysis engineer will undoubtedly be elevated to the next level.

We highly encourage you to experience the full potential of this universal tool—from fluid dynamics to cosmic observations—alongside the excellent source code available in the original Qiita article.
