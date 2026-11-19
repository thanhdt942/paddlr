(function () {
  "use strict";

  /* =========================================================================
     1. Maintainable Agent Compatibility & Installation Catalog
        Single source of truth for agent metadata, installation methods,
        step-by-step commands, verification procedures, and usage examples.
     ========================================================================= */
  var AGENTS_CATALOG = {
    claude: {
      id: "claude",
      name: "Claude Code",
      status: "Supported",
      manifest: ".claude-plugin/plugin.json",
      description:
        "Native Claude Code plugin shipping 8 skills, 8 /pdl:* slash commands, SessionStart hook (hooks/hooks.json), and rules/CLAUDE.md instruction router.",
      prerequisites: ["Claude Code CLI", "Git", "Python 3.10+ (SessionStart hook)"],
      methods: [
        {
          label: "Marketplace (Recommended)",
          note: "Run inside an interactive Claude Code session to install Paddlr from the repository marketplace catalog (.claude-plugin/marketplace.json).",
          steps: [
            {
              title: "Step 1 — Install Paddlr from marketplace in Claude Code",
              lang: "claude-code",
              command: "/plugin install paddlr --marketplace thanhdt942/paddlr"
            }
          ]
        },
        {
          label: "Direct Git Repository",
          note: "Install Paddlr directly from the GitHub repository inside your Claude Code session.",
          steps: [
            {
              title: "Step 1 — Install directly from GitHub repository",
              lang: "claude-code",
              command: "/plugin install thanhdt942/paddlr"
            }
          ]
        }
      ],
      verification: {
        note: "Validate the plugin manifest from a local clone or confirm SessionStart bootstrap on session launch:",
        lang: "bash",
        command: "claude plugin validate ."
      },
      usage: {
        note: "Invoke any Paddlr slash command inside your Claude Code session:",
        command: "/pdl:feature-development Add webhook signature verification"
      },
      docAnchor: "#doc-installation"
    },

    antigravity: {
      id: "antigravity",
      name: "Google Antigravity",
      status: "Supported",
      manifest: "plugin.json & hooks.json",
      description:
        "First-class Google Antigravity plugin with root plugin.json manifest, suggested prompts, rules/AGENTS.md, and automatic SessionStart context injection.",
      prerequisites: ["Google Antigravity (agy CLI)", "Git", "Python 3.10+ (SessionStart hook)"],
      methods: [
        {
          label: "agy CLI",
          note: "Install Paddlr directly from GitHub in a single command using the Antigravity CLI.",
          steps: [
            {
              title: "Step 1 — Install plugin via agy CLI",
              lang: "bash",
              command: "agy plugin install https://github.com/thanhdt942/paddlr"
            }
          ]
        }
      ],
      verification: {
        note: "Validate the Antigravity plugin manifest and confirm zero error findings:",
        lang: "bash",
        command: "agy plugin validate . --json"
      },
      usage: {
        note: "Start a new conversation and trigger a Paddlr workflow in chat:",
        command: "/pdl:writing-specs Design an idempotent payment retry service"
      },
      docAnchor: "#doc-installation"
    },

    opencode: {
      id: "opencode",
      name: "OpenCode",
      status: "Supported",
      manifest: "package.json & index.js",
      description:
        "Conforms to OpenCode v1 (@opencode-ai/plugin) and v2 (@opencode/plugin), exposing pdl_bootstrap, pdl_status, pdl_scan tools and destructive Git guardrails.",
      prerequisites: ["OpenCode CLI", "Node.js 18+", "Python 3.10+ (for pdl_scan)"],
      methods: [
        {
          label: "OpenCode CLI (Recommended)",
          note: "Install and register Paddlr globally using the OpenCode CLI.",
          steps: [
            {
              title: "Step 1 — Add Paddlr plugin from GitHub",
              lang: "bash",
              command: "opencode plugin add paddlr@git+https://github.com/thanhdt942/paddlr.git"
            }
          ]
        },
        {
          label: "opencode.json (v2)",
          note: "Add Paddlr to the plural \"plugins\" array in your project or global opencode.json file.",
          steps: [
            {
              title: "Step 1 — Configure opencode.json for OpenCode v2",
              lang: "json",
              command:
                '{\n  "$schema": "https://opencode.ai/config.json",\n  "plugins": [\n    "paddlr@git+https://github.com/thanhdt942/paddlr.git"\n  ]\n}'
            }
          ]
        },
        {
          label: "opencode.json (v1)",
          note: "For OpenCode v1 runtimes, declare Paddlr in the singular \"plugin\" array in opencode.json.",
          steps: [
            {
              title: "Step 1 — Configure opencode.json for OpenCode v1",
              lang: "json",
              command:
                '{\n  "$schema": "https://opencode.ai/config.json",\n  "plugin": [\n    "paddlr@git+https://github.com/thanhdt942/paddlr.git"\n  ]\n}'
            }
          ]
        },
        {
          label: "Local Plugin Directory",
          note: "For offline workspaces, clone Paddlr and re-export index.js from .opencode/plugins/paddlr.js.",
          steps: [
            {
              title: "Step 1 — Clone the Paddlr repository",
              lang: "bash",
              command: "git clone https://github.com/thanhdt942/paddlr.git"
            },
            {
              title: "Step 2 — Export Paddlr from .opencode/plugins/paddlr.js",
              lang: "javascript",
              command: 'export { default } from "./path/to/paddlr/index.js";'
            }
          ]
        }
      ],
      verification: {
        note: "Verify that OpenCode loads Paddlr and invokes pdl_bootstrap:",
        lang: "bash",
        command: 'opencode run "Show me the Paddlr engineering discipline bootstrap context"'
      },
      usage: {
        note: "Ask OpenCode to inspect project memory or run a skill workflow:",
        command: "/pdl:test-driven-development Implement token bucket rate limiter"
      },
      docAnchor: "#doc-customization"
    },

    codex: {
      id: "codex",
      name: "OpenAI Codex",
      status: "Supported",
      manifest: ".codex-plugin/plugin.json",
      description:
        "Native OpenAI Codex plugin and marketplace catalog (.agents/plugins/marketplace.json) equipping Codex with all 8 Paddlr engineering skills.",
      prerequisites: ["OpenAI Codex CLI (codex)", "Git", "Python 3.10+"],
      methods: [
        {
          label: "Codex CLI Marketplace",
          note: "Register the Paddlr marketplace first, then install the paddlr plugin in two separate commands.",
          steps: [
            {
              title: "Step 1 — Add the Paddlr marketplace catalog",
              lang: "bash",
              command: "codex plugin marketplace add https://github.com/thanhdt942/paddlr"
            },
            {
              title: "Step 2 — Install the Paddlr plugin",
              lang: "bash",
              command: "codex plugin add paddlr"
            }
          ]
        }
      ],
      verification: {
        note: "Confirm Paddlr is discovered in your Codex marketplace catalog:",
        lang: "bash",
        command: "codex plugin list --marketplace paddlr --available"
      },
      usage: {
        note: "Run a Paddlr engineering skill inside your Codex session:",
        command: "/pdl:sre-debugging Investigate intermittent timeout in worker queue"
      },
      docAnchor: "#doc-installation"
    }
  };

  /* =========================================================================
     2. Theme Toggle (Light / Dark)
     ========================================================================= */
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
      } catch (e) {}
    });
  }

  /* =========================================================================
     3. Mobile Navigation Drawer
     ========================================================================= */
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
      setMobileMenu(!mobileNav.classList.contains("is-open"));
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
  }

  /* =========================================================================
     4. Interactive Agent Compatibility & Installation Hub
     ========================================================================= */
  var selectedAgentId = "claude";
  var selectedMethodIndex = 0;

  var agentHub = document.getElementById("agent-hub");
  var agentDirectory = document.getElementById("agent-directory");
  var workbench = document.getElementById("agent-workbench");
  var agentCards = Array.prototype.slice.call(document.querySelectorAll(".agent-card[data-agent]"));

  var wbName = document.getElementById("wb-agent-name");
  var wbStatus = document.getElementById("wb-agent-status");
  var wbManifest = document.getElementById("wb-agent-manifest");
  var wbDesc = document.getElementById("wb-agent-desc");
  var wbMethodSwitcher = document.getElementById("wb-method-switcher");
  var wbPrereqs = document.getElementById("wb-prereqs");
  var wbMethodNote = document.getElementById("wb-method-note");
  var wbCmdSteps = document.getElementById("wb-cmd-steps");
  var wbVerifyNote = document.getElementById("wb-verify-note");
  var wbVerifyLang = document.getElementById("wb-verify-lang");
  var wbVerifyCmd = document.getElementById("wb-verify-cmd");
  var wbUsageNote = document.getElementById("wb-usage-note");
  var wbUsageCmd = document.getElementById("wb-usage-cmd");
  var wbDocLink = document.getElementById("wb-doc-link");

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /**
   * Position the installation workbench:
   * - On mobile (<= 768px): place directly beneath the selected agent card inside #agent-directory
   * - On desktop (> 768px): place directly beneath #agent-directory inside #agent-hub
   */
  function positionWorkbenchForViewport() {
    if (!agentHub || !agentDirectory || !workbench) return;
    var activeCard = document.querySelector('.agent-card[data-agent="' + selectedAgentId + '"]');
    if (window.innerWidth <= 768 && activeCard && activeCard.parentNode === agentDirectory) {
      activeCard.insertAdjacentElement("afterend", workbench);
    } else if (workbench.parentNode !== agentHub) {
      agentHub.appendChild(workbench);
    }
  }

  function renderWorkbench() {
    var agent = AGENTS_CATALOG[selectedAgentId];
    if (!agent || !workbench) return;

    var methods = agent.methods || [];
    if (selectedMethodIndex >= methods.length) {
      selectedMethodIndex = 0;
    }
    var activeMethod = methods[selectedMethodIndex];

    // 1. Update card selection states
    agentCards.forEach(function (card) {
      var isSelected = card.getAttribute("data-agent") === selectedAgentId;
      card.classList.toggle("is-selected", isSelected);
      card.setAttribute("aria-selected", String(isSelected));
      card.setAttribute("tabindex", isSelected ? "0" : "-1");
    });

    // 2. Update header info
    if (wbName) wbName.textContent = agent.name;
    if (wbStatus) {
      wbStatus.innerHTML = '<span class="status-badge-dot" aria-hidden="true"></span>' + escapeHtml(agent.status);
    }
    if (wbManifest) wbManifest.textContent = agent.manifest;
    if (wbDesc) wbDesc.textContent = agent.description;

    // 3. Render secondary method switcher if agent has >1 method
    if (wbMethodSwitcher) {
      if (methods.length > 1) {
        wbMethodSwitcher.hidden = false;
        var html = '<span class="method-label">Method:</span>';
        methods.forEach(function (m, idx) {
          var activeClass = idx === selectedMethodIndex ? " is-active" : "";
          html +=
            '<button class="method-btn' +
            activeClass +
            '" type="button" role="tab" aria-selected="' +
            String(idx === selectedMethodIndex) +
            '" data-method-index="' +
            idx +
            '">' +
            escapeHtml(m.label) +
            "</button>";
        });
        wbMethodSwitcher.innerHTML = html;
      } else {
        wbMethodSwitcher.hidden = true;
        wbMethodSwitcher.innerHTML = "";
      }
    }

    // 4. Render prerequisites
    if (wbPrereqs) {
      wbPrereqs.innerHTML = agent.prerequisites
        .map(function (item) {
          return "<li>" + escapeHtml(item) + "</li>";
        })
        .join("");
    }

    // 5. Render method note & step-by-step command blocks (each command separate!)
    if (wbMethodNote && activeMethod) {
      wbMethodNote.textContent = activeMethod.note;
    }

    if (wbCmdSteps && activeMethod) {
      wbCmdSteps.innerHTML = activeMethod.steps
        .map(function (step) {
          return (
            '<div class="cmd-step">' +
            '<div class="cmd-step-label">' +
            escapeHtml(step.title) +
            "</div>" +
            '<div class="code-block">' +
            '<div class="code-header">' +
            '<span class="code-lang">' +
            escapeHtml(step.lang) +
            "</span>" +
            '<button class="copy-btn" type="button" data-copy>Copy</button>' +
            "</div>" +
            "<pre><code>" +
            escapeHtml(step.command) +
            "</code></pre>" +
            "</div>" +
            "</div>"
          );
        })
        .join("");
    }

    // 6. Render verification, usage example, and doc link
    if (wbVerifyNote) wbVerifyNote.textContent = agent.verification.note;
    if (wbVerifyLang) wbVerifyLang.textContent = agent.verification.lang;
    if (wbVerifyCmd) wbVerifyCmd.textContent = agent.verification.command;
    if (wbUsageNote) wbUsageNote.textContent = agent.usage.note;
    if (wbUsageCmd) wbUsageCmd.textContent = agent.usage.command;
    if (wbDocLink) wbDocLink.setAttribute("href", agent.docAnchor || "#docs");

    positionWorkbenchForViewport();
  }

  function selectAgent(agentId) {
    if (!AGENTS_CATALOG[agentId]) return;
    selectedAgentId = agentId;
    selectedMethodIndex = 0;
    renderWorkbench();
  }

  // Card click & keyboard navigation
  agentCards.forEach(function (card, index) {
    card.addEventListener("click", function () {
      selectAgent(card.getAttribute("data-agent"));
    });

    card.addEventListener("keydown", function (event) {
      var targetIdx = null;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") {
        targetIdx = (index + 1) % agentCards.length;
      } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
        targetIdx = (index - 1 + agentCards.length) % agentCards.length;
      } else if (event.key === "Home") {
        targetIdx = 0;
      } else if (event.key === "End") {
        targetIdx = agentCards.length - 1;
      }

      if (targetIdx !== null) {
        event.preventDefault();
        var nextCard = agentCards[targetIdx];
        selectAgent(nextCard.getAttribute("data-agent"));
        nextCard.focus();
      }
    });
  });

  // Secondary installation method click delegation (preserves selected agent)
  if (wbMethodSwitcher) {
    wbMethodSwitcher.addEventListener("click", function (event) {
      var btn = event.target.closest("[data-method-index]");
      if (!btn) return;
      var idx = parseInt(btn.getAttribute("data-method-index"), 10);
      if (!isNaN(idx)) {
        selectedMethodIndex = idx;
        renderWorkbench();
      }
    });
  }

  // Hero quick-select agent links (data-select-agent)
  document.querySelectorAll("[data-select-agent]").forEach(function (link) {
    link.addEventListener("click", function () {
      var targetAgent = link.getAttribute("data-select-agent");
      if (targetAgent) {
        selectAgent(targetAgent);
      }
    });
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 768 && mobileNav && mobileNav.classList.contains("is-open")) {
      setMobileMenu(false);
    }
    positionWorkbenchForViewport();
  });

  // Initialize workbench state
  renderWorkbench();

  /* =========================================================================
     5. Delegated Copy-to-Clipboard for All Static & Dynamic Code Blocks
     ========================================================================= */
  function copyTextToClipboard(text) {
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

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-copy]");
    if (!button) return;

    var block = button.closest(".code-block");
    var codeEl = block ? block.querySelector("pre code") : null;
    if (!codeEl) return;

    var text = codeEl.textContent.trim();
    copyTextToClipboard(text)
      .then(function () {
        button.textContent = "Copied!";
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

  /* =========================================================================
     6. Scroll-Spy Active Navigation Highlighting (Primary Nav & Docs Nav)
     ========================================================================= */
  if ("IntersectionObserver" in window) {
    var topNavLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
    var docNavLinks = Array.prototype.slice.call(document.querySelectorAll('.docs-nav a[href^="#"]'));

    function observeTargets(links, rootMargin) {
      var targets = links
        .map(function (link) {
          var href = link.getAttribute("href");
          return href ? document.querySelector(href) : null;
        })
        .filter(Boolean);

      if (targets.length === 0) return;

      var obs = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              var activeHref = "#" + entry.target.id;
              links.forEach(function (link) {
                link.classList.toggle("is-active", link.getAttribute("href") === activeHref);
              });
            }
          });
        },
        { rootMargin: rootMargin, threshold: 0 }
      );

      targets.forEach(function (el) {
        obs.observe(el);
      });
    }

    observeTargets(topNavLinks, "-25% 0px -65% 0px");
    observeTargets(docNavLinks, "-20% 0px -65% 0px");
  }
})();
