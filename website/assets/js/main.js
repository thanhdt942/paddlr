/*
 * Paddlr landing page UI logic: i18n, installer tabs, clipboard copy, and theme toggle.
 * Data lives in assets/js/i18n.js (window.PADDLR_I18N).
 */

const { SUPPORTED_LOCALES, STRINGS, AGENTS } = window.PADDLR_I18N;

let currentLang = "en";
let installerApi = null;
let themeApi = null;

function t(key, lang = currentLang) {
  const dict = STRINGS[lang] || STRINGS.en;
  if (Object.prototype.hasOwnProperty.call(dict, key)) return dict[key];
  return STRINGS.en[key] || "";
}

function pickLocalized(value, lang = currentLang) {
  if (value && typeof value === "object" && !Array.isArray(value)) {
    return value[lang] !== undefined ? value[lang] : value.en;
  }
  return value;
}

function resolveInitialLang() {
  const params = new URLSearchParams(window.location.search);
  const queryLang = params.get("lang");
  if (queryLang && SUPPORTED_LOCALES.includes(queryLang)) return queryLang;

  try {
    const saved = localStorage.getItem("paddlr-lang");
    if (saved && SUPPORTED_LOCALES.includes(saved)) return saved;
  } catch {
    // Ignore storage read errors in private browsing.
  }

  const browserLang = (navigator.language || "").toLowerCase();
  return browserLang.startsWith("vi") ? "vi" : "en";
}

function applyLanguage(lang, { persist = false, announce = false } = {}) {
  const next = SUPPORTED_LOCALES.includes(lang) ? lang : "en";
  currentLang = next;
  document.documentElement.lang = next;

  document.title = t("meta.title", next);
  const desc = document.querySelector('meta[name="description"]');
  if (desc) desc.setAttribute("content", t("meta.description", next));
  const ogTitle = document.querySelector('meta[property="og:title"]');
  if (ogTitle) ogTitle.setAttribute("content", t("meta.ogTitle", next));
  const ogDesc = document.querySelector('meta[property="og:description"]');
  if (ogDesc) ogDesc.setAttribute("content", t("meta.ogDescription", next));

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const key = node.getAttribute("data-i18n");
    if (node.classList.contains("copy") && node.classList.contains("is-done")) return;
    node.textContent = t(key, next);
  });

  document.querySelectorAll("[data-i18n-html]").forEach((node) => {
    const key = node.getAttribute("data-i18n-html");
    node.innerHTML = t(key, next);
  });

  document.querySelectorAll("[data-i18n-aria-label]").forEach((node) => {
    const key = node.getAttribute("data-i18n-aria-label");
    node.setAttribute("aria-label", t(key, next));
  });

  document.querySelectorAll("[data-lang-btn]").forEach((btn) => {
    const active = btn.getAttribute("data-lang-btn") === next;
    btn.setAttribute("aria-pressed", String(active));
  });

  if (themeApi) themeApi.syncLabel();
  if (installerApi) installerApi.rerender();

  if (persist) {
    try {
      localStorage.setItem("paddlr-lang", next);
    } catch {
      // Storage may be unavailable in private browsing.
    }

    const url = new URL(window.location.href);
    if (url.searchParams.has("lang")) {
      url.searchParams.set("lang", next);
      history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
    }
  }

  if (announce) {
    const live = document.querySelector("[data-live]");
    if (live) live.textContent = t(next === "vi" ? "lang.liveVi" : "lang.liveEn", next);
  }
}

function initLanguage() {
  document.querySelectorAll("[data-lang-btn]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetLang = btn.getAttribute("data-lang-btn");
      if (targetLang && targetLang !== currentLang) {
        applyLanguage(targetLang, { persist: true, announce: true });
      }
    });
  });
}

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
      el("button", { class: "copy", type: "button", text: t("copy.idle") }),
    ]),
    el("pre", {}, el("code", { text: cmd })),
  ]);
}

function renderPanel(agent) {
  const nodes = [];
  const title = agent.fullName || agent.name;
  const statusLabel = t(`status.${agent.status}`);

  nodes.push(
    el("div", { class: "panel-head" }, [
      el("h3", { text: title }),
      el("span", { class: `status status--${agent.status}`, text: statusLabel }),
    ])
  );

  if (agent.status === "planned") {
    nodes.push(el("p", { class: "muted", text: `${title} ${t("install.planned")}` }));
    return nodes;
  }

  const prerequisites = pickLocalized(agent.prerequisites);
  if (prerequisites && prerequisites.length) {
    nodes.push(
      el("div", { class: "block" }, [
        el("h4", { text: t("install.prerequisites") }),
        el("ul", {}, prerequisites.map((p) => el("li", { text: p }))),
      ])
    );
  }

  agent.methods.forEach((method, i) => {
    const label = pickLocalized(method.label);
    const note = pickLocalized(method.note);
    const heading =
      agent.methods.length > 1
        ? `${t("install.option")} ${i + 1}: ${label}`
        : t("install.install");

    const hasSteps = Array.isArray(method.steps) && method.steps.length > 0;
    const stepsList = hasSteps
      ? el(
          "ol",
          { class: "steps" },
          method.steps.map((step, n) =>
            el("li", {}, [
              method.steps.length > 1
                ? el("span", { class: "step-label", text: `${t("install.step")} ${n + 1}` })
                : null,
              codeBlock(step.where, step.cmd),
            ])
          )
        )
      : null;

    nodes.push(
      el("div", { class: "block" }, [
        el("h4", { text: heading }),
        note ? el("p", { class: "muted", text: note }) : null,
        stepsList,
      ])
    );
  });

  if (agent.verify) {
    nodes.push(
      el("div", { class: "block" }, [
        el("h4", { text: t("install.verify") }),
        codeBlock(agent.verify.where, agent.verify.cmd),
        el("p", { class: "muted", text: pickLocalized(agent.verify.text) }),
      ])
    );
  }

  if (agent.docs) {
    const docsLabel = pickLocalized(agent.docs.label);
    nodes.push(
      el("p", { class: "block" }, el("a", { href: agent.docs.href, text: `${docsLabel} →` }))
    );
  }

  return nodes;
}

function initInstaller(root) {
  const tablist = root.querySelector("[data-tablist]");
  const panel = root.querySelector("[data-panel]");
  let activeIndex = 0;

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
    activeIndex = index;
    tabs.forEach((tab, i) => {
      const active = i === index;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
    });
    panel.setAttribute("aria-labelledby", tabs[index].id);
    panel.replaceChildren(...renderPanel(AGENTS[index]));
    if (focus) tabs[index].focus();
    if (updateHash) {
      const url = new URL(window.location.href);
      history.replaceState(null, "", `${url.pathname}${url.search}#${AGENTS[index].id}`);
    }
  }

  function rerender() {
    panel.replaceChildren(...renderPanel(AGENTS[activeIndex]));
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

  function selectFromHash() {
    const index = AGENTS.findIndex((a) => `#${a.id}` === location.hash);
    if (index < 0) return false;
    select(index, { updateHash: false });
    root.closest("section").scrollIntoView();
    return true;
  }

  if (!selectFromHash()) select(0, { updateHash: false });
  window.addEventListener("hashchange", selectFromHash);

  return { rerender };
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
      button.textContent = t("copy.done");
      button.classList.add("is-done");
      if (live) live.textContent = t("copy.liveDone");
    } catch {
      button.textContent = t("copy.fallback");
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      if (live) live.textContent = t("copy.liveFail");
    }
    clearTimeout(button._timer);
    button._timer = setTimeout(() => {
      button.textContent = t("copy.idle");
      button.classList.remove("is-done");
    }, 1800);
  });
}

/* ---------- Theme ---------- */

function initTheme() {
  const toggle = document.querySelector("[data-theme-toggle]");
  if (!toggle) return null;

  const root = document.documentElement;
  const meta = document.querySelector('meta[name="theme-color"]');
  const live = document.querySelector("[data-live]");
  const mq = window.matchMedia("(prefers-color-scheme: dark)");

  function syncLabel() {
    const dark = root.getAttribute("data-theme") === "dark";
    toggle.setAttribute("aria-label", dark ? t("theme.toLight") : t("theme.toDark"));
  }

  function apply(theme, announce = false) {
    const dark = theme === "dark";
    root.setAttribute("data-theme", theme);
    toggle.setAttribute("aria-pressed", String(dark));
    syncLabel();
    if (meta) meta.setAttribute("content", dark ? "#0f1115" : "#ffffff");
    if (announce && live) live.textContent = dark ? t("theme.liveDark") : t("theme.liveLight");
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

  return { syncLabel };
}

document.addEventListener("DOMContentLoaded", () => {
  currentLang = resolveInitialLang();
  themeApi = initTheme();
  const installer = document.querySelector("[data-installer]");
  if (installer) installerApi = initInstaller(installer);
  initLanguage();
  applyLanguage(currentLang, { persist: false, announce: false });
  initCopy();
});
