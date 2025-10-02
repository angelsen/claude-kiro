# KIRO SPECS METHODOLOGY

Research compiled from local Kiro documentation (kiro.dev)

## Executive Summary

Kiro's Spec-Driven Development methodology transforms how AI-assisted development works by treating the LLM as a thinking partner throughout the entire development lifecycle, not just a code generator. The methodology enforces a structured 3-phase workflow (Requirements → Design → Tasks) that catches problems before they're expensive, maximizes coding context efficiency, and creates living documentation that stays synchronized with code.

## Core Philosophy

Traditional AI coding assistants jump immediately into code generation from high-level prompts, leading to:
- Repeated clarification cycles ("actually, I meant...")
- Context windows cluttered with exploratory conversations
- Limited space for final code generation
- Requirements discovered mid-implementation

**Kiro's approach**: Externalize planning into structured specification files, keeping active context focused on immediate coding tasks while maintaining clear decision trails.

## The 3-Phase Workflow

### Phase 1: Requirements

**Purpose**: Transform vague feature requests into structured, testable requirements.

**Output File**: `requirements.md`

**Format**: User stories with EARS notation acceptance criteria

#### EARS Notation (Easy Approach to Requirements Syntax)

EARS provides a structured format for writing clear, testable requirements:

```
WHEN [condition/event]
THE SYSTEM SHALL [expected behavior]
```

**Real Example from Documentation**:
```
WHEN a user submits a form with invalid data
THE SYSTEM SHALL display validation errors next to the relevant fields
```

**Benefits of EARS**:
- **Clarity**: Requirements are unambiguous and easy to understand
- **Testability**: Each requirement can be directly translated into test cases
- **Traceability**: Individual requirements can be tracked through implementation
- **Completeness**: The format encourages thinking through all conditions and behaviors

#### Requirements Phase Process

1. User provides high-level prompt (e.g., "Add a review system for products")
2. Kiro generates user stories for:
   - Viewing functionality
   - Creating functionality
   - Filtering/sorting
   - Rating systems
3. Each user story includes EARS notation acceptance criteria covering edge cases
4. User reviews and can request refinements
5. User approves with "LGTM" or provides specific feedback

**Example from E-commerce Case Study**:
- User Story: "As a customer, I want to leave product reviews"
- Acceptance Criteria using EARS:
  - WHEN a user clicks "Write Review" on a product page, THE SYSTEM SHALL display a review form
  - WHEN a user submits a review without selecting a rating, THE SYSTEM SHALL display a validation error
  - WHEN a user successfully submits a review, THE SYSTEM SHALL display a confirmation message

### Phase 2: Design

**Purpose**: Document technical architecture, sequence diagrams, and implementation considerations.

**Output File**: `design.md`

**Contents**:
- Architecture overview
- Data Flow diagrams
- Component Hierarchy diagrams (Mermaid)
- Interfaces (TypeScript/language-specific)
- Data Models
- API endpoints
- Error Handling strategy
- Unit Testing Strategy
- Database schemas
- Integration points

#### Design Phase Process

1. Kiro analyzes existing codebase
2. Compares requirements against current architecture
3. Generates design document with:
   - Data flow diagrams
   - TypeScript interfaces / data structures
   - Database schemas
   - API endpoint definitions
   - Sequence diagrams
4. Design includes example code snippets (pseudocode showing intended API)
5. User reviews in Preview mode (for proper diagram rendering)
6. User approves or requests design changes

**Note from Documentation**: "Think of it more as pseudocode that is imagining the API. The actual implementation may end slightly different."

### Phase 3: Implementation Planning

**Purpose**: Break down work into discrete, trackable tasks with clear descriptions and outcomes.

**Output File**: `tasks.md`

**Task Structure**:
- Main tasks with clear descriptions
- Sub-tasks for complex items
- Each task includes:
  - Clear description
  - Expected outcome
  - Unit tests requirements
  - Integration tests
  - Loading states
  - Mobile responsiveness
  - Accessibility requirements
  - Necessary resources/dependencies

#### Task Planning Process

1. Kiro uses requirements + design to generate task sequence
2. Tasks are ordered by dependencies
3. Each task links back to requirements (nothing falls through cracks)
4. Tasks include:
   - Implementation steps
   - Testing requirements
   - UI/UX considerations
5. User reviews task list
6. User can modify task order or request changes
7. User approves with "LGTM"

**Real Example from Documentation**:
For email verification and password reset feature:
- Email verification implementation
  - Frontend client side components
  - Backend server routes and Cognito integration
- Password reset implementation
  - Frontend client side screens
  - Backend server routes and Cognito integration

### Phase 4: Execution

