/**
 * Paddlr — OpenCode Plugin Standard Conformance
 *
 * Conforms to OpenCode plugin specification:
 * - Reference: https://opencode.ai/docs/plugins
 * - Supports OpenCode v2 (@opencode/plugin) with default export { id, setup }
 * - Supports OpenCode v1 (@opencode-ai/plugin) with callable function export
 * - Exposes Paddlr tools: pdl_scan, pdl_bootstrap, pdl_status (with backwards-compatible hsiw_* aliases)
 * - Exposes lifecycle hooks: event, tool.execute.before, experimental.chat.system.transform
 */

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export const BOOTSTRAP_CONTEXT = `=== Paddlr Engineering Discipline Active ===
You are operating with the Paddlr software engineering framework.
Tagline: Simple on the Surface. Sophisticated Underneath.
Philosophy: Handle the complexity. Simplify the experience.
Authority / Source of Truth: rules/AGENTS.md

Core Operating Principles:
1. UNDERSTAND BEFORE MODIFYING: Discover repository conventions, architecture, and dependencies.
2. CLARIFY BEFORE ASSUMING: Disclose ambiguities in requirements early.
3. INCREMENTAL IMPLEMENTATION: Work in small, self-contained, verifiable slices (Red-Green-Refactor).
4. EVIDENCE-BASED VERIFICATION: Never report success without capturing concrete command output (PASS/FAIL).
5. PERSISTENT CONTEXT & PLANS: Maintain project context, ADRs (docs/paddlr/DECISIONS.md), feature specs (docs/paddlr/specs/), and plans (docs/paddlr/plans/) in docs/paddlr/. Always create a new plan file for each new request. Never store plans solely in ephemeral IDE chat artifacts.

Available Skills:
- skills/feature-development: Orchestrate end-to-end feature delivery coordinating all companion skills
- skills/writing-specs: Clarify requirements and draft reviewable feature specifications in docs/paddlr/specs/
- skills/writing-plans: Decompose approved specifications into verifiable, contract-first implementation plans in docs/paddlr/plans/
- skills/test-driven-development: Implement code strictly test-first (RED -> GREEN -> REFACTOR)
- skills/sre-debugging: Systematic root cause analysis and scientific troubleshooting for bugs and failures
- skills/code-review: Independent, read-only code review before merging or completing tasks
- skills/release-management: Manage software release lifecycle and persist release conventions in RELEASE.md
- skills/skill-creator: Design, draft, verify, and package reusable AI agent skills

CRITICAL: Before writing or modifying application code, check which Paddlr skill applies to your task.
===========================================================`;

/**
 * Core plugin setup / handler function compatible with both OpenCode v1 and v2.
 * @param {object} ctx - OpenCode context (project, directory, worktree, client, app, $)
 */
