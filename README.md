# 🎮 Personal Chatbot Speedrun Any% (No Glitches)

> *"It's not about the destination, it's about the friends we made along the way... and the bugs we introduced."*

## 🧙‍♂️ The Party (Who's Grinding This Quest)

| Hero Name | Class | Discord Handle | Sync Days | Raid Time |
|Mateusz|Technowizard|vetekinna_60775|24.11|IDK : D |
| | | | | |
| | | | | |

> ⚠️ **Fill this out first or you're literally cooked**

---

## 📜 The Lore (What Even Is This)

You've been summoned to build a **Personal Chatbot** — the most basic of bots, yet infinitely extensible. Think of it as the tutorial boss before the real game begins.

**The Stack (Your Loadout):**
- 🧠 **LangChain** — The brain (makes bot go brr)
- 📝 **Pydantic** — The bouncer (no sus data allowed)
- 🎨 **Streamlit** — The face (pretty UI, no cap)
- 🚀 **FastAPI** — The optional drip (API layer if you're feeling spicy)
- 🧪 **Pytest** — The reality check (tests or it didn't happen)

**Your Mission:**
1. Research everything (no speedrunning this part fr fr)
2. Build components in isolation (trust the process bestie)
3. Integrate them (this is where it gets real)
4. Document your Ls and Ws (self-awareness arc)

---

## ⚔️ The Rules of Engagement

### 🚫 Forbidden Techniques (Instant Game Over)
- Writing code before researching → *skill issue*
- Skipping isolation testing → *that's not very cash money*
- Merging without PR approval → *caught in 4K*
- Raw dicts crossing boundaries → *Pydantic didn't die for this*

### ✅ Based Moves (XP Multipliers)
- Asking clarifying questions → *big brain energy, DM papa*
- Documenting in GitHub issues → *audit trail supremacy*
- Isolated pytest tests → *chef's kiss*
- Clean git history → *immaculate vibes*

---

## 🏕️ Setting Up Camp (Environment Setup)

### Step 1: Summon UV (Package Manager Diff)

```bash
**If you don't have uv yet, install it (it's bussin)**
`curl -LsSf https://astral.sh/uv/install.sh | sh`

Or if you're on Windows (no shade)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Create Your Lair

```bash
# Clone the repo (you know the drill)
git clone <your-assigned-repo-url>
cd <repo-name>

# Spawn a virtual environment
uv venv

# Activate it
source .venv/bin/activate  # Unix/macOS
# OR
.venv\Scripts\activate     # Windows
```

### Step 3: Add Your Dependencies

```bash
# Add packages as you need them (research first tho)
uv add <package-name>

# Need a specific version? Say less
uv add <package-name>==<version>

# Dev dependencies (testing stuff)
uv add --dev <package-name>
```

> 🚨 **IMPORTANT:** You decide which packages and versions to use. That's literally the quest. Check the docs, validate compatibility, ask questions if confused. No hand-holding here bestie.

### Step 4: Lock It In

```bash
# This creates/updates uv.lock (commit this file)
uv lock

# Sync your environment from lock file
uv sync
```

---

## 🗺️ The Quest Log (Milestones)

| Phase | Milestone | Vibe Check |
|-------|-----------|------------|
| 1️⃣ | Research & Technology Validation | *"I actually read the docs"* |
| 2️⃣ | Isolated Component Proof | *"It works on my machine (in isolation)"* |
| 3️⃣ | Integration & Demo | *"Witness me"* |
| 4️⃣ | Reflection & Handoff | *"Character development arc complete"* |

### 🌿 Branch Strategy (Don't Be Sus)

```
main (protected - no direct pushes, srs)
├── milestone-1/research
├── milestone-2/isolated-components
├── milestone-3/integration
└── milestone-4/reflection
```

**Workflow:**
1. Create branch from \`main\` for your milestone
2. Work on issues, commit often (atomic commits = based)
3. Open PR when milestone complete
4. Get approved by reviewer (that's @ArturNiklewicz)
5. Merge and level up 🎉

---

## 📚 The Sacred Texts (Documentation)

### Core Technologies
| Tech | Docs | Why You Need This |
|------|------|-------------------|
| 🐍 Python | [docs.python.org](https://docs.python.org/3/) | ...seriously? |
| 📦 uv | [docs.astral.sh/uv](https://docs.astral.sh/uv/) | Package manager that doesn't make you mass |
| 🧠 LangChain | [python.langchain.com/docs](https://python.langchain.com/docs/introduction/) | The chatbot brain docs |
| 📝 Pydantic | [docs.pydantic.dev](https://docs.pydantic.dev/latest/) | Data validation bible (USE V2) |
| 🧪 Pytest | [docs.pytest.org](https://docs.pytest.org/en/stable/) | Testing framework goat |
| 🚀 FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) | API framework that's actually good |
| 🎨 Streamlit | [docs.streamlit.io](https://docs.streamlit.io/) | UI framework for the lazy (affectionate) |

### Bonus Reading (Side Quests)
| Resource | Link | Vibe |
|----------|------|------|
| Git Branching | [learngitbranching.js.org](https://learngitbranching.js.org/) | Interactive git tutorial |
| Conventional Commits | [conventionalcommits.org](https://www.conventionalcommits.org/) | Commit message etiquette |
| Python Type Hints | [mypy.readthedocs.io](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) | Types are your friend |

---

## 🎯 Evaluation Criteria (How You Get Judged)

| Criteria | Weight | What We're Looking For |
|----------|--------|------------------------|
| 🤔 Asking Clarifying Questions | HIGH | You ask before assuming |
| 📖 Research Rigor | HIGH | Official docs > Stack Overflow copypasta |
| 🧩 Code Isolation | HIGH | Components work alone before together |
| 🌿 Git Hygiene | MEDIUM | Clean history, good PR descriptions |
| 📝 Documentation | MEDIUM | Your issues tell the story |

---

## 💀 Common L's (Don't Be This Person)

- *"I'll just figure it out as I go"* → Research milestone exists for a reason
- *"Tests are optional right?"* → They are not. Pytest or perish.
- *"I'll document later"* → You won't. Document in issues AS YOU GO.
- *"Let me just merge real quick"* → PR gate exists. Respect it.

---

## 🏆 GG WP (Success Criteria)

By the end, you should have:
- [ ] A working chatbot (even if basic)
- [ ] Clean, isolated components
- [ ] Documented decision trail in GitHub issues
- [ ] Honest self-assessment
- [ ] Zero regrets (okay maybe some regrets)

---

> *"The real chatbot was the documentation we wrote along the way."*
>
> — Ancient Developer Proverb, probably

**Now go touch grass (after you finish the milestone). GLHF! 🚀**
