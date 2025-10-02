# Feature: GitHub Pages Marketing Site for Claude Kiro

## Overview

Create a GitHub Pages website in the `docs/` directory that introduces Claude Kiro - a spec-driven development methodology for Claude Code. The site will adapt Kiro IDE's marketing structure and messaging to promote the configuration-based approach, emphasizing how Claude Code primitives (output styles, slash commands, hooks) can replicate Kiro's proven spec-driven workflow without requiring external tools.

**Files to create:**
- `docs/index.html` - Main marketing page (~39KB)
- `docs/ghost-icon.svg` - Kiro ghost logo (~1.5KB)
- `docs/purple-line-art.svg` - Decorative background (~2KB)
- `docs/gray-line-art.svg` - Alternative decoration (~2KB)
- `docs/install.sh` - Installation script (~3KB)

**Target Audience:** Developers using Claude Code who want structured, production-ready development workflow

**Key Message:** Get Kiro's spec-driven development methodology using pure Claude Code configuration - no custom IDE needed

## User Stories

### Story 1: Landing Page Hero Section
**As a** developer visiting the site
**I want** to immediately understand what Claude Kiro offers
**So that** I can decide if this methodology fits my development needs

**Acceptance Criteria (EARS notation):**
- WHEN a user visits docs/index.html, THE SYSTEM SHALL display a hero section with headline "Spec-Driven Development for Claude Code"
- WHEN a user reads the hero section, THE SYSTEM SHALL present the value proposition: "Bring Kiro's proven methodology to Claude Code using output styles, slash commands, and hooks"
- WHEN a user views the hero, THE SYSTEM SHALL include a clickable install command: `curl -sSL https://angelsen.github.io/claude-kiro/install.sh | bash`
- WHEN a user clicks the install command, THE SYSTEM SHALL copy it to clipboard with visual feedback
- WHEN a user sees the pitch, THE SYSTEM SHALL display 3 animated badges: "92% Kiro Parity", "Zero Dependencies", "Instant Setup"
- WHEN the page loads, THE SYSTEM SHALL use enhanced visual hierarchy with glass-morphism and gradient effects

### Story 2: Feature Showcase Section
**As a** developer evaluating Claude Kiro
**I want** to see the key capabilities and how they map to Kiro IDE
**So that** I can understand what I'm getting without the IDE

**Acceptance Criteria (EARS notation):**
- WHEN a user scrolls to the features section, THE SYSTEM SHALL display 4 primary features adapted from Kiro's messaging:
  - "Structured Requirements with EARS Notation" (replaces "Tame complexity with spec-driven development")
  - "Automated Task Tracking with TodoWrite" (replaces "Automate tasks with agent hooks")
  - "Pure Configuration, No Custom Code" (replaces "Built for agents")
  - "92% Feature Parity with Kiro IDE" (unique to Claude Kiro)
- WHEN a user views each feature, THE SYSTEM SHALL include a brief description (2-3 sentences) explaining the capability
- WHEN the features are presented, THE SYSTEM SHALL use a grid/card layout similar to Kiro's secondary features
- WHEN a user sees feature descriptions, THE SYSTEM SHALL replace "Kiro IDE" references with "Claude Code" and "Download" with "GitHub repository"

### Story 3: ~~Social Proof / Testimonials Section~~ REMOVED
**Status:** ❌ NOT IMPLEMENTED - Section removed per user request

~~**As a** potential user~~
~~**I want** to see evidence that this approach works~~
~~**So that** I can trust the methodology~~

**Note:** This section was removed from the implementation to streamline the page

### Story 4: "How It Works" Section
**As a** developer new to spec-driven development
**I want** to understand the workflow
**So that** I can visualize how I would use it

**Acceptance Criteria (EARS notation):**
- WHEN a user views the "How It Works" section, THE SYSTEM SHALL display the 3-phase workflow:
  1. "Create Spec with /spec-create" - Requirements → Design → Tasks
  2. "Track Progress with TodoWrite" - Native task tracking
  3. "Implement with /spec-implement" - Task-by-task execution
- WHEN each phase is shown, THE SYSTEM SHALL include a brief description and example
- WHEN the workflow is presented, THE SYSTEM SHALL use numbered steps or visual progression
- WHEN a user sees phase descriptions, THE SYSTEM SHALL emphasize the approval gates between phases

### Story 5: "Everything You Need" Grid
**As a** user exploring the offering
**I want** to see secondary features and benefits
**So that** I can understand the complete capability set

**Acceptance Criteria (EARS notation):**
- WHEN a user scrolls to the secondary features, THE SYSTEM SHALL display a grid of 6 cards adapted from Kiro's "Everything you need" section:
  - "EARS Notation for Testable Requirements"
  - "TodoWrite Integration for Task Tracking"
  - "Thinking Mode for Deep Planning"
  - "ExitPlanMode for Approval Gates"
  - "Hooks for Automation" (Phase 2)
  - "Pure Configuration Files"
- WHEN each card is displayed, THE SYSTEM SHALL include a 2-3 sentence description
- WHEN the grid is shown on mobile, THE SYSTEM SHALL stack cards vertically
- WHEN the grid is shown on desktop, THE SYSTEM SHALL use 3-column layout

### Story 6: Call-to-Action Section
**As a** user ready to try Claude Kiro
**I want** clear next steps
**So that** I can get started quickly

**Acceptance Criteria (EARS notation):**
- WHEN a user reaches the CTA section, THE SYSTEM SHALL display "Get Started for Free" heading
- WHEN the CTA is shown, THE SYSTEM SHALL include a prominent button linking to GitHub repository
- WHEN a user views the CTA, THE SYSTEM SHALL communicate that setup takes "4-6 hours for 5 config files"
- WHEN the section is displayed, THE SYSTEM SHALL use a highlighted background box (matching Kiro's pattern)
- WHEN a user clicks the CTA button, THE SYSTEM SHALL navigate to the GitHub repo (new tab)

### Story 7: Footer with Project Context
**As a** user
**I want** to find additional resources and context
**So that** I can learn more or contribute

**Acceptance Criteria (EARS notation):**
- WHEN a user scrolls to the footer, THE SYSTEM SHALL display links to:
  - GitHub Repository
  - VISION.md (project vision)
  - Phase 1 Implementation Guide
  - Research Documentation
- WHEN the footer is shown, THE SYSTEM SHALL include project attribution: "Built for developers who want structure without sacrificing speed"
- WHEN links are displayed, THE SYSTEM SHALL open GitHub links in new tab
- WHEN the footer is rendered, THE SYSTEM SHALL use simple text layout (not complex navigation)

## Non-Functional Requirements

### Performance
- WHEN the page loads, THE SYSTEM SHALL render initial content within 2 seconds on 3G connection
- WHEN images are used, THE SYSTEM SHALL use inline SVG or optimized images (<100KB total)
- WHEN CSS is included, THE SYSTEM SHALL use inline styles to eliminate additional HTTP requests

### Accessibility
- WHEN a screen reader is used, THE SYSTEM SHALL provide descriptive alt text for all images
- WHEN keyboard navigation is used, THE SYSTEM SHALL support tab navigation through all interactive elements
- WHEN color contrast is checked, THE SYSTEM SHALL meet WCAG 2.1 AA standards (4.5:1 for normal text)
- WHEN headings are used, THE SYSTEM SHALL follow proper semantic hierarchy (h1 → h2 → h3)

### Responsive Design
- WHEN viewed on mobile (320px-768px), THE SYSTEM SHALL stack content vertically and use full-width elements
- WHEN viewed on tablet (768px-1024px), THE SYSTEM SHALL use 2-column layout where appropriate
- WHEN viewed on desktop (1024px+), THE SYSTEM SHALL use full grid layouts and optimal line length (60-80 characters)
- WHEN viewport size changes, THE SYSTEM SHALL adapt layout without horizontal scroll

### Visual Design
- WHEN the page is rendered, THE SYSTEM SHALL use a dark theme matching Kiro's aesthetic (dark background, light text)
- WHEN typography is displayed, THE SYSTEM SHALL use system font stack for performance: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif`
- WHEN purple accents are used (matching Kiro), THE SYSTEM SHALL use consistent purple shade: `#A855F7` (purple-500)
- WHEN spacing is applied, THE SYSTEM SHALL use consistent vertical rhythm (multiples of 8px or 1rem)

### Content Adaptation
- WHEN Kiro content is adapted, THE SYSTEM SHALL preserve the intent and structure while updating terminology
- WHEN terminology is changed, THE SYSTEM SHALL replace:
  - "Kiro IDE" → "Claude Code with Spec-Driven Config"
  - "Download Kiro" → "Get Started on GitHub"
  - "Kiro helps you" → "This methodology helps you"
  - "agentic IDE" → "structured AI coding workflow"

## Constraints

### Technical Constraints
- Must be deployable as `docs/` folder for GitHub Pages
- Must use inline CSS in index.html (no external stylesheets)
- SVG assets must be separate files (ghost-icon.svg, line art SVGs)
- Must not require build process or JavaScript frameworks
- Minimal JavaScript allowed for UX enhancements (copy-to-clipboard)
- Must work with GitHub Pages default hosting (no server-side processing)
- Total size should be under 150KB for fast loading (4 files combined)

### Content Constraints
- Must source testimonials and messaging from existing Kiro scraped content
- Must accurately represent Claude Code capabilities (no false claims)
- Must link to actual GitHub repository and existing documentation files
- Must maintain Kiro's professional tone while adapting to configuration-based approach

### Timeline Constraints
- Should be implementable in single session (2-4 hours)
- Must be ready for immediate GitHub Pages deployment
- No iterative design process - adapt proven Kiro structure directly

## Out of Scope

The following are explicitly **NOT** included in this feature:

- **Multi-page site structure** - This is a single landing page, not a full documentation site
- **Interactive demos or code playgrounds** - Static content only
- **Blog or changelog section** - Focus on marketing the methodology
- **User analytics or tracking** - No tracking, cookies, or data collection
- **Dynamic content or API integration** - Fully static HTML + SVGs
- **Custom illustrations** - Use Kiro's actual ghost icon and line art SVGs
- **Video or animated content** - SVG graphics and CSS animations only
- **Email capture or waitlist** - Link to GitHub, not collecting user data
- **Pricing information** - This is a free, open-source methodology
- **Search functionality** - Single page doesn't require search
- **Internationalization** - English only for initial version
- **Dark/light mode toggle** - Dark theme only (matching Kiro)
- **Inline SVG code** - Use separate .svg files, not embedded SVG markup
- **Heavy JavaScript** - Only minimal JS for copy-to-clipboard (19 lines)

## Success Metrics

This feature will be considered successful when:

1. **Content Fidelity:** All implemented user stories (6 of 7) meet acceptance criteria
2. **Visual Consistency:** Page uses Kiro's visual hierarchy with enhanced glass-morphism effects
3. **Performance:** Page loads in <2s and achieves Lighthouse score >90
4. **Responsiveness:** Layout adapts correctly on mobile (375px), tablet (768px), and desktop (1440px)
5. **Accessibility:** Meets WCAG 2.1 AA standards (verified with axe DevTools or similar)
6. **Deployment Ready:** All 5 files can be committed to docs/ folder and immediately hosted on GitHub Pages
7. **Assets Working:** Ghost icon displays in header, SVGs load without errors, install.sh accessible via GitHub Pages
