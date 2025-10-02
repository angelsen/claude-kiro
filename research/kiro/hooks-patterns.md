# Kiro Agent Hooks - Research Documentation

## Overview

Kiro Agent Hooks are powerful automation tools that execute predefined AI agent actions when specific events occur in your IDE. Unlike traditional hooks that execute shell commands, Kiro hooks leverage natural language prompts to trigger intelligent, context-aware agent actions.

**Key difference from Claude Code hooks:** Kiro hooks use AI agent prompts instead of shell commands, making them more accessible and context-aware.

## What Are Agent Hooks?

Agent Hooks are automated triggers that execute predefined agent actions when specific events occur. They eliminate the need to manually request routine tasks and ensure consistency across your codebase.

### How Agent Hooks Work

The system follows a three-step process:

1. **Event Detection**: The system monitors for specific events in your IDE
2. **Prompt Execution**: When an event occurs, a predefined prompt is sent to the agent
3. **Automated Action**: The agent processes the prompt and performs the requested actions

## Hook Types

Kiro supports 4 different trigger types:

### 1. On File Create

**When it triggers:** When new files matching specific patterns are created in your workspace.

**Use Cases:**
- Generate boilerplate code for new components
- Add license headers to new files
- Set up test files when creating implementation files
- Initialize configuration files

**Example: React Component Setup**

```
When a new React component file is created, add:
1. Import statements for React and necessary hooks
2. A functional component with TypeScript props interface
3. Export statement
4. Basic styling if applicable
5. A skeleton test file in the appropriate directory
```

### 2. On File Save

**When it triggers:** When files matching specific patterns are saved.

**Use Cases:**
- Run linting and formatting
- Update related files
- Generate documentation
- Run tests for changed files
- Synchronize translations
- Update API documentation

**Example: Update Test Coverage**

```
When a JavaScript/TypeScript file is saved:
1. Identify the corresponding test file
2. Update tests to maintain coverage for any new functions
3. Run the tests to verify they pass
4. Update any snapshots if necessary
```

### 3. On File Delete

**When it triggers:** When files matching specific patterns are deleted.

**Use Cases:**
- Clean up related files
- Update import references in other files
- Maintain project integrity
- Remove test files
- Update index files

**Example: Clean Up References**

```
When a component file is deleted:
1. Find all imports of this component across the codebase
2. Remove or comment out those import statements
3. Suggest replacements if appropriate
```

### 4. Manual Trigger

**When it triggers:** When you explicitly execute the hook.

**Use Cases:**
- On-demand code reviews
- Documentation generation
- Security scanning
- Performance optimization
- Comprehensive analysis

**Example: Code Review Button**

```
Review the current file for:
1. Code quality issues
2. Potential bugs
3. Performance optimizations
4. Security vulnerabilities
5. Accessibility concerns
```

## Hook Configuration

### Configuration File Format

Hooks are stored in `.kiro/hooks/` directory with `.kiro.hook` extension.

```json
{
  "name": "Hook Name",
  "description": "Description of what this hook does",
  "version": "1",
  "when": {
    "type": "fileCreated" | "fileEdited" | "fileDeleted" | "userTriggered",
    "patterns": [
      "glob/pattern/**/*.ts"
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Natural language instructions for the agent"
  }
}
```

### Configuration Options

#### General Options

- **name**: Human-readable name of the hook
- **description**: Explanation of the hook's purpose
- **version**: Hook configuration version (currently "1")

#### Trigger Options (when)

- **type**: The event type
  - `fileCreated`: Monitor file creation
  - `fileEdited`: Monitor file modifications
  - `fileDeleted`: Handle file deletion events
  - `userTriggered`: Manual execution
- **patterns**: Array of glob patterns for file matching
  - Supports standard glob syntax
  - Can exclude patterns with `!` prefix
  - Examples: `**/*.ts`, `!**/*.test.ts`, `!**/node_modules/**`

#### Action Options (then)

- **type**: Currently only `askAgent` is supported
- **prompt**: Natural language instructions for what the agent should do
  - Can be multi-line
  - Should be specific and actionable
  - Can reference project conventions
  - Can include numbered steps

## Setting Up Agent Hooks

### Method 1: Using the Explorer View

1. Navigate to the Agent Hooks section in the Kiro panel
2. Click the + button to create a new hook
3. Define the hook workflow using natural language in the input field
4. Press Enter or click Submit to proceed
5. Configure the hook settings and save

### Method 2: Using the Command Palette

1. Open the command palette with Cmd + Shift + P (Mac) or Ctrl + Shift + P (Windows/Linux)
2. Type `Kiro: Open Kiro Hook UI`
3. Follow the on-screen instructions to create your hook

### Method 3: Manual File Creation

1. Create a `.kiro.hook` file in the `.kiro/hooks/` directory
2. Define the hook configuration in JSON format
3. The hook will automatically appear in the Kiro panel

## Hook Management

### Enable/Disable Hooks

Toggle hooks on/off without deleting them:
- **Quick toggle**: Click the eye icon next to any hook in the Agent Hooks panel
- **From hook view**: Select a hook and use the Hook Enabled switch in the top-right corner

### Edit Existing Hooks

1. Select your hook in the Agent Hooks panel
2. Modify settings like triggers, file patterns, instructions, or descriptions
3. Updates apply immediately

### Delete Hooks

1. Select the hook in the Agent Hooks panel
2. Click Delete Hook located at the bottom view
3. Confirm deletion (this action cannot be undone)

### Run Manual Trigger Hooks

Execute a manual trigger hook using:
- **Quick run**: Click the play button (▷) next to the hook name
- **From hook view**: Select the hook and click Start Hook in the top-right corner

### Viewing Hook Execution

- Click the "Task list" button at the top of chat panel
- Click on an active "Current Task" to view live execution
- Click the "History" button to view completed hook executions

## Practical Examples

### Example 1: Security Pre-Commit Scanner

**Trigger Type:** File Save
**Target:** `**/*`

```
Review changed files for potential security issues:
1. Look for API keys, tokens, or credentials in source code
2. Check for private keys or sensitive credentials
3. Scan for encryption keys or certificates
4. Identify authentication tokens or session IDs
5. Flag passwords or secrets in configuration files
6. Detect IP addresses containing sensitive data
7. Find hardcoded internal URLs
8. Spot database connection credentials

For each issue found:
1. Highlight the specific security risk
2. Suggest a secure alternative approach
3. Recommend security best practices
```

### Example 2: Internationalization Helper

**Trigger Type:** File Save
**Target:** `src/locales/en/*.json`

```
When an English locale file is updated:
1. Identify which string keys were added or modified
2. Check all other language files for these keys
3. For missing keys, add them with a "NEEDS_TRANSLATION" marker
4. For modified keys, mark them as "NEEDS_REVIEW"
5. Generate a summary of changes needed across all languages
```

### Example 3: Documentation Generator

**Trigger Type:** Manual Trigger

```
Generate comprehensive documentation for the current file:
1. Extract function and class signatures
2. Document parameters and return types
3. Provide usage examples based on existing code
4. Update the README.md with any new exports
5. Ensure documentation follows project standards
```

### Example 4: Test Coverage Maintainer

**Trigger Type:** File Save
**Target:** `src/**/*.{js,ts,jsx,tsx}`

```
When a source file is modified:
1. Identify new or modified functions and methods
2. Check if corresponding tests exist and cover the changes
3. If coverage is missing, generate test cases for the new code
4. Run the tests to verify they pass
5. Update coverage reports
```

### Example 5: TypeScript Test Updater

**Trigger Type:** File Save
**Target:** `**/*.ts`, `!**/*.test.ts`, `!**/*.spec.ts`, `!**/node_modules/**`

```json
{
  "name": "TypeScript Test Updater",
  "description": "Monitors changes to TypeScript source files and updates corresponding test files",
  "version": "1",
  "when": {
    "type": "fileEdited",
    "patterns": [
      "**/*.ts",
      "!**/*.test.ts",
      "!**/*.spec.ts",
      "!**/node_modules/**"
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "I noticed you've edited a TypeScript file. I'll analyze the changes and update the corresponding test file.\n1. First, I'll identify any new functions or methods added to the source file\n2. Then I'll locate or create the corresponding test file (either .test.ts or .spec.ts in the same directory)\n3. I'll generate appropriate test cases for the new functions/methods\n4. I'll ensure the tests follow the project's existing testing patterns and conventions\n\nHere are my suggested test updates based on your changes:"
  }
}
```

### Example 6: Image Asset Indexer

**Trigger Type:** File Create
**Target:** `client/src/assets/*.{png,jpg,jpeg,gif,svg}`

```json
{
  "name": "Image Asset Indexer",
  "description": "Automatically adds references to newly added image files to the index.ts file",
  "version": "1",
  "when": {
    "type": "fileCreated",
    "patterns": [
      "client/src/assets/*.png",
      "client/src/assets/*.jpg",
      "client/src/assets/*.jpeg",
      "client/src/assets/*.gif",
      "client/src/assets/*.svg"
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A new image file has been added to the assets folder. Please update the index.ts file in the assets folder to include a reference to this new image. First, check the current structure of the index.ts file to understand how images are referenced. Then add an appropriate export statement for the new image file following the existing pattern. Make sure to maintain alphabetical order if that's the current convention."
  }
}
```

### Example 7: Image Asset Remover

**Trigger Type:** File Delete
**Target:** `client/src/assets/*.{png,jpg,jpeg,gif,svg}`

```json
{
  "name": "Image Asset Remover",
  "description": "Automatically removes references to deleted image files from the index.ts file",
  "version": "1",
  "when": {
    "type": "fileDeleted",
    "patterns": [
      "client/src/assets/*.png",
      "client/src/assets/*.jpg",
      "client/src/assets/*.jpeg",
      "client/src/assets/*.gif",
      "client/src/assets/*.svg"
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "An image file has been removed from the assets folder. Please update the index.ts file in the assets folder to remove any references to this removed image."
  }
}
```

### Example 8: Python Test Generator

**Trigger Type:** File Save
**Target:** `*.py`, `!test_*.py`

```
You are a test-driven development assistant. The user has modified a Python source file. Your task is to:
1. Analyze the changes in the source file
2. Identify any new functions, methods, or classes that were added
3. Update or create the corresponding test file (same filename but with test_ prefix)
4. Add appropriate test cases for the new functionality
5. Ensure test coverage for the new code while maintaining existing tests

Focus on writing practical, meaningful tests that verify the behavior of the new code. Use the existing testing patterns in the project if available. If using unit test, add new test methods to the appropriate test class. If using pytest, add new test functions.
```

### Example 9: Validate Figma Design (with MCP)

**Trigger Type:** File Save
**Target:** `*.css`, `*.html`

```
Use the Figma MCP to analyze the updated html or css files and check that they follow established design patterns in the figma design. Verify elements like hero sections, feature highlights, navigation elements, colors, and button placements align.
```

## Integration with MCP

Agent Hooks can be enhanced with Model Context Protocol (MCP) capabilities:

- **Access to External Tools**: Hooks can leverage MCP servers to access specialized tools and APIs
- **Enhanced Context**: MCP provides additional context for more intelligent hook actions
- **Domain-Specific Knowledge**: Specialized MCP servers can provide domain expertise

**To use MCP with hooks:**
1. Configure MCP servers in Kiro
2. Reference MCP tools in your hook instructions
3. Set appropriate auto-approval settings for frequently used tools

**Use Cases:**
- Validate designs against Figma design systems
- Update ticket status after task completion
- Sync databases from sample files
- Access external APIs for data validation
- Integrate with project management tools

## Best Practices

### Hook Design

#### Be Specific and Clear
- Write detailed, unambiguous instructions
- Focus on one specific task per hook
- Use numbered steps for complex operations
- Provide context about project conventions

#### Test Thoroughly
- Test hooks on sample files before deploying
- Verify hooks work with edge cases
- Start with limited file patterns before expanding
- Review hook output in the chat history

#### Monitor Performance
- Ensure hooks don't slow down your workflow
- Consider the frequency of trigger events
- Optimize prompts for efficiency
- Disable hooks that aren't actively needed

### Security Considerations

#### Validate Inputs
- Ensure hooks handle unexpected file content gracefully
- Consider potential edge cases in file formats
- Test with malformed or unexpected input
- Review hook actions before they execute

#### Limit Scope
- Target specific file types or directories when possible
- Use precise file patterns to avoid unnecessary executions
- Consider the impact of hooks on your entire codebase
- Use exclusion patterns (`!pattern`) to skip certain files

#### Review Regularly
- Update hook logic as your project evolves
- Remove hooks that are no longer needed
- Refine prompts based on actual results
- Monitor hook execution frequency

### Team Collaboration

