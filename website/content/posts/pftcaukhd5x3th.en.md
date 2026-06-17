+++
title = "3000行の「神main.py」に終止符を。Pythonで実践する「依存性の注入（DI）」設計パターン (English)"
date = "2026-06-10T23:42:09.754686"
tags = ["AI", "Tools", "LLM", "RAG", "AIエージェント", "Python"]
draft = false
description = "Introduction to 3000行の「神main.py」に終止符を。Pythonで実践する「依存性の注入（DI）」設計パターン (English)"
canonicalUrl = "https://techtrend-watch.com/posts/pftcaukhd5x3th/"
+++


# Ending the Era of the 3000-Line "God main.py": Implementing the "Dependency Injection (DI)" Design Pattern in Python

Python boasts overwhelming convenience when it comes to rapid prototyping and quick implementations of AI agents. However, in the rush for speed, have you ever found yourself packing all processing into `main.py` and unwittingly giving birth to a 3000+ line "God File"?

Bloated spaghetti code is the single biggest factor slowing down development speed. The ultimate remedy to fundamentally solve this issue and guide your project toward a clean, robust design is "Dependency Injection (DI)." This article explains practical DI techniques in Python and the architectural paradigm shift they bring.

## The Essential Value of Dependency Injection (DI)

<div class="expert-opinion">
For those who think, "Python is dynamically typed, so DI is over-engineering," this is the article you need to read. Sure, we might not need to be as rigid as static languages like Java or C#. But when you consider how much easier it makes writing mock tests, or the future cost of swapping databases and APIs, the value of incorporating simple DI into Python skyrockets. Especially in today's landscape where AI APIs evolve at breakneck speed, the flexibility to switch LLM providers (e.g., from OpenAI to Anthropic) without rewriting your core code is a make-or-break issue directly tied to development efficiency. Knowing this pattern will make your day-to-day operations several times lighter.
</div>

## Why is the "God main.py" Born? Three Tragedies Caused by Tight Coupling

In the early stages of development, writing API calls, database connections, and business logic seamlessly in a single file feels convenient. However, as the product grows, this "tight coupling" comes back to haunt developers as serious technical debt, manifesting in three main ways:

1. **Loss of Testability**:
   Because external API integrations and database connection logic are hardcoded inside, running a unit test triggers actual network requests or database operations every single time.
2. **The Change Domino Effect**:
   Database schema changes or external library updates ripple through to business logic that should ideally be completely unrelated, causing unexpected bugs.
3. **Reaching the Limits of Cognitive Load**:
   Debugging while scrolling through a codebase of several thousand lines severely drains a developer's cognitive resources, sharply degrading productivity.

All of these issues stem from components being "too tightly bound together" (tight coupling).

## What is Dependency Injection (DI)? Understanding Loose Coupling Through Metaphor

The core of DI (Dependency Injection) is a design pattern where a class or function does not create (instantiate) the objects it depends on by itself, but rather **receives them from the outside (injects them)**.

To use an everyday metaphor, it is like **the difference between "appliances hardwired directly into the wall" and "plug-in appliances."**
A vacuum cleaner soldered directly to the wall is extremely difficult to replace if it breaks, let alone upgrade to a newer model with stronger suction. On the other hand, if you route it through an outlet (a standardized interface), you can freely plug in a vacuum cleaner, a TV, or an air purifier. DI is what brings this "pluggable flexibility" to the world of code.

### Before: Chaotic Code (Tight Coupling)

```python
class UserService:
    def __init__(self):
        # Directly instantiating database connection inside (tight coupling)
        self.db = MySQLDatabase()
    
    def get_user(self, user_id):
        return self.db.find(user_id)
```

In this design, `UserService` completely depends on `MySQLDatabase`. If you want to change the database to PostgreSQL or swap it with a mock for testing, you are forced to rewrite this class itself.

### After: Clean Code (Loose Coupling)

