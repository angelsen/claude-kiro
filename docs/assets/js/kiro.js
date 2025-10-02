/**
 * Kiro Documentation Framework
 * Interactive behaviors for the documentation site
 */

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

  /**
   * Navigation with mobile menu
   */
  initNavigation() {
    const nav = document.querySelector(".nav");
    const mobileToggle = document.querySelector(".nav-toggle");
    const mobileMenu = document.querySelector(".nav-mobile");

    if (mobileToggle && mobileMenu) {
      mobileToggle.addEventListener("click", () => {
        mobileMenu.classList.toggle("active");

        // Animate hamburger icon
        mobileToggle.classList.toggle("active");
      });

      // Close mobile menu when clicking outside
      document.addEventListener("click", (e) => {
        if (
          !nav.contains(e.target) &&
          mobileMenu.classList.contains("active")
        ) {
          mobileMenu.classList.remove("active");
          mobileToggle.classList.remove("active");
        }
      });

      // Close mobile menu when clicking a link
      mobileMenu.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
          mobileMenu.classList.remove("active");
          mobileToggle.classList.remove("active");
        });
      });
    }

    // Highlight active page
    this.setActiveNavItem();
  }

  /**
   * Sidebar navigation
   */
  initSidebar() {
    const sidebar = document.querySelector(".sidebar");
    if (!sidebar) return;

    // Collapsible sections (for future enhancement)
    const toggles = sidebar.querySelectorAll(".sidebar-toggle");
    toggles.forEach((toggle) => {
      toggle.addEventListener("click", () => {
        toggle.parentElement.classList.toggle("collapsed");
      });
    });

    // Highlight current page
    this.setActiveSidebarItem();
  }

  /**
   * Code blocks with copy functionality
   */
  initCodeBlocks() {
    const blocks = document.querySelectorAll(".code-block");

    blocks.forEach((block) => {
      const button = document.createElement("button");
      button.className = "code-copy";
      button.textContent = "Copy";
      button.setAttribute("aria-label", "Copy code to clipboard");

      button.addEventListener("click", () => this.copyCode(block, button));
      block.appendChild(button);
    });
  }

  /**
   * Copy code to clipboard
   */
  copyCode(block, button) {
    const code = block.querySelector("code") || block;
    const text = code.textContent;

    navigator.clipboard
      .writeText(text)
      .then(() => {
        button.textContent = "Copied!";
        button.classList.add("copied");

        setTimeout(() => {
          button.textContent = "Copy";
          button.classList.remove("copied");
        }, 2000);
      })
      .catch((err) => {
        console.error("Failed to copy code:", err);
        button.textContent = "Failed";

        setTimeout(() => {
          button.textContent = "Copy";
        }, 2000);
      });
  }

  /**
   * Tab components
   */
  initTabs() {
    const tabGroups = document.querySelectorAll(".tabs");

    tabGroups.forEach((group) => {
      const buttons = group.querySelectorAll(".tab-button");
      const panels = group.querySelectorAll(".tab-panel");

      buttons.forEach((button, index) => {
        button.addEventListener("click", () => {
          // Remove active class from all buttons and panels
          buttons.forEach((b) => {
            b.classList.remove("active");
            b.setAttribute("aria-selected", "false");
          });
          panels.forEach((p) => {
            p.classList.remove("active");
            p.setAttribute("hidden", "");
          });

          // Add active class to clicked button and corresponding panel
          button.classList.add("active");
          button.setAttribute("aria-selected", "true");

          if (panels[index]) {
            panels[index].classList.add("active");
            panels[index].removeAttribute("hidden");
          }
        });
      });

      // Set first tab as active by default if none are active
      if (!group.querySelector(".tab-button.active")) {
        buttons[0]?.click();
      }
    });
  }

  /**
   * Theme management (future dark/light toggle)
   */
  initTheme() {
    // Prepare for theme toggle, currently dark-only
    document.documentElement.setAttribute("data-theme", "dark");

    // Future: Check for saved theme preference
    // const savedTheme = localStorage.getItem('kiro-theme');
    // if (savedTheme) {
    //   document.documentElement.setAttribute('data-theme', savedTheme);
    // }
  }

  /**
   * Utility: Set active navigation item
   */
  setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav a");

    navLinks.forEach((link) => {
      const href = link.getAttribute("href");

      // Match exact path or if we're on a doc page and this is the docs link
      if (
        href === currentPath ||
        (currentPath !== "/" &&
          currentPath !== "/index.html" &&
          href === "/getting-started.html")
      ) {
        link.classList.add("active");
      }
    });
  }

  /**
   * Utility: Set active sidebar item
   */
  setActiveSidebarItem() {
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll(".sidebar a");

    sidebarLinks.forEach((link) => {
      const href = link.getAttribute("href");

      if (href === currentPath) {
        link.classList.add("active");

        // Expand parent section if collapsed
        const section = link.closest(".sidebar-section");
        if (section) {
          section.classList.remove("collapsed");
        }
      }
    });
  }

  /**
   * Utility: Smooth scroll to anchor
   */
  smoothScrollToAnchor(anchor) {
    const target = document.querySelector(anchor);
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }
}

// Initialize framework on DOM ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    new KiroFramework();
  });
} else {
  // DOM already loaded
  new KiroFramework();
}

// Handle anchor links with smooth scrolling
document.addEventListener("click", (e) => {
  const link = e.target.closest('a[href^="#"]');
  if (link) {
    e.preventDefault();
    const anchor = link.getAttribute("href");
    const target = document.querySelector(anchor);

    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });

      // Update URL without jumping
      history.pushState(null, null, anchor);
    }
  }
});
