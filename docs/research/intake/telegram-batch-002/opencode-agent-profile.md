# OpenCode Coding Agent - Comprehensive Profile

## Executive Summary

OpenCode is a **model-agnostic, multi-interface, open-source AI coding agent** by Anomaly. Written in Go/Bun (embedded JS runtime using Vercel AI SDK). 140K+ GitHub stars, 75+ providers, 14 built-in tools, agent system with permission gating, plugin architecture, MCP support, and multiple interfaces (TUI, CLI, Web, Desktop, IDE).

**Binary:** opencode-ai (npm package)
**Author:** Anomaly
**Domain:** opencode.ai
**Repo:** github.com/anomaly/opencode (via sst/opencode)
**Install:** npm install -g opencode-ai@latest

---

## 1. Architecture

### Core Design
- Go binary with embedded Bun/JavaScript runtime
- Uses Vercel AI SDK for provider abstraction
- SQLite database for session storage (migrated from JSON)
- Plugin system for extensibility
- MCP (Model Context Protocol) client support
- ACP (Agent Communication Protocol) server support

### Multi-Interface
- **TUI** — Full terminal UI with themes, keyboard shortcuts, session management
- **CLI** — One-shot `opencode run 'prompt'` for automation
- **Web UI** — `opencode web --port 4096` for browser-based access
- **Server** — `opencode serve` for headless HTTP API
- **Desktop** — Electron wrapper (separate install)
- **IDE** — VS Code/JetBrains extensions

### Key Data Paths

| Path | Purpose |
|------|---------|
| `~/.local/share/opencode/` | Data directory |
| `~/.local/share/opencode/auth.json` | API keys & OAuth tokens |
| `~/.local/share/opencode/log/` | Log files |
| `~/.config/opencode/` | Global config |
| `~/.cache/opencode/` | Cache & binary cache |
| `~/.local/state/opencode/` | Runtime state |
| `./opencode.json` | Project-level provider/model config |

---

## 2. Agent System

OpenCode has 7 built-in agents, each with specific tool permissions:

| Agent | Type | Tools | Purpose |
|-------|------|-------|---------|
| **build** | Primary | ALL tools | Main coding agent — reads, writes, edits, runs commands |
| **plan** | Read-only | read, grep, glob | Code review and planning — writes only to `.opencode/plans/*.md` |
| **explore** | Subagent | read, grep, glob, webfetch, websearch | Read-only search + web — spawned by `task` tool |
| **general** | Subagent | ALL except todowrite | General purpose worker — spawned by `task` tool |
| **compaction** | System | read, write | Auto-context summarization |
| **summary** | System | read | Generates session summaries |
| **title** | System | read | Generates session titles |

**Key insight:** The `task` tool lets build/plan agents spawn explore/general subagents for parallel work. This is OpenCode's built-in delegation mechanism.

---

## 3. Built-in Tools (14)

| Tool | Purpose | Notes |
|------|---------|-------|
| `bash` | Execute shell commands | Full shell access |
| `read` | Read file contents | Supports text and images |
| `edit` | Find/replace text editing | Precise edits |
| `write` | Create/overwrite files | Auto-creates dirs |
| `grep` | Search file contents | ripgrep-powered |
| `glob` | Find files by pattern | Glob matching |
| `webfetch` | Fetch URL content | Built-in web access |
| `websearch` | Search the web | Built-in search |
| `task` | Spawn subagent | Creates explore/general subagents |
| `todowrite` | Manage todo list | Project tracking |
| `question` | Ask user a question | Interactive prompts |
| `skill` | Use a skill | Agent Skills standard |
| `lsp` | Language Server Protocol | Experimental, code intelligence |
| `apply_patch` | Apply diff patches | Bulk file changes |

**Notable:** Pi has 7 tools, OpenCode has 14. The extra tools (webfetch, websearch, task, todowrite, question, lsp, apply_patch) make OpenCode significantly more capable for autonomous work.

---

## 4. Provider System

### 75+ Built-in Providers
OpenAI, Anthropic, Google (Gemini), Azure OpenAI, AWS Bedrock, Mistral, Groq, Cerebras, xAI, Fireworks, OpenRouter, DeepSeek, Ollama, LM Studio, LiteLLM, and many more.

### Custom Provider Setup (Z.AI example)

Create `opencode.json` in project directory:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "zai": {
      "name": "Z.AI",
      "api": "https://api.z.ai/api/coding/paas/v4",
      "models": {
        "glm-5-turbo": {
          "name": "GLM 5 Turbo",
          "limit": { "context": 128000, "input": 120000, "output": 16384 },
          "reasoning": true,
          "temperature": true,
          "tool_call": true,
          "attachment": true
        }
      }
    }
  }
}
```

**Auto-discovery:** Even if you define only one model in opencode.json, OpenCode auto-discovers ALL models from the provider's API. With Z.AI, this reveals 18+ models including glm-4.5, glm-4.6, glm-4.7, glm-5, glm-5-turbo, glm-5.1, and vision variants.

### Auth Configuration

API keys in `~/.local/share/opencode/auth.json`:
```json
{ "zai": { "type": "api", "key": "YOUR_KEY" } }
```

OAuth for interactive login:
```bash
opencode auth login    # Interactive OAuth
opencode auth list     # Verify connected providers
```

### Model Properties

Each model in config can declare:
- `limit.context` — Total context window
- `limit.input` — Max input tokens
- `limit.output` — Max output tokens
- `reasoning` — Supports thinking/reasoning
- `temperature` — Supports temperature control
- `tool_call` — Supports function calling
- `attachment` — Supports file attachments

---

## 5. Permission System

OpenCode has a built-in, granular permission system (unlike Pi which has none):

| Permission | Default | Description |
|------------|---------|-------------|
| `read` | ✅ Allowed | Read files within project |
| `external_directory` | ❌ Ask | Access files outside project dir |
| `doom_loop` | ❌ Ask | Potentially infinite loops (while true, etc.) |
| `question` | ❌ Then allow | Asking user questions |
| `plan_enter` / `plan_exit` | ❌ Then allow | Entering/exiting plan mode |
| `bash` | ⚙️ Configurable | Shell command execution |
| `edit` | ⚙️ Configurable | File editing |
| `write` | ⚙️ Configurable | File creation |

**Bypass:** `--dangerously-skip-permissions` flag disables all prompts (useful for autonomous/ci use).

---

## 6. CLI Reference

### One-Shot Execution
```bash
opencode run 'Your task here'
opencode run -m zai/glm-5-turbo 'task'         # Specific model
opencode run --thinking 'task'                    # Show thinking
opencode run --variant high 'task'                # Reasoning effort
opencode run --format json 'task'                 # Machine-readable
opencode run -f config.yaml -- "Review this"      # With file attachment
opencode run --dangerously-skip-permissions 'task' # No permission prompts
opencode run --title "name" 'task'                # Named session
opencode run -c 'follow-up'                       # Continue last session
opencode run -s ses_abc123 'continue'             # Specific session
opencode run --fork -s ses_abc123 'alt approach'  # Fork session
```

**CRITICAL:** `-f` files must come BEFORE `--`, message after:
- ❌ `opencode run -f file "msg"` (parses "msg" as another file)
- ✅ `opencode run -f file -- "msg"` (correct)

### Interactive TUI
```bash
opencode                    # Start fresh
opencode -c                 # Continue last session
opencode -s <session-id>    # Specific session
```

**Keybindings:**
- `Enter` — Submit (double press: finalize text, then send)
- `Tab` — Switch agent (build ↔ plan)
- `Ctrl+P` — Command palette
- `Ctrl+X L` — Switch session
- `Ctrl+X M` — Switch model
- `Ctrl+X N` — New session
- `Ctrl+X E` — Open editor
- `Ctrl+C` — Exit (DO NOT use `/exit` — it opens agent selector!)

### Session Management
```bash
opencode session list       # List sessions
opencode session delete <id> # Delete session
opencode export <id>        # Export as JSON
opencode import <file>      # Import session
opencode stats              # Token usage & cost
```

### Server Mode
```bash
opencode serve --port 4096       # Headless HTTP API
opencode web --port 4096         # Browser UI
opencode acp --port 4096         # ACP protocol server
opencode run --attach http://localhost:4096 "task"  # Remote task
```

### Debug & Diagnostics
```bash
opencode debug config       # Resolved configuration
opencode debug paths        # All data/config/cache paths
opencode debug skill        # Available skills
opencode debug agent <name> # Agent config details
opencode debug startup      # Startup timing
opencode debug lsp          # LSP utilities
opencode debug rg           # ripgrep utilities
opencode debug file         # File system utilities
opencode debug scrap        # List known projects
opencode debug snapshot     # Snapshot utilities
```

### Database
```bash
opencode db                          # Interactive SQLite shell
opencode db "SELECT * FROM sessions" # Run query
opencode db path                     # Print DB path
opencode db migrate                  # Migrate JSON → SQLite
```

### GitHub Integration
```bash
opencode github install    # Install GitHub agent
opencode github run        # Run GitHub agent
opencode pr <number>       # Fetch PR, checkout, start review
```

### MCP
```bash
opencode mcp add <name>    # Add MCP server
opencode mcp list          # List servers & status
opencode mcp auth <name>   # OAuth for MCP server
```

---

## 7. JSON Output Format

`--format json` streams newline-delimited JSON events:

```json
{"type":"step_start","sessionID":"ses_...","part":{"agent":"build","model":"zai/glm-5-turbo"}}
{"type":"text","sessionID":"ses_...","part":{"type":"text","text":"Hello!"}}
{"type":"tool_start","sessionID":"ses_...","part":{"tool":"bash","input":"ls -la"}}
{"type":"tool_end","sessionID":"ses_...","part":{"tool":"bash","output":"total 42"}}
{"type":"step_finish","sessionID":"ses_...","part":{"reason":"stop","tokens":{"total":10021,"input":2,"output":3,"reasoning":17,"cache":{"read":9999}},"cost":0.002}}
```

Event types: `step_start`, `text`, `tool_start`, `tool_end`, `step_finish`, `error`

Parse text only: `opencode run --format json 'task' | jq -s 'map(select(.type=="text")) | .[].part.text'`

---

## 8. Behavior Patterns (Observed)

### Self-Correction
OpenCode aggressively self-corrects. When a command fails:
1. It reads the error
2. Tries alternative approaches (kill -9, fuser, ss, lsof)
3. If stuck, modifies its own code to work around the issue
4. Keeps iterating until it succeeds or exhausts options

### Code Writing
- Writes files using `Write` tool (not bash echo)
- Uses proper file paths (resolves relative paths)
- Tests code after writing (runs it, checks output)
- Follows existing project conventions

### Command Batching
- Groups independent shell commands into single bash blocks
- Uses `&&` and `;` for sequential operations
- Uses `&` for background processes with `sleep` for timing

### Web-First Tendency
- Default behavior is to use `webfetch` before thinking locally
- Will search the web for package docs, APIs, etc.
- This can be slow — sometimes it's faster to just use local knowledge

---

## 9. Strengths & Weaknesses

### Strengths
1. **Most complete tool set** — 14 tools including web, subagents, todo, LSP
2. **Built-in subagents** — `task` tool spawns explore/general workers
3. **Permission system** — Granular control over what agents can do
4. **Multi-interface** — TUI, CLI, Web, Desktop, IDE, Server
5. **MCP + ACP** — Full protocol support
6. **75+ providers** — Most provider coverage of any agent
7. **Plugin system** — Extendable via npm packages
8. **GitHub integration** — PR review workflow built-in
9. **SQLite storage** — Efficient session persistence
10. **Session forking** — Branch sessions for exploration

### Weaknesses
1. **Slower startup** — Go binary, ~1-2s cold start vs Pi's ~0.5s
2. **Less token-efficient** — More overhead per request
3. **Web-happy** — Defaults to web fetch even when unnecessary
4. **TUI quirks** — Double-Enter, `/exit` trap
5. **External directory restriction** — Can't read files outside cwd by default
6. **Binary complexity** — Go/Bun hybrid is harder to debug than pure Node
7. **Smaller extension ecosystem** — Pi has 70+ examples, OpenCode relies on plugins

### Best Practices
1. Use `opencode run` for automation — no pty needed
2. Always use `--` after `-f` flags
3. Use `--dangerously-skip-permissions` for CI/autonomous use
4. Scope sessions to single repo/workdir
5. Use `--format json` for programmatic integration
6. Configure custom providers via `opencode.json`, not env vars
7. Use `opencode stats` to monitor token usage
8. Kill with Ctrl+C or process kill, never `/exit`

---

## 10. OpenCode vs Pi — Comparative Analysis

| Factor | OpenCode | Pi |
|--------|----------|-----|
| **Tools** | 14 (bash, read, edit, write, grep, glob, webfetch, websearch, task, todowrite, question, skill, lsp, apply_patch) | 7 (bash, read, edit, write, grep, find, ls) |
| **Providers** | 75+ | 25+ |
| **Subagents** | ✅ Built-in (task tool → explore/general) | ❌ Via extension only |
| **Web access** | ✅ webfetch + websearch | ❌ |
| **Permissions** | ✅ Granular system | ❌ None (trusts everything) |
| **Extensibility** | Plugins + MCP + ACP | TypeScript extensions (more powerful hooks) |
| **Session branching** | Fork + clone | Tree-structured JSONL (more powerful) |
| **Startup speed** | ~1-2s | ~0.5s |
| **Token efficiency** | Lower (Go overhead) | Higher (Node, lighter) |
| **Interfaces** | TUI, CLI, Web, Desktop, IDE, Server | TUI, CLI, RPC, SDK |
| **MCP** | ✅ Built-in client | Via extension |
| **ACP** | ✅ Server mode | ❌ |
| **GitHub** | ✅ Built-in PR review | ❌ |
| **Database** | ✅ SQLite | JSONL files |
| **JSON output** | `--format json` (rich events) | `--mode json` (simpler) |
| **RPC** | ❌ (uses server mode) | ✅ JSONL over stdin/stdout |
| **Guardrails** | doom_loop detector | None |
| **Best for** | Autonomous multi-step, web-aware, long sessions | Quick coding, pipelines, deep customization |

---

## 11. VPS Deployment State

- **Binary:** `/usr/lib/node_modules/opencode-ai/bin/.opencode` (Go binary)
- **Version:** v1.14.29
- **Config:** `/home/fangai/project/opencode.json` (Z.AI provider)
- **Auth:** `~/.local/share/opencode/auth.json` (Z.AI API key)
- **Fang service:** `fang-opencode.service` (port 3004)
- **Default model:** `zai/glm-5-turbo`
- **Available Z.AI models:** 18+ (auto-discovered from API)
- **A2A endpoint:** `http://localhost:3004/a2a/jsonrpc`
- **Status:** ✅ Working via direct CLI, A2A has known SSE parsing bug
