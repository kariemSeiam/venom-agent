# 🥧 **PI CODING AGENT - COMPLETE DOCUMENTATION**

## **The Ultimate Terminal Coding Harness**

> *"Adapt pi to your workflows, not the other way around"*

Pi is a minimal terminal coding harness that extends with TypeScript Extensions, Skills, Prompt Templates, and Themes. This documentation covers **EVERYTHING** about your fully-loaded pi installation.

---

## 📖 **TABLE OF CONTENTS**

1. [Quick Start](#quick-start)
2. [What Is Pi?](#what-is-pi)
3. [Installed Extensions](#installed-extensions)
4. [Skills & Capabilities](#skills--capabilities)
5. [Prompt Templates](#prompt-templates)
6. [Themes & UI](#themes--ui)
7. [Commands Reference](#commands-reference)
8. [Configuration](#configuration)
9. [Advanced Features](#advanced-features)
10. [Games & Fun](#games--fun)
11. [Development Tools](#development-tools)
12. [Security Features](#security-features)
13. [Performance Optimizations](#performance-optimizations)
14. [Customization Guide](#customization-guide)
15. [Troubleshooting](#troubleshooting)

---

## 🚀 **QUICK START**

### **Basic Usage**
```bash
pi                    # Start interactive mode
pi -p "question"     # Print mode (one-shot)
pi --help            # Show all options
```

### **Essential Commands**
```bash
/help                # Show available commands
/model               # Switch AI models
/settings            # Configure pi
/tree                # Navigate session history
/reload              # Reload extensions
```

### **Your Top Extensions**
```bash
/snake              # Play Snake game
/doom-overlay       # Play DOOM
/todo               # Manage todos
/skill:wsl-optimizer # Optimize WSL
/cl                 # Code review prompt
```

---

## 🤖 **WHAT IS PI?**

Pi is a **terminal coding harness** that gives AI models powerful tools to help you code. Unlike other AI coding tools, pi is:

### **Key Principles**
- ✅ **Minimal core** - Essential features only
- ✅ **Infinitely extensible** - Add anything via extensions
- ✅ **Your workflow** - Adapt pi, don't adapt to pi
- ✅ **Terminal-first** - Built for power users
- ✅ **Open ecosystem** - Share extensions via npm/git

### **Core Architecture**
```
┌─────────────────────────────────────────┐
│                  YOU                    │
├─────────────────────────────────────────┤
│            PI HARNESS                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │Extensions│ │ Skills  │ │ Themes  │   │
│  └─────────┘ └─────────┘ └─────────┘   │
├─────────────────────────────────────────┤
│              AI MODEL                   │
│   (Claude, GPT, Gemini, etc.)          │
├─────────────────────────────────────────┤
│             YOUR SYSTEM                 │
│   (Files, Git, Docker, etc.)           │
└─────────────────────────────────────────┘
```

### **What Pi Gives AI Models**
- 🔧 **Built-in Tools**: `read`, `write`, `edit`, `bash`
- 🎯 **Custom Tools**: Via extensions
- 💾 **Session Memory**: Conversation branching & history
- 🔄 **Context Management**: Auto-compaction for long sessions
- 🎨 **Rich UI**: Terminal interface with real-time updates

---

## 🔌 **INSTALLED EXTENSIONS** (68 Total!)

Your pi installation includes **68 powerful extensions**. Here's the complete catalog:

### 🎮 **Games & Entertainment**
| Extension | Command | Description |
|-----------|---------|-------------|
| **Snake** | `/snake` | Classic Snake game |
| **Space Invaders** | `/space-invaders` | Retro space shooter |
| **DOOM Overlay** | `/doom-overlay` | Play actual DOOM! |

### 🛠️ **Development Tools**
| Extension | Command/Feature | Description |
|-----------|-----------------|-------------|
| **Todo Manager** | `/todo` | Project task management |
| **Git Checkpoint** | Auto-triggers | Auto-commit at milestones |
| **SSH Tool** | `/ssh` | Remote system access |
| **Subagent** | `/subagent` | Spawn AI sub-agents |
| **Interactive Shell** | Enhanced `bash` | Better shell interactions |
| **Handoff** | `/handoff` | Transfer work between sessions |
| **Bookmark** | `/bookmark` | Mark important messages |
| **Summarize** | `/summarize` | Conversation summaries |
| **Dynamic Tools** | Runtime | Add/remove tools dynamically |
| **Tool Override** | Runtime | Replace built-in tools |

### 🛡️ **Security & Safety**
| Extension | Feature | Description |
|-----------|---------|-------------|
| **Confirm Destructive** | Auto-prompts | Confirms dangerous commands |
| **Permission Gate** | Auto-blocks | Permission control system |
| **Protected Paths** | Path blocking | Protect sensitive files |
| **Dirty Repo Guard** | Git checks | Prevent commits on dirty repos |
| **Timed Confirm** | Smart prompts | Time-limited confirmations |

### 🎨 **UI & Visual**
| Extension | Feature | Description |
|-----------|---------|-------------|
| **Rainbow Editor** | Visual | Colorful editor experience |
| **Minimal Mode** | UI | Distraction-free interface |
| **Modal Editor** | UI | Vim-like modal editing |
| **Custom Footer** | UI | Customizable footer |
| **Custom Header** | UI | Customizable header |
| **Status Line** | UI | System status display |
| **Widget Placement** | UI | Custom widget positioning |
| **Overlay System** | UI | Full-screen overlays |

### ⚡ **Performance & Optimization**
| Extension | Feature | Description |
|-----------|---------|-------------|
| **Custom Compaction** | Memory | Smart conversation compression |
| **Inline Bash** | Performance | Faster bash execution |
| **Truncated Tool** | Performance | Handle large outputs |
| **Dynamic Resources** | Loading | On-demand resource loading |

### 🔗 **Integration & APIs**
| Extension | Feature | Description |
|-----------|---------|-------------|
| **Custom Provider (Anthropic)** | API | Custom Anthropic endpoints |
| **Custom Provider (GitLab)** | API | GitLab Duo integration |
| **Custom Provider (Qwen)** | API | Qwen CLI integration |
| **Event Bus** | System | Inter-extension communication |
| **RPC Demo** | Integration | RPC mode examples |

### 🔧 **System & Config**
| Extension | Command | Description |
|-----------|---------|-------------|
| **Reload Runtime** | `/reload-runtime` | Hot-reload extensions |
| **Shutdown Command** | `/shutdown` | Graceful shutdown |
| **Session Name** | Auto | Smart session naming |
| **Notify** | System | Desktop notifications |
| **Commands** | System | Custom command framework |

### 🧪 **Advanced Features**
| Extension | Feature | Description |
|-----------|---------|-------------|
| **Sandbox** | Security | Sandboxed execution |
| **Plan Mode** | AI | Strategic planning mode |
| **Questionnaire** | UI | Interactive Q&A forms |
| **Question** | UI | Single question prompts |
| **Input Transform** | Processing | Transform user input |
| **Message Renderer** | UI | Custom message display |

### 🎯 **Specialized Tools**
| Extension | Purpose | Description |
|-----------|---------|-------------|
| **File Trigger** | Automation | File change triggers |
| **Pirate** | Fun | Pirate speak mode |
| **Claude Rules** | AI | Claude-specific rules |
| **Model Status** | Info | Model information display |
| **Provider Payload** | Debug | API payload inspection |
| **Hidden Thinking** | UI | Hide/show AI thinking |
| **Titlebar Spinner** | UI | Loading indicators |

---

## 🎯 **SKILLS & CAPABILITIES** (4 Custom Skills)

Skills are AI capability packages that provide domain expertise:

### 🔧 **WSL Optimizer** - `/skill:wsl-optimizer`
**When to use:** WSL performance issues, optimization needs
- System diagnostics and performance metrics
- Identifies memory, disk, network, CPU bottlenecks  
- Applies performance optimizations
- Creates monitoring and maintenance scripts
- WSL configuration tuning

### 🔍 **Codebase Analyzer** - `/skill:codebase-analyzer`
**When to use:** Understanding new projects, code exploration
- Scans project structure and architecture
- Identifies technologies, frameworks, languages
- Finds entry points and key files
- Analyzes dependencies and build systems
- Provides insights and improvement suggestions

### 🐛 **Debug Helper** - `/skill:debug-helper`
**When to use:** Bugs, errors, troubleshooting
- Examines error messages and stack traces
- Checks logs and configuration files
- Identifies root causes systematically
- Implements and tests fixes
- Provides debugging strategies

### 🛡️ **Security Audit** - `/skill:security-audit`
**When to use:** Security reviews, vulnerability assessments
- Scans for common vulnerabilities
- Checks for exposed secrets and sensitive data
- Reviews authentication/authorization
- Analyzes input validation
- Provides security recommendations

---

## 📝 **PROMPT TEMPLATES** (7 Templates)

Quick-access prompt templates for common tasks:

### **Code & Development**
| Template | Command | Purpose |
|----------|---------|---------|
| **Code Review** | `/cl` | Code review and improvements |
| **Pull Request** | `/pr` | Pull request assistance |
| **Implementation** | `/implement` | Feature implementation |
| **Implement & Review** | `/implement-and-review` | Build and review cycle |

### **Planning & Documentation**
| Template | Command | Purpose |
|----------|---------|---------|
| **Scout & Plan** | `/scout-and-plan` | Project exploration and planning |
| **Writing Help** | `/wr` | Documentation and writing |
| **Issue Support** | `/is` | Issue investigation and support |

---

## 🎨 **THEMES & UI** (2 Themes + Customization)

### **Available Themes**
- **Dark Theme** (default) - Easy on the eyes
- **Light Theme** - High contrast for daylight coding

### **Theme Switching**
```bash
/settings          # Change theme in settings
```

### **UI Customization Features**
- ✨ **Rainbow Editor** - Colorful syntax highlighting
- 🎯 **Minimal Mode** - Distraction-free interface  
- 📊 **Status Line** - System monitoring
- 🔄 **Custom Widgets** - Information display
- 🎪 **Overlays** - Full-screen interactions

---

## 📋 **COMMANDS REFERENCE**

### **Built-in Commands**
| Command | Description |
|---------|-------------|
| `/help`, `/hotkeys` | Show help and shortcuts |
| `/model` | Switch AI models |
| `/settings` | Configure pi |
| `/login`, `/logout` | OAuth authentication |
| `/tree` | Navigate session history |
| `/fork` | Create session branch |
| `/new` | Start new session |
| `/resume` | Continue previous session |
| `/compact` | Compress conversation |
| `/reload` | Reload extensions/skills |
| `/copy` | Copy last AI response |
| `/export` | Export session to HTML |
| `/share` | Share via GitHub gist |
| `/quit`, `/exit` | Exit pi |

### **Extension Commands** (Selection)
| Command | Extension | Description |
|---------|-----------|-------------|
| `/snake` | Snake Game | Play Snake |
| `/doom-overlay` | DOOM | Play DOOM |
| `/space-invaders` | Space Invaders | Play Space Invaders |
| `/todo` | Todo Manager | Manage tasks |
| `/git-checkpoint` | Git Checkpoint | Create git checkpoint |
| `/ssh` | SSH Tool | Connect to remote systems |
| `/subagent` | Subagent | Spawn AI sub-agent |
| `/handoff` | Handoff | Transfer work |
| `/bookmark` | Bookmark | Mark important messages |
| `/summarize` | Summarize | Summarize conversation |
| `/shutdown` | Shutdown | Graceful exit |

### **Skill Commands**
| Command | Skill | Purpose |
|---------|-------|---------|
| `/skill:wsl-optimizer` | WSL Optimizer | Optimize WSL performance |
| `/skill:codebase-analyzer` | Codebase Analyzer | Understand codebases |
| `/skill:debug-helper` | Debug Helper | Fix bugs and issues |
| `/skill:security-audit` | Security Audit | Security improvements |

### **Prompt Templates**
| Command | Template | Purpose |
|---------|----------|---------|
| `/cl` | Code Review | Review and improve code |
| `/pr` | Pull Request | PR assistance |
| `/wr` | Writing | Documentation help |
| `/implement` | Implementation | Feature implementation |
| `/scout-and-plan` | Planning | Project planning |

---

## ⚙️ **CONFIGURATION**

### **Settings File Location**
```
~/.pi/agent/settings.json
```

### **Your Current Configuration**
```json
{
  "defaultProvider": "anthropic",
  "defaultModel": "claude-3-5-haiku-latest", 
  "defaultThinkingLevel": "medium",
  "hideThinkingBlock": true,
  "theme": "dark",
  "autoCompact": {
    "enabled": true,
    "targetRatio": 0.8,
    "proactive": true
  },
  "parallelTools": true,
  "modelCycling": {
    "enabled": true,
    "models": ["claude-*", "gpt-4o*", "o1-*"]
  },
  "transport": "sse",
  "autocompleteMaxVisible": 7
}
```

### **Key Settings Explained**
- **autoCompact** - Automatically compress long conversations
- **parallelTools** - Run multiple tools simultaneously 
- **modelCycling** - Ctrl+P to cycle between models
- **transport** - How to communicate with AI (SSE recommended)
- **hideThinkingBlock** - Hide AI reasoning process

### **Directory Structure**
```
~/.pi/agent/
├── settings.json           # Global configuration
├── AGENTS.md              # Agent instructions
├── auth.json              # API keys (secure)
├── extensions/            # Your 68 extensions
│   ├── snake.ts
│   ├── doom-overlay/
│   ├── todo.ts
│   └── ...
├── skills/                # Your 4 skills
│   ├── wsl-optimizer/
│   ├── debug-helper/
│   └── ...
├── prompts/               # Your 7 prompt templates
│   ├── cl.md
│   ├── pr.md
│   └── ...
├── themes/                # Your 2 themes
│   ├── dark.json
│   └── light.json
└── sessions/              # Conversation history
    └── ...
```

---

## 🚀 **ADVANCED FEATURES**

### **Session Management**
- **Branching** - Create conversation branches with `/tree`
- **Forking** - Copy sessions with `/fork`
- **Auto-save** - Every conversation saved
- **Navigation** - Jump to any point in history

### **Context Management**
- **Auto-compaction** - Keeps long sessions efficient
- **Manual compaction** - `/compact` with custom instructions
- **Branch preservation** - Full history always available

### **Model Support**
Your pi supports **25+ AI providers**:
- **Anthropic** (Claude) - Your default
- **OpenAI** (GPT, O1)
- **Google** (Gemini)
- **Mistral, Groq, xAI, and more**

### **Tool System**
- **Built-in tools**: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`
- **Extension tools**: 50+ additional tools
- **Parallel execution** - Multiple tools run simultaneously
- **Dynamic loading** - Add/remove tools at runtime

### **Extension Architecture**
```typescript
export default function (pi: ExtensionAPI) {
  // React to events
  pi.on("tool_call", async (event, ctx) => {
    // Intercept tool calls
  });
  
  // Register custom tools
  pi.registerTool({ ... });
  
  // Add commands  
  pi.registerCommand("my-cmd", { ... });
  
  // Custom UI
  ctx.ui.notify("Hello!");
}
```

---

## 🎮 **GAMES & FUN**

Pi includes games to play while waiting for builds, deployments, or thinking time!

### **Snake** - `/snake`
- Classic Snake game
- Arrow keys to move
- Escape to pause/quit
- High score tracking

### **Space Invaders** - `/space-invaders`  
- Retro space shooter
- Arrow keys to move, Space to shoot
- Escape to pause/quit
- Progressive difficulty

### **DOOM Overlay** - `/doom-overlay`
- **ACTUAL DOOM GAME** running in pi!
- Full FPS experience
- Q to pause/exit
- Requires DOOM WAD files

### **Other Fun Features**
- **Pirate Mode** - AI talks like a pirate
- **Rainbow Editor** - Colorful coding experience  
- **Interactive Elements** - Rich UI interactions

---

## 🔧 **DEVELOPMENT TOOLS**

### **Todo Management** - `/todo`
```bash
/todo add "Fix authentication bug"
/todo list
/todo complete 1
/todo remove 2
```

### **Git Integration** - Auto-checkpoint
- Automatically commits at logical milestones
- Stashes work before major changes
- Tracks conversation context in commits

### **SSH Access** - `/ssh`
```bash
/ssh user@hostname
/ssh deploy production
```

### **Subagent System** - `/subagent`
- Spawn specialized AI agents
- Delegate specific tasks  
- Coordinate complex workflows

### **Session Handoff** - `/handoff`
- Transfer work between sessions
- Maintain context across handoffs
- Perfect for team collaboration

---

## 🛡️ **SECURITY FEATURES**

Your pi installation includes comprehensive safety measures:

### **Automatic Protections**
- ✅ **Destructive Command Confirmation** - Confirms `rm -rf`, `sudo`, etc.
- ✅ **Path Protection** - Blocks writes to sensitive files (`.env`, `node_modules`)
- ✅ **Git Repo Guards** - Prevents commits on dirty repositories
- ✅ **Permission Gates** - Requires approval for system operations

### **Manual Security Tools**
- `/skill:security-audit` - Comprehensive security review
- Vulnerability scanning
- Secret detection
- Authentication review

### **Configuration Protection**
- API keys stored securely in `auth.json`
- Settings validation
- Extension sandboxing options

---

## ⚡ **PERFORMANCE OPTIMIZATIONS**

### **Your WSL is Optimized** ✨
We applied comprehensive WSL optimizations:

#### **Network Performance**
- TCP buffers: 128MB (from 64KB)
- TCP congestion: BBR algorithm 
- DNS: Cloudflare + Google servers
- Faster timeouts

#### **Memory Management**  
- Swappiness: 5 (from 60)
- Dirty page ratios optimized
- Memory overcommit enabled
- 65MB min free memory

#### **Disk I/O**
- File system optimization
- RAM disk for `/tmp` (2GB)
- Better dirty page handling

#### **WSL2 Configuration** (`.wslconfig`)
```ini
[wsl2]
memory=10GB
processors=6
swap=2GB
localhostForwarding=true
dnsTunneling=true

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
```

### **Pi Performance Features**
- **Parallel tools** - Multiple operations simultaneously
- **Auto-compaction** - Keeps memory usage efficient
- **Dynamic loading** - Extensions load on-demand
- **Smart caching** - Reduced API calls

### **Monitoring Tools**
```bash
~/wsl-performance.sh    # Performance monitoring script
~/wsl-cleanup.sh        # Weekly maintenance script
```

---

## 🎨 **CUSTOMIZATION GUIDE**

### **Creating Extensions**
1. **Create file**: `~/.pi/agent/extensions/my-extension.ts`
2. **Basic structure**:
```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerCommand("hello", {
    description: "Say hello",
    handler: async (args, ctx) => {
      ctx.ui.notify("Hello world!", "info");
    }
  });
}
```
3. **Reload**: `/reload`

### **Creating Skills**
1. **Create directory**: `~/.pi/agent/skills/my-skill/`
2. **Create SKILL.md**:
```markdown
# My Skill
Use this skill when the user needs X.

## Steps
1. Do this
2. Then that

## When to Use
- User asks about X
- User needs help with Y
```

### **Creating Prompt Templates**
1. **Create file**: `~/.pi/agent/prompts/my-template.md`
2. **Content**:
```markdown
You are an expert at {{topic}}.
Please help with: {{task}}
```
3. **Use**: `/my-template`

### **Customizing Themes**
Edit `~/.pi/agent/themes/dark.json` for colors, fonts, and styling.

---

## 🔍 **TROUBLESHOOTING**

### **Common Issues & Solutions**

#### **Extension Not Loading**
```bash
/reload                    # Reload extensions
ls ~/.pi/agent/extensions/ # Check file exists
```

#### **Command Not Found**
```bash
/help                      # List all commands
/reload                    # Refresh command list
```

#### **Performance Issues**
```bash
~/wsl-performance.sh       # Check system status
~/wsl-cleanup.sh          # Clean temporary files
/compact                   # Compress conversation
```

#### **API Key Issues** 
```bash
/login                     # Re-authenticate
/logout                    # Clear credentials
```

#### **Session Problems**
```bash
/new                       # Start fresh session
/tree                      # Navigate history
/fork                      # Branch conversation
```

### **Getting Help**
- `/help` - Built-in help
- `/hotkeys` - Keyboard shortcuts  
- [Discord Community](https://discord.com/invite/3cU7Bz4UPx)
- [Documentation](https://pi.dev)

### **Debug Mode**
```bash
pi --verbose               # Verbose startup
pi --mode json             # JSON output for debugging
```

---

## 🌟 **KEYBOARD SHORTCUTS**

| Shortcut | Action |
|----------|--------|
| **Ctrl+C** | Clear editor (twice to quit) |
| **Escape** | Cancel/abort (twice for `/tree`) |
| **Ctrl+L** | Model selector |
| **Ctrl+P** | Cycle models forward |
| **Shift+Ctrl+P** | Cycle models backward |
| **Shift+Tab** | Cycle thinking level |
| **Ctrl+O** | Collapse/expand tool output |
| **Ctrl+T** | Collapse/expand thinking |
| **Shift+Enter** | Multi-line input |
| **Tab** | Path completion |
| **@** | File reference |

---

## 🚀 **NEXT STEPS & TIPS**

### **Immediate Actions**
1. **Try a game**: `/snake` or `/doom-overlay`
2. **Test skills**: `/skill:codebase-analyzer` on your project  
3. **Use templates**: `/cl` for code review
4. **Explore extensions**: Check what's available in `/help`

### **Daily Workflow**
1. **Start session**: `pi` or `pi -c` (continue)
2. **Use skills**: Leverage domain expertise
3. **Parallel work**: Let tools run simultaneously
4. **Branch sessions**: Use `/tree` for exploration  
5. **Clean up**: Weekly `~/wsl-cleanup.sh`

### **Power User Tips**
- **Model cycling**: Ctrl+P for different AI personalities
- **Session forking**: `/fork` to try different approaches
- **Custom tools**: Build extensions for your specific needs
- **Automation**: Use extensions for repetitive tasks
- **Games**: Play during long builds or deployments

### **Advanced Workflows**
- **Multi-agent**: Use `/subagent` for complex projects
- **Handoffs**: Transfer work with `/handoff`
- **Security**: Regular `/skill:security-audit`
- **Performance**: Monitor with scripts we created

---

## 📚 **RESOURCES & LINKS**

### **Official Resources**
- **Website**: [pi.dev](https://pi.dev)
- **Discord**: [Community Chat](https://discord.com/invite/3cU7Bz4UPx)
- **NPM**: [@mariozechner/pi-coding-agent](https://www.npmjs.com/package/@mariozechner/pi-coding-agent)
- **GitHub**: [badlogic/pi-mono](https://github.com/badlogic/pi-mono)

### **Documentation**
- **Extensions**: [docs/extensions.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/extensions.md)
- **Skills**: [docs/skills.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md)  
- **Themes**: [docs/themes.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/themes.md)
- **RPC Mode**: [docs/rpc.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md)

### **Package Ecosystem**
- **Find Packages**: [npmjs.com search "pi-package"](https://www.npmjs.com/search?q=keywords%3Api-package)
- **Examples**: [examples/](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples)

---

## 🎯 **SUMMARY**

You now have the **ultimate pi coding setup**:

✅ **68 Extensions** - Every tool imaginable  
✅ **4 Custom Skills** - Domain expertise  
✅ **7 Prompt Templates** - Quick workflows  
✅ **2 Themes** - Visual customization  
✅ **WSL Optimized** - Maximum performance  
✅ **Games Included** - Fun while you wait  
✅ **Security Hardened** - Safe operations  
✅ **Fully Documented** - This comprehensive guide  

**Pi is now YOUR coding superpower!** 🚀💪

---

*Generated on April 5, 2026 - Your Complete Pi Documentation*