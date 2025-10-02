# Design: Documentation Site with Mini-Framework

## Architecture Overview

Create a completely fresh documentation site in `next.docs/` with a shadcn-inspired mini-framework. This approach allows us to build a modern, maintainable documentation system without being constrained by the existing implementation. Once tested and approved locally, we'll replace the current `docs/` directory.

The framework will be a self-contained CSS/JS system inspired by shadcn/ui's philosophy: modern, minimal, copy-paste friendly components with a focus on developer experience.

## Component Analysis

### Existing Components to Reference
- `docs/index.html` - Use as inspiration for content and branding only
- `docs/*.svg` - Copy existing SVG assets to new structure
- `docs/install.sh` - Update for new documentation structure

### New Components to Create

**Directory Structure:**
```
next.docs/
├── index.html                 # Landing page with hero
├── methodology.html           # Spec-driven workflow explanation
├── getting-started.html       # Installation and setup
├── cli.html                  # CLI command reference
├── commands.html             # Slash commands documentation
├── examples.html             # Real-world examples
├── install.sh                # Installation script
├── assets/
│   ├── css/
│   │   ├── kiro.css         # Main framework
│   │   └── theme.css        # CSS variables and theming
│   ├── js/
│   │   └── kiro.js          # Interactive behaviors
│   └── img/
│       ├── ghost-icon.svg   # Kiro ghost logo
│       ├── purple-line.svg  # Decorative element
│       └── gray-line.svg    # Alternative decoration
```

## Data Models

### CSS Framework Architecture (kiro.css)

```css
/* Shadcn-inspired CSS Framework Structure */

/* ===== 1. CSS Reset & Base ===== */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* ===== 2. Design Tokens (theme.css) ===== */
:root {
  /* Colors - HSL for easy manipulation */
  --background: 222.2 84% 4.9%;      /* Dark background */
  --foreground: 210 40% 98%;         /* Light text */
  --card: 222.2 84% 4.9%;           /* Card backgrounds */
  --card-foreground: 210 40% 98%;   /* Card text */

  --primary: 262.1 83.3% 57.8%;     /* Purple accent */
  --primary-foreground: 210 40% 98%;

  --secondary: 217.2 32.6% 17.5%;   /* Muted backgrounds */
  --secondary-foreground: 210 40% 98%;

  --muted: 217.2 32.6% 17.5%;       /* Muted elements */
  --muted-foreground: 215 20.2% 65.1%;

  --accent: 217.2 32.6% 17.5%;      /* Accent elements */
  --accent-foreground: 210 40% 98%;

  --destructive: 0 84.2% 60.2%;     /* Error states */
  --border: 217.2 32.6% 17.5%;      /* Borders */
  --input: 217.2 32.6% 17.5%;       /* Form inputs */
  --ring: 262.1 83.3% 57.8%;        /* Focus rings */

  /* Spacing */
  --radius: 0.5rem;
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;

  /* Typography */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif;
  --font-mono: "SF Mono", "Monaco", "Inconsolata", "Fira Code", monospace;
}

/* ===== 3. Layout Components ===== */
.container {
  width: 100%;
  margin-right: auto;
  margin-left: auto;
  padding-right: var(--space-4);
  padding-left: var(--space-4);
}

@media (min-width: 640px) {
  .container { max-width: 640px; }
}
@media (min-width: 768px) {
  .container { max-width: 768px; }
}
@media (min-width: 1024px) {
  .container { max-width: 1024px; }
}
@media (min-width: 1280px) {
  .container { max-width: 1280px; }
}

/* ===== 4. Component Classes ===== */

/* Navigation */
.nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: hsl(var(--background) / 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid hsl(var(--border));
}

/* Sidebar */
.sidebar {
  position: sticky;
  top: 4rem;
  height: calc(100vh - 4rem);
  overflow-y: auto;
}

/* Cards */
.card {
  border-radius: var(--radius);
  border: 1px solid hsl(var(--border));
  background: hsl(var(--card));
  color: hsl(var(--card-foreground));
  padding: var(--space-6);
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 500;
  padding: var(--space-2) var(--space-4);
  transition: all 0.2s;
}

.btn-primary {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}

.btn-outline {
  border: 1px solid hsl(var(--border));
  background: transparent;
}

/* Code Blocks */
.code-block {
  position: relative;
  background: hsl(var(--muted));
  border-radius: var(--radius);
  padding: var(--space-4);
  font-family: var(--font-mono);
  font-size: 0.875rem;
}

/* Callouts */
.callout {
  border-radius: var(--radius);
  border: 1px solid hsl(var(--border));
  padding: var(--space-4);
}

.callout-info {
  border-left: 4px solid hsl(var(--primary));
}
```

