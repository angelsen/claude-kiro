---
description: Create a structured specification (requirements → design → tasks)
argument-hint: [feature-description]
allowed-tools: Read, Write, Grep, Glob, TodoWrite, ExitPlanMode
model: claude-sonnet-4-5-20250929
---

You are creating a formal specification for: $ARGUMENTS

# Spec-Driven Development Workflow

## Evolution Check

First, determine if this specification is evolving from or building upon an existing spec. Look for any indication in the description that this relates to, improves, replaces, or extends existing work.

If this appears to be an evolution:
- Find and read the original spec
- Understand what worked and what needs to change
- Include a "Specification Heritage" section in requirements
- Clean up the original spec:
  - Update its tasks.md status to "EVOLVED - See: [new-spec-name]"
  - Mark completed tasks as done, superseded tasks as "EVOLVED"
  - Create evolution.md documenting the transition, lessons learned, and what remains valid
- Reference preserved components and explain the evolution
- Update any active TodoWrite tasks from the original spec

Follow this structured process to create comprehensive specifications before coding.

**CRITICAL: This is a multi-phase process. You MUST stop and use ExitPlanMode after EACH phase. Do NOT proceed to the next phase until the user approves the current phase.**

## Phase 1: Requirements Analysis (STOP AFTER THIS PHASE)

Think deeply about the feature requirements. Create `.claude/specs/[feature-name]/requirements.md` with:

### Structure
```
# Feature: [Name]

## Overview
Brief description of what this feature does and why it exists.

## User Stories

### Story 1: [Title]
**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria (EARS notation):**
- WHEN [condition/event], THE SYSTEM SHALL [expected behavior]
- WHEN [condition/event], THE SYSTEM SHALL [expected behavior]
- WHEN [error condition], THE SYSTEM SHALL [error handling]

### Story 2: [Title]
[Repeat structure]

## Specification Heritage (if this is an evolution)
**Evolves From:** [original-spec-name]
**Preserves:** [List components/tasks that remain valid]
**Supersedes:** [List what's being replaced]
**Evolution Reason:** [Why the new approach is needed]

## Non-Functional Requirements
- Performance: [specific metrics]
- Security: [security requirements]
- Scalability: [scaling requirements]
- Accessibility: [accessibility standards]

## Constraints
- Technical constraints
- Business constraints
- Timeline constraints

## Out of Scope
Explicitly list what this feature does NOT include.
```

### Requirements Phase Instructions

1. **Make assumptions explicit** - Document all assumptions about user behavior, system state, edge cases
2. **Use EARS notation** for all acceptance criteria: "WHEN [condition] THE SYSTEM SHALL [behavior]"
3. **Cover edge cases** - Think through error conditions, boundary cases, invalid inputs
4. **Be testable** - Each requirement should be verifiable

**WORKFLOW:**
1. Generate the requirements content in your response
2. Use ExitPlanMode to present the requirements for review
3. When user accepts ExitPlanMode, write `.claude/specs/[feature-name]/requirements.md`
4. Confirm file creation and say "Requirements phase complete. Say 'continue' to proceed to design phase."

DO NOT proceed to Phase 2 until user says "continue" or similar.

## Phase 2: Design Documentation (ONLY START AFTER PHASE 1 APPROVAL)

**You should only be reading this section if the user has approved Phase 1 requirements.**

After user approves requirements, create `.claude/specs/[feature-name]/design.md` with:

### Structure
```
# Design: [Feature Name]

## Architecture Overview
High-level description of how this fits into the existing system.

## Component Analysis

### Existing Components to Modify
- `path/to/file.ts` - [what changes are needed]
- `path/to/file.ts` - [what changes are needed]

### New Components to Create
- `path/to/new-file.ts` - [purpose and responsibilities]

## Data Models

### New Interfaces/Types
\`\`\`typescript
interface FeatureName {
  field: type;  // Purpose and constraints
  field: type;  // Purpose and constraints
}
\`\`\`

### Modified Interfaces
\`\`\`typescript
// Add to existing interface
interface ExistingInterface {
  newField: type;  // Why this is needed
}
\`\`\`

## API Endpoints (if applicable)

### POST /api/feature
**Purpose:** [description]
**Request:**
\`\`\`json
{
  "field": "value"
}
\`\`\`
**Response:**
\`\`\`json
{
  "field": "value"
}
\`\`\`
**Errors:** [error conditions and codes]

## Data Flow

\`\`\`mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Database

    User->>Frontend: Action
    Frontend->>API: Request
    API->>Database: Query
    Database-->>API: Result
    API-->>Frontend: Response
    Frontend-->>User: Update
\`\`\`

## Error Handling Strategy
- [Error type 1]: [how to handle]
- [Error type 2]: [how to handle]
- Validation errors: [strategy]
- Network errors: [strategy]
- Database errors: [strategy]

## Testing Strategy

### Unit Tests
- Test [component 1] in isolation
- Test [component 2] edge cases
- Test error handling for [scenarios]

### Integration Tests
- Test [workflow 1] end-to-end
- Test [interaction 2] between components

### Performance Considerations
- Expected load: [metrics]
- Optimization strategy: [approach]
- Caching strategy: [if applicable]

## Security Considerations
- Authentication/Authorization requirements
- Input validation requirements
- Data encryption requirements
- CORS/CSP considerations

## Migration Strategy (if applicable)
- Database migrations needed
- Data migration approach
- Backward compatibility plan
- Rollback strategy
```

