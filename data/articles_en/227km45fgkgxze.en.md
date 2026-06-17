---
title: "その歩数は「誰」のものか？プライバシー原理主義者のための究極歩数計『Steps』に震えろ (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# Whose Steps Are They? The Ultimate Pedometer for Privacy Fundamentalists: Behold "Steps"

You spend all day interacting with displays, brewing coffee while waiting for builds to finish. Then, you happen to check your iPhone’s Health app and stand there aghast. Your step count is a mere "three digits."

For us engineers, a sedentary lifestyle is practically an occupational hazard. However, the moment you install a pedometer app for your health, an eerie noise crawls into the back of your mind: "My activity logs are being sucked up into some server somewhere." The balancing act between convenience and privacy. "Steps: Workout & Pedometer" is the app that puts an end to this dilemma.

The philosophy of this app can be described in one word: "Uncompromising."

## 🚀 The Aesthetic of "Tracking Steps, Not You"

In an era where many fitness apps hungrily eye user location and demographic data as "assets," Steps champions a singular concept: **"Track steps, not you."**

It is no exaggeration to call this a love letter to engineers who want to defend the sanctuary of their privacy.

### 💡 Three Points That Will Electrify You
- **Trust in "Local Execution"**: It performs absolutely no data collection that identifies the user. Your data exists only within your device and is never sold to anyone. This peace of mind is irreplaceable.
- **A Minimalist "Architectural UI"**: Necessary information is placed in the right place, in the right form. It feels as comfortable as reading refined code. The visibility of the dashboard is bordering on a work of art.
- **Stoicism Regarding Resource Consumption**: It doesn't commit the barbaric act of constantly draining GPS. It utilizes device sensors efficiently to preserve battery life. As an engineer, you can't help but feel a sense of sympathy for this stance on resource optimization.

## 🛠️ The Ideal Integration with Apple HealthKit

Usage is incredibly simple. Just install it and grant the necessary permissions. With that alone, Steps begins to record your pulse—quietly and accurately—in the background.

Wondering how it hits the Apple HealthKit APIs under the hood or how securely it handles data... contemplating the elegance of its implementation is perhaps one of the unique ways to enjoy this app.

```swift
// Conceptual code: Imagining the design philosophy of Steps
// There are no impure functions to transmit data to external servers.
let stepCountType = HKQuantityType.quantityType(forIdentifier: .stepCount)!
// Everything is contained within your local storage.
```

## 🎯 Moments When Steps is by Your Side

- **On an afternoon stuck in a debugging rut**: The cold, hard number of "only 500 steps today" gives you the push you need to go breathe some outside air.
- **Amidst the hustle and bustle of a tech conference**: You can look back at the record of walking across a massive venue and smirk to yourself, knowing no one else has that data.
- **For the "On-Prem over Cloud" enthusiast**: You can uphold the pride of refusing to hand over sovereignty of your life logs to a tech giant.

## ✅ The Only "Drawback" is the Solitude

This app has no social features to compete with friends, nor any mechanisms to satisfy a flashy desire for validation.

- **Pros**: No registration required, no ads, zero concern about data sales. Performance is incredibly snappy.
- **Cons**: For those who "can't work hard unless someone is watching," this level of stoicism might be a bit harsh.

However, for those of us who operate autonomously, this should be nothing more than "the removal of noise."


## 💾 Summary: The Body is Hardware, Data is a Sanctuary.

Our bodies are the ultimate hardware for producing code. If you neglect maintenance, performance will visibly drop. However, selling off your "soul"—your privacy—for the sake of that maintenance isn't a smart move for a professional.

"Steps" solves the two requirements of health and privacy—which should naturally coexist—in the coolest way possible.

Just "leave it installed." Tomorrow, the 1,000 steps you take before sitting down at your display should make your thoughts even clearer.

Now, why don't you get up and go record some logs? 🔥
