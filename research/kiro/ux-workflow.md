# KIRO UX & Workflow Patterns Research

**Research Date:** 2025-10-02
**Source:** Local KIRO documentation from kiro.dev
**Purpose:** Understanding KIRO's user experience patterns for Claude Code implementation

---

## Executive Summary

KIRO represents a paradigm shift from "vibe coding" to **spec-driven development**, emphasizing **structure before implementation**. The UX is built around three core pillars:

1. **Specs** - Structured requirements → design → tasks workflow
2. **Steering** - Persistent project context that eliminates repetitive prompting
3. **Hooks** - Event-driven automation that acts like an "experienced developer watching over your shoulder"

The key insight: **KIRO treats the planning phase as a first-class citizen**, not overhead. This creates natural checkpoints for human review and keeps AI focused on implementation rather than requirements clarification.

---

## 1. User Journey: Creating Specifications

### Entry Points

Users can start specs through multiple natural entry points:
- **From chat**: Click "Spec" button during conversation
- **From Kiro panel**: Click `+` in Specs section
- **From vibe coding**: Say "Generate spec" to transition from exploratory chat

### The Three-Phase Workflow

#### Phase 1: Requirements Generation
**User Action:** Describe feature in natural language
**Example:** "Add a user authentication system with login, logout, and password reset functionality"

**KIRO Response:**
- Transforms vague prompt into structured user stories
- Uses EARS notation (Easy Approach to Requirements Syntax)
- Format: `WHEN [condition] THE SYSTEM SHALL [behavior]`
- Makes assumptions explicit and testable

**UX Pattern:**
- Requirements displayed in markdown format (`requirements.md`)
- User reviews and can edit directly
- Checkpoint: Must approve before proceeding to design

**Key Principle:** "The way you wish your PM would give you requirements"

#### Phase 2: Design Documentation
**KIRO Action:**
- Analyzes existing codebase
- Creates technical architecture matching current patterns
- Generates sequence diagrams, interfaces, data models
- Documents in `design.md`

**Content Includes:**
- Architecture decisions
- Data flow diagrams
- TypeScript interfaces / data models
- Error handling strategy
- Unit testing approach
- Integration points

**UX Pattern:**
- Preview button in upper-right for rendered view (shows diagrams properly)
- User can provide "detailed feedback" or say "LGTM" to proceed
- Code snippets shown as "pseudocode imagining the API"

**Key Principle:** "Eliminates lengthy back-and-forth on requirements clarity"

#### Phase 3: Task Planning
**KIRO Action:**
- Breaks work into discrete, trackable tasks
- Sequences tasks based on dependencies
- Links each task back to requirements
- Auto-includes: unit tests, integration tests, loading states, mobile responsiveness, accessibility

**Output:** `tasks.md` with:
- Clear task descriptions
- Expected outcomes
- Sub-tasks for granular tracking
- Dependencies mapped out

**UX Pattern:**
- Tasks shown with "Start Task" links
- Real-time status updates (pending → in progress → done)
- Can execute tasks one-by-one or all at once
- Progress indicator during execution

---

## 2. Task Execution Interface

### Visual Feedback Mechanisms

**Task Status Display:**
- **Pending** - Not started, shown with "Start Task" link
- **In Progress** - Currently executing, live indicator
- **Done** - Completed, with inline completion status

**Post-Execution:**
- View code diffs to audit work
- Access agent execution history
- Inline completion markers in task list

### Execution Modes

#### Autopilot Mode (Default)
- Agent works autonomously end-to-end
- Makes changes across multiple files
- Runs commands without step-by-step approval
- **User maintains control through:**
  - "View all changes" - comprehensive diff view
  - "Revert all" - undo all modifications
  - Interrupt execution - stop mid-task

#### Supervised Mode
- Agent applies changes then pauses for review
- User can accept, reject, or request adjustments
- Step-by-step visibility
- Best for: critical codebases, learning, unfamiliar code

**UX Toggle:**
- Simple switch in chat interface
- Can toggle between modes anytime
- Context-aware recommendations (e.g., "Use supervised for critical code")

### Progress Tracking

**Built-in mechanisms:**
- Task list with real-time updates
- Execution history panel
- Native OS notifications for:
  - Action required (needs approval)
  - Success (task completion)
  - Failure (errors encountered)

**History Features:**
- Search through past sessions
- Restore previous sessions
- Delete specific sessions
- View all actions: code changes, commands, searches, file ops

---

## 3. Steering Files: Persistent Context

### The Problem Solved
Traditional AI coding: "Explain your conventions in every chat"
KIRO's solution: "Write it once, KIRO remembers forever"

### Auto-Generated Foundation Files

**User Action:** Click "Generate Steering Docs" in Kiro panel

**KIRO Creates:**
1. **product.md** - Product purpose, users, features, business objectives
2. **tech.md** - Frameworks, libraries, tools, constraints
3. **structure.md** - File organization, naming conventions, architecture

**Storage:** `.kiro/steering/` (version controlled)

**Inclusion:** Automatically included in every interaction by default

### Custom Steering Files

**Creation Flow:**
1. Click `+` in Steering section
2. Choose descriptive name (e.g., `api-standards.md`)
3. Write guidance in natural language
4. Click "Refine" - KIRO formats it properly

### Inclusion Modes (YAML frontmatter)

```yaml
---
inclusion: always
---
```
**Always Included** - Core standards, tech preferences, security policies

```yaml
---
inclusion: fileMatch
fileMatchPattern: "components/**/*.tsx"
---
```
**Conditional** - Domain-specific rules loaded when working with matching files

```yaml
---
inclusion: manual
---
```
**Manual** - Reference with `#steering-file-name` in chat when needed

### File References
Link to live project files:
```markdown
#[[file:<relative_file_name>]]
```

**Examples:**
- `#[[file:api/openapi.yaml]]` - API specs
- `#[[file:components/ui/button.tsx]]` - Component patterns
- `#[[file:.env.example]]` - Config templates

### UX Benefits Highlighted by Users

**Quote:** "I was able to spend a lot less time thinking about prompt engineering, and more time just asking for what I wanted"

**Quote:** "In just four lines into a spec, Kiro was able to write user stories like a product manager and capture so many details that I didn't even need to mention"

---

## 4. Agent Hooks: Automated Workflows

### The Mental Model
"Like delegating tasks to a collaborator" / "An experienced developer catching things you miss"

### Hook Creation Flow

**Entry Points:**
- Agent Hooks section in Kiro panel → `+` button
- Command Palette: "Kiro: Open Kiro Hook UI"

**Creation Steps:**
1. Describe hook in natural language
2. OR select from templates
3. Review configuration:
   - Title and description
   - Event type (file saved/created/deleted/manual)
   - File patterns (glob support)
   - Instructions prompt

**Storage:** `.kiro/hooks/` as `***.kiro.hook` JSON files

### Hook Configuration Structure

```json
{
  "name": "TypeScript Test Updater",
  "description": "Monitors changes and updates test files",
  "version": "1",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/*.ts", "!**/*.test.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Analyze changes and update corresponding test file..."
  }
}
```

### Trigger Types
- **fileEdit** - Monitor file modifications
- **fileCreate** - Respond to new files
- **fileDelete** - Handle deletions
- **userTriggered** - Manual execution

### Management Interface

**Hook Panel Features:**
- Enable/disable hooks on demand
- Edit configurations in UI or directly in `.kiro/hooks/`
- Delete hooks
- View execution history

**Team Collaboration:**
- Hooks committed to version control
- Team pulls and uses instantly
- "Like having a shared cookbook of automation recipes"

### Common Use Cases

**From Documentation:**
- Test synchronization (update tests when code changes)
- Documentation updates (README sync with API changes)
- Internationalization (translate docs)
- Git assistance (changelog generation, commit messages)
- Compliance checks (standards validation)
- Style consistency (auto-formatting)

**Real User Example:**
"When I save a React component file, automatically create or update its corresponding test file"

**Power User Pattern:**
"Kiro's autonomous agents were game-changers. Every time we saved a file, agents would automatically generate unit tests, optimize performance, and update documentation. What used to take hours of manual work happened instantly in the background."

---

## 5. Chat & Context Management

### Smart Intent Detection

**Information Requests:**
- Questions like "How does this work?" or "What's the purpose?"
- KIRO responds with explanations
- No code modifications

**Action Requests:**
- Directives like "Create a component" or "Fix this bug"
- KIRO proposes/implements changes
- Executes commands, manages files

**UX Benefit:** "Seamless intent recognition without explicit mode switching"

### Context Providers (# symbol)

| Provider | Usage | Example |
|----------|-------|---------|
| `#codebase` | Auto-find relevant files | `#codebase explain authentication flow` |
| `#file` | Reference specific files | `#auth.ts explain this` |
| `#folder` | Include folder contents | `#components/ what components exist?` |
| `#git diff` | Current changes | `#git diff explain PR changes` |
| `#terminal` | Terminal output & history | `#terminal help fix build error` |
| `#problems` | Current file issues | `#problems resolve these` |
| `#url` | Web documentation | `#url:https://docs.api.com explain` |
| `#code` | Code snippets | `#code:const sum = (a,b) => a+b;` |
| `#repository` | Repo structure map | `#repository how is this organized?` |
| `#current` | Active file | `#current explain component` |
| `#steering` | Steering files | `#steering:coding-standards.md review` |
| `#mcp` | MCP tools | `#mcp:aws-docs configure S3` |

**Power Pattern:** Combine multiple providers
```
#codebase #auth.ts explain how authentication works with our database
```

### Session Management

**Features:**
- Create new sessions for different topics
- Switch between ongoing conversations via tabs
- View history through History button
- Track progress through Task list button
- Search/restore/delete sessions

**Execution History:**
- Detailed log of all actions
- Code changes, commands, searches, file ops
- Searchable and restorable

---

## 6. What Makes the Experience "Natural"

### 1. Progressive Disclosure
- Start simple (single prompt)
- Progressively reveal structure (requirements → design → tasks)
- Each phase builds on previous
- Natural checkpoints prevent premature commitment

### 2. Familiar Patterns
- Markdown for all artifacts (requirements.md, design.md, tasks.md)
- Version control friendly (commit specs with code)
- Code OSS foundation (VS Code compatible)
- Standard Git integration

### 3. Flexible Workflows
- Can start from vibe coding, transition to specs
- Can execute tasks individually or all at once
- Can switch between autopilot and supervised
- Can iterate: update specs → regenerate tasks

### 4. Context Preservation
- Steering files eliminate repetition
- Specs document decisions
- Task lists maintain focus
- History preserves learning

### 5. Feedback Loops
- LGTM checkpoints at each spec phase
- Preview buttons for visualizing designs
- Diff views for code review
- Revert capabilities for safety

---

## 7. Pain Points & Solutions

### Pain Point: "Vibe coding context overload"
**User Quote:** "You spend the next hour going back and forth, refining requirements, clarifying edge cases, and watching your context window fill up with exploratory conversations"

**KIRO Solution:**
- Separate requirements phase clears context
- Specs externalized to files, not conversation
- "Maximum context space available for actual coding task"

### Pain Point: "Losing track of decisions"
**User Quote:** "It's difficult to keep track of all the decisions that were made along the way"

**KIRO Solution:**
- Requirements.md documents all assumptions
- Design.md captures architectural choices
- Version controlled artifacts create audit trail
- "Every decision is documented, creating clear context for future team members"

### Pain Point: "AI jumps to code too quickly"
**User Quote:** "AI immediately jumps into code generation, often before fully understanding requirements"

**KIRO Solution:**
- Forced requirements phase before any code
- Design phase validates approach
- Tasks phase creates execution plan
- "Catch problems before they're expensive"

### Pain Point: "Repetitive explanation of standards"
**Traditional:** "Explain your conventions in every chat"

**KIRO Solution:**
- Steering files provide persistent context
- Auto-generated foundation docs
- File-match patterns for context-aware loading

### Pain Point: "Forgotten routine tasks"
**User Quote:** "I often forget to add unit tests, or update documentation when pushing changes"

**KIRO Solution:**
- Hooks automate repetitive tasks
- Event-driven triggers ensure consistency
- "Never having to think twice"

---

## 8. Success Stories & User Testimonials

### Velocity Improvements

**Quote (Håkon Eriksen Drange, Cloud Architect):**
"We've accelerated feature development dramatically, reducing time to customer value from weeks to days"

**Quote (Dakota Lewallen, Software Engineer):**
"Thanks to Kiro's spec-driven development, I was able to go from concept to working prototype in a single weekend"

### Quality Improvements

**Quote (Ihor Sasovets, Security Engineer):**
"In roughly two days, I built a secure file sharing application from scratch. By simply sharing my requirements with Kiro, I was able to create a fully secure application that incorporates encryption and various security coding practices—no additional prompts needed"

**Quote (Blake Romano, Senior Software Engineer):**
"Kiro comes equipped with all the best practices that I would put in my specs, and builds me the application I want, faster"

### Learning & Capability Expansion

**Quote (Danielle Heberling, Infrastructure Engineer):**
"Kiro lowers the barrier to entry, whether that be, you don't even know how to code, you're new to coding, or you're like me and you're just learning a new tech stack"

**Quote (Michael Walmsley, Serverless Architect):**
"As an open source developer, I typically don't build games, but last night I was able to create one using Kiro. I didn't have to think too hard about implementation since Kiro handled the logic"

### Process & Collaboration

**Quote (Kento Ikeda, Founder):**
"Kiro is a strong ally for startups. It naturally turns overlooked docs and specs into robust assets, making growth smoother and future scaling more effective"

**Quote (Farah Abdirahman, AI Engineer):**
"Most tools are great at generating code, but Kiro gives structure to the chaos before you write a single line"

---

## 9. Key UX Principles Extracted

### 1. Structure as Liberation, Not Constraint
- Specs aren't overhead; they're the "North Star to guide agent work"
- "Working backwards" from desired outcome
- Freedom to iterate at requirements level is faster than fixing code

### 2. Explicit Over Implicit
- EARS notation makes requirements testable
- Design docs show the "why" behind technical choices
- Task lists break complexity into manageable units
- "Make all requirements and constraints explicit"

### 3. Artifacts as First-Class Citizens
- Requirements, designs, tasks are version-controlled files
- Markdown format keeps them human-readable
- Living documentation that stays current
- "By writing down those details... changes AI development from vibe coding to real, durable collaboration"

### 4. Context as Configuration
- Steering files are "persistent knowledge"
- File-match patterns enable context-aware assistance
- Live file references keep steering current
- "More context, less repetition"

### 5. Automation with Oversight
- Hooks automate the routine
- Autopilot for speed, supervised for control
- Revert capabilities provide safety net
- Execution history enables learning

### 6. Natural Transitions
- Vibe → Spec transition ("Generate spec" command)
- Single-task → Multi-task (individual execution vs. "Execute all")
- Autopilot ↔ Supervised (toggle anytime)
- Manual → Automated (hooks for repeated patterns)

### 7. Progressive Trust Building
- Start with supervised mode for new users
- Graduate to autopilot as confidence grows
- Checkpoints at each spec phase
- "You stay in control, especially when running scripts or commands"

---

## 10. Lessons for Claude Code Implementation

### Core Workflow Insights

**1. Separate Planning from Execution**
- Create distinct "spec mode" vs "vibe mode"
- Force requirements articulation before coding
- Use structured formats (EARS-like notation)
- Make transitions explicit and user-controlled

**2. Persistent Context Mechanisms**
- Implement steering file equivalent
- Auto-generate project understanding docs
- Support conditional loading based on file patterns
- Version control friendly (markdown in .claude/)

**3. Task Decomposition Interface**
- Visual task list with status indicators
- Click-to-execute individual tasks
- Progress tracking with real-time updates
- Link tasks back to requirements for traceability

**4. Automation Through Hooks**
- Event-driven automation system
- Natural language hook configuration
- Shared via version control
- Enable/disable controls for user comfort

### UX Patterns to Adopt

**1. Checkpoint Approval Pattern**
- Requirements → user review → LGTM/feedback
- Design → user review → LGTM/feedback
- Tasks → user review → LGTM/feedback
- Creates natural pause points for human oversight

**2. Multi-Entry Point Pattern**
- Chat button for specs
- Panel `+` button
- Transition from vibe coding
- Reduces friction to structured workflow

**3. Diff-Based Review Pattern**
- "View all changes" comprehensive diff
- "Revert all" safety mechanism
- Individual change review in supervised mode
- Execution history for auditing

**4. Context Provider Pattern**
- Use `#` prefix for explicit context
- Support file, folder, codebase, terminal contexts
- Combine multiple providers in single prompt
- Make context visible/manageable

### Visual Feedback Best Practices

**1. Status Indicators**
- Clear pending/in-progress/done states
- Real-time updates during execution
- Completion markers inline with tasks
- OS-level notifications for background work

**2. Preview Capabilities**
- Render diagrams in design docs
- Show formatted markdown previews
- Diff views for code changes
- Before/after comparisons

**3. History & Audit Trail**
- Searchable execution history
- Restore previous sessions
- View all actions taken
- Document decision rationale

### Documentation Strategy

**1. Generate Project Understanding**
- Auto-create structure.md equivalent
- Auto-create tech.md equivalent
- Auto-create product.md equivalent
- Keep updated as project evolves

**2. Spec as Documentation**
- Requirements.md captures user stories
- Design.md explains architecture
- Tasks.md shows implementation plan
- Commit with code for context preservation

**3. Living Documentation**
- File references link to actual code
- Updates propagate automatically
- Version controlled with implementation
- Serves as onboarding material

### Error Handling & Safety

**1. Revert Capabilities**
- All changes revertable before commit
- Clear "undo" mechanism
- Interrupt execution option
- Non-destructive by default

**2. Incremental Commitment**
- Review before proceeding to next phase
- Task-by-task execution available
- Supervised mode for critical work
- User always maintains control

**3. Notification System**
- Action required notifications
- Success confirmations
- Failure alerts
- Respect OS notification settings

---

## 11. Comparative Analysis: KIRO vs Traditional AI Coding

### Traditional Vibe Coding Pattern
1. User provides high-level prompt
2. AI immediately generates code
3. User says "actually, I meant..."
4. Back-and-forth refinement cycle
5. Context window fills with exploration
6. Limited space for final implementation
7. Decisions not documented

### KIRO Spec-Driven Pattern
1. User provides feature description
2. KIRO generates requirements (EARS notation)
3. User reviews/approves requirements
4. KIRO generates technical design
5. User reviews/approves design
6. KIRO generates task breakdown
7. User reviews/approves tasks
8. KIRO executes with full context
9. All decisions documented in version control

**Key Difference:** "Treats LLM as thinking partner throughout entire development lifecycle, not just code generator"

---

## 12. Implementation Priorities for Claude Code

### Phase 1: Core Spec Workflow (MVP)
**Must Have:**
- [ ] Spec creation command (transition from chat)
- [ ] Three-file structure: requirements.md, design.md, tasks.md
- [ ] Sequential workflow with approval checkpoints
- [ ] Basic task execution interface
- [ ] Status tracking (pending/in-progress/done)

**Why First:** Establishes fundamental paradigm shift from vibe to structured

### Phase 2: Context Management
**Must Have:**
- [ ] Steering files support (.claude/steering/)
- [ ] Auto-generation of structure/tech/product docs
- [ ] Always-included by default
- [ ] File reference syntax support
- [ ] Context provider enhancements (#file, #folder, etc.)

**Why Second:** Reduces repetitive prompting, improves code quality

### Phase 3: Visual Feedback & Control
**Must Have:**
- [ ] Diff view for changes
- [ ] Revert all capability
- [ ] Execution history viewer
- [ ] Progress indicators
- [ ] Autopilot vs supervised toggle

**Why Third:** Enhances user confidence and control

### Phase 4: Automation
**Should Have:**
- [ ] Hook system (event-driven automation)
- [ ] Natural language hook configuration
- [ ] Enable/disable controls
- [ ] Execution history for hooks

**Why Fourth:** Powerful but not essential for core workflow

### Phase 5: Polish & Integration
**Nice to Have:**
- [ ] OS-level notifications
- [ ] Session restore functionality
- [ ] Advanced search in history
- [ ] Template system for common specs/hooks
- [ ] MCP integration for external tools

**Why Last:** Refinements that enhance existing workflows

---

## Conclusion

KIRO's UX success stems from treating **structure as a feature, not a bug**. By forcing articulation of requirements before implementation, it:

1. **Prevents premature commitment** - "Catch problems before they're expensive"
2. **Preserves decisions** - "Every decision documented, creating clear audit trail"
3. **Maximizes AI effectiveness** - "Maximum context space for actual coding task"
4. **Enables team collaboration** - "Living documentation that stays current"
5. **Builds confidence** - "You stay in control, especially when running scripts"

For Claude Code, the core lesson is: **Make planning visible, valuable, and version-controlled**. Users will initially resist the "overhead" but quickly discover it's their competitive advantage.

The path forward:
1. Start with spec workflow (requirements → design → tasks)
2. Add persistent context (steering files)
3. Layer on visual feedback (diffs, history, status)
4. Gradually introduce automation (hooks)
5. Continuously refine based on user feedback

**Key Metric of Success:** Users saying "I don't know how I worked without specs before" - indicating the paradigm shift has stuck.

---

**Research compiled from:**
- /home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/docs/
- /home/fredrik/Projects/Python/project-autumn-25/claude-kiro/resources/scraped/kiro.dev/blog/
- Focus on UX patterns, user workflows, feedback mechanisms, and success stories
