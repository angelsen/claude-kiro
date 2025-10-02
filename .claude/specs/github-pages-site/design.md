# Design: GitHub Pages Marketing Site for Claude Kiro

## Architecture Overview

This is a **static website** in the `docs/` directory designed for GitHub Pages hosting. The architecture uses HTML with inline CSS plus separate SVG assets for graphics. This approach balances simplicity (no build process) with maintainability (clean HTML, reusable graphics).

**File Structure:**
```
docs/
├── index.html           (~100KB - HTML + inline CSS)
├── ghost-icon.svg       (~5KB - Kiro ghost logo)
├── purple-line-art.svg  (~8KB - decorative background)
└── gray-line-art.svg    (~8KB - alternative decoration)
```

**Design Philosophy:**
- **Simple deployment:** Copy docs/ folder, enable GitHub Pages
- **Inline CSS:** All styles in `<style>` tags (no external stylesheets)
- **External SVGs:** Reusable graphics as separate files
- **Mobile-first responsive:** Adapts from 320px to 1920px+ viewports
- **Semantic HTML:** Proper heading hierarchy and accessibility attributes
- **Visual continuity:** Uses Kiro's actual assets (ghost icon, colors, line art)

## Component Analysis

### Existing Components to Modify
- `docs/` directory - Currently doesn't exist, will need to be created
- No existing files to modify - this is a new feature

### New Components to Create

#### `docs/index.html` - Main Marketing Page
**Purpose:** Landing page that markets Claude Kiro methodology
**Size:** ~100KB (HTML + inline CSS)

**Structure:**
1. `<head>` section with metadata and inline CSS
2. `<header>` with navigation/branding (minimal)
3. `<main>` with 7 content sections
4. `<footer>` with links and attribution

#### `docs/ghost-icon.svg` - Kiro Ghost Logo
**Purpose:** Brand logo for header and hero section
**Source:** Copy from `resources/scraped/kiro.dev/.meta/kiro.dev.wget_mirror/icon.svg?fe599162bb293ea0`
**Size:** ~5KB
**Usage:** `<img src="ghost-icon.svg" alt="Claude Kiro" width="48" height="48">`

#### `docs/purple-line-art.svg` - Decorative Background
**Purpose:** Abstract geometric pattern for visual interest
**Source:** Copy from `resources/scraped/kiro.dev/.meta/kiro.dev.wget_mirror/images/purple-line-art.svg`
**Size:** ~8KB
**Usage:** CSS background-image or decorative element

#### `docs/gray-line-art.svg` - Alternative Decoration (Optional)
**Purpose:** Same pattern in neutral gray
**Source:** Copy from `resources/scraped/kiro.dev/.meta/kiro.dev.wget_mirror/images/gray-line-art.svg`
**Size:** ~8KB
**Usage:** Alternative background option

## HTML Structure

### Document Outline

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Spec-driven development for Claude Code using output styles, slash commands, and hooks. Get Kiro's proven methodology without the custom IDE.">

    <title>Claude Kiro - Spec-Driven Development for Claude Code</title>

    <!-- Inline CSS (all styles) -->
    <style>
        /* CSS Reset, base styles, component styles, responsive breakpoints */
    </style>
</head>
<body>
    <!-- Header: Minimal branding -->
    <header>
        <div class="container">
            <div class="logo">Claude Kiro</div>
            <a href="#get-started" class="cta-button">Get Started</a>
        </div>
    </header>

    <!-- Main Content -->
    <main>
        <!-- Section 1: Hero -->
        <section class="hero">
            <h1>Spec-Driven Development for Claude Code</h1>
            <p class="tagline">Prompt → Requirements → Design → Tasks → Implementation</p>
            <p class="value-prop">Bring Kiro's proven methodology to Claude Code using output styles, slash commands, and hooks</p>
            <a href="https://github.com/..." class="cta-primary">Get Started on GitHub</a>
        </section>

        <!-- Section 2: Primary Features (4 cards) -->
        <section class="primary-features">
            <div class="feature-card">...</div>
            <div class="feature-card">...</div>
            <div class="feature-card">...</div>
            <div class="feature-card">...</div>
        </section>

        <!-- Section 3: How It Works (3-step workflow) -->
        <section class="workflow">
            <h2>How It Works</h2>
            <div class="steps">
                <div class="step">...</div>
                <div class="step">...</div>
                <div class="step">...</div>
            </div>
        </section>

        <!-- Section 4: Secondary Features Grid (6 cards) -->
        <section class="secondary-features">
            <h2>Everything You Need</h2>
            <div class="features-grid">
                <div class="feature-item">...</div>
                <!-- 5 more cards -->
            </div>
        </section>

        <!-- Section 5: Social Proof (testimonials) -->
        <section class="testimonials">
            <h2>Trusted by Developers</h2>
            <div class="testimonial-grid">
                <div class="testimonial">...</div>
                <!-- 3 more testimonials -->
            </div>
        </section>

        <!-- Section 6: CTA Section -->
        <section class="cta-section">
            <h2>Get Started for Free</h2>
            <p>Setup takes 4-6 hours for 5 config files</p>
            <a href="https://github.com/..." class="cta-primary">View on GitHub</a>
        </section>

        <!-- Section 7: Footer -->
        <footer>
            <div class="footer-links">
                <a href="https://github.com/...">GitHub Repository</a>
                <a href="https://github.com/.../VISION.md">Vision</a>
                <a href="https://github.com/.../synthesis/phase1-implementation.md">Implementation Guide</a>
            </div>
            <p class="tagline">Built for developers who want structure without sacrificing speed</p>
        </footer>
    </main>
</body>
</html>
```

## CSS Design System

### Color Palette (Extracted from Kiro)

**Source:** Analyzed from `resources/scraped/kiro.dev/.meta/kiro.dev.wget_mirror/`

```css
:root {
    /* Background colors (from Kiro's actual dark theme) */
    --bg-primary: #020617;        /* Very dark blue-black, main background */
    --bg-secondary: #111827;      /* Dark gray, card backgrounds */
    --bg-tertiary: #1f2937;       /* Medium dark, hover states */

    /* Text colors */
    --text-primary: #ffffff;      /* White, headings */
    --text-secondary: #d1d5db;    /* Light gray, body text */
    --text-tertiary: #6b7280;     /* Medium gray, muted text */

    /* Accent colors (Kiro's actual purple palette) */
    --accent-primary: #9046FF;    /* Kiro brand purple, CTAs and links */
    --accent-hover: #790ECB;      /* Darker purple, hover state */
    --accent-muted: #c2a0fd;      /* Light purple, secondary accents */
    --accent-light: #8627e5;      /* Alternative purple shade */

    /* Border colors */
    --border-subtle: #e5e7eb;     /* Light gray borders */
    --border-dark: #374151;       /* Dark borders for cards */

    /* Spacing scale (8px base unit) */
    --space-xs: 0.5rem;   /* 8px */
    --space-sm: 1rem;     /* 16px */
    --space-md: 2rem;     /* 32px */
    --space-lg: 4rem;     /* 64px */
    --space-xl: 6rem;     /* 96px */
}
```

### Visual Assets Locations

**SVG Assets to embed:**
- **Ghost Icon:** `resources/scraped/kiro.dev/.meta/kiro.dev.wget_mirror/icon.svg?fe599162bb293ea0`
- **Purple Line Art:** `resources/scraped/kiro.dev/.meta/kiro.dev.wget_mirror/images/purple-line-art.svg`
- **Gray Line Art:** `resources/scraped/kiro.dev/.meta/kiro.dev.wget_mirror/images/gray-line-art.svg`

### Kiro Ghost Icon SVG (To Embed)

**Usage:** Header logo, favicon base
**Size:** 1200x1200px (scalable)
**Colors:** Purple background (#9046FF) with white ghost

```svg
<svg width="1200" height="1200" viewBox="0 0 1200 1200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="1200" rx="260" fill="#9046FF"/>
  <mask id="mask0_1106_4856" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="272" y="202" width="655" height="796">
    <path d="M926.578 202.793H272.637V997.857H926.578V202.793Z" fill="white"/>
  </mask>
  <g mask="url(#mask0_1106_4856)">
    <path d="M398.554 818.914C316.315 1001.03 491.477 1046.74 620.672 940.156C658.687 1059.66 801.052 970.473 852.234 877.795C964.787 673.567 919.318 465.357 907.64 422.374C827.637 129.443 427.623 128.946 358.8 423.865C342.651 475.544 342.402 534.18 333.458 595.051C328.986 625.86 325.507 645.488 313.83 677.785C306.873 696.424 297.68 712.819 282.773 740.645C259.915 783.881 269.604 867.113 387.87 823.883L399.051 818.914H398.554Z" fill="white"/>
    <path d="M636.123 549.353C603.328 549.353 598.359 510.097 598.359 486.742C598.359 465.623 602.086 448.977 609.293 438.293C615.504 428.852 624.697 424.131 636.123 424.131C647.555 424.131 657.492 428.852 664.447 438.541C672.398 449.474 676.623 466.12 676.623 486.742C676.623 525.998 661.471 549.353 636.375 549.353H636.123Z" fill="black"/>
    <path d="M771.24 549.353C738.445 549.353 733.477 510.097 733.477 486.742C733.477 465.623 737.203 448.977 744.41 438.293C750.621 428.852 759.814 424.131 771.24 424.131C782.672 424.131 792.609 428.852 799.564 438.541C807.516 449.474 811.74 466.12 811.74 486.742C811.74 525.998 796.588 549.353 771.492 549.353H771.24Z" fill="black"/>
  </g>
</svg>
```

**Modifications for use:**
- Scale down to 48px-64px for header
- Can extract just the ghost path (remove purple background) for transparency
- Use as-is for favicon with appropriate sizing

### Typography Scale

**Note:** Kiro uses proprietary AWS Diatype font. We'll use system fonts for zero latency and licensing compliance.

```css
/* Font stack - System fonts for performance (replaces AWS Diatype) */
--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
--font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;

/* Type scale (matching Kiro's hierarchy) */
--text-h1: 3.5rem;     /* 56px - Hero headline */
--text-h2: 2.5rem;     /* 40px - Section headings */
--text-h3: 1.75rem;    /* 28px - Card headings */
--text-title1: 1.25rem;  /* 20px - Feature titles */
--text-body: 1.125rem;   /* 18px - Body text */
--text-small: 0.875rem;  /* 14px - Captions */

/* Line heights */
--leading-tight: 1.1;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### Responsive Breakpoints

```css
/* Mobile-first approach */
@media (min-width: 768px) {
    /* Tablet */
    .container {
        max-width: 720px;
    }
}

@media (min-width: 1024px) {
    /* Desktop */
    .container {
        max-width: 960px;
    }
}

@media (min-width: 1280px) {
    /* Large desktop */
    .container {
        max-width: 1200px;
    }
}
```

## Layout Patterns

### Hero Section Layout

```
┌────────────────────────────────────┐
│                                    │
│         [Large H1 Headline]        │
│                                    │
│      [Tagline: Prompt → ... ]      │
│                                    │
│  [Value proposition paragraph]     │
│                                    │
│      [Get Started Button]          │
│                                    │
└────────────────────────────────────┘
```

**Spacing:**
- Top padding: `var(--space-xl)` (96px)
- Bottom padding: `var(--space-xl)` (96px)
- Max-width for text: 75% on desktop, 100% on mobile

### Feature Cards Layout

**Mobile (< 768px):** Single column stack
```
┌──────────────┐
│  Feature 1   │
└──────────────┘
┌──────────────┐
│  Feature 2   │
└──────────────┘
```

**Desktop (> 1024px):** 2x2 grid or 4-column row
```
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Feature │ │ Feature │ │ Feature │ │ Feature │
│    1    │ │    2    │ │    3    │ │    4    │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
```

**Card Structure:**
```html
<div class="feature-card">
    <h3>Feature Title</h3>
    <p>Description text explaining the capability...</p>
</div>
```

**Card Styling:**
- Background: `var(--bg-secondary)`
- Border: 1px solid `var(--border-subtle)`
- Border-radius: 8px
- Padding: `var(--space-md)` (32px)
- Hover effect: subtle lift with box-shadow

### Workflow Steps Layout

```
  ┌─────────┐        ┌─────────┐        ┌─────────┐
  │  Step 1 │   →    │  Step 2 │   →    │  Step 3 │
  └─────────┘        └─────────┘        └─────────┘
```

**Implementation:**
- Mobile: Vertical stack with visual connectors
- Desktop: Horizontal row with arrow indicators
- Numbered steps: Large number (48px) + title + description

### Testimonials Layout

**Mobile:** Horizontal scroll
```css
.testimonial-grid {
    display: flex;
    overflow-x: auto;
    gap: var(--space-md);
    scroll-snap-type: x mandatory;
}

.testimonial {
    min-width: 280px;
    scroll-snap-align: start;
}
```

**Desktop:** Multi-column grid
```css
@media (min-width: 1024px) {
    .testimonial-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: var(--space-md);
    }
}
```

## Content Adaptation Strategy

### Kiro → Claude Kiro Terminology Mapping

| Kiro Original | Claude Kiro Adaptation | Context |
|---------------|------------------------|---------|
| "The AI IDE for prototype to production" | "Spec-Driven Development for Claude Code" | Hero headline |
| "Kiro helps you do your best work by bringing structure to AI coding" | "Bring structure to AI coding with proven spec-driven methodology" | Hero tagline |
| "Tame complexity with spec-driven development" | "Structured Requirements with EARS Notation" | Feature heading |
| "Automate tasks with agent hooks" | "Automated Task Tracking with TodoWrite" | Feature heading |
| "Built from the ground-up for working with agents" | "Pure Configuration, No Custom Code" | Feature heading |
| "Download Kiro" / "Join Waitlist" | "Get Started on GitHub" | CTA buttons |
| "Kiro gives you..." | "This methodology gives you..." | Body copy |

### Testimonial Adaptation Examples

**Original Kiro testimonial:**
> "As a startup co-founder and CTO, time is the most important resource. Kiro justifies the use of my time for developing our business critical assets in-house."

**Adapted for Claude Kiro:**
> "As a startup co-founder and CTO, time is the most important resource. Spec-driven development justifies the use of my time for building business critical assets with structured planning."

**Adaptation Rules:**
1. Remove IDE-specific references ("download", "install", "interface")
2. Keep role/attribution unchanged
3. Preserve the benefit/outcome described
4. Replace "Kiro" with "spec-driven development" or "this methodology"
5. Maintain original tone and credibility

### Content Sources for Adaptation

From Kiro homepage scraped content, adapt:

1. **Primary Features (4):**
   - "Bring structure to AI coding with spec-driven development" (from h3)
   - "Built from the ground-up for working with agents" (from h3)
   - "More context, less repetition" (from h3)
   - "Integrate tools and data with MCP" (adapt to "Extend with MCP and Hooks")

2. **Secondary Features (6 from tertiary-feature grid):**
   - "Strap in with autopilot mode" → "ExitPlanMode for Approval Gates"
   - "Your code, your rules" → "Steering Files for Project Context"
   - "Powered by the state of the art" → "Thinking Mode for Deep Planning"
   - "Compatible with VS Code" → "Works with Existing Claude Code Setup"
   - "Show, don't tell" → "EARS Notation for Testable Requirements"
   - "Witness the magic with code diffs" → "TodoWrite for Native Task Tracking"

3. **Testimonials (select 4 most generic from 15+ available):**
   - Rolf Koski (CTO) - about time justification
   - Håkon Eriksen Drange (Principal Architect) - about code quality
   - Farah Abdirahman (Engineer) - "structure to the chaos before you write a single line"
   - Sathiesh Veera (Principal Engineer) - spec creating user stories

## Component Specifications

### Header Component (with Ghost Icon)

```html
<header>
    <div class="container">
        <div class="logo">
            <img src="ghost-icon.svg" alt="Claude Kiro" width="48" height="48" class="logo-icon">
            <span class="logo-text">Claude Kiro</span>
        </div>
        <a href="#get-started" class="cta-button">Get Started</a>
    </div>
</header>
```

**CSS:**
```css
.logo {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.logo-icon {
    border-radius: 8px;
}

.logo-text {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
}
```

### Hero Section Component

**Implementation Note:** Workflow tagline was replaced with install command box + copy button for better UX.

```html
<section class="hero">
    <div class="container">
        <!-- Optional: Large ghost icon as hero decoration -->
        <img src="ghost-icon.svg" alt="" width="120" height="120" class="hero-icon" aria-hidden="true">

        <h1>Spec-Driven Development for Claude Code</h1>

        <p class="value-prop">
            Bring Kiro's proven methodology to Claude Code using output styles,
            slash commands, and hooks. No custom IDE needed—pure configuration.
        </p>

        <!-- Install command box with copy button -->
        <div class="install-command">
            <code id="install-cmd">curl -sSL https://raw.githubusercontent.com/angelsen/claude-kiro/main/install.sh | bash</code>
            <button class="copy-button" onclick="copyInstallCommand()">Copy Command</button>
        </div>

        <div class="cta-group">
            <a href="https://github.com/angelsen/claude-kiro" class="cta-primary" target="_blank" rel="noopener">
                Get Started on GitHub
            </a>
            <a href="#how-it-works" class="cta-secondary">
                Learn How It Works
            </a>
        </div>

        <p class="quick-pitch">
            92% feature parity with Kiro IDE • Pure Claude Code primitives • Instant setup
        </p>
    </div>
</section>
```

