(function () {
  "use strict";

  /* -----------------------------------------------------------------------
     1. Theme Toggle (Light / Dark)
     ----------------------------------------------------------------------- */
  var themeToggle = document.getElementById("theme-toggle");

  function getCurrentTheme() {
    return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    if (themeToggle) {
      var nextTheme = theme === "dark" ? "light" : "dark";
      themeToggle.setAttribute("aria-label", "Switch to " + nextTheme + " theme");
      themeToggle.setAttribute("title", "Switch to " + nextTheme + " theme");
    }
  }

  applyTheme(getCurrentTheme());

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var next = getCurrentTheme() === "dark" ? "light" : "dark";
      applyTheme(next);
      try {
        localStorage.setItem("paddlr-theme", next);
      } catch (e) {
        // Ignore storage errors in restricted environments
      }
    });
  }

  /* -----------------------------------------------------------------------
     2. Mobile Navigation Drawer
     ----------------------------------------------------------------------- */
  var mobileToggle = document.getElementById("mobile-menu-toggle");
  var mobileNav = document.getElementById("mobile-nav");

  function setMobileMenu(open) {
    if (!mobileToggle || !mobileNav) return;
    mobileToggle.setAttribute("aria-expanded", String(open));
    mobileToggle.setAttribute("aria-label", open ? "Close navigation menu" : "Open navigation menu");
    mobileNav.classList.toggle("is-open", open);
  }

  if (mobileToggle && mobileNav) {
    mobileToggle.addEventListener("click", function () {
      var isOpen = mobileNav.classList.contains("is-open");
      setMobileMenu(!isOpen);
    });

    mobileNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setMobileMenu(false);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && mobileNav.classList.contains("is-open")) {
        setMobileMenu(false);
        mobileToggle.focus();
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 768 && mobileNav.classList.contains("is-open")) {
        setMobileMenu(false);
      }
    });
  }

  /* -----------------------------------------------------------------------
     3. Accessible Platform Install Tabs
     ----------------------------------------------------------------------- */
  var tabButtons = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));

  function activateTab(tab) {
    tabButtons.forEach(function (btn) {
      var selected = btn === tab;
      btn.setAttribute("aria-selected", String(selected));
      btn.setAttribute("tabindex", selected ? "0" : "-1");
      var panelId = btn.getAttribute("aria-controls");
      var panel = panelId ? document.getElementById(panelId) : null;
      if (panel) {
        panel.hidden = !selected;
      }
    });
  }

  tabButtons.forEach(function (btn, index) {
    btn.addEventListener("click", function () {
      activateTab(btn);
    });

    btn.addEventListener("keydown", function (event) {
      var targetIndex = null;
      if (event.key === "ArrowRight") {
        targetIndex = (index + 1) % tabButtons.length;
      } else if (event.key === "ArrowLeft") {
        targetIndex = (index - 1 + tabButtons.length) % tabButtons.length;
      } else if (event.key === "Home") {
        targetIndex = 0;
      } else if (event.key === "End") {
        targetIndex = tabButtons.length - 1;
      }

      if (targetIndex !== null) {
        event.preventDefault();
        activateTab(tabButtons[targetIndex]);
        tabButtons[targetIndex].focus();
      }
    });
  });

  /* -----------------------------------------------------------------------
     4. Copy-to-Clipboard for Code Blocks
     ----------------------------------------------------------------------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand("copy");
        resolve();
      } catch (err) {
        reject(err);
      } finally {
        document.body.removeChild(textarea);
      }
    });
  }

  document.querySelectorAll("[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      var block = button.closest(".code-block");
      var codeEl = block ? block.querySelector("pre code") : null;
      if (!codeEl) return;

      var text = codeEl.textContent.trim();
      copyText(text)
        .then(function () {
          button.textContent = "Copied";
          button.classList.add("is-copied");
          setTimeout(function () {
            button.textContent = "Copy";
            button.classList.remove("is-copied");
          }, 1800);
        })
        .catch(function () {
          button.textContent = "Failed";
          setTimeout(function () {
            button.textContent = "Copy";
          }, 1800);
        });
    });
  });

  /* -----------------------------------------------------------------------
     5. Active Navigation Highlighting on Scroll
     ----------------------------------------------------------------------- */
  if ("IntersectionObserver" in window) {
    var docLinks = Array.prototype.slice.call(document.querySelectorAll(".docs-nav a"));
    var docSections = docLinks
      .map(function (link) {
        var href = link.getAttribute("href");
        return href && href.charAt(0) === "#" ? document.querySelector(href) : null;
      })
      .filter(Boolean);

    if (docSections.length > 0) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              var id = "#" + entry.target.id;
              docLinks.forEach(function (link) {
                link.classList.toggle("is-active", link.getAttribute("href") === id);
              });
            }
          });
        },
        { rootMargin: "-20% 0px -65% 0px", threshold: 0 }
      );

      docSections.forEach(function (section) {
        observer.observe(section);
      });
    }
  }
})();
