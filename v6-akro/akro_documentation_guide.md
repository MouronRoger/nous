# AI Documentation Guide - Akro

**IMPORTANT: The only canonical source of project documentation is the Markdown files in `/docs`, which are synchronized to the memory system via the knowledge graph. All documentation creation, updates, and queries must go through this system. The central progress log (`docs/progress.md`) tracks all changes and activities.**

This guide provides comprehensive information about the Akro documentation system, which uses a knowledge graph for relationship tracking and integrates with the MCP server.

## System Overview

The Akro project uses a deterministic, document-driven development framework for AI-augmented implementation with a focus on prompt-driven engineering.

### Key Components

1. **Documentation Structure**
   - **Directory**: `/docs` - All project documentation
   - **Core Files**: 
     - `client_spec.md` - Client requirements
     - `project_roadmap.md` - Project phases and timeline
     - `progress.md` - Central activity and decision log
   - **Directories**:
     - `phases/` - Phase documentation
     - `stages/` - Implementation stage guides
     - `reports/` - Stage completion reports

2. **Memory Integration**
   - **System**: MCP server with knowledge graph
   - **Memory File**: `.claude/memory.jsonl` or Claude app's memory
   - **Sync Command**: `python akro.py --sync`
   - **Relationship Detection**: Automatically detects relationships between documents

3. **Stage Implementation**
   - **Structure**: Each stage divided into testable segments
   - **Methodology**: Test-first development approach
   - **Cycle**: Write tests → Implement → Test → Refine until passing
   - **Constraints**: Each segment must fit within context window

## Working with Documentation

### Document Creation

To create new stage documents or reports:

```bash
# Create a stage document
python akro.py --create-stage --phase=1 --stage=1 --name="Project Setup"

# Create a completion report
python akro.py --create-report --phase=1 --stage=1
```

These commands:
- Generate properly formatted templates
- Follow naming conventions
- Update the progress log
- Create relationships in the knowledge graph when synced

### Synchronization

After making significant changes, sync the documentation to memory:

```bash
python akro.py --sync
```

This process:
- Reads all documentation files
- Extracts metadata and content
- Detects relationships between documents
- Creates memory entries for the knowledge graph
- Updates the progress log with sync information

### Progress Tracking

All significant events should be recorded in the central progress log (`progress.md`):

- Stage creation and implementation
- Component completion
- Decision records
- Memory synchronization
- Phase transitions

The `akro.py` script automatically updates the progress log when using its commands.

## Document Categories and Templates

### 1. Stage Template

Each stage document follows a structured template:

```markdown
# 🚧 STAGE {phase}.{stage}: {name}

## 📝 OBJECTIVES
- [Objective 1]
- [Objective 2]

## 🔧 IMPLEMENTATION SEGMENTS

### SEGMENT 1: [Component Name]
* 📝 **Test Requirements**:
  - [Test 1]
  - [Test 2]
* 🛠️ **Implementation Tasks**:
  - [Task 1]
  - [Task 2]
* ✅ **Verification Criteria**:
  - [Criterion 1]
  - [Criterion 2]

## 🎯 SUCCESS CRITERIA
- [Success criterion 1]
- [Success criterion 2]

## 📊 SYSTEM MEMORY UPDATE
document_component(
  name="[Component Name]",
  overview="Brief overview",
  purpose="Component purpose",
  implementation="Implementation details",
  status="Completed"
)
```

### 2. Completion Report Template

After completing a stage, create a report:

```markdown
# Stage {phase}.{stage}: {name} - Completion Report

## 📝 Summary
[Brief description of what was implemented]

## 🔧 Components Implemented
- [Component 1]
- [Component 2]

## 🧪 Testing Results
- [Test result 1]
- [Test result 2]

## 🎯 Achievements
- [Achievement 1]
- [Achievement 2]

## 📋 Lessons Learned
- [Lesson 1]
- [Lesson 2]

## 🚀 Next Steps
- [Next step 1]
- [Next step 2]
```

### 3. Progress Log Template

The central progress log tracks all activity:

```markdown
# Project Progress Log

## Current Status
- Current Phase: [Phase 1]
- Current Stage: [Stage 1.1: Setup]
- Status: [In Progress]

## Stage Completion Log
- {timestamp}: Stage 1.1 completed

## Memory Sync Log
- {timestamp}: Documentation synchronized

## Implementation Decisions
- **{timestamp}**: [Decision description]
  - **Context**: [Why this decision was needed]
  - **Alternatives**: [What other options were evaluated]
  - **Rationale**: [Why this option was chosen]

## Activity Log
- {timestamp}: Created stage document for Stage 1.1: Setup
```

## Memory Update Instructions

When documenting completion of segments or stages, use these formats:

```
document_component(
  name="[Component Name]",
  overview="Brief overview",
  purpose="Component purpose",
  implementation="Implementation details",
  status="Completed",
  coverage="100%"
)

update_stage_progress(
  phase="[Phase Number]",
  stage="[Stage Number]",
  name="[Stage Name]",
  status="Completed",
  completed=["List of completed segments"],
  issues=["Any issues encountered"],
  next=["Next steps"]
)

record_decision(
  title="[Decision Title]",
  status="Accepted",
  context="[Decision context]",
  decision="[Decision details]",
  consequences="[Impact of decision]",
  alternatives=["Alternative 1", "Alternative 2"]
)
```

## Key Principles

1. **Documentation as Source of Truth**: All project information is centralized in Markdown files
2. **Human-Directed AI Implementation**: Humans determine what to implement, AI assists with implementation
3. **Segmented Development**: Tasks broken into segments fitting within AI context windows
4. **Test-First Methodology**: Testing criteria defined before implementation
5. **Explicit Memory Management**: Central system for maintaining context across AI interactions

## Implementation Workflow

1. Define client requirements (`client_spec.md`)
2. Create project roadmap (`project_roadmap.md`)
3. Generate stage document (`akro.py --create-stage`)
4. Present stage to AI for implementation, one segment at a time
5. Document progress in progress log
6. Create completion report (`akro.py --create-report`)
7. Sync to memory (`akro.py --sync`)
8. Proceed to next stage

This workflow ensures a deterministic, linear development process with clear context preservation.
