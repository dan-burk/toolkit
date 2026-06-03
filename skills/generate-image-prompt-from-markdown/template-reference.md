# Image Generation Prompt: R Playground Architecture (Simplified)

## Overview
Create a clean, easy-to-understand architecture diagram showing how a development environment works across different layers - from your Windows PC down to specialized MCP servers that provide tools to Claude Code.

**Target Audience**: Non-technical stakeholders, managers, or anyone wanting to understand the project structure without deep technical knowledge.

## Visual Style
- **Style**: Clean, modern, friendly (not overly technical)
- **Layout**: Vertical layers from top (your PC) to bottom (specialized tools)
- **Color Scheme** (soft, approachable colors):
  - Windows PC: Sky blue (#E3F2FD)
  - Linux Environment: Soft green (#E8F5E9)
  - Development Container: Warm orange (#FFF3E0)
  - AI Tool Containers: Light cyan (#E0F7FA)
- **Typography**: Clear, readable sans-serif fonts
- **Icons**: Friendly, recognizable icons (not technical symbols)

---

## The Four Main Layers

### Layer 1: Your Windows PC 💻
**Color**: Sky blue background
**Position**: Top of diagram

**What's Here:**
1. **VS Code** (code editor icon)
   - Where you write and edit code

2. **Claude Code** (AI assistant icon)
   - Your AI coding assistant

3. **Your Project Files** (folder icon)
   - Just show: "Project Folder" with R scripts and configuration inside
   - Label: "Your code and files live here"

**Simple Label**: "Windows 11 Computer"
**Security Note**: "⚠️ Vulnerable - Direct access to your files"

---

### Layer 2: Linux Environment 🐧
**Color**: Soft green background
**Position**: Below Windows

**What's Here:**
1. **Ubuntu Linux** (penguin icon)
   - A Linux system running inside Windows
   - Label: "Provides Linux capabilities on Windows"

2. **Docker** (whale icon)
   - Manages containers (isolated workspaces)
   - Label: "Container manager"

**Simple Label**: "Linux Environment (WSL2)"

---

### Layer 3: Development Container 🔧
**Color**: Warm orange background
**Position**: Large box inside the Linux layer (managed by Docker)

**What's Here:**

**Label**: "Your Working Environment"
**Technical Note**: "Runs as a Docker container, NOT in Ubuntu subsystem"

**The Tools Inside** (show as simple icons in a row):
- **Claude Code** - AI assistant for coding
- **R Language** - Data analysis software
- **R BTW MCP Server** - Lets Claude Code talk to R (runs inside this container)
- **Node.js** - JavaScript runtime
- **Docker CLI** - To launch specialized Docker containers

**Key Connection**:
"Claude Code ↔ R BTW MCP Server ↔ R Language"
(Show with a small arrow connecting these three)

**What It Does**:
"This is your isolated workspace where all your development tools run together safely. The R BTW MCP Server inside this container allows Claude Code to communicate with R directly. It runs in Docker to keep everything contained and reproducible."

---

### Layer 4: External MCP Servers 🤖
**Color**: Light cyan background (one color for all)
**Position**: Row of smaller boxes below the development container

**Show 5 External MCP Server Boxes** (arranged horizontally, each in a Docker container):

1. **DuckDuckGo MCP Server**
   - Icon: Magnifying glass
   - Purpose: "Provides search tools"
   - Container type: Docker

2. **Fetch MCP Server**
   - Icon: Globe/browser
   - Purpose: "Provides web fetching tools"
   - Container type: Docker

3. **YouTube MCP Server**
   - Icon: YouTube play button
   - Purpose: "Provides video transcript tools"
   - Container type: Docker

4. **Obsidian MCP Server**
   - Icon: Document/notebook
   - Purpose: "Provides note access tools"
   - Container type: Docker

5. **Toggl MCP Server**
   - Icon: Clock/stopwatch
   - Purpose: "Provides time tracking tools"
   - Container type: Docker

**Group Label**: "External MCP Servers in Docker Containers (Launch on demand)"
**Technical Note**: "Each MCP server runs in its own isolated Docker container and provides specific tools to Claude Code"

---

## How Things Connect (Simple Arrows)

### Connection 1: From Your PC to Development Container
**Arrow Color**: Blue
**Flow**:
```
Your Windows PC
      ↓
Opens VS Code
      ↓
Connects to Development Container
      ↓
You can work with R, Claude Code, and all tools
```
**Label on Arrow**: "Remote connection - work happens here"

---

### Connection 2: Claude Code to R (INSIDE Development Container)
**Arrow Color**: Orange (internal connection)
**Flow**:
```
You ask Claude Code to run R code
      ↓
Claude Code → R BTW MCP Server
      ↓
R BTW MCP Server → R Language
      ↓
R executes the code
      ↓
Results return: R → R BTW MCP Server → Claude Code → You
```
**Label on Arrow**: "Internal communication - R BTW MCP Server bridges Claude and R"

---

### Connection 3: Claude Code to External MCP Servers
**Arrow Color**: Purple (dashed)
**Flow**:
```
You ask Claude Code a question
      ↓
Claude needs an external MCP server (e.g., DuckDuckGo for search)
      ↓
Launches the appropriate external MCP server in a Docker container (DuckDuckGo, Obsidian, Fetch, YouTube, or Toggl)
      ↓
MCP server provides tools, gets the answer
      ↓
Returns result to you
```
**Label on Arrow**: "External MCP servers launch automatically in Docker containers when needed"

---

### Connection 4: Authentication
**Arrow Color**: Green
**Flow**:
```
Login once on Windows (Claude Code)
      ↓
Authentication shared with Development Container
      ↓
Both environments use same login
```
**Label on Arrow**: "Single sign-on"

---

## Key Concepts (Simple Callouts)

### Callout 1: "What are Containers and MCP Servers?"
**Position**: Near Development Container

**Text**:
```
Container = A self-contained workspace with everything you need,
isolated from the rest of your computer. Like a portable office!

MCP Server = A program that PROVIDES tools to Claude Code.
Each MCP server runs in a container and offers specialized tools:
• R BTW MCP Server provides tools for working with R
• DuckDuckGo MCP Server provides search tools
• YouTube MCP Server provides video transcript tools
... and so on!
```

---

### Callout 2: "Two Types of MCP Servers"
**Position**: Near external MCP server containers

**Text**:
```
INSIDE the Development Container:
• R BTW MCP Server - Always running, provides tools for Claude to talk to R

EXTERNAL MCP Servers (launch on demand in Docker containers):
• DuckDuckGo MCP Server - Provides web search tools
• Obsidian MCP Server - Provides note access tools
• Fetch MCP Server - Provides web page fetching tools
• YouTube MCP Server - Provides video transcript tools
• Toggl MCP Server - Provides time tracking tools

External MCP servers launch only when needed,
then disappear - keeping everything clean!
```

---

### Callout 3: "How Claude Code Uses MCP Servers"
**Position**: Between Development Container and external MCP servers

**Text**:
```
R BTW MCP Server (INSIDE Development Container):
• Bridges Claude Code and R Language
• Provides tools for Claude to run R code directly
• Provides tools to access R packages, data, and analyses

External MCP Servers (OUTSIDE in Docker containers):
• DuckDuckGo MCP Server - Provides web search tools
• Fetch MCP Server - Provides web page fetching tools
• YouTube MCP Server - Provides video transcript tools
• Obsidian MCP Server - Provides note access tools
• Toggl MCP Server - Provides time tracking tools

Claude Code connects to MCP servers to get tools.
Internal MCP server for R, external ones for everything else!
```

---

## Visual Enhancements (Keep It Simple)

### Simple Legend (Bottom corner):
```
Symbols:
→    Information flows this way
- -→ Tools connect on demand
💻   Application or software
📁   Files and folders
```

### Simplified Title Block:
```
Main Title: "R Playground with AI Integration"
Subtitle: "How everything works together"
```

---

## What to Show in Each Layer

### Windows PC Layer:
- 2 application icons (VS Code, Claude Code)
- 1 folder icon labeled "Your Project"
- Security warning: "⚠️ Vulnerable - Direct access to your files"
- Clean, not cluttered

### Linux Environment Layer:
- Ubuntu penguin icon
- Docker whale icon
- Brief label explaining purpose

### Development Container:
- 5 tool icons in a simple row (Claude Code, R Language, R BTW MCP Server, Node.js, Docker CLI)
- Small connecting arrows: Claude Code ↔ R BTW MCP Server ↔ R Language
- Label: "Your Working Environment (Docker Container)"
- Note: "Runs as a Docker container, NOT in Ubuntu subsystem"
- Highlight: "R BTW MCP Server runs INSIDE here - lets Claude talk to R"
- NO file paths, NO mount details, NO excessive technical jargon

### External MCP Servers Layer:
- 5 small Docker container boxes, each with:
  - One icon
  - MCP server name (DuckDuckGo MCP Server, Fetch MCP Server, YouTube MCP Server, Obsidian MCP Server, Toggl MCP Server)
  - One-line purpose (what tools it provides)
- Equal size boxes, evenly spaced
- Label: "Each MCP server runs in its own Docker container"

---

## Color and Flow Guidance

**Layer Colors** (light, distinct):
1. Sky blue (Windows) - Familiar, comfortable
2. Soft green (Linux) - Natural, supporting
3. Warm orange (Development Container) - Active, creative
4. Light cyan (External MCP Servers) - Cool, technical but friendly

**Arrow Colors**:
- Blue arrows = "How you connect and work" (PC to Development Container)
- Orange arrows = "Internal MCP server communication" (Claude Code ↔ R BTW MCP Server ↔ R, inside Development Container)
- Purple dashed arrows = "External MCP server connections" (Development Container launches external MCP servers in Docker containers)
- Green arrows = "Security and authentication" (shared login)

---

## Composition Guidelines

- **Whitespace**: Generous - don't crowd the diagram
- **Fonts**: Large enough to read in a presentation
- **Icons**: Recognizable, not overly detailed
- **Arrows**: Clear direction, labeled with simple text
- **Callouts**: 2-3 maximum, positioned in empty spaces

---

## Example Short Prompt for AI Generation

```
Create a clean, friendly architecture diagram for non-technical audiences showing:

Four vertical layers:
1. Top: Windows PC (sky blue) with VS Code and Claude Code icons, marked as "⚠️ Vulnerable - Direct access to your files"
2. Middle-top: Linux environment (soft green) with Ubuntu and Docker Engine
3. Middle-bottom: Development Docker container (warm orange) with 5 tool icons: Claude Code, R Language, R BTW MCP Server, Node.js, Docker CLI
   - Show connection: Claude Code ↔ R BTW MCP Server ↔ R Language (with small orange arrows)
   - Note: "Runs as a Docker container, NOT in Ubuntu subsystem"
   - Highlight: "R BTW MCP Server runs INSIDE - provides tools for Claude to talk to R"
4. Bottom: 5 EXTERNAL MCP Servers in Docker containers (light cyan) with specific names:
   - DuckDuckGo MCP Server (provides web search tools)
   - Fetch MCP Server (provides web page fetching tools)
   - YouTube MCP Server (provides video transcript tools)
   - Obsidian MCP Server (provides note access tools)
   - Toggl MCP Server (provides time tracking tools)
   - Label: "Each MCP server runs in its own isolated Docker container (EXTERNAL, launch on demand)"

Simple blue arrows showing: PC connects to Development Container
Orange arrows INSIDE Development Container: Claude Code ↔ R BTW MCP Server ↔ R Language
Purple dashed arrows showing: Development Container launches EXTERNAL MCP servers in Docker containers on demand (specify: DuckDuckGo, Obsidian, Fetch, YouTube, Toggl MCP servers)
Green arrows showing: Shared authentication from Windows to containers

Style: Clean, modern, approachable - like an infographic for a business presentation
Icons: Friendly, recognizable (whale for Docker, penguin for Linux, magnifying glass for DuckDuckGo search)
Text: Minimal, clear labels with specific MCP server names (DuckDuckGo MCP Server, Obsidian MCP Server, etc.) AND highlight R BTW MCP Server
Layout: Generous whitespace, professional but not intimidating

Include 3 simple callout boxes explaining:
- "What are Containers and MCP Servers?" (Container = portable workspace, MCP Server = provides tools to Claude Code)
- "Two Types of MCP Servers" (INSIDE: R BTW MCP Server | EXTERNAL: DuckDuckGo, Obsidian, Fetch, YouTube, Toggl MCP Servers)
- "How Claude Code Uses MCP Servers" (connects to MCP servers to get tools - R BTW MCP Server for R, external MCP servers for other capabilities)
```

---

## Key Differences from Technical Version

**Removed**:
- ❌ File system paths and mount points
- ❌ Docker socket technical details
- ❌ Configuration file lists (.yaml, .json, etc.)
- ❌ Exact version numbers
- ❌ Technical terminology (stdio, ephemeral, siblings, etc.)
- ❌ Security implementation details
- ❌ Port numbers and network details

**Emphasized**:
- ✅ WHAT each component does (purpose)
- ✅ WHY we have different layers (benefits)
- ✅ HOW things connect at a high level (user experience)
- ✅ Docker containers for isolation and organization
- ✅ MCP servers vs tools: MCP servers PROVIDE tools to Claude Code
- ✅ TWO types of MCP servers: INSIDE (R BTW MCP Server) vs EXTERNAL (DuckDuckGo, Obsidian, Fetch, YouTube, Toggl)
- ✅ R BTW MCP Server runs INSIDE development container - provides tools for Claude Code to talk to R
- ✅ Specific external MCP server names (DuckDuckGo MCP Server, Obsidian MCP Server, Fetch MCP Server, YouTube MCP Server, Toggl MCP Server)
- ✅ Development container runs in Docker, NOT Ubuntu subsystem
- ✅ Simple, relatable metaphors (portable office, translator/assistant inside, specialist MCP server consultants outside)
- ✅ Clear visual hierarchy
- ✅ Approachable language

---

## Metaphors to Guide the Design

Think of the architecture like:

**Your PC** = Your desk (vulnerable, direct access)
**Linux Environment** = A workspace platform that manages containers
**Development Docker Container** = Your portable office with:
  - Your work tools (Claude Code, R, Node.js)
  - Your personal assistant INSIDE (R BTW MCP Server) who provides tools to help Claude communicate with R
**R BTW MCP Server** = Your in-house translator/assistant who lives in your office and provides specialized tools for R work
**External MCP Servers** = Specialist consultants (DuckDuckGo, Obsidian, Fetch, YouTube, Toggl) you call when needed - each in their own separate office, each providing specialized tools

The diagram should make someone think: "Oh, I get it! MCP servers provide tools to Claude Code. There's an MCP server INSIDE my workspace for R, plus external MCP servers I can call on demand for other tasks."

---

## Alternative Presentation Styles

If the vertical layers feel too technical, consider:

1. **Concentric Circles**:
   - Your PC (outer ring)
   - Linux (middle ring)
   - Development Container with R BTW MCP Server (inner circle)
   - External MCP Servers (satellites around the center)

2. **Left-to-Right Flow**:
   - You (person icon) → Your PC → Development Environment with R BTW MCP Server → External MCP Servers → Results

3. **Building Blocks**:
   - Each layer as a foundational block
   - Simple stacking visual

---

## Metadata

- **Created**: 2025-12-22
- **Version**: 2nd Try (Simplified)
- **Target Audience**: Non-technical stakeholders, managers, students
- **Purpose**: Communicate the architecture in an accessible way
- **Tone**: Friendly, educational, clear
- **Complexity Level**: Business presentation / General audience