export async function setup(ctx = {}) {
  const targetDir = ctx.directory || ctx.worktree || process.cwd();

  const toolBootstrap = {
    description: "Returns the Paddlr engineering discipline instructions and operating principles.",
    args: {},
    execute: async () => {
      return BOOTSTRAP_CONTEXT;
    },
  };

  const toolStatus = {
    description: "Inspects docs/paddlr persistent project memory (PROGRESS.md, PLAN.md, DECISIONS.md) in the active repository.",
    args: {
      path: {
        type: "string",
        description: "Optional repository path (defaults to current working directory)",
      },
    },
    execute: async (args = {}) => {
      const root = args.path ? resolve(args.path) : targetDir;
      const candidatePaddlr = join(root, "docs", "paddlr");
      const candidateDocsHsiw = join(root, "docs", "hsiw");
      const candidateDotPdl = join(root, ".pdl");
      const candidateDotHsiw = join(root, ".hsiw");

      let memoryDir = null;
      if (existsSync(candidatePaddlr)) {
        memoryDir = candidatePaddlr;
      } else if (existsSync(candidateDocsHsiw)) {
        memoryDir = candidateDocsHsiw;
      } else if (existsSync(candidateDotPdl)) {
        memoryDir = candidateDotPdl;
      } else if (existsSync(candidateDotHsiw)) {
        memoryDir = candidateDotHsiw;
      }

      if (!memoryDir) {
        return JSON.stringify({
          initialized: false,
          message: "Repository is not initialized with docs/paddlr project memory. Run onboarding to initialize.",
        }, null, 2);
      }

      const files = ["PROGRESS.md", "PLAN.md", "DECISIONS.md", "PROJECT.md"];
      const summary = { initialized: true, root, memoryDir, files: {} };

      for (const file of files) {
        const filePath = join(memoryDir, file);
        if (existsSync(filePath)) {
          const content = readFileSync(filePath, "utf-8");
          summary.files[file] = {
            exists: true,
            lines: content.split("\n").length,
            preview: content.split("\n").slice(0, 10).join("\n"),
          };
        } else {
          summary.files[file] = { exists: false };
        }
      }

      return JSON.stringify(summary, null, 2);
    },
  };

  const toolScan = {
    description: "Scans repository structure, technology stacks, entrypoints, and test frameworks using the Paddlr scanner.",
    args: {
      path: {
        type: "string",
        description: "Path to repository root to scan (defaults to current working directory)",
      },
      depth: {
        type: "number",
        description: "Maximum scan depth (default: 3)",
      },
    },
    execute: async (args = {}) => {
      const scanPath = args.path ? resolve(args.path) : targetDir;
      const depth = args.depth || 3;
      const scannerScript = join(__dirname, "scripts", "scan_repo.py");

      if (existsSync(scannerScript)) {
        const py = process.platform === "win32" ? "python" : "python3";
        const res = spawnSync(py, [scannerScript, scanPath, "--json", "--depth", String(depth)], {
          encoding: "utf-8",
          maxBuffer: 10 * 1024 * 1024,
        });

        if (res.status === 0 && res.stdout) {
          return res.stdout.trim();
        }
      }

      return JSON.stringify({
        target: scanPath,
        status: "scanned",
        note: "Scanner script fallback: inspect files directly or run scripts/scan_repo.py",
      }, null, 2);
    },
  };

  return {
    event: async ({ event }) => {
      if (event && event.type === "session.created") {
        if (ctx.client?.app?.log) {
          ctx.client.app.log({
            body: {
              level: "info",
              message: "Paddlr engineering discipline active for session",
            },
          });
        }
      }
    },

    "experimental.chat.system.transform": async (input, output) => {
      if (output && Array.isArray(output.system)) {
        output.system.push(BOOTSTRAP_CONTEXT);
      }
    },

    "tool.execute.before": async (input, output) => {
      // Evidence-based safety guard: warn or log before potentially destructive tool commands
      if (input && input.tool === "bash" && output?.args?.command) {
        const cmd = String(output.args.command);
        if (
          cmd.includes("git reset --hard") ||
          cmd.includes("git clean -fd") ||
          cmd.includes("git push --force")
        ) {
          throw new Error(
            "[Paddlr Guardrail] Destructive Git command blocked by rules/AGENTS.md. " +
              "Never run destructive git operations without explicit user confirmation."
          );
        }
      }
    },

    tool: {
      pdl_bootstrap: toolBootstrap,
      pdl_status: toolStatus,
      pdl_scan: toolScan,
      // Backwards compatibility aliases
      hsiw_bootstrap: toolBootstrap,
      hsiw_status: toolStatus,
      hsiw_scan: toolScan,
    },
  };
}

/**
 * OpenCode V2 plugin definition object.
 */
const pluginDef = {
  id: "paddlr",
  name: "Paddlr",
  version: "1.0.0",
  description: "Agent-agnostic software engineering framework. Simple on the surface, sophisticated underneath.",
  setup,
  effect: setup,
};

// Callable function wrapper for OpenCode V1 backward compatibility
async function callablePlugin(ctx) {
  return setup(ctx);
}

callablePlugin.id = pluginDef.id;
pluginDef.default = pluginDef;
callablePlugin.setup = setup;
callablePlugin.effect = setup;

export const PaddlrPlugin = pluginDef;
export const HolyShitItWorksPlugin = pluginDef;
export { pluginDef as Plugin, pluginDef as plugin };
export default pluginDef;