```python
class UserService:
    # Depend on abstraction and inject from the outside
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_user(self, user_id):
        return self.db.find(user_id)
```

`UserService` does not care what kind of `db_connection` is passed to it. It only expects it to be "an object that has a `find` method." Because of this, you can inject a `MockDatabase` during testing and a `PostgreSQLDatabase` in production, controlling the entire behavior simply by changing the caller (entry point).

This "always swappable" state is the ultimate beauty of loose coupling.

## Criteria for Choosing Between "Manual DI (Pure DI)" and "DI Container Libraries"

When adopting DI in Python, you don't always need a heavy, feature-rich framework. It is highly rational to choose between the following two approaches based on the scale and complexity of your project.

### 1. Manual DI (Pure DI)
This approach manually instantiates dependent objects at the program's entry point (e.g., `main.py`) and passes them via constructors without using any external libraries. For small to medium-scale projects, this approach is more than sufficient to achieve your goals. Because there is no black box, code readability remains exceptionally high.

### 2. Using DI Container Libraries
This involves using specialized libraries like `dependency-injector` or `pinject`. When dependency hierarchies become deep and complex (e.g., Class A depends on B, B depends on C, C depends on D, etc.), these libraries can automatically analyze and generate (autowire) them.

| Comparison | Manual DI (Pure DI) | DI Container Library |
| :--- | :--- | :--- |
| **Learning Curve** | Extremely low. Can be adopted with just an understanding of the basic design. | Requires learning library-specific syntax and lifecycle management. |
| **Code Clarity** | Very high. The flow of code can be intuitively followed. | Harder to trace as dependencies are resolved implicitly, creating a black box. |
| **Suitable Projects** | Small-to-medium development, scripts, microservices | Large enterprise, services with complex domain models |

## Implementation Pitfalls: Avoiding Antipatterns

While DI is a powerful design pattern, it is not a silver bullet. You must keep the following points in mind when implementing it:

- **Avoiding Over-engineering**:
  You do not need to apply DI to one-off throwaway scripts or simple utility tools under 100 lines. The practical criteria for judgment should be: "Will I need to write unit tests for this in the future?" or "Is there a chance the external service implementation will change?"
- **Guarding Against Over-mocking**:
  If you take DI to the extreme and abstract or mock every single component, you might end up in a situation where "all unit tests pass, but nothing works when integrated in production." It is crucial to strike a balance between the "behaviors" guaranteed by unit tests and integration tests that use actual systems.

## FAQ

**Q1: Python doesn't have an interface type. How do you achieve polymorphism?**  
A: By using `typing.Protocol` (structural subtyping) or `abc` (Abstract Base Classes), you can leverage duck typing (interface definitions) while taking full advantage of static analysis tools (Mypy) and modern IDE autocomplete. This gives you safety on par with statically typed languages.

**Q2: Does introducing DI decrease execution speed (performance)?**  
A: While there is an extremely minor overhead in resolving object references and instantiation, it is negligible (on the nanosecond to microsecond scale) compared to web application I/O processing, API calls, or database access. The benefits brought by architectural robustness are far greater.

**Q3: Migrating an existing 3000-line file all at once seems too daunting...**  
A: You should avoid full rewrites all at once, as they easily introduce new bugs. The recommended approach is a "small-step migration": identify a single boundary with the highest frequency of business logic changes and dependency on external APIs, and convert just that part into a class with DI.

## Conclusion: Code Flexibility Dictates Business Agility

Maintaining a 3000-line "God File" is akin to sitting on a "technical debt time bomb" that slowly eats away at your team's development productivity.

Adopting DI is not just about keeping code clean. It is a strategic investment to ensure your systems remain "safely, quickly, and cost-effectively changeable" in today's fast-paced tech industry.

Harness Python's dynamic flexibility while bringing order through DI. Starting today, draw beautiful boundaries in your `main.py` and transform it into a sustainable codebase.


---

> This article is also available in [Japanese](https://techtrend-watch.com/posts/pftcaukhd5x3th/).