#### Document Hooks
- Maintain clear documentation of hook purposes
- Include examples of expected behavior
- Document any limitations or edge cases
- Use descriptive names and descriptions

#### Share Configurations
- Store hook configurations in version control (`.kiro/hooks/`)
- Use consistent hooks across team members
- Create standard hooks for common team workflows
- Review team hooks during onboarding

#### Version Control Integration
- Commit `.kiro/hooks/` directory to git
- Consider hooks that integrate with your version control system
- Create hooks for code review workflows
- Use hooks to enforce team standards

### Writing Effective Prompts

#### Good vs Better Prompts

**Good:**
```
Update the test file to cover the new authentication method, including edge cases for invalid tokens and expired sessions
```

**Better:**
```
Review the authentication changes in this file and update tests/auth.test.js to include comprehensive tests for the new authentication method. Cover success cases, invalid token scenarios, expired session handling, and ensure all tests follow our existing test patterns using Jest and supertest.
```

#### Leverage Workspace Context

**Good:**
```
Update or create new test files to cover the new functions, make sure to include multiple tests for each function to cover different paths.
```

**Better:**
```
Update or create new test files to cover the new functions, make sure to include multiple tests for each function to cover different paths. Look at the existing unit tests and follow the same format and use the same testing libraries used, read the package.json file to understand how we initiate the unit tests.
```

## Troubleshooting

### Hook Not Triggering

- Verify the file pattern matches your target files
- Check that the hook is enabled (eye icon in panel)
- Ensure the event type is correct
- Test pattern matching with a simple file
- Check for conflicting exclusion patterns

### Unexpected Hook Behavior

- Review the hook instructions for clarity
- Check for conflicting hooks
- Verify file patterns aren't too broad
- Review the hook execution in chat history
- Test with a simpler version of the prompt

### Performance Issues

- Limit hook scope with more specific file patterns
- Simplify complex hook instructions
- Reduce the frequency of triggering events
- Disable hooks you're not actively using
- Use exclusion patterns to skip generated files

### Agent Not Understanding Instructions

- Make prompts more specific and detailed
- Break complex tasks into numbered steps
- Reference project conventions and standards
- Include examples in the prompt
- Test the prompt manually in chat first

## Key Benefits Over Traditional Hooks

1. **Natural Language Configuration**: Define hooks using plain English instead of complex scripting
2. **Context-Aware AI**: Hooks understand your codebase structure and make intelligent decisions
3. **Real-Time Execution**: Actions happen immediately as you work
4. **Collaborative**: Hooks can be shared through version control
5. **Customizable**: Tailor automation to your specific workflow and coding patterns
6. **No Shell Scripting Required**: Accessible to developers of all skill levels
7. **Intelligent Decision Making**: AI can adapt to different scenarios
8. **Project Context**: Hooks can read and understand project documentation

## Workflow Tips

### Start Simple
Begin with basic file-to-file relationships like updating tests when you change source code. You'll see the value right away and can build up to more complex workflows.

### Monitor and Iterate
Use your chat history to review hook performance and refine prompts based on results. The task list shows all hook executions.

### Pattern Library
Build a library of reusable patterns:
- Test synchronization
- Documentation updates
- Style enforcement
- Security scanning
- Import management

### Common File Patterns

```
**/*.ts                  # All TypeScript files
!**/*.test.ts           # Exclude test files
!**/node_modules/**     # Exclude dependencies
src/**/*.{js,jsx}       # All JS/JSX in src
**/*.py                 # All Python files
!test_*.py              # Exclude test files
client/src/assets/*     # Direct children only
docs/**/*.md            # All markdown in docs
```

## Getting Started Checklist

1. ✓ Open the Kiro panel and find Agent Hooks section
2. ✓ Create your first simple hook (e.g., log file saves)
3. ✓ Test the hook with a sample file
4. ✓ Review execution in chat history
5. ✓ Refine the prompt based on results
6. ✓ Add more sophisticated hooks as needed
7. ✓ Share useful hooks with your team
8. ✓ Commit `.kiro/hooks/` to version control

## Future of Automation

Kiro's agent hooks bring intelligent automation to daily development work, handling repetitive tasks so you can focus on creative problem-solving. The natural language configuration makes advanced automation accessible to developers of all experience levels. Simply describe what you need, and the AI-powered actions ensure automated changes are intelligent and contextually appropriate.
