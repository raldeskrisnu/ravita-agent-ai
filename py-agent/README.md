# Ravita Agent AI – Python Edition

> **Autonomous coding agent** powered by [LangChain](https://python.langchain.com/) + [LangGraph](https://langchain-ai.github.io/langgraph/) + [Anthropic Claude](https://www.anthropic.com/), with an optional **BMad Method multi-agent** team.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
  - [Single-Agent Mode](#single-agent-mode)
  - [BMad Multi-Agent Mode](#bmad-multi-agent-mode)
- [BMad Method](#bmad-method)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the Agent](#running-the-agent)
  - [Single-Agent Mode](#running-single-agent-mode)
  - [BMad Multi-Agent Mode](#running-bmad-multi-agent-mode)
- [Available Tools](#available-tools)
- [Interactive Commands](#interactive-commands)
- [Extending the Agent](#extending-the-agent)

---

## Overview

Ravita is an autonomous senior software engineer powered by Anthropic Claude. It can:

- **Read and write files** in your workspace
- **Explore codebases** with tree maps and directory listings
- **Run shell commands** (builds, tests, linters, scripts)
- **Analyse code** and answer questions about it
- **Use Git** (status, diff, log)
- **Coordinate specialised sub-agents** via the BMad Method (optional)

---

## Architecture

### Single-Agent Mode

```
User ──▶ Ravita (LangChain ReAct Agent)
               │
               ├── read_file
               ├── write_file
               ├── list_files
               ├── repo_map
               ├── git_status / git_diff / git_log
               ├── analyze_code
               └── execute_command
```

Ravita uses the [ReAct](https://react-lm.github.io/) loop: **Reason → Act → Observe → Repeat** until a final answer is produced.

### BMad Multi-Agent Mode

```
User ──▶ BMad Orchestrator (LangGraph Supervisor)
               │
               ├── architect        – system design, ADRs
               ├── developer        – Ravita (full toolset)
               ├── qa               – testing, code review
               └── product_manager  – backlog, prioritisation
```

The orchestrator uses a **LangGraph StateGraph** with a supervisor node. The supervisor LLM reads the conversation and routes each turn to the most appropriate specialist agent, looping until the task is complete.

---

## BMad Method

The [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) (**B**usiness **M**odel **A**gile **D**evelopment) is an agile AI-driven development framework that uses specialised AI agents for each role in a software team:

| Agent | Name | Responsibilities |
|---|---|---|
| `architect` | Sage | System design, ADRs, technology decisions |
| `developer` | Ravita | Code implementation, bug fixes, refactoring |
| `qa` | Quinn | Testing strategy, test code, code review |
| `product_manager` | Morgan | Backlog, prioritisation, roadmap |

The **Orchestrator** supervises all agents and routes requests following the BMad cycle:  
**Analyse → Design → Implement → Test → Retrospect**

---

## Project Structure

```
py-agent/
├── main.py                          # CLI entry point
├── pyproject.toml                   # Project metadata and dependencies (uv)
├── uv.lock                          # Locked dependency tree (uv)
├── .env.example                     # Environment variable template
├── README.md                        # This file
│
├── agents/
│   ├── base_agent.py                # Base LangChain ReAct agent
│   ├── ravita_agent.py              # Single-agent Ravita (with history)
│   └── bmad/
│       ├── architect.py             # BMad Architect agent
│       ├── developer.py             # BMad Developer agent (Ravita)
│       ├── qa.py                    # BMad QA agent
│       ├── product_manager.py       # BMad Product Manager agent
│       └── orchestrator.py          # LangGraph supervisor orchestrator
│
├── tools/
│   ├── file_tools.py                # read_file, write_file, list_files, repo_map
│   ├── git_tools.py                 # git_status, git_diff, git_log
│   ├── code_tools.py                # analyze_code
│   └── command_tools.py             # execute_command
│
├── loaders/
│   ├── personality_loader.py        # Loads personality/personality.md
│   └── skills_loader.py             # Loads skills/*.md
│
├── personality/
│   └── personality.md               # Ravita's identity and core traits
│
└── skills/
    ├── architecture_skills.md       # Architecture knowledge
    ├── core_skills.md               # General backend engineering skills
    ├── debugging_skills.md          # Debugging methodology
    └── testing_skills.md            # Testing philosophy and practices
```

---

## Prerequisites

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/)** – fast Python package and project manager (`pip install uv` or see [installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- An **Anthropic API key** (get one at [console.anthropic.com](https://console.anthropic.com/account/keys))
- **git** (for git tools; must be available in your `PATH`)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/raldeskrisnu/ravita-agent-ai.git
cd ravita-agent-ai/py-agent
```

### 2. Install dependencies

`uv` handles the virtual environment and all dependencies for you:

```bash
uv sync
```

This creates a `.venv` directory and installs all pinned dependencies from `uv.lock`.

### 3. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values (see [Configuration](#configuration) below).

### 4. Create a workspace directory

The agent works inside a **workspace** directory — point it at an existing codebase or let it create a new one:

```bash
mkdir -p workspace
# Or set WORKSPACE_PATH in .env to an existing project path
```

---

## Configuration

Edit `.env` (copied from `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | *(required)* | Your Anthropic API key |
| `ANTHROPIC_MODEL` | `claude-opus-4-5` | Claude model to use |
| `WORKSPACE_PATH` | `./workspace` | Path to the codebase the agent works on |
| `AGENT_VERBOSE` | `false` | Set `true` to log tool calls and routing decisions |
| `BMAD_MODE` | `false` | Set `true` to enable the BMad multi-agent team |

**Model options:**
- `claude-opus-4-5` – most capable, best for complex tasks
- `claude-sonnet-4-5` – balanced speed and capability
- `claude-haiku-4-5` – fastest and cheapest

---

## Running the Agent

Make sure `.env` is configured.

### Running Single-Agent Mode

```bash
uv run python main.py
```

Example session:
```
╔══════════════════════════════════════════════════╗
║       Ravita – Autonomous Coding Agent           ║
║       Powered by LangChain + Claude              ║
╚══════════════════════════════════════════════════╝
Mode:      Single-Agent (Ravita)
Model:     claude-opus-4-5
Workspace: /your/project/workspace

You > Show me the structure of this codebase
Agent > Here is the structure of your workspace: ...

You > Fix the bug in auth/handler.go where nil is not checked
Agent > I'll read the file first, then apply the fix...
```

### Running BMad Multi-Agent Mode

Set `BMAD_MODE=true` in `.env`, then:

```bash
uv run python main.py
```

Or run directly without editing `.env`:

```bash
BMAD_MODE=true uv run python main.py
```

Example BMad session:
```
╔══════════════════════════════════════════════════╗
║       Ravita – Autonomous Coding Agent           ║
║       Powered by LangChain + Claude              ║
╚══════════════════════════════════════════════════╝
Mode:      BMad Multi-Agent
Model:     claude-opus-4-5
Workspace: /your/project/workspace

You > We need a user authentication feature with JWT
Agent > [PRODUCT-MANAGER]: Here are the user stories for JWT authentication:
        As a user, I want to log in with email and password so that ...
        Acceptance Criteria: ...

You > Design the architecture for this
Agent > [ARCHITECT]: Here is the proposed system design for JWT auth: ...

You > Implement the login endpoint
Agent > [DEVELOPER]: I'll read the existing code first, then implement the endpoint...
```

---

## Available Tools

All tools are available to the Developer (Ravita) agent. Other BMad agents have access to a subset appropriate for their role.

| Tool | Description |
|---|---|
| `read_file` | Read the full contents of a file |
| `write_file` | Create or overwrite a file with given content |
| `list_files` | List files and directories in a path |
| `repo_map` | Generate a tree-style map of the codebase |
| `git_status` | Show modified, staged, and untracked files |
| `git_diff` | Show uncommitted changes or diff against a ref |
| `git_log` | Show recent commit history |
| `analyze_code` | Read a file and answer a specific question about it |
| `execute_command` | Run any shell command in the workspace directory |

---

## Interactive Commands

During a session, you can type:

| Command | Effect |
|---|---|
| `exit` or `quit` | Stop the agent |
| `reset` | Clear conversation history (keeps workspace and config) |

---

## Extending the Agent

### Add a new tool

1. Create a function in `tools/` decorated with `@tool` from `langchain_core.tools`.
2. Import and add it to the tools list in `agents/ravita_agent.py` and/or `agents/bmad/developer.py`.

### Add a new BMad agent

1. Create a new file in `agents/bmad/` (e.g., `devops.py`) with a class inheriting from `BaseRavitaAgent`.
2. Write a role-specific system prompt.
3. Register the agent in `agents/bmad/orchestrator.py`:
   - Add it to `self._agents`
   - Add its name to `_AGENT_NAMES`
   - Update `_SUPERVISOR_SYSTEM` with routing guidance for the new role.

### Swap the LLM provider

Replace `ChatAnthropic` in `agents/base_agent.py` with any LangChain-compatible chat model (e.g., `ChatOpenAI`, `ChatGoogleGenerativeAI`) and update the `.env` accordingly.
