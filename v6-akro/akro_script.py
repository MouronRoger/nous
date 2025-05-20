#!/usr/bin/env python3
"""
Akro - Document-Driven Development Framework with MCP Integration
Handles documentation, memory synchronization and relationship detection
while respecting the human-in-the-loop methodology
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for Akro framework."""
    parser = argparse.ArgumentParser(
        description="Akro - Document-Driven Development Framework"
    )
    parser.add_argument(
        "--setup", action="store_true", help="Initialize the framework"
    )
    parser.add_argument(
        "--sync", action="store_true", help="Sync documentation to memory"
    )
    parser.add_argument(
        "--create-stage", action="store_true",
        help="Create a new stage template"
    )
    parser.add_argument(
        "--create-report", action="store_true",
        help="Create a completion report template"
    )
    parser.add_argument(
        "--phase", type=int, help="Phase number for stage/report"
    )
    parser.add_argument(
        "--stage", type=int, help="Stage number for stage/report"
    )
    parser.add_argument(
        "--name", type=str, help="Name for stage/report"
    )
    return parser.parse_args()


# ——— Configuration ———
PROJECT: str = Path.cwd().name
HOME: Path = Path.home()
CLAUDE_MEM: Path = (
    HOME / "Library/Application Support/Claude" / PROJECT / "memory.jsonl"
)
LOCAL_MEM: Path = Path.cwd() / ".claude" / "memory.jsonl"

DOCS: Path = Path("docs")
TEMPLATES: Path = Path("templates")
PHASES: Path = DOCS / "phases"
STAGES: Path = DOCS / "stages"
REPORTS: Path = DOCS / "reports"
PROGRESS: Path = DOCS / "progress.md"
CLIENT_SPEC: Path = DOCS / "client_spec.md"
ROADMAP: Path = DOCS / "project_roadmap.md"
CURSOR_DIR: Path = Path(".cursor")
MCP_JSON: Path = CURSOR_DIR / "mcp.json"
AKRO_YAML: Path = Path("akro.yaml")

MCP_CMD: List[str] = ["npx", "-y", "@itseasy21/mcp-knowledge-graph"]
# ——— End config ———

# ——— Template definitions ———
STAGE_TMPL = (
    """\
# 🚧 STAGE {phase}.{stage}: {name}

## 📝 OBJECTIVES
- [Objective 1]
- [Objective 2]
- [Objective 3]

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

### SEGMENT 2: [Component Name]
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
- [Success criterion 3]

## 🚫 CONSTRAINTS
- [Constraint 1]
- [Constraint 2]

## 📋 DEPENDENCIES
- [Dependency 1]
- [Dependency 2]

## 📊 SYSTEM MEMORY UPDATE
For tracking completion, use:

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
  phase="{phase}",
  stage="{stage}",
  name="{name}",
  status="In Progress/Completed",
  completed=["List of completed segments"],
  issues=["Any issues encountered"],
  next=["Next steps"]
)
```
"""
)

REPORT_TMPL = (
    """\
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
"""
)

PROGRESS_TMPL = (
    """\
---
title: "Project Progress Log"
updated: "{timestamp}"
---

# Project Progress Log

## Current Status
- Current Phase: [Phase 1]
- Current Stage: [Not Started]
- Status: [In Progress]

## Stage Completion Log

## Memory Sync Log
- {timestamp}: Initial memory file created

## Implementation Decisions

## Activity Log
- {timestamp}: Project initialized
"""
)

CLIENT_SPEC_TMPL = (
    """\
---
title: "Client Specification"
updated: "{timestamp}"
---

# Client Specification

[Project requirements and objectives]

## Key Features

1. [Feature 1]
2. [Feature 2]
3. [Feature 3]
"""
)

ROADMAP_TMPL = (
    """\
---
title: "Project Roadmap"
updated: "{timestamp}"
---

# Project Roadmap

## Phase 1: Foundation
- [Deliverable 1]
- [Deliverable 2]

## Phase 2: Core Implementation
- [Deliverable 3]
- [Deliverable 4]
"""
)

README_TMPL = (
    """\
# Akro Document-Driven Development Framework

This project uses the Akro document-driven development framework for \
AI-augmented implementation.

## Key Principles

1. **Documentation as Source of Truth**: Canonical documentation drives \
the development
2. **Human-Directed AI Implementation**: All implementation is guided by \
humans
3. **Segmented Stage Implementation**: Tasks broken down to fit AI context \
windows
4. **Test-First Development**: Tests defined before implementation
5. **Explicit Memory Management**: All documentation synchronized to AI \
memory

## Documentation Structure

- `docs/client_spec.md` - Client requirements
- `docs/project_roadmap.md` - Project phases and timeline
- `docs/progress.md` - Central progress tracking
- `docs/phases/` - Phase-specific documentation
- `docs/stages/` - Implementation stage guides
- `docs/reports/` - Stage completion reports

## Working with this Project

### For Humans

1. Edit documentation in the `docs/` directory
2. Run `python akro.py --sync` to update AI memory
3. Create stage templates with `python akro.py --create-stage`
4. Create report templates with `python akro.py --create-report`

### For AI Assistants

- Only work on one stage at a time
- Implement each segment with test-first methodology
- Document all implementation in the progress log
- Report completion for stage tracking
"""
)
# ——— End template definitions ———


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.datetime.now().isoformat()


def choose_memory() -> Path:
    """Choose appropriate memory location."""
    if CLAUDE_MEM.parent.exists():
        mem_path = CLAUDE_MEM
    else:
        mem_path = LOCAL_MEM
    mem_path.parent.mkdir(parents=True, exist_ok=True)
    return mem_path


def touch(path: Path) -> None:
    """Create empty file and parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def setup_framework() -> None:
    """Initialize the framework structure."""
    print(f"Setting up Akro framework for {PROJECT}")
    mem = choose_memory()
    touch(mem)
    for d in (DOCS, TEMPLATES, PHASES, STAGES, REPORTS, CURSOR_DIR):
        d.mkdir(parents=True, exist_ok=True)
    if not CLIENT_SPEC.exists():
        CLIENT_SPEC.write_text(
            CLIENT_SPEC_TMPL.format(timestamp=get_timestamp())
        )
        print(f"Created {CLIENT_SPEC}")
    if not ROADMAP.exists():
        ROADMAP.write_text(ROADMAP_TMPL.format(timestamp=get_timestamp()))
        print(f"Created {ROADMAP}")
    if not PROGRESS.exists():
        PROGRESS.write_text(PROGRESS_TMPL.format(timestamp=get_timestamp()))
        print(f"Created {PROGRESS}")
    (TEMPLATES / "stage_template.md").write_text(
        STAGE_TMPL.format(phase="{phase}", stage="{stage}", name="{name}")
    )
    print(f"Created {TEMPLATES}/stage_template.md")
    (TEMPLATES / "report_template.md").write_text(
        REPORT_TMPL.format(phase="{phase}", stage="{stage}", name="{name}")
    )
    print(f"Created {TEMPLATES}/report_template.md")
    readme = Path("README.md")
    if not readme.exists():
        readme.write_text(README_TMPL)
        print(f"Created {readme}")
    if not AKRO_YAML.exists():
        AKRO_YAML.write_text(
            json.dumps(
                {
                    "mcp": {
                        "command": " ".join(MCP_CMD),
                        "memory_file": str(mem),
                    },
                    "doc_flow": {
                        "sequence": [
                            {"client_spec": str(CLIENT_SPEC)},
                            {"roadmap": str(ROADMAP)},
                            {"progress": str(PROGRESS)},
                            {"phases": str(PHASES) + "/*.md"},
                            {"stages": str(STAGES) + "/*.md"},
                            {"reports": str(REPORTS) + "/*.md"},
                        ]
                    },
                },
                indent=2,
            )
            + "\n"
        )
        print(f"Created {AKRO_YAML}")
    data: Dict[str, Any] = {}
    if MCP_JSON.exists():
        try:
            data = json.loads(MCP_JSON.read_text())
        except json.JSONDecodeError:
            data = {}
    data.setdefault("projects", {})[PROJECT] = {
        "root": str(Path.cwd().resolve()),
        "memory": {
            "command": MCP_CMD[0],
            "args": MCP_CMD[1:],
            "env": {"MEMORY_FILE_PATH": str(mem)},
        },
        "canonical_docs": [
            str(CLIENT_SPEC),
            str(ROADMAP),
            str(PROGRESS),
            str(PHASES) + "/*.md",
            str(STAGES) + "/*.md",
            str(REPORTS) + "/*.md",
        ],
    }
    MCP_JSON.write_text(json.dumps(data, indent=2))
    print(f"Configured {MCP_JSON}")
    print("\nSetup complete! Framework is ready to use.")
    print(f"Memory file: {mem}")
    print("\nNext steps:")
    print("1. Edit docs/client_spec.md with your requirements")
    print("2. Edit docs/project_roadmap.md with your phases")
    print("3. Run 'python akro.py --sync' to update memory")
    print(
        "4. Use 'python akro.py --create-stage --phase=1 --stage=1 --name=\"Setup\"' "
        "to create your first stage"
    )


def get_all_docs() -> List[Path]:
    """Get all documentation files as Path objects."""
    markdown_files: List[Path] = []
    for item in [CLIENT_SPEC, ROADMAP, PROGRESS]:
        if item.exists():
            markdown_files.append(item)
    for directory in [PHASES, STAGES, REPORTS]:
        if directory.exists():
            for file in directory.glob("**/*.md"):
                if file.is_file():
                    markdown_files.append(file)
    return markdown_files


def extract_metadata(file_path: Path) -> Optional[Dict[str, Any]]:
    """Extract metadata and content from a Markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "phases" in str(file_path):
            category = "phase"
        elif "stages" in str(file_path):
            category = "stage"
        elif "reports" in str(file_path):
            category = "report"
        elif file_path.name == "client_spec.md":
            category = "spec"
        elif file_path.name == "project_roadmap.md":
            category = "roadmap"
        elif file_path.name == "progress.md":
            category = "progress"
        else:
            category = "document"
        title = file_path.stem.replace("-", " ").replace("_", " ").title()
        heading_match = re.search(r"# (.+?)$", content, re.MULTILINE)
        if heading_match:
            title = heading_match.group(1).strip()
        return {
            "path": str(file_path),
            "title": title,
            "category": category,
            "content": content,
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def create_memory_entries(
    documents: List[Optional[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Create memory entries with relationships from document metadata."""
    memory_entries: List[Dict[str, Any]] = []
    for doc in documents:
        if not doc:
            continue
        entity = {
            "type": "entity",
            "name": doc["title"],
            "entityType": doc["category"].capitalize(),
            "observations": [doc["content"]],
        }
        memory_entries.append(entity)
    spec = next((d for d in documents if d and d["category"] == "spec"), None)
    roadmap = next((d for d in documents if d and d["category"] == "roadmap"), None)
    progress = next(
        (d for d in documents if d and d["category"] == "progress"), None
    )
    phases = [d for d in documents if d and d["category"] == "phase"]
    stages = [d for d in documents if d and d["category"] == "stage"]
    reports = [d for d in documents if d and d["category"] == "report"]
    if spec and roadmap:
        memory_entries.append(
            {
                "type": "relation",
                "from": spec["title"],
                "to": roadmap["title"],
                "relationType": "informs",
            }
        )
    if progress:
        for doc in documents:
            if doc and doc != progress:
                memory_entries.append(
                    {
                        "type": "relation",
                        "from": progress["title"],
                        "to": doc["title"],
                        "relationType": "tracks",
                    }
                )
    if roadmap:
        for phase in phases:
            memory_entries.append(
                {
                    "type": "relation",
                    "from": roadmap["title"],
                    "to": phase["title"],
                    "relationType": "contains",
                }
            )
    for stage in stages:
        stage_match = re.search(r"Stage (\d+)[._]", stage["title"])
        if stage_match:
            phase_num = stage_match.group(1)
            for phase in phases:
                if f"Phase {phase_num}" in phase["title"]:
                    memory_entries.append(
                        {
                            "type": "relation",
                            "from": phase["title"],
                            "to": stage["title"],
                            "relationType": "implements",
                        }
                    )
    for stage in stages:
        for report in reports:
            stage_id = re.search(r"Stage (\d+[._]\d+)", stage["title"])
            if stage_id and stage_id.group(1) in report["title"]:
                memory_entries.append(
                    {
                        "type": "relation",
                        "from": stage["title"],
                        "to": report["title"],
                        "relationType": "completed_by",
                    }
                )
    return memory_entries


def update_progress_log(action: str) -> bool:
    """Update the progress log with an action."""
    if not PROGRESS.exists():
        return False
    try:
        with open(PROGRESS, "r") as f:
            content = f.read()
        timestamp = get_timestamp()
        activity_entry = f"- {timestamp}: {action}"
        if "## Activity Log" in content:
            content = content.replace(
                "## Activity Log", f"## Activity Log\n{activity_entry}"
            )
        else:
            content += f"\n\n## Activity Log\n{activity_entry}"
        if action.startswith("Sync"):
            sync_entry = f"- {timestamp}: Documentation synchronized"
            if "## Memory Sync Log" in content:
                content = content.replace(
                    "## Memory Sync Log", f"## Memory Sync Log\n{sync_entry}"
                )
            else:
                content += f"\n\n## Memory Sync Log\n{sync_entry}"
        content = re.sub(r'updated: ".*?"', f'updated: "{timestamp}"', content)
        with open(PROGRESS, "w") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error updating progress log: {e}")
        return False


def sync_memory() -> None:
    """Sync all documentation to memory with relationship detection."""
    print(f"Syncing documentation to memory for {PROJECT}")
    docs = get_all_docs()
    if not docs:
        print("No documentation found.")
        return
    print(f"Found {len(docs)} documentation files")
    documents = [extract_metadata(doc) for doc in docs]
    valid_docs: List[Optional[Dict[str, Any]]] = [doc for doc in documents if doc]
    memory_entries = create_memory_entries(valid_docs)
    mem_path = choose_memory()
    with open(mem_path, "w", encoding="utf-8") as f:
        for entry in memory_entries:
            f.write(json.dumps(entry) + "\n")
    print(f"Synced {len(memory_entries)} entries to {mem_path}")
    update_progress_log(f"Synced {len(valid_docs)} documents to memory")


def create_stage(phase: int, stage: int, name: str) -> None:
    """Create a new stage document from template."""
    STAGES.mkdir(parents=True, exist_ok=True)
    filename = f"stage{phase}_{stage}-{name.lower().replace(' ', '-')}.md"
    stage_file = STAGES / filename
    if stage_file.exists():
        print(f"Error: {stage_file} already exists.")
        return
    template_file = TEMPLATES / "stage_template.md"
    if not template_file.exists():
        print(f"Using built-in template (no file found at {template_file})")
        template = STAGE_TMPL
    else:
        with open(template_file, "r") as f:
            template = f.read()
    content = template.format(phase=phase, stage=stage, name=name)
    with open(stage_file, "w") as f:
        f.write(content)
    print(f"Created stage document: {stage_file}")
    update_progress_log(
        f"Created stage document: Stage {phase}.{stage}: {name}"
    )


def create_report(
    phase: int, stage: int, name: Optional[str] = None
) -> None:
    """Create a completion report for a stage."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    if name is None:
        stage_files = list(STAGES.glob(f"stage{phase}_{stage}*.md"))
        if not stage_files:
            print(f"Error: No stage document found for Stage {phase}.{stage}")
            return
        stage_file = stage_files[0]
        name = ""
        with open(stage_file, "r") as f:
            content = f.read()
            match = re.search(r"# 🚧 STAGE \d+\.\d+: (.+)", content)
            if match:
                name = match.group(1)
            else:
                name = (
                    stage_file.stem.split("-", 1)[-1]
                    .replace("-", " ")
                    .title()
                )
    filename = f"report{phase}_{stage}-{name.lower().replace(' ', '-')}.md"
    report_file = REPORTS / filename
    if report_file.exists():
        print(f"Error: {report_file} already exists.")
        return
    template_file = TEMPLATES / "report_template.md"
    if not template_file.exists():
        print(f"Using built-in template (no file found at {template_file})")
        template = REPORT_TMPL
    else:
        with open(template_file, "r") as f:
            template = f.read()
    content = template.format(phase=phase, stage=stage, name=name)
    with open(report_file, "w") as f:
        f.write(content)
    print(f"Created completion report: {report_file}")
    update_progress_log(
        f"Created completion report for Stage {phase}.{stage}: {name}"
    )
    if PROGRESS.exists():
        try:
            with open(PROGRESS, "r") as f:
                content = f.read()
            timestamp = get_timestamp()
            completion_entry = (
                f"- {timestamp}: Stage {phase}.{stage}: {name} completed"
            )
            if "## Stage Completion Log" in content:
                content = content.replace(
                    "## Stage Completion Log",
                    f"## Stage Completion Log\n{completion_entry}",
                )
            else:
                if "## Current Status" in content:
                    content = content.replace(
                        "## Current Status",
                        (
                            "## Current Status\n\n## Stage Completion Log\n"
                            f"{completion_entry}"
                        ),
                    )
                else:
                    content += (
                        f"\n\n## Stage Completion Log\n{completion_entry}"
                    )
            with open(PROGRESS, "w") as f:
                f.write(content)
        except Exception as e:
            print(f"Error updating Stage Completion Log: {e}")


def main() -> None:
    """Main entry point for Akro script."""
    args = parse_args()
    if args.setup:
        setup_framework()
    elif args.sync:
        sync_memory()
    elif args.create_stage:
        if not args.phase or not args.stage or not args.name:
            print(
                "Error: phase, stage, and name are required to create a stage"
            )
            print(
                "Example: python akro.py --create-stage --phase=1 --stage=1 "
                "--name=\"Project Setup\""
            )
            sys.exit(1)
        create_stage(args.phase, args.stage, args.name)
    elif args.create_report:
        if not args.phase or not args.stage:
            print("Error: phase and stage are required to create a report")
            print(
                "Example: python akro.py --create-report --phase=1 --stage=1"
            )
            sys.exit(1)
        create_report(args.phase, args.stage, args.name)
    else:
        print("Akro - Document-Driven Development Framework")
        print("\nUsage:")
        print(
            "  python akro.py --setup                    Initialize the framework"
        )
        print(
            "  python akro.py --sync                     Sync documentation to memory"
        )
        print(
            "  python akro.py --create-stage [options]   Create a stage document"
        )
        print(
            "  python akro.py --create-report [options]  "
            "Create a completion report"
        )
        print("\nExamples:")
        print("  python akro.py --setup")
        print("  python akro.py --sync")
        print(
            '  python akro.py --create-stage --phase=1 --stage=1 '
            '--name="Project Setup"'
        )
        print("  python akro.py --create-report --phase=1 --stage=1")
        print("\nSee README.md for more details on the methodology.")
        sys.exit(1)


if __name__ == "__main__":
    main()
