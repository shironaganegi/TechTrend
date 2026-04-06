+++
title = "30_OOF予測値によるIsotonic Regression：予測の「歪み」を正し、モデルに実戦的な信頼性を宿す手法 (English)"
date = "2026-04-06T22:43:33.083494"
tags = ["AI", "Tools"]
draft = false
description = "Introduction to 30_OOF予測値によるIsotonic Regression：予測の「歪み」を正し、モデルに実戦的な信頼性を宿す手法 (English)"
canonicalUrl = "https://techtrend-watch.com/posts/55f0vd8x7bufwp/"
+++


# 30_Isotonic Regression using OOF Predictions: Correcting Prediction "Distortion" and Infusing Models with Practical Reliability

In machine learning projects—particularly in Kaggle-style competitions or domains like horse racing and finance where "probabilistic accuracy" directly translates to profit or risk—there is a wall that every practitioner inevitably hits after chasing evaluation metrics like RMSE or LogLoss. That wall is **"Model Calibration."**

If a model predicts an event has an 80% probability of occurring, but it actually only happens 60% of the time, this discrepancy becomes a fatal flaw in business decision-making. No matter how impressive the score, if the "scale" of the predicted values diverges from reality, the model cannot be considered battle-ready for real-world applications.

This article provides a detailed explanation of a powerful technique to rectify this "distortion" in predicted values and evolve your model into an "honest prophet": applying **Isotonic Regression** to **OOF (Out-Of-Fold) predictions**.

<div class="expert-opinion">
Tech Watch Perspective: While many engineers pour their heart and soul into "building the model," it is actually the "calibration of the output" that often determines true success in production. Isotonic Regression is particularly potent as a final layer in stacking because it can correct probability distortions post-hoc, regardless of the model's internal algorithm. However, since it is prone to overfitting with small datasets, using OOF (cross-validated predictions) has become the gold standard approach.
</div>

## 1. The Essence of Isotonic Regression

If one were to describe Isotonic Regression in a single sentence, it is **non-parametric regression analysis constrained by "monotonic increase."**

It fits a stepwise function to minimize the mean squared error with actual observations while maintaining the intuitive ordinal relationship (monotonicity) that "if the original predicted value is higher, the corrected probability should also be higher." This process is akin to taking a "distorted mirror" and hammering it straight—flexibly following the data's trends without disrupting the order.

- **Non-parametric Flexibility**: Unlike methods that assume a specific shape (like the sigmoid function in Platt Scaling), it can follow complex distortions without parametric constraints.
- **Guaranteed Monotonicity**: It operates under the constraint that if $x_i \le x_j$, then $\hat{y}_i \le \hat{y}_j$ must hold.
- **Practical Benefit**: It allows you to transform the "scores" output by classification models into mathematically rigorous "probabilities."

## 2. Why it Must Be "OOF Predictions"

The most critical pitfall to avoid when applying this method is **Data Leakage**.

If you train Isotonic Regression using the predictions made on the training data itself (In-sample), the model is correcting values for "data it already knows the answer to." This results in an extremely optimistic correction where the model essentially validates its own overfitting, rendering it useless for unseen data.

This is where **OOF (Out-Of-Fold) predictions** become essential.
During the Cross-Validation process, you aggregate predictions for "held-out data" that the model never saw during its specific training fold. By applying Isotonic Regression to these OOF values, you can objectively capture and appropriately correct the model's inherent "biases"—such as overconfidence or timidness—toward unknown data.

## 3. Platt Scaling vs. Isotonic Regression: Selection Guidelines

While "Platt Scaling" (applying logistic regression) is another common method for probability calibration, the characteristics of the two are contrasting.

| Feature | Platt Scaling | Isotonic Regression |
| :--- | :--- | :--- |
| **Mathematical Model** | Sigmoid curve (fixed shape) | Stepwise function (data-driven) |
| **Prerequisites** | Error distribution is near-sigmoid | None (only monotonicity) |
| **Data Volume Tolerance** | Stable even with small data | Requires ample data (1,000+ records) |
| **Calibration Flexibility** | Low (smooth correction) | Very high (strong against non-linear distortion) |

In conclusion, **Isotonic Regression exerts overwhelming power in cases where "model distortion is severe and training data is sufficient."** Conversely, if data is extremely scarce, Platt Scaling is more likely to maintain generalization performance.

## 4. Technical Hurdles and Workarounds in Implementation

To pursue high precision, you must be aware of the following "pitfalls" beyond simply calling a library function.

### ① Dealing with Tied Values
When there are many data points with identical predicted values but different ground truth labels, the stepwise function of Isotonic Regression can become unstable. In such cases, adding infinitesimal random noise (jitter) to the predicted values or inserting Quantile Binning as a preprocessing step can improve the stability of the calibration.

### ② Outlier Sensitivity at Boundaries
Due to its nature as a stepwise function, it tends to be pulled strongly by noise at the edges of the data (predicted values near 0 or 1). To prevent this, you should use stable OOF predictions averaged across multiple seeds or folds rather than the OOF from a single model.

## 5. Field Insights: FAQ

**Q: Can this be used for score transformation in regression problems?**
A: Theoretically, yes. For example, if a model's output has a non-linear distortion relative to the target variable, as long as the ranking order is correct, Isotonic Regression can optimize the output to the scale of the target variable.

**Q: How is the compatibility with LightGBM’s `is_unbalance=True`?**
A: Excellent. Models treated for imbalanced data often tend to output "probabilities" that are exaggerated. Isotonic Regression masterfully pulls that distorted distribution back toward the actual probability of occurrence.

## Conclusion: Elevating the Model to a "Trusted Entity"

Isotonic Regression using 30_OOF predictions is not merely a post-processing technique. It is the final stage of data science that transforms cold, inorganic numbers spat out by an algorithm into "reliable indicators" that humans and systems can trust.

When you find yourself stuck with feature engineering to improve accuracy, return to this perspective of "calibration." A model that combines mathematical consistency with practical robustness is what delivers truly valuable results.


---

> This article is also available in [Japanese](https://techtrend-watch.com/posts/55f0vd8x7bufwp/).