### Design Phase Instructions

1. **Analyze existing codebase** - Use Grep/Glob to find relevant files
2. **Be specific** - Actual file paths, actual interface names, actual implementation patterns
3. **Include diagrams** - Use Mermaid for sequence diagrams, component hierarchies
4. **Think through edge cases** - Error handling, validation, performance

**WORKFLOW:**
1. Generate the design content in your response
2. Use ExitPlanMode to present the design for review
3. When user accepts ExitPlanMode, write `.claude/specs/[feature-name]/design.md`
4. Confirm file creation and say "Design phase complete. Say 'continue' to proceed to task planning."

DO NOT proceed to Phase 3 until user says "continue" or similar.

## Phase 3: Task Planning (ONLY START AFTER PHASE 2 APPROVAL)

**You should only be reading this section if the user has approved Phase 2 design.**

After user approves design, create `.claude/specs/[feature-name]/tasks.md` AND use TodoWrite:

### Structure
```
# Implementation Tasks: [Feature Name]

**Status:** Not Started
**Spec:** [link to requirements.md and design.md]

## Task Breakdown

### Task 1: [Clear, action-oriented title]
**Description:** [What needs to be done]
**Files:**
- `path/to/file.ts` - [specific changes]
- `path/to/test.spec.ts` - [test requirements]

**Acceptance:**
- [ ] Implementation complete
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Error handling implemented
- [ ] Edge cases covered
- [ ] Code reviewed
- [ ] Documentation updated

**Dependencies:** None (or list task numbers)

**Estimated Complexity:** Low/Medium/High

---

### Task 2: [Title]
[Repeat structure]

---

## Task Dependencies

\`\`\`mermaid
graph TD
    T1[Task 1: Foundation] --> T2[Task 2: Build on foundation]
    T1 --> T3[Task 3: Parallel work]
    T2 --> T4[Task 4: Integration]
    T3 --> T4
\`\`\`

## Testing Checklist

After all tasks:
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Manual testing complete
- [ ] Performance benchmarks met
- [ ] Security review complete
- [ ] Accessibility review complete
- [ ] Documentation complete
- [ ] Ready for code review
```

### Task Planning Instructions

1. **Order by dependencies** - Tasks should be sequenced correctly
2. **Be specific** - Each task should be implementable independently
3. **Include testing** - Every task must specify test requirements

**WORKFLOW:**
1. Generate the tasks content in your response
2. Use ExitPlanMode to present the tasks for review
3. When user accepts ExitPlanMode:
   - Write `.claude/specs/[feature-name]/tasks.md`
   - Create TodoWrite list with ALL tasks
4. Confirm completion: "Specification complete! All 3 phases documented. Use `/spec-implement [task-number]` to begin implementation."

The specification is now ready for implementation.

## Guidelines for All Phases

### Thinking Mode
Use extended thinking for:
- Complex architectural decisions
- Tradeoff analysis
- Edge case identification
- Security considerations

### File Organization
- All specs in `.claude/specs/[feature-name]/`
- Naming: lowercase-with-hyphens (e.g., `user-authentication`)
- Keep related: requirements.md, design.md, tasks.md together

### Communication
- Use ExitPlanMode at end of each phase for approval
- Explain your reasoning for design decisions
- Highlight risks and tradeoffs
- Ask clarifying questions when requirements are ambiguous

### Quality Standards
- Requirements must be testable
- Design must be specific and implementable
- Tasks must be sequenced and granular
- All phases must link back to user stories

## Success Criteria

By the end of this command:
- [ ] Requirements documented with EARS notation
- [ ] Design specifies exact files and interfaces
- [ ] Tasks are sequenced and tracked in TodoWrite
- [ ] User has approved all three phases via ExitPlanMode checkpoints
- [ ] Implementation can begin with full context
