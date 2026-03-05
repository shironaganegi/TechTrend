---
title: "JupyterLabの「環境汚染」に終止符を。仮想環境をカーネルに追加して、開発の解像度を爆上げする最短ルート (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# Ending "Environment Pollution" in JupyterLab: The Fastest Way to Boost Development Clarity by Adding Virtual Environments as Kernels

You added a single library, and suddenly the code that worked perfectly yesterday starts throwing a tantrum. Or perhaps you're staring at the red "ModuleNotFoundError" text in Jupyter, looking up at the ceiling and sighing, "But I *just* installed it..."

Does this sound familiar?
If you are stuffing every library into JupyterLab’s base environment, you are essentially over-simmering a "secret sauce" until the pot becomes an unrecognizable mess.

The key to unlocking the true power of JupyterLab lies in a simple habit: **"Registering virtual environments as independent kernels."** By the time you finish reading this article, your development environment will have the clarity of a fog that has finally lifted.

### 💡 Why "Environment Isolation" is a Critical Issue Right Now

The modern world of AI and Data Science is, in a sense, a "Warring States period" for libraries. Updates happen at a staggering pace, and "dependency conflicts"—where the latest library for one project breaks the lifeline of another—are a daily occurrence.

- **Environment Sanctification**: Building an "isolated clean room" (virtual environment) for each project is a minimum requirement for professional work.
- **Trust via Reproducibility**: Graduate from the "it works on my machine" excuse and ensure your code runs in anyone's environment.
- **The Aesthetic of Switching**: Switching kernels with a single click in the GUI. That instant transition creates a rhythm for the engineer.

### 🔧 The 3-Step Ritual: Taming Virtual Environments as "Kernels"

The procedure is surprisingly simple. However, these few lines of command will save you hours of frustration. We'll use the standard `venv` as an example to walk through the steps.

#### 1. Constructing the Sanctuary (Virtual Environment)
It begins by creating a dedicated sandbox for your project.

```bash
# Summon the virtual environment "my_env"
python -m venv my_env

# Enter the sanctuary (Mac/Linux)
source my_env/bin/activate
# For Windows
# .\my_env\Scripts\activate
```

#### 2. Inviting the Interpreter (ipykernel)
This is the most important "missing link." Simply creating a virtual environment isn't enough; JupyterLab doesn't know it exists yet. You need to install an "interpreter" inside the virtual environment to communicate with Jupyter.

```bash
pip install ipykernel
```

#### 3. "Resident Registration" in JupyterLab
Finally, register this environment in JupyterLab’s management directory. You are essentially telling it, "Show up in the menu with this name."

```bash
python -m ipykernel install --user --name=my_env --display-name="Python (My_Env)"
```

That’s it. Try clicking the kernel name in the top-right corner of JupyterLab. You should see your proudly named "Python (My_Env)" listed there. ✨

### 🚀 Use Cases: When This Technique Really Shines

This environment management proves its worth in "battlefield" situations like these:

- **LLM and PyTorch Experiments**: When you want to try libraries with strict version requirements without breaking other projects.
- **Team Deliverables**: When you want to build the exact library configuration for a deliverable without mixing it with your cluttered local environment.
- **Parallel Projects**: When you need to smartly handle chaotic situations like "Project A is Python 3.9, but Project B is 3.11."

### ✅ Benefits and a Bit of Housekeeping

- **Benefits**: Your base environment stays clean. You minimize the risk of your PC becoming unstable and gain peace of mind.
- **Housekeeping**: As virtual environments proliferate, they will eventually start eating up storage. When an environment has served its purpose, let it go with gratitude using `jupyter kernelspec uninstall <env_name>`.

<!-- AFFILIATE_START -->

### 👇 Recommended Services for Engineers 👇
[**🌐 Get your unique domain at "Onamae.com". TechTrend Watch uses it too!**](https://www.onamae.com/)

<!-- AFFILIATE_END -->

### 🏁 Conclusion: Stop Wasting Energy on the Base Environment

If you think of JupyterLab as just a "notebook where you can write code," you're missing out. It is an "external brain" for engineers, capable of parallel processing by instantly switching between multiple brains (kernels).

Trying to do everything in the base environment is like trying to race on a circuit while dragging the handbrake.
Hit the terminal right now and build your own "ultimate specialized environment."

That single step will push your development efficiency into another dimension. Welcome to a smarter development experience. 💻✨
