# Akro - Document-Driven Development Framework

## What's Included

This package contains everything you need to implement the Akro document-driven development framework with human-directed AI implementation:

1. **`akro.py`** - The main script that handles all framework operations:
   - Framework setup: `python akro.py --setup`
   - Document synchronization: `python akro.py --sync`
   - Stage creation: `python akro.py --create-stage`
   - Report generation: `python akro.py --create-report`

2. **Documentation Files**:
   - `README.md` - Overview of the framework
   - `QUICK_START.md` - Getting started guide
   - `METHODOLOGY.md` - The principles behind the approach
   - `docs/guides/AI_DOCUMENTATION_GUIDE.md` - Comprehensive guide to the documentation system
   - `docs/guides/AI_DOCUMENTATION_PROMPT.md` - Prompt for AI sessions

3. **Templates**:
   - Stage template with segmented, test-first structure
   - Completion report template
   - Progress log template

## Installation

1. **Drop this package into your project root**:
   ```bash
   # Option 1: Copy the package contents
   cp -r akro/* your_project/
   cd your_project
   
   # Option 2: Download just the main script
   curl -o akro.py https://raw.githubusercontent.com/yourusername/akro/main/akro.py
   chmod +x akro.py
   ```

2. **Run the setup script**:
   ```bash
   python akro.py --setup
   ```

3. **Start the MCP server**:
   ```bash
   npx -y @itseasy21/mcp-knowledge-graph
   ```

## Quick Start Workflow

1. **Edit the client specification**:
   Open and edit `docs/client_spec.md` to define your project requirements.

2. **Sync to memory system**:
   ```bash
   python akro.py --sync
   ```

3. **Create the project roadmap**:
   Edit `docs/project_roadmap.md` to outline the development phases.

4. **Create a stage document**:
   ```bash
   python akro.py --create-stage --phase=1 --stage=1 --name="Project Setup"
   ```

5. **Implement stages with AI assistance**:
   Present the stage document to AI assistants one segment at a time, following the test-first methodology.

6. **Create completion reports**:
   ```bash
   python akro.py --create-report --phase=1 --stage=1
   ```

7. **Sync to memory**:
   ```bash
   python akro.py --sync
   ```

## Key Features

- **Prompt-Driven Engineering**: Documentation serves as structured prompts for AI
- **Deterministic Execution**: Linear, step-by-step implementation flow
- **Test-First Development**: Tests define requirements before implementation
- **Segmented Structure**: Fits within AI context windows
- **Human Direction**: All actions explicitly initiated by humans
- **Progress Tracking**: Central log of all activities
- **Relationship Detection**: Intelligent document relationships in the knowledge graph

## The Akro Method

Akro isn't just a tool - it's a method for reliable, deterministic AI-augmented development:

1. **Documentation as Interface**: Stage documents are the primary interface for directing AI
2. **Segmented Implementation**: Break work into context-window-friendly chunks
3. **Test-First Discipline**: Define expected behavior before implementing
4. **Explicit Memory Management**: Maintain context through documentation
5. **Human Control**: Explicit human direction at all decision points

## Directory Structure

```
docs/                       # All project documentation
├── client_spec.md          # Project requirements
├── project_roadmap.md      # Development phases and timeline
├── progress.md             # Central activity log
├── phases/                 # Phase documentation
├── stages/                 # Implementation stage guides
└── reports/                # Completion reports

templates/                  # Document templates
.cursor/                    # Cursor integration
.claude/                    # Claude memory files
```

## Remember

- The human is always in control
- Stage documents are delivered one at a time
- Progress is documented in a standardized format
- Memory is explicitly synchronized
- No automation surprises - all updates are human-initiated

For more detailed information, see the guides in `docs/guides/`.
