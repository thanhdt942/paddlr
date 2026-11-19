# Installing Paddlr on OpenCode

> **Simple on the Surface. Sophisticated Underneath.**  
> Specification Reference: [OpenCode Plugins Documentation](https://opencode.ai/docs/plugins)

Paddlr natively conforms to the OpenCode plugin specification (supporting both OpenCode v1 and v2 runtime loaders).

---

## 1. Quick Installation

### Option A: OpenCode CLI (Recommended)

Run in your terminal:

```bash
opencode plugin add paddlr@git+https://github.com/thanhdt942/paddlr.git
```

This installs the package and registers it in your global configuration.

### Option B: Configuration File (`opencode.json`)

Add Paddlr to your project or global `opencode.json` (or `opencode.jsonc`):

#### OpenCode v2 (`plugins` array):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "paddlr@git+https://github.com/thanhdt942/paddlr.git"
  ]
}
```

#### OpenCode v1 (`plugin` array):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "paddlr@git+https://github.com/thanhdt942/paddlr.git"
  ]
}
```

### Option C: Local Plugin Directory

If developing locally or working in an offline workspace:

1. Clone or submodule Paddlr into your project:
   ```bash
   git clone https://github.com/thanhdt942/paddlr.git
   ```
2. Place or link `.opencode/plugins/paddlr.js` in your repository:
   ```javascript
   export { default } from "./path/to/paddlr/index.js";
   ```

---

## 2. Capabilities & Tools Exposed

When the plugin is loaded, OpenCode gains access to:

| Capability | Type | Description |
|---|---|---|
| `pdl_bootstrap` | Tool | Injects the Paddlr Engineering Discipline prompt and operating principles. |
| `pdl_status` | Tool | Inspects `docs/paddlr/` persistent project memory (`PROGRESS.md`, `PLAN.md`, `DECISIONS.md`). |
| `pdl_scan` | Tool | Scans repository structure, entrypoints, and test frameworks via `scan_repo.py`. |
| `session.created` | Lifecycle Hook | Logs session activation and confirms Paddlr discipline is active. |
| `tool.execute.before` | Safety Hook | Blocks unconfirmed destructive Git operations (`git reset --hard`, `git push --force`). |
| `system.transform` | Context Hook | Injects core engineering principles into the agent's system prompt. |

*(Note: Legacy aliases `hsiw_bootstrap`, `hsiw_status`, and `hsiw_scan` are automatically retained for backward compatibility).*

---

## 3. Verifying Installation

Verify that the plugin is detected and functional:

```bash
opencode run "Show me the Paddlr engineering discipline bootstrap context"
```

The assistant will invoke `pdl_bootstrap` and navigate according to Paddlr skills.
