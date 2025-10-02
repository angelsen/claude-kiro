# Evolution: GitHub Pages Site → Documentation Mini-Framework

## Status: EVOLVED

**Evolved To:** docs-mini-framework
**Evolution Date:** 2024-10-02
**Reason:** Need for comprehensive documentation system with reusable framework

## What Remains Valid

The original landing page successfully:
- ✅ Established visual identity (glass-morphism, gradients, dark theme)
- ✅ Created brand assets (SVG icons)
- ✅ Deployed to GitHub Pages
- ✅ Provided installation script

These elements are preserved in the new implementation.

## What Was Superseded

**Single Page → Multi-Page Documentation:**
- Old: One landing page with basic information
- New: Complete documentation site with multiple pages

**Inline Styles → Framework Approach:**
- Old: All CSS inline in index.html
- New: Modular CSS framework (kiro.css + theme.css)

**Limited Content → Comprehensive Docs:**
- Old: Marketing-focused landing page
- New: Full documentation (methodology, CLI reference, examples)

## Lessons Learned

1. **Start with a framework mindset** - Even for "simple" sites, a framework pays off quickly
2. **Separate concerns early** - CSS, JS, and HTML should be in separate files
3. **Plan for growth** - Documentation sites always expand beyond initial scope
4. **Mobile-first matters** - Retrofitting responsive design is harder than starting with it
5. **Component thinking** - Reusable components save time and ensure consistency

## Migration Path

The new spec creates documentation in `next.docs/` to allow:
- Risk-free development alongside existing site
- Local testing before deployment
- Easy rollback if needed
- Clean fresh start without legacy code

## What Transfers Forward

- Visual design language (colors, shadows, animations)
- Brand assets (ghost icon, decorative SVGs)
- Installation approach (install.sh script)
- GitHub Pages deployment strategy
- Core messaging about Claude Kiro

## Technical Improvements

The evolution brings:
- Proper CSS architecture (custom properties, component classes)
- JavaScript framework for interactions
- Responsive design from the ground up
- Accessibility improvements (semantic HTML, ARIA)
- Better performance (optimized assets, lazy loading)
- Maintainable codebase (modular structure)

## References

- Original spec: [requirements.md](./requirements.md) | [design.md](./design.md) | [tasks.md](./tasks.md)
- Evolution spec: [../docs-mini-framework/requirements.md](../docs-mini-framework/requirements.md)