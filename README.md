# Akro Document-Driven Development Framework

This project uses the Akro document-driven development framework for AI-augmented implementation.

## Key Principles

1. **Documentation as Source of Truth**: Canonical documentation drives the development
2. **Human-Directed AI Implementation**: All implementation is guided by humans
3. **Segmented Stage Implementation**: Tasks broken down to fit AI context windows
4. **Test-First Development**: Tests defined before implementation
5. **Explicit Memory Management**: All documentation synchronized to AI memory

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
