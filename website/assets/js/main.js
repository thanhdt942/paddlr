/*
 * Paddlr landing page.
 * Agent install data lives in AGENTS; rendering and interaction below it.
 * To add an agent, append an entry to AGENTS. No markup changes needed.
 */

const REPO = "https://github.com/thanhdt942/paddlr";

/**
 * status: "supported" | "experimental" | "planned"
 * methods[].steps[]: one entry per command that must be run separately.
 * steps[].where: label shown above the block (e.g. "Terminal").
 */
const AGENTS = [
  {
    id: "claude-code",
    name: "Claude Code",
    status: "supported",
    prerequisites: ["Claude Code with plugin support (the /plugin command)."],
    methods: [
      {
        label: "One step",
        note: "Run inside a Claude Code session. Adds the Paddlr marketplace and installs the plugin.",
        steps: [{ where: "Claude Code", cmd: "/plugin install paddlr --marketplace thanhdt942/paddlr" }],
      },
      {
        label: "Two steps",
        note: "For Claude Code versions without the --marketplace flag.",
        steps: [
          { where: "Claude Code", cmd: "/plugin marketplace add thanhdt942/paddlr" },
          { where: "Claude Code", cmd: "/plugin install paddlr@paddlr" },
        ],
      },
    ],
    verify: { text: "paddlr@paddlr should show as enabled.", where: "Terminal", cmd: "claude plugin list" },
    docs: { label: "Installation guide", href: `${REPO}#claude-code` },
  },
  {
    id: "codex",
    name: "Codex",
    status: "supported",
    prerequisites: ["OpenAI Codex CLI with plugin support (codex plugin)."],
    methods: [
      {
        label: "Codex CLI",
        note: "Add the Paddlr marketplace, then install the plugin from it.",
        steps: [
          { where: "Terminal", cmd: "codex plugin marketplace add thanhdt942/paddlr" },
          { where: "Terminal", cmd: "codex plugin add paddlr@paddlr" },
        ],
      },
    ],
    verify: { text: "paddlr@paddlr should show as installed, enabled.", where: "Terminal", cmd: "codex plugin list" },
    docs: null,
  },
  {
    id: "opencode",
    name: "OpenCode",
    status: "supported",
    prerequisites: ["OpenCode CLI.", "Git, to fetch the plugin from GitHub."],
    methods: [
      {
        label: "OpenCode CLI",
        note: "Run in your project. Adds Paddlr to .opencode/opencode.json. Add -g to install globally.",
        steps: [{ where: "Terminal", cmd: "opencode plugin paddlr@git+https://github.com/thanhdt942/paddlr.git" }],
      },
      {
        label: "Config file",
        note: "Or add Paddlr to the plugin list in your opencode.json.",
        steps: [
          {
            where: "opencode.json",
            cmd: '{\n  "$schema": "https://opencode.ai/config.json",\n  "plugin": ["paddlr@git+https://github.com/thanhdt942/paddlr.git"]\n}',
          },
        ],
      },
    ],
    verify: {
      text: "The agent should call the pdl_bootstrap tool and print Paddlr's operating principles.",
      where: "Terminal",
      cmd: 'opencode run "Show me the Paddlr engineering discipline bootstrap context"',
    },
    docs: { label: "OpenCode details and exposed tools", href: `${REPO}/blob/HEAD/.opencode/INSTALL.md` },
  },
  {
    id: "antigravity",
    name: "Antigravity",
    fullName: "Google Antigravity",
    status: "supported",
    prerequisites: ["Google Antigravity CLI (agy)."],
    methods: [
      {
        label: "agy CLI",
        note: "Installs the skills, rules, and session-start hook.",
        steps: [{ where: "Terminal", cmd: "agy plugin install https://github.com/thanhdt942/paddlr" }],
      },
    ],
    verify: { text: "paddlr should be listed as enabled.", where: "Terminal", cmd: "agy plugin list" },
    docs: { label: "Installation guide", href: `${REPO}#google-antigravity-agy` },
  },
];

const STATUS_LABELS = {
  supported: "Supported",
  experimental: "Experimental",
  planned: "Planned",
};

/* ---------- Rendering ---------- */

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value === null || value === undefined || value === false) continue;
    if (key === "text") node.textContent = value;
    else node.setAttribute(key, value === true ? "" : value);
  }
  for (const child of [].concat(children)) {
    if (child) node.append(child);
  }
  return node;
}

function codeBlock(where, cmd) {
  return el("div", { class: "code", "data-code": true }, [
    el("div", { class: "code-head" }, [
      el("span", { text: where }),
      el("button", { class: "copy", type: "button", text: "Copy" }),
    ]),
    el("pre", {}, el("code", { text: cmd })),
  ]);
}

function renderPanel(agent) {
  const nodes = [];
  const title = agent.fullName || agent.name;

  nodes.push(
    el("div", { class: "panel-head" }, [
      el("h3", { text: title }),
      el("span", { class: `status status--${agent.status}`, text: STATUS_LABELS[agent.status] }),
    ])
  );

  if (agent.status === "planned") {
    nodes.push(el("p", { class: "muted", text: `${title} support is planned and not installable yet.` }));
    return nodes;
  }

  if (agent.prerequisites && agent.prerequisites.length) {
    nodes.push(
      el("div", { class: "block" }, [
        el("h4", { text: "Prerequisites" }),
        el("ul", {}, agent.prerequisites.map((p) => el("li", { text: p }))),
      ])
    );
  }

  agent.methods.forEach((method, i) => {
    const heading = agent.methods.length > 1 ? `Option ${i + 1}: ${method.label}` : "Install";
    const steps = method.steps.map((step, n) =>
      el("li", {}, [
        method.steps.length > 1 ? el("span", { class: "step-label", text: `Step ${n + 1}` }) : null,
        codeBlock(step.where, step.cmd),
      ])
    );
    nodes.push(
      el("div", { class: "block" }, [
        el("h4", { text: heading }),
        method.note ? el("p", { class: "muted", text: method.note }) : null,
        el("ol", { class: "steps" }, steps),
      ])
    );
  });

  if (agent.verify) {
    nodes.push(
      el("div", { class: "block" }, [
        el("h4", { text: "Verify" }),
        codeBlock(agent.verify.where, agent.verify.cmd),
        el("p", { class: "muted", text: agent.verify.text }),
      ])
    );
  }

  if (agent.docs) {
    nodes.push(el("p", { class: "block" }, el("a", { href: agent.docs.href, text: `${agent.docs.label} →` })));
  }

  return nodes;
}

function initInstaller(root) {
  const tablist = root.querySelector("[data-tablist]");
  const panel = root.querySelector("[data-panel]");
  const tabs = AGENTS.map((agent) =>
    el("button", {
      class: "tab",
      type: "button",
      role: "tab",
      id: `tab-${agent.id}`,
      "aria-controls": "install-panel",
      "data-agent": agent.id,
      text: agent.name,
    })
  );
  tablist.replaceChildren(...tabs);
  panel.id = "install-panel";

  function select(index, { focus = false, updateHash = true } = {}) {
    tabs.forEach((tab, i) => {
      const active = i === index;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
    });
    panel.setAttribute("aria-labelledby", tabs[index].id);
    panel.replaceChildren(...renderPanel(AGENTS[index]));
    if (focus) tabs[index].focus();
    if (updateHash) history.replaceState(null, "", `#${AGENTS[index].id}`);
  }

  tablist.addEventListener("click", (event) => {
    const tab = event.target.closest("[role=tab]");
    if (tab) select(tabs.indexOf(tab));
  });

  tablist.addEventListener("keydown", (event) => {
    const current = tabs.indexOf(document.activeElement);
    if (current < 0) return;
    const last = tabs.length - 1;
    const next = {
      ArrowRight: current === last ? 0 : current + 1,
      ArrowLeft: current === 0 ? last : current - 1,
      Home: 0,
      End: last,
    }[event.key];
    if (next === undefined) return;
    event.preventDefault();
    select(next, { focus: true });
  });

  // Deep link: #codex, #opencode, ... selects that agent and scrolls to the installer.
  function selectFromHash() {
    const index = AGENTS.findIndex((a) => `#${a.id}` === location.hash);
    if (index < 0) return false;
    select(index, { updateHash: false });
    root.closest("section").scrollIntoView();
    return true;
  }
  if (!selectFromHash()) select(0, { updateHash: false });
  window.addEventListener("hashchange", selectFromHash);
}

/* ---------- Copy to clipboard ---------- */

async function writeClipboard(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const area = el("textarea", { readonly: true, "aria-hidden": "true" });
  area.value = text;
  area.style.position = "fixed";
  area.style.opacity = "0";
  document.body.append(area);
  area.select();
  const ok = document.execCommand("copy");
  area.remove();
  if (!ok) throw new Error("Copy command failed");
}

function initCopy() {
  const live = document.querySelector("[data-live]");
  document.addEventListener("click", async (event) => {
    const button = event.target.closest(".copy");
    if (!button) return;
    const code = button.closest("[data-code]").querySelector("code");
    try {
      await writeClipboard(code.textContent);
      button.textContent = "Copied";
      button.classList.add("is-done");
      if (live) live.textContent = "Copied to clipboard";
    } catch {
      button.textContent = "Press Ctrl+C";
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      if (live) live.textContent = "Copy failed. Text selected, press Ctrl+C.";
    }
    clearTimeout(button._timer);
    button._timer = setTimeout(() => {
      button.textContent = "Copy";
      button.classList.remove("is-done");
    }, 1800);
  });
}

/* ---------- Theme ---------- */

function initTheme() {
  const toggle = document.querySelector("[data-theme-toggle]");
  if (!toggle) return;

  const root = document.documentElement;
  const meta = document.querySelector('meta[name="theme-color"]');
  const live = document.querySelector("[data-live]");
  const mq = window.matchMedia("(prefers-color-scheme: dark)");

  function apply(theme, announce = false) {
    const dark = theme === "dark";
    root.setAttribute("data-theme", theme);
    toggle.setAttribute("aria-pressed", String(dark));
    toggle.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    if (meta) meta.setAttribute("content", dark ? "#0f1115" : "#ffffff");
    if (announce && live) live.textContent = dark ? "Dark mode enabled" : "Light mode enabled";
  }

  const current = root.getAttribute("data-theme") || (mq.matches ? "dark" : "light");
  apply(current);

  toggle.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    apply(next, true);
    try {
      localStorage.setItem("paddlr-theme", next);
    } catch {
      // Storage may be unavailable in private browsing.
    }
  });

  mq.addEventListener("change", (event) => {
    try {
      if (localStorage.getItem("paddlr-theme")) return;
    } catch {
      // Ignore storage read errors.
    }
    apply(event.matches ? "dark" : "light");
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  const installer = document.querySelector("[data-installer]");
  if (installer) initInstaller(installer);
  initCopy();
});