### JavaScript Module Structure (kiro.js)

```javascript
// Kiro Documentation Framework
class KiroFramework {
  constructor() {
    this.init();
  }

  init() {
    this.initNavigation();
    this.initSidebar();
    this.initCodeBlocks();
    this.initTabs();
    this.initTheme();
  }

  // Navigation with mobile menu
  initNavigation() {
    const nav = document.querySelector('.nav');
    const mobileToggle = document.querySelector('.nav-toggle');
    const mobileMenu = document.querySelector('.nav-mobile');

    if (mobileToggle) {
      mobileToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
      });
    }

    // Highlight active page
    this.setActiveNavItem();
  }

  // Sidebar navigation
  initSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;

    // Collapsible sections
    const toggles = sidebar.querySelectorAll('.sidebar-toggle');
    toggles.forEach(toggle => {
      toggle.addEventListener('click', () => {
        toggle.parentElement.classList.toggle('collapsed');
      });
    });

    // Highlight current page
    this.setActiveSidebarItem();
  }

  // Code blocks with copy functionality
  initCodeBlocks() {
    const blocks = document.querySelectorAll('.code-block');

    blocks.forEach(block => {
      const button = document.createElement('button');
      button.className = 'code-copy';
      button.innerHTML = 'Copy';
      button.onclick = () => this.copyCode(block);
      block.appendChild(button);
    });
  }

  copyCode(block) {
    const code = block.querySelector('code').innerText;
    navigator.clipboard.writeText(code).then(() => {
      const button = block.querySelector('.code-copy');
      button.innerHTML = 'Copied!';
      setTimeout(() => button.innerHTML = 'Copy', 2000);
    });
  }

  // Tab components
  initTabs() {
    const tabGroups = document.querySelectorAll('.tabs');

    tabGroups.forEach(group => {
      const buttons = group.querySelectorAll('.tab-button');
      const panels = group.querySelectorAll('.tab-panel');

      buttons.forEach((button, index) => {
        button.addEventListener('click', () => {
          buttons.forEach(b => b.classList.remove('active'));
          panels.forEach(p => p.classList.remove('active'));

          button.classList.add('active');
          panels[index].classList.add('active');
        });
      });
    });
  }

  // Theme management (future dark/light toggle)
  initTheme() {
    // Prepare for theme toggle, currently dark-only
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  // Utility methods
  setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav a');

    navLinks.forEach(link => {
      if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
      }
    });
  }

  setActiveSidebarItem() {
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar a');

    sidebarLinks.forEach(link => {
      if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
        // Expand parent section if collapsed
        const section = link.closest('.sidebar-section');
        if (section) section.classList.remove('collapsed');
      }
    });
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  new KiroFramework();
});
```

### Page Template Structure

```html
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="[PAGE_DESCRIPTION]">
    <title>[PAGE_TITLE] - Claude Kiro</title>

    <!-- Framework CSS -->
    <link rel="stylesheet" href="/assets/css/theme.css">
    <link rel="stylesheet" href="/assets/css/kiro.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="nav">
        <div class="container nav-container">
            <a href="/" class="nav-brand">
                <img src="/assets/img/ghost-icon.svg" alt="Claude Kiro" class="nav-logo">
                <span>Claude Kiro</span>
            </a>

            <!-- Desktop Nav -->
            <div class="nav-links">
                <a href="/getting-started.html">Docs</a>
                <a href="/methodology.html">Methodology</a>
                <a href="https://github.com/angelsen/claude-kiro">GitHub</a>
            </div>

            <!-- Mobile Toggle -->
            <button class="nav-toggle">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>

        <!-- Mobile Menu -->
        <div class="nav-mobile">
            <a href="/getting-started.html">Getting Started</a>
            <a href="/methodology.html">Methodology</a>
            <a href="/cli.html">CLI Reference</a>
            <a href="/commands.html">Slash Commands</a>
            <a href="/examples.html">Examples</a>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container">
        <div class="docs-layout">
            <!-- Sidebar (for doc pages) -->
            <aside class="sidebar">
                <div class="sidebar-section">
                    <h4>Introduction</h4>
                    <ul>
                        <li><a href="/getting-started.html">Getting Started</a></li>
                        <li><a href="/methodology.html">Methodology</a></li>
                    </ul>
                </div>

                <div class="sidebar-section">
                    <h4>Reference</h4>
                    <ul>
                        <li><a href="/cli.html">CLI Commands</a></li>
                        <li><a href="/commands.html">Slash Commands</a></li>
                    </ul>
                </div>

                <div class="sidebar-section">
                    <h4>Guides</h4>
                    <ul>
                        <li><a href="/examples.html">Examples</a></li>
                    </ul>
                </div>
            </aside>

            <!-- Page Content -->
            <main class="content">
                <!-- PAGE CONTENT HERE -->
            </main>
        </div>
    </div>

    <!-- Framework JS -->
    <script src="/assets/js/kiro.js"></script>
</body>
</html>
```

