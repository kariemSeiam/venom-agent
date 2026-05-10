# Pi Coding Agent - Comprehensive Profile

## Executive Summary

Pi is a **minimal, aggressively extensible terminal coding agent** built by Mario Zechner. Version 0.70.6, MIT licensed, actively developed (changelog 2026-04-28).

**Package:** @mariozechner/pi-coding-agent (npm)
**Author:** Mario Zechner (@badlogic)
**Domain:** pi.dev
**Repo:** github.com/badlogic/pi-mono
**Install:** npm install -g @mariozechner/pi-coding-agent

---

## 1. Architecture

### Three-Layer Design
- **pi-tui**: Terminal UI components, themes, overlays, keyboard handling
- **pi-coding-agent**: Session management, tools, extensions, compaction
- **pi-ai**: Multi-provider LLM API, streaming, caching

### Core Runtime Loop
1. User sends prompt via terminal editor (supports @ file refs, image paste, multi-line, path completion)
2. System prompt assembled: built-in instructions + AGENTS.md context files + skills + extension-injected content
3. Model responds, potentially calling tools
4. Tools execute (with extension hooks for gating/modification)
5. Results return to model, may call more tools or finish
6. Session saved as branching tree-structured JSONL

### Key Concepts
- **Sessions as Trees**: JSONL with id + parentId per entry. In-place branching, no file duplication.
- **Extension System**: TypeScript modules via jiti (no compilation). 20+ lifecycle events.
- **Message Queue**: Steering (mid-turn) and follow-up (post-completion) messages.
- **Compaction**: Auto/manual context summarization. Full history preserved in JSONL.

---

## 2. Modes of Operation

| Mode | Flag | Description |
|------|------|-------------|
| Interactive | (default) | Full TUI with editor, messages, themes, keyboard shortcuts |
| Print | -p / --print | Non-interactive: process prompt, print, exit. Supports piped stdin. |
| JSON | --mode json | Stream all events as JSON lines to stdout |
| RPC | --mode rpc | JSONL-over-stdin/stdout protocol for process integration |
| SDK | (programmatic) | Embed via createAgentSession() in Node.js apps |

### RPC Mode Details
- LF-delimited JSONL over stdin/stdout
- Commands: prompt, steer, follow_up, abort, bash, get_state, get_messages, set_model, cycle_model, get_available_models, set_thinking_level, compact, new_session, switch_session, fork, clone, get_session_stats, export_html, set_session_name, get_last_assistant_text, get_commands, get_fork_messages
- Events: agent_start/end, turn_start/end, message_start/update/end, tool_execution_start/update/end, queue_update, compaction_start/end, auto_retry_start/end, extension_error, extension_ui_request/response
- Extension UI protocol for dialogs (select, confirm, input, editor) and fire-and-forget (notify, setStatus, setWidget, setTitle)
- CRITICAL: Do NOT use Node readline for parsing. Split on newline only.

---

## 3. Built-in Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| read | Read file contents (text + images) | Offset/limit for large files |
| write | Create or overwrite files | Auto-creates parent dirs |
| edit | Precise find/replace text editing | Multiple non-overlapping edits per call |
| bash | Execute shell commands | Optional timeout, streaming output |
| grep | Search file contents | Read-only, OFF by default |
| find | Find files by glob pattern | Read-only, OFF by default |
| ls | List directory contents | Read-only, OFF by default |

**Tool control flags:**
- --tools read,bash,edit,write (allowlist)
- --no-tools (disable all)
- --no-builtin-tools (disable built-in, keep extension tools)

**Output truncation:** 50KB / 2000 lines default. Full output saved to temp file when truncated.

---

## 4. Provider System

### Supported Providers (25+)
Anthropic, OpenAI, Google (Gemini, Vertex, Antigravity), Azure OpenAI, DeepSeek, Mistral, Groq, Cerebras, xAI, Fireworks, OpenRouter, Vercel AI Gateway, ZAI, OpenCode Zen, OpenCode Go, Hugging Face, Kimi, MiniMax, Cloudflare Workers AI, Amazon Bedrock.

### ZAI Provider
- Env var: ZAI_API_KEY
- CLI: --provider zai --model zai/glm-4.5-air
- Available models:
  - zai/glm-4.5-air: 131.1K context, 98.3K max output, thinking=yes, images=no
  - zai/glm-4.7: 204.8K context, 131.1K max output, thinking=yes, images=no
  - zai/glm-5-turbo: 200K context, 131.1K max output, thinking=yes, images=no
  - zai/glm-5.1: 200K context, 131.1K max output, thinking=yes, images=no
- Thinking format: zai (custom provider compat)

### Custom Providers
- ~/.pi/agent/models.json for OpenAI-compatible APIs
- TypeScript extensions via pi.registerProvider()
- Supported APIs: openai-completions, openai-responses, anthropic-messages, google-generative-ai, google-vertex, bedrock-converse-stream, mistral-conversations, custom streamSimple
- OAuth/SSO support via extensions

---

## 5. Extension System

### Capabilities
- Custom tools with JSON Schema (TypeBox)
- 20+ lifecycle event hooks
- Custom commands, keyboard shortcuts, CLI flags
- User interaction (select, confirm, input, editor, custom overlays)
- Session persistence via pi.appendEntry()
- Custom rendering for tools and messages
- Custom providers via pi.registerProvider()

### Key Events
- Session: session_start, session_shutdown, session_before_switch, session_before_fork, session_before_compact, session_before_tree
- Agent: before_agent_start, agent_start, agent_end, turn_start, turn_end
- Messages: message_start, message_update, message_end
- Tools: tool_call (can block!), tool_execution_start/update/end, tool_result
- Provider: before_provider_request, after_provider_response
- Input: input (intercept/transform)

### Locations
- ~/.pi/agent/extensions/*.ts (global)
- .pi/extensions/*.ts (project-local)
- settings.json extensions array
- pi packages (pi install npm:... or git:...)

### 70+ Built-in Examples
Permission gates, git checkpointing, SSH, sandbox, sub-agents, plan-mode, custom providers, games (Snake, Space Invaders, Doom!), todo lists, file watchers, custom editors (vim mode), overlays, autocomplete, and more.

---

## 6. Skills System

- Agent Skills standard (agentskills.io)
- SKILL.md with YAML frontmatter (name, description)
- Progressive disclosure: descriptions in system prompt, full instructions on-demand
- Invoke via /skill:name or automatically by model
- Cross-compatible with Claude Code and Codex skills

---

## 7. Session Management

- JSONL files in ~/.pi/agent/sessions/<project-dir>/
- Tree structure with /tree, /fork, /clone
- Compaction: auto (threshold) + manual (/compact [instructions])
- Settings: compaction.enabled, reserveTokens (16K), keepRecentTokens (20K)
- Ephemeral mode: --no-session

---

## 8. Configuration

### Settings Files
- ~/.pi/agent/settings.json (global)
- .pi/settings.json (project override)
- ~/.pi/agent/models.json (custom providers)
- ~/.pi/agent/keybindings.json (custom keybindings)
- ~/.pi/agent/auth.json (OAuth credentials)

### Key Settings
- defaultProvider, defaultModel, defaultThinkingLevel
- compaction.enabled, reserveTokens, keepRecentTokens
- retry.enabled, maxRetries, baseDelayMs
- steeringMode, followUpMode (one-at-a-time or all)
- theme (dark, light, or custom)
- packages, extensions, skills, prompts, themes arrays
- enabledModels (Ctrl+P cycling scope)

### Context Files
- AGENTS.md or CLAUDE.md from ~/.pi/agent/, parent dirs, cwd
- Custom system prompt: .pi/SYSTEM.md
- Append: APPEND_SYSTEM.md

---

## 9. Thinking Levels

off, minimal, low, medium (default), high, xhigh (OpenAI only)

Set via --thinking, Shift+Tab, or RPC set_thinking_level.

---

## 10. Strengths and Weaknesses

### Strengths
1. Radical extensibility via TypeScript extensions
2. 25+ provider freedom with easy switching
3. Tree-structured session branching
4. Message queuing (steer + follow-up)
5. Lightweight terminal-native (no Electron)
6. SDK, RPC, JSON integration modes
7. Package ecosystem (npm/git)
8. Agent Skills standard compatible
9. 20+ lifecycle event hooks

### Weaknesses
1. No guardrails (no permission popups)
2. No codebase indexing (relies on model exploration)
3. No IDE integration (terminal-only)
4. No built-in sub-agents/plan mode
5. Smaller community than Claude Code/Copilot
6. TypeScript needed for advanced customization
7. No background execution (use tmux)

### Best Practices
1. Use AGENTS.md aggressively for project context
2. Write skills for repeatable workflows
3. Invest in extensions for your workflow
4. Use @ file references to guide the model
5. Run in containers (no safety net)
6. Use /tree branching when model goes wrong
7. Compact proactively with custom instructions
8. Use print mode for pipelines: cat file | pi -p "explain"

---

## 11. CLI Quick Reference

```bash
# Interactive
pi "prompt"                    # With initial prompt
pi @file.md "explain this"     # With file reference

# Non-interactive
pi -p "prompt"                 # Print and exit
cat file | pi -p "summarize"   # Piped stdin

# RPC mode
pi --mode rpc --no-session     # JSONL protocol

# Model selection
pi --provider zai --model zai/glm-4.5-air
pi --model zai/glm-5-turbo --thinking high

# Read-only mode
pi --tools read,grep,find,ls -p "review code"

# Session management
pi -c                          # Continue last session
pi -r                          # Resume from list
pi --no-session                # Ephemeral

# Package management
pi install npm:@foo/pi-tools
pi install git:github.com/user/repo
pi list
pi update [--self]

# List models
pi --list-models [search]

# Export
pi --export session.jsonl output.html
```

---

## 12. Integration Patterns for Our VPS

### Direct CLI Invocation
```bash
ZAI_API_KEY=key PI_PROVIDER=zai PI_MODEL=zai/glm-4.5-air pi -p --no-session "prompt"
```

### RPC Mode for Persistent Sessions
```bash
ZAI_API_KEY=key PI_PROVIDER=zai PI_MODEL=zai/glm-4.5-air pi --mode rpc --no-session
```

### With High Thinking
```bash
ZAI_API_KEY=key PI_PROVIDER=zai PI_MODEL=zai/glm-5-turbo pi -p --thinking high "complex task"
```

---

## 13. Current VPS State

- Package: @mariozechner/pi-coding-agent@0.70.6 (global npm)
- Also pulled in by: openclaw@2026.4.2 (has own dep on v0.64.0)
- Config dir: ~/.pi/agent/
- Auth: ~/.pi/agent/auth.json (empty {})
- Sessions: 3 previous sessions exist
- No settings.json, models.json, extensions, or skills configured yet