**Purpose**: Track progress as tasks are completed with ability to update and refine.

**Execution Interface Features**:
- Task execution interface in tasks.md
- Real-time status updates
- Tasks marked as: pending → in-progress → completed
- "Start Task" link above each task
- View code diffs after completion
- View agent execution history
- Audit completed work

**Best Practice from Documentation**:
"You will likely still need to review, test, and iterate on generated code for each task, even though the task list marks the task as 'Task completed'."

## How Specs Stay Synced with Code

Kiro addresses the common problem where documentation becomes outdated during implementation:

### Bidirectional Updates

1. **Code → Specs**:
   - Developers can ask Kiro to update specs based on code changes
   - Click "Update tasks" in tasks.md
   - Kiro scans codebase and marks completed tasks

2. **Specs → Code**:
   - Modify requirements.md or design.md
   - Navigate to design.md and select "Refine"
   - Both design documentation AND task list update to reflect changes
   - Navigate to tasks.md and choose "Update tasks"
   - New tasks generated that map to new requirements

### Handling Already-Implemented Tasks

**Option 1: Automatic Update**
1. Open tasks.md file
2. Click "Update tasks"
3. Kiro automatically marks completed tasks

**Option 2: Manual Check**
1. In spec session, ask: "Check which tasks are already complete"
2. Kiro analyzes codebase
3. Kiro identifies implemented functionality
4. Kiro automatically marks completed tasks

## File Organization

### Directory Structure

```
.kiro/
├── steering/          # Project context and guidelines
│   ├── product.md     # Business context, features, user workflows
│   ├── tech.md        # Tech stack, patterns, constraints
│   ├── structure.md   # Architecture, file organization
│   └── [custom].md    # Domain-specific guidance
│
└── specs/             # Feature specifications
    ├── feature-name-1/
    │   ├── requirements.md
    │   ├── design.md
    │   └── tasks.md
    │
    └── feature-name-2/
        ├── requirements.md
        ├── design.md
        └── tasks.md
```

### Example: E-commerce Application

```
.kiro/specs/
├── user-authentication/       # Login, signup, password reset
├── product-catalog/           # Product listing, search, filtering
├── shopping-cart/             # Add to cart, quantity updates, checkout
├── payment-processing/        # Payment gateway integration, order confirmation
└── admin-dashboard/           # Product management, user analytics
```

**Benefits**:
- Work on features independently without conflicts
- Maintain focused, manageable spec documents
- Iterate on specific functionality without affecting other areas
- Collaborate with team members on different features simultaneously

### Steering Files (Foundational Context)

Kiro generates three foundational steering documents that provide persistent project knowledge:

1. **product.md**:
   - Product purpose
   - Target users
   - Key features
   - Business objectives
   - Helps Kiro understand "why" behind technical decisions

2. **tech.md**:
   - Technology stack
   - Frameworks and libraries
   - Development tools
   - Technical constraints
   - Ensures Kiro prefers established stack over alternatives

3. **structure.md**:
   - File organization
   - Naming conventions
   - Import patterns
   - Architectural decisions
   - Ensures generated code fits seamlessly into existing codebase

**Steering File Inclusion Modes**:

```yaml
---
inclusion: always           # Default: loaded in every interaction
---

---
inclusion: fileMatch        # Conditional: loaded when matching files
fileMatchPattern: "components/**/*.tsx"
---

---
inclusion: manual          # On-demand: referenced with #file-name
---
```

## Key Principles to Adopt

### 1. Planning Before Coding

**Anti-Pattern**: Jumping into code generation immediately
**Kiro Pattern**: Spend time in requirements and design phases

**Research Finding**: Issues found during development phase are 5-7x more costly than during planning phase. This holds true even with AI agents.

**Benefit**: Single spec request accomplishes what would otherwise require multiple vibe requests during implementation.

### 2. Make Requirements Explicit

**Anti-Pattern**: Vague prompts leading to clarification cycles
**Kiro Pattern**: Use EARS notation to make all requirements and constraints explicit

**Example Transformation**:
- Vague: "Add a review system"
- Explicit: User stories with EARS criteria covering all edge cases

### 3. Maximize Context Efficiency

**Anti-Pattern**: Context window cluttered with exploratory conversation
**Kiro Pattern**: Externalize planning to files, keep active context for coding

**Benefit**: Maximum context space available for actual coding task

### 4. Natural Pause Points

**Anti-Pattern**: AI makes all decisions without human review
**Kiro Pattern**: Each phase has approval checkpoint (Requirements → Design → Tasks → Execution)

**Benefit**: Humans review, modify, and approve direction before resources invested

### 5. Iterative Refinement

**Anti-Pattern**: Starting over when requirements change
**Kiro Pattern**: Modify specification files and regenerate affected components

**Benefit**: Iterate without losing entire conversation history

### 6. Living Documentation

**Anti-Pattern**: Documentation as afterthought, quickly outdated
**Kiro Pattern**: Specs as source of truth, bidirectionally synced with code

**Benefit**:
- Every decision documented
- Clear audit trail of technical choices
- Context preserved for future team members
- Institutional knowledge built automatically

### 7. Version Control Integration

**Anti-Pattern**: Specs stored separately from code
**Kiro Pattern**: Commit specs to repo alongside code they describe

**Benefit**:
- All project artifacts together
- Connection between requirements and implementation maintained
- Standard development workflows (review, comment, contribute)
- Team collaboration using Git

### 8. Feature-Based Organization

**Anti-Pattern**: Single monolithic spec for entire codebase
**Kiro Pattern**: Multiple specs for different features

**Benefit**:
- Focused, manageable documents
- Independent feature work
- Reduced conflicts
- Parallel collaboration

### 9. Steering for Consistency

**Anti-Pattern**: Explaining conventions in every chat
**Kiro Pattern**: Persistent knowledge in .kiro/steering/

**Benefit**:
- Consistent code generation
- Reduced repetition
- Team alignment
- Scalable project knowledge

### 10. Task-Wise Execution

**Anti-Pattern**: "Execute all tasks in spec" in single shot
**Kiro Pattern**: Task-by-task execution with review

**Quote from Documentation**: "We do not recommend doing this as we recommend a task-wise execution to get better results."

## Real-World Example: Review System Feature

### Initial Prompt
```
"Add a review system for products"
```

### Requirements Generated (requirements.md)
User stories with EARS notation:
- Viewing reviews
  - WHEN a user navigates to a product page, THE SYSTEM SHALL display existing reviews
  - WHEN no reviews exist, THE SYSTEM SHALL display "No reviews yet"
- Creating reviews
  - WHEN a user submits a review without rating, THE SYSTEM SHALL display validation error
- Filtering reviews
  - WHEN a user selects "5 stars" filter, THE SYSTEM SHALL show only 5-star reviews
- Rating reviews
  - WHEN a user submits rating, THE SYSTEM SHALL update average rating

### Design Generated (design.md)
```typescript
interface Review {
  id: string;
  userId: string;
  productId: string;
  rating: number;
  comment: string;
  createdAt: Date;
}

// Component Hierarchy Diagram (Mermaid)
// API Endpoints
// Database Schema
// Error Handling Strategy
```

### Tasks Generated (tasks.md)
1. Create Review data model and database schema
   - Unit tests for model validation
2. Implement Review API endpoints
   - Integration tests for CRUD operations
3. Build ReviewList component
   - Unit tests
   - Loading states
   - Responsive design
4. Build ReviewForm component
   - Form validation
   - Error handling
   - Accessibility (ARIA labels)
5. Integrate with Product page
   - Integration tests

### Execution
- Click "Start Task" for each task
- Review generated code
- Test and iterate
- Mark complete
- Move to next task

## Workflow Variations

### Starting from Vibe Session

User can have vibe conversation, then say "Generate spec"
- Kiro asks confirmation to start spec session
- Generates requirements based on vibe session context

### Importing Existing Requirements

**Option 1: MCP Integration**
- Connect to requirements tool with MCP server (STDIO support)
- Import directly into spec session

**Option 2: Manual Import**
1. Copy existing requirements (e.g., foo-prfaq.md) into repo
2. Open spec chat session
3. Say: `#foo-prfaq.md Generate a spec from it`
4. Kiro reads requirements and generates requirement and design specs

### Updating Specifications

**Update Requirements**:
- Modify requirements.md directly, OR
- Initiate spec session and instruct Kiro to add new requirements

**Update Design**:
- Navigate to design.md
- Select "Refine"
- Updates both design documentation and task list

**Update Tasks**:
- Navigate to tasks.md
- Choose "Update tasks"
- Creates new tasks mapping to new requirements

## Multi-Team Collaboration

### Sharing Across Teams

**Approach 1: Central Specs Repository**
- Dedicated repository for shared specifications
- Multiple projects reference it

**Approach 2: Git Submodules**
- Link central specs to individual projects
- Or use package references or symbolic links

**Best Practices**:
- Cross-repository workflows for proposing/reviewing shared specs
- Processes for updates affecting multiple projects

### Multiple Specs in Single Repo

No limit on number of specs per repo

**Recommendation**: Multiple specs for different features rather than single spec for entire codebase

## Integration with Steering

Specs work in conjunction with steering files:

1. **Steering files** (generated once, updated occasionally):
   - Provide persistent project context
   - Included in every interaction
   - Guide overall approach

2. **Spec files** (created per feature):
   - Feature-specific requirements, design, tasks
   - Referenced during implementation
   - Updated as feature evolves

**Workflow**:
1. Generate steering files first: "Set up steering for this project"
   - Creates product.md, tech.md, structure.md
2. Create spec for feature: "I want to build [feature]"
   - Kiro uses steering context to generate appropriate spec
3. Spec respects steering guidelines throughout

## Custom Steering for Specs

Can modify Kiro's spec behavior using steering files:

**Example**: `.kiro/steering/specs.md`
```yaml
---
inclusion: fileMatch
fileMatchPattern: "**/*.md"
---

# Spec Development Guidelines

When generating task lists:
- Always write tests first before writing code (TDD approach)
- Include performance considerations for each task
- Add security review as separate task
```

**Use Cases**:
- Enforce TDD vs tests-last approach
- Require specific documentation standards
- Add custom review steps
- Include organization-specific compliance checks

## Metrics and Usage

From pricing documentation:

**Spec Request**: Executing a single task from tasks.md
- Starting task directly = 1 spec request
- Executing subtask = 1 spec request per subtask + 1 vibe for coordination

**Vibe Request**: Any operation not involving spec task execution
- Creating/refining spec documents = minimum 1 vibe request
- Chat interactions = 1 vibe request
- Complex prompts may use multiple vibe requests

**Cost Efficiency**: Single spec request often accomplishes what would require multiple vibe requests, because planning is externalized.

## Success Patterns

From documentation and blog posts:

### Pattern 1: Catch Problems Early
- Ambiguities identified upfront
- Prevents costly rewrites
- Alignment before coding begins

### Pattern 2: Stay in Control
- Natural pause points for human review
- Modify and approve before implementation
- No surprise decisions

### Pattern 3: Context Optimization
- Planning externalized to files
- Active context focused on coding
- Higher quality code generation

### Pattern 4: Team Collaboration
- Specs as living documentation
- Standard development workflows
- Clear communication between product and engineering

### Pattern 5: Knowledge Preservation
- Decision trails maintained
- "Why" captured alongside "what"
- Future team members have context

## Comparison: Traditional vs Spec-Driven

| Aspect | Traditional AI Coding | Kiro Spec-Driven |
|--------|----------------------|------------------|
| Initial prompt | Jumps to code | Generates requirements |
| Requirements | Discovered during coding | Explicit upfront (EARS) |
| Context window | Cluttered with exploration | Optimized for coding |
| Design decisions | Inferred from conversation | Documented in design.md |
| Task breakdown | Ad-hoc | Structured with dependencies |
| Progress tracking | Unclear | Real-time status updates |
| Documentation | Afterthought | Integral to process |
| Iteration | Restart conversation | Update spec files |
| Team collaboration | Difficult | Git-based workflows |
| Knowledge retention | Lost in chat history | Preserved in specs |

## Key Takeaways for Implementation

1. **Adopt EARS Notation**: Transform all requirements into "WHEN...THE SYSTEM SHALL" format
2. **Enforce 3-Phase Approval**: Requirements → Design → Tasks with human checkpoints
3. **Externalize Planning**: Keep specifications in files, not in context
4. **Organize by Feature**: Multiple focused specs > single monolithic spec
5. **Version Control Everything**: Specs live alongside code in repo
6. **Bidirectional Sync**: Support both code→spec and spec→code updates
7. **Task-by-Task Execution**: Avoid "execute all" approach
8. **Use Steering Files**: Provide persistent project context
9. **Include Test Strategy**: Every task should specify testing requirements
10. **Preserve Decision Trail**: Document "why" not just "what"

## Questions for Further Research

1. How does Kiro detect which tasks are already implemented?
2. What constitutes "average complexity" for spec vs vibe requests?
3. How are sequence diagrams and data flow diagrams generated?
4. What format does tasks.md use for status tracking?
5. How do task dependencies get represented?
6. What triggers automatic spec updates vs manual?

## Source References

All information compiled from:
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/docs/specs/concepts.md`
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/docs/specs/best-practices.md`
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/docs/specs.md`
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/blog/from-chat-to-specs-deep-dive.md`
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/blog/introducing-kiro.md`
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/docs/guides/learn-by-playing/05-using-specs-for-complex-work.md`
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/docs/steering.md`
- `/home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/blog/understanding-kiro-pricing-specs-vibes-usage-tracking.md`

---

**Compiled**: 2025-10-02
**Research Focus**: Spec-Driven Development Methodology from Kiro Documentation