## Component Specifications

### Navigation Component
- **Desktop**: Horizontal nav with brand, links, and GitHub
- **Mobile**: Hamburger menu with full navigation
- **Sticky**: Fixed to top with backdrop blur
- **Active state**: Highlight current page

### Sidebar Component
- **Structure**: Collapsible sections with nested links
- **Behavior**: Auto-expand active section, highlight current
- **Mobile**: Hidden on small screens, accessible via nav
- **Sticky**: Follows scroll on desktop

### Card Component
- **Variants**: Default, bordered, elevated
- **Content**: Title, description, optional icon
- **Hover**: Subtle shadow elevation
- **Grid**: Responsive card grids

### Code Block Component
- **Syntax**: Basic highlighting with CSS
- **Copy**: Button appears on hover
- **Tabs**: Support for multiple examples
- **Line numbers**: Optional

### Button Component
- **Variants**: Primary, outline, ghost
- **Sizes**: sm, md, lg
- **States**: Hover, active, disabled
- **Icons**: Optional icon support

## Responsive Design Strategy

```css
/* Mobile First Breakpoints */
/* sm: 640px - Phones landscape */
/* md: 768px - Tablets */
/* lg: 1024px - Desktop */
/* xl: 1280px - Wide screens */

/* Layout Changes */
@media (max-width: 768px) {
  .docs-layout {
    grid-template-columns: 1fr;
  }
  .sidebar {
    display: none;
  }
}

@media (min-width: 769px) {
  .docs-layout {
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: var(--space-8);
  }
}
```

## Testing Strategy

### Visual Testing
- All breakpoints: mobile, tablet, desktop
- Cross-browser: Chrome, Firefox, Safari, Edge
- Component consistency across pages
- Animation performance
- Color contrast (WCAG AA)

### Functional Testing
- Navigation interactions
- Mobile menu toggle
- Copy code functionality
- Tab switching
- Sidebar collapse/expand
- Keyboard navigation

### Performance Testing
- Page load < 1s
- CSS ~20KB minified
- JS ~10KB minified
- No layout shift

## Performance Considerations

- **CSS**: Single framework file, minified
- **JavaScript**: Vanilla JS, no dependencies
- **Fonts**: System fonts only
- **Images**: SVGs optimized
- **Caching**: Long cache headers for assets

## Security Considerations

- **XSS**: No user input or dynamic content
- **Links**: External links use rel="noopener noreferrer"
- **CSP**: Appropriate Content Security Policy headers
- **Copy**: Sanitize clipboard content

## Migration Strategy

**Phase 1: Build Fresh**
1. Create `next.docs/` directory structure
2. Build CSS framework (theme.css + kiro.css)
3. Implement JavaScript framework (kiro.js)
4. Create page template

**Phase 2: Create Pages**
1. Build landing page (index.html)
2. Create documentation pages
3. Add navigation and sidebar
4. Test all interactions

**Phase 3: Content Migration**
1. Write methodology content
2. Document CLI commands
3. Add examples
4. Create getting started guide

**Phase 4: Deploy**
1. Test locally: `open next.docs/index.html`
2. Verify all links work
3. Check responsive design
4. When approved: `rm -rf docs && mv next.docs docs`

**Rollback Plan**: Keep original `docs/` until new site is fully tested and approved.