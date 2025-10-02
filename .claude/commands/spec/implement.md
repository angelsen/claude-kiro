---
description: Implement a task from the specification
argument-hint: [task-number-or-description]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite
---

Implement task: $ARGUMENTS

# Implementation Guidelines

## Before Starting

1. **Load the spec context:**
   - Read requirements.md to understand the "why"
   - Read design.md to understand the "how"
   - Read tasks.md to understand dependencies

2. **Update TodoWrite:**
   - Mark this task as "in_progress"
   - Use activeForm for the task description

3. **Verify prerequisites:**
   - Check that dependent tasks are completed
   - Ensure you have all necessary context

## During Implementation

### Follow the Design
- Implement exactly as specified in design.md
- Use the file paths specified
- Use the interfaces/types specified
- Follow the error handling strategy specified

### Test-Driven Approach
1. Write failing tests first (based on acceptance criteria)
2. Implement minimum code to pass tests
3. Refactor while keeping tests green

### Code Quality
- Follow project coding standards (check CLAUDE.md)
- Add clear comments for complex logic
- Use meaningful variable names
- Handle edge cases from requirements.md

## After Implementation

### Verification Checklist
- [ ] All unit tests passing
- [ ] Integration tests passing (if applicable)
- [ ] Error handling implemented
- [ ] Edge cases covered
- [ ] Code follows project standards
- [ ] Documentation updated

### TodoWrite Update
- Mark task as "completed" ONLY if ALL verification items pass
- If blocked, keep as "in_progress" and create new task for blocker

### Spec Sync
If implementation differs from design:
- Document the deviation in tasks.md
- Explain why the change was necessary
- Update design.md if the deviation is intentional

## Output

Provide:
1. Summary of what was implemented
2. Files changed/created
3. Test results
4. Any deviations from spec and why
5. Next recommended task (if any)
