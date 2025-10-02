# Extended Thinking Mode in Claude Code

## Overview

Extended thinking is a feature that gives Claude enhanced reasoning capabilities for complex tasks by allowing it to work through problems step-by-step before delivering final answers. The thinking process is visible to users, providing transparency into Claude's reasoning.

## How to Trigger Extended Thinking

### Interactive Mode

#### Tab Key Toggle
- Press **Tab** to toggle extended thinking on/off during a session
- Status indicator shows at bottom of terminal when thinking is enabled
- Toggle is temporary for the current session

#### Prompt Keywords
Extended thinking can be triggered naturally through prompts:

**Basic Thinking:**
- "think about..."
- "think through this..."
- "please think..."

**Deeper Thinking (Intensified):**
- "think harder"
- "think more"
- "think deeply"
- "think longer"
- "keep thinking"
- "think a lot"

### Permanent Configuration

Set the `MAX_THINKING_TOKENS` environment variable to enable thinking by default:

```bash
# In settings.json or environment
export MAX_THINKING_TOKENS=16000
```

Recommended starting budget: **1024-16000 tokens** (minimum: 1024)

### API Usage

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{
        "role": "user",
        "content": "Your complex question here"
    }]
)
```

## What Extended Thinking Provides

### Enhanced Capabilities

1. **Step-by-step reasoning** - Claude works through problems methodically
2. **Multiple approach exploration** - Can try different methods if first doesn't work
3. **Self-verification** - Claude can check and correct its own work
4. **Complex problem solving** - Better performance on:
   - STEM problems
   - Architectural decisions
   - Constraint optimization
   - Multi-step implementations
   - Code debugging

### Visible Thinking Process

- **In CLI**: Thinking appears as italic gray text above responses
- **In API**: Returns `thinking` content blocks before `text` blocks
- **Claude 4 models**: Returns summarized thinking (billed for full tokens)
- **Claude Sonnet 3.7**: Returns full thinking output

### Response Format

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me analyze this step by step...",
      "signature": "..."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

## When to Use for Planning

### Ideal Use Cases

#### 1. Complex Architectural Changes
```
> Think deeply about the best approach for implementing OAuth2
> authentication in our codebase. Consider security, scalability,
> and backward compatibility.
```

#### 2. Multi-step Feature Planning
```
> I need to refactor our authentication system. Think through:
> 1. Current implementation analysis
> 2. Migration strategy
> 3. Backward compatibility
> 4. Database schema changes
> 5. Testing approach
```

#### 3. Debugging Complex Issues
```
> Think about what could be causing this intermittent authentication
> failure. Consider race conditions, caching issues, and network timeouts.
```

#### 4. Code Review and Analysis
```
> Think carefully about potential security vulnerabilities in this
> authentication module. Look for edge cases and potential exploits.
```

#### 5. Optimization Planning
```
> Think through different approaches to optimize our database queries.
> Consider indexing, caching, and query restructuring.
```

### Planning Workflows

**Use Plan Mode + Extended Thinking together:**

```bash
# Start in Plan Mode with thinking enabled
claude --permission-mode plan

> Think deeply about our microservices architecture and suggest
> improvements. Create a detailed migration plan.
```

**Benefits of combining Plan Mode + Thinking:**
- Plan Mode restricts to read-only operations
- Extended thinking provides deep analysis
- Safe exploration before making changes
- Detailed planning with reasoning transparency

## Output Format and Behavior

### Thinking Display

**In Interactive Mode:**
- Thinking appears in italic gray text
- Shows before the final response
- Can be quite lengthy for complex problems

**Streaming:**
- Thinking streams in real-time via `thinking_delta` events
- May arrive in chunks rather than token-by-token
- Normal behavior for optimal performance

### Token Budgets

**Budget Tokens:**
- Minimum: 1024 tokens
- Recommended start: 1024-16000 tokens
- High complexity: Up to 32K tokens
- Above 32K: Use batch processing to avoid timeouts

**Important Notes:**
- Claude may not use entire budget
- You're billed for actual tokens used
- Budget can exceed max_tokens with interleaved thinking
- Summarized thinking (Claude 4) bills for full tokens generated

## Prompting Techniques for Spec Planning

### General vs. Specific Instructions

**Better: Start General**
```
> Please think about this math problem thoroughly and in great detail.
> Consider multiple approaches and show your complete reasoning.
> Try different methods if your first approach doesn't work.
```

**Avoid: Over-prescription (initially)**
```
> Think through this math problem step by step:
> 1. First, identify the variables
> 2. Then, set up the equation
> 3. Next, solve for x
> ...
```

**Strategy:** Start with general instructions, observe thinking, then provide specific guidance if needed.

### Self-Verification Prompting

```
> Write a function to calculate factorials. Before finishing,
> verify your solution with test cases for n=0, n=1, n=5, n=10.
> Fix any issues you find.
```

### Reflection and Checking

```
> After implementing the authentication flow, think about:
> - What edge cases might break this?
> - Are there security vulnerabilities?
> - What could go wrong during deployment?
```

### Multi-Framework Analysis

```
> Develop a strategy for entering the market. Think using:
> 1. Blue Ocean Strategy canvas
> 2. Porter's Five Forces analysis
> 3. SWOT analysis
> 4. Three Horizons framework
```

### Constraint Optimization

```
> Plan a system architecture with these constraints:
> - Must handle 10K requests/sec
> - 99.99% uptime requirement
> - Budget of $5000/month
> - Team of 3 developers
> - 6-month timeline
> - Must use existing PostgreSQL database
```

## Best Practices for Spec Planning

### 1. Define Context Clearly

```
> I'm working on a React e-commerce application. Think about
> the best state management approach for:
> - Shopping cart (persists across sessions)
> - User authentication (JWT tokens)
> - Product catalog (large dataset, needs caching)
> - Real-time inventory updates
```

### 2. Request Tradeoff Analysis

```
> Think through the tradeoffs between:
> 1. Monorepo vs multi-repo
> 2. SQL vs NoSQL for our use case
> 3. Server-side vs client-side rendering
> Provide detailed reasoning for each decision.
```

### 3. Ask for Multiple Approaches

```
> Think of 3 different approaches to implement real-time
> notifications. For each approach, analyze:
> - Complexity
> - Scalability
> - Cost
> - Maintenance burden
```

### 4. Sequential Planning

```
> Think through a phased implementation plan:
> Phase 1: What MVP features are essential?
> Phase 2: What can we add after validation?
> Phase 3: What are long-term enhancements?
> For each phase, consider timeline, resources, and risks.
```

## Technical Considerations

### Performance
- Thinking tokens have minimum budget of 1024
- Start with minimum and increase as needed
- Above 32K: use batch processing
- Long thinking can cause timeouts

### Language Support
- Extended thinking performs best in English
- Final outputs can be in any supported language
- Thinking internally may occur in English even for non-English prompts

### With Tool Use
- Supports `tool_choice: "auto"` or `"none"`
- Does NOT support forcing specific tools (`"any"` or `{"type": "tool", "name": "..."}`)
- Must pass thinking blocks back when providing tool results
- Supports interleaved thinking (Claude 4) with beta header

### Caching Impact
- Extended thinking impacts prompt caching efficiency
- Thinking blocks are dynamic and change between requests
- May reduce cache hit rates

## Supported Models

**Claude 4 Family (Summarized Thinking):**
- Claude Opus 4.1 (`claude-opus-4-1-20250805`)
- Claude Opus 4 (`claude-opus-4-20250514`)
- Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`)

**Note:** Claude Sonnet 3.7 returns full thinking output; Claude 4 models return summarized thinking.

## Common Pitfalls to Avoid

1. **Don't pass thinking back in user messages** - This degrades performance
2. **Don't prefill thinking blocks** - Not allowed, will cause errors
3. **Don't use for simple tasks** - Wastes tokens and time
4. **Don't ignore the thinking output** - Use it to understand and refine Claude's approach
5. **Don't use overly large budgets initially** - Start small, increase as needed

## Example: Planning a Feature Implementation

```bash
# Start Claude in Plan Mode
claude --permission-mode plan

# Use extended thinking for comprehensive planning
> Think deeply about implementing a real-time collaboration feature
> for our document editor. Consider:
>
> 1. Architecture (WebSocket vs. SSE vs. polling)
> 2. Conflict resolution (OT vs. CRDT)
> 3. Data persistence and synchronization
> 4. Scalability (10 vs. 1000 concurrent users)
> 5. Security (authentication, authorization)
> 6. Offline support and reconnection
> 7. Performance optimization
> 8. Testing strategy
>
> Create a detailed implementation plan with phases, risks,
> and technical decisions explained.
```

Claude will:
1. Analyze current codebase structure
2. Think through each consideration systematically
3. Explore tradeoffs between approaches
4. Provide phased implementation plan
5. Explain reasoning for technical decisions
6. Identify risks and mitigation strategies

You can then refine:
```
> Think more about the conflict resolution approach.
> Compare Operational Transformation vs. CRDTs in detail
> for our specific use case.
```

## Resources

- **Extended Thinking Guide**: `/docs/build-with-claude/extended-thinking`
- **Extended Thinking Tips**: `/docs/build-with-claude/prompt-engineering/extended-thinking-tips`
- **Models Overview**: `/docs/about-claude/models/overview`
- **Cookbook Examples**: `https://github.com/anthropics/anthropic-cookbook/tree/main/extended_thinking`
