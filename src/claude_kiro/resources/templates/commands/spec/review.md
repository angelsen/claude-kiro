---
description: Review a specification for completeness and quality
argument-hint: [spec-directory]
allowed-tools: Read, Grep, Glob
---

Review the specification at: @.claude/specs/$1/

# Specification Review Checklist

## Requirements Review (requirements.md)

### Completeness
- [ ] All user stories have clear "As a/I want/So that" structure
- [ ] All user stories have acceptance criteria in EARS notation
- [ ] Edge cases are documented
- [ ] Error conditions are specified
- [ ] Non-functional requirements are defined
- [ ] Constraints are listed
- [ ] Out-of-scope items are explicit

### Quality
- [ ] Requirements are testable (can be verified)
- [ ] Requirements are unambiguous (single interpretation)
- [ ] Requirements are atomic (one requirement per statement)
- [ ] EARS notation is used correctly: "WHEN [condition] THE SYSTEM SHALL [behavior]"
- [ ] No implementation details in requirements (focus on WHAT, not HOW)

### Coverage
- [ ] Happy path scenarios covered
- [ ] Error scenarios covered
- [ ] Edge cases covered
- [ ] Security requirements covered
- [ ] Performance requirements covered
- [ ] Accessibility requirements covered

## Design Review (design.md)

### Architecture
- [ ] Component responsibilities are clear
- [ ] Existing components to modify are identified
- [ ] New components to create are specified
- [ ] Integration points are documented
- [ ] Fits with existing system architecture

### Technical Specification
- [ ] Data models/interfaces are complete
- [ ] All fields have types and descriptions
- [ ] API endpoints are fully specified (if applicable)
- [ ] Data flow is documented (diagrams included)
- [ ] Error handling strategy is defined

### Testing & Quality
- [ ] Unit testing strategy is clear
- [ ] Integration testing approach is defined
- [ ] Performance considerations are addressed
- [ ] Security considerations are documented
- [ ] Migration strategy is defined (if needed)

### Implementability
- [ ] Design uses actual file paths from codebase
- [ ] Design follows existing patterns
- [ ] Technical approach is feasible
- [ ] Dependencies are identified
- [ ] Risks are called out

## Task Review (tasks.md)

### Task Quality
- [ ] Each task has clear, action-oriented title
- [ ] Each task specifies exact files to change
- [ ] Each task has acceptance criteria
- [ ] Each task includes testing requirements
- [ ] Dependencies between tasks are documented

### Sequencing
- [ ] Tasks are ordered by dependencies
- [ ] No circular dependencies
- [ ] Parallelizable work is identified
- [ ] Critical path is clear

### Completeness
- [ ] Tasks cover all requirements
- [ ] Tasks align with design
- [ ] Testing tasks are included
- [ ] Documentation tasks are included
- [ ] No obvious gaps

## Cross-Document Consistency

### Traceability
- [ ] All requirements map to design decisions
- [ ] All design components map to tasks
- [ ] No tasks without corresponding requirements

### Naming Consistency
- [ ] Feature names are consistent across documents
- [ ] Component names match across documents
- [ ] File paths are consistent

## Output Format

Provide review in this format:

## Review Summary
- Overall Quality: [Excellent/Good/Needs Work/Insufficient]
- Ready for Implementation: [Yes/No/With Changes]

## Strengths
- [List 3-5 strong points]

## Issues Found

### Critical (Must Fix)
- [Issue with specific location and recommendation]

### Warnings (Should Fix)
- [Issue with specific location and recommendation]

### Suggestions (Consider)
- [Improvement idea with rationale]

## Recommendations
- [Next steps]