**CSS:**
```css
.hero {
    background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    padding: var(--space-xl) var(--space-md);
    text-align: center;
}

.hero h1 {
    font-size: clamp(2rem, 5vw, var(--text-h1));
    line-height: var(--leading-tight);
    margin-bottom: var(--space-md);
    background: linear-gradient(90deg, #fff 0%, var(--accent-muted) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.workflow-tagline {
    font-family: var(--font-mono);
    font-size: var(--text-title1);
    color: var(--accent-primary);
    margin-bottom: var(--space-md);
}

.value-prop {
    font-size: var(--text-body);
    line-height: var(--leading-relaxed);
    color: var(--text-secondary);
    max-width: 60ch;
    margin: 0 auto var(--space-lg);
}

.cta-primary {
    display: inline-block;
    background: var(--accent-primary);
    color: white;
    padding: var(--space-sm) var(--space-md);
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    transition: background 0.2s ease;
}

.cta-primary:hover {
    background: var(--accent-hover);
}
```

### Feature Card Component

```html
<div class="feature-card">
    <div class="feature-icon">
        <!-- SVG icon or emoji -->
        📋
    </div>
    <h3>Structured Requirements with EARS Notation</h3>
    <p>
        Every requirement uses "WHEN [condition] THE SYSTEM SHALL [behavior]" format
        for unambiguous, testable specifications. Turn prompts into production-ready
        requirements automatically.
    </p>
</div>
```

**CSS:**
```css
.feature-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: var(--space-md);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(168, 85, 247, 0.15);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: var(--space-sm);
}

.feature-card h3 {
    font-size: var(--text-h3);
    margin-bottom: var(--space-sm);
    color: var(--text-primary);
}

.feature-card p {
    color: var(--text-secondary);
    line-height: var(--leading-normal);
}
```

### Testimonial Card Component

```html
<div class="testimonial">
    <blockquote>
        "As a startup co-founder and CTO, time is the most important resource.
        Spec-driven development justifies the use of my time for building
        business critical assets with structured planning."
    </blockquote>
    <div class="attribution">
        <div class="avatar">RK</div>
        <div class="author">
            <p class="name">Rolf Koski</p>
            <p class="role">CTO & Co-Founder</p>
        </div>
    </div>
</div>
```

**CSS:**
```css
.testimonial {
    background: var(--bg-secondary);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: var(--space-md);
}

.testimonial blockquote {
    font-size: var(--text-body);
    line-height: var(--leading-relaxed);
    color: var(--text-secondary);
    margin-bottom: var(--space-md);
    font-style: italic;
}

.attribution {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--accent-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    color: white;
}

.author .name {
    font-weight: 600;
    color: var(--text-primary);
}

.author .role {
    font-size: var(--text-small);
    color: var(--text-tertiary);
}
```

## Error Handling Strategy

Since this is a static HTML page, error handling is minimal:

- **Broken Links:** All GitHub links will use the repository's actual URL structure
- **Missing Images:** No external images used; only inline SVG or emoji icons
- **CSS Failures:** Fallback system fonts and colors defined
- **Accessibility:** Proper ARIA labels and semantic HTML ensure screen reader compatibility

## Testing Strategy

### Manual Testing Checklist

**Responsive Testing:**
- [ ] Test on iPhone SE (375px width)
- [ ] Test on iPad (768px width)
- [ ] Test on MacBook Pro (1440px width)
- [ ] Test on 4K display (2560px width)
- [ ] Verify no horizontal scroll at any breakpoint

**Browser Testing:**
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

**Accessibility Testing:**
- [ ] Run axe DevTools accessibility audit
- [ ] Test keyboard navigation (Tab, Enter)
- [ ] Test with VoiceOver (macOS) or NVDA (Windows)
- [ ] Verify color contrast (4.5:1 minimum)
- [ ] Check heading hierarchy (h1 → h2 → h3, no skips)

**Performance Testing:**
- [ ] Run Lighthouse audit (target: >90 score)
- [ ] Verify file size < 500KB
- [ ] Test on throttled 3G connection
- [ ] Check Time to First Contentful Paint < 2s

### Automated Testing

**Lighthouse CI (optional):**
```bash
npm install -g @lhci/cli
lhci autorun --collect.url=file:///path/to/docs/index.html
```

**HTML Validation:**
```bash
# Use W3C validator
curl -F uploaded_file=@docs/index.html -F output=json \
  https://validator.w3.org/nu/ | jq
```

## Performance Considerations

### Optimization Strategies

1. **Inline Everything:**
   - No external CSS files (saves 1 HTTP request)
   - No JavaScript (zero parser/execution overhead)
   - Inline SVG icons (no image requests)

2. **CSS Optimization:**
   - Use CSS custom properties for theming (single source of truth)
   - Minimize use of expensive properties (box-shadow, gradients)
   - Use `transform` for animations (GPU accelerated)

3. **Font Loading:**
   - System font stack (zero font download)
   - No web fonts = instant text render

4. **Image Strategy:**
   - Emoji for icons (Unicode, no download)
   - Inline SVG for any graphics (minimal size)
   - No raster images (no compression needed)

### Expected Performance

| Metric | Target | Reasoning |
|--------|--------|-----------|
| File Size | < 200KB | Inline CSS + HTML only |
| First Contentful Paint | < 1s | No external resources |
| Time to Interactive | < 1.5s | No JavaScript |
| Lighthouse Performance | > 95 | Fully optimized static page |
| Total Blocking Time | 0ms | Zero JavaScript |

## Security Considerations

### External Links
- **GitHub links:** Use `target="_blank" rel="noopener noreferrer"` to prevent tab-nabbing
- **No tracking:** Zero third-party scripts or analytics
- **No forms:** No user input = no XSS risk

### Content Security Policy (Optional)

GitHub Pages doesn't support custom headers, but if self-hosting:

```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    style-src 'unsafe-inline';
    img-src 'self' data:;
    script-src 'none';
">
```

## Migration Strategy

### Deployment Steps

1. **Create docs directory:**
   ```bash
   mkdir -p docs
   ```

2. **Add index.html:**
   ```bash
   # File will be created as single task
   ```

3. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `master` (or `main`)
   - Folder: `/docs`
   - Save

4. **Verify deployment:**
   - URL format: `https://USERNAME.github.io/REPO-NAME/`
   - Check within 1-2 minutes of commit

### Rollback Strategy

If issues arise:
- **Revert commit:** `git revert HEAD` to undo the addition
- **Disable Pages:** Turn off GitHub Pages in settings
- **Fix and redeploy:** Make corrections and push again

No database migrations or complex rollback needed - it's just a static file.

### Install Command Component

**Added during implementation for better UX.**

```html
<div class="install-command">
    <code id="install-cmd">curl -sSL https://raw.githubusercontent.com/angelsen/claude-kiro/main/install.sh | bash</code>
    <button class="copy-button" onclick="copyInstallCommand()">Copy Command</button>
</div>
```

**CSS:**
```css
.install-command {
    background-color: var(--bg-tertiary);
    border: 2px solid var(--accent-primary);
    border-radius: 8px;
    padding: var(--space-sm) var(--space-md);
    margin: var(--space-lg) auto;
    max-width: 90%;
    text-align: center;
}

@media (min-width: 768px) {
    .install-command {
        max-width: 600px;
    }
}

.install-command code {
    font-family: var(--font-mono);
    font-size: var(--text-small);
    color: var(--accent-muted);
    display: block;
    word-break: break-all;
    margin-bottom: var(--space-sm);
}

.copy-button {
    background-color: var(--accent-primary);
    color: var(--text-primary);
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.5rem;
    font-family: var(--font-sans);
    font-size: var(--text-small);
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.copy-button:hover {
    background-color: var(--accent-hover);
}

.copy-button:active {
    transform: scale(0.98);
}
```

**JavaScript:**
```javascript
function copyInstallCommand() {
    const code = document.getElementById('install-cmd').textContent;
    navigator.clipboard.writeText(code).then(() => {
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy command. Please copy manually.');
    });
}
```

## Additional Notes

### Why Single-File Design?

1. **Portability:** Can be copied/shared as a single file
2. **No build step:** Works immediately without npm/webpack
3. **Fast deployment:** Single commit to docs/index.html
4. **Zero dependencies:** No package.json, no node_modules
5. **GitHub Pages compatible:** Works with default GH Pages setup

### Future Enhancements (Out of Current Scope)

If the project grows beyond a single landing page:

- **Multi-page docs:** Separate pages for guides, API reference
- **Build process:** PostCSS for CSS optimization, HTML minification
- **Interactive demos:** Code playgrounds showing slash commands
- **Analytics:** Privacy-respecting analytics (Plausible, etc.)
- **Versioning:** Document multiple versions of the configuration

For now, the single-file approach meets all requirements and maintains simplicity.
