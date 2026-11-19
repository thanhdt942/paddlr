/**
 * Paddlr — OpenCode Plugin TypeScript Definitions
 *
 * Reference: https://opencode.ai/docs/plugins
 */

export interface OpenCodeContext {
  directory?: string;
  worktree?: string;
  project?: {
    name?: string;
    path?: string;
  };
  client?: {
    app?: {
      log?: (entry: { body: { level: string; message: string } }) => void;
    };
  };
  $?: any;
}

export interface OpenCodeToolDefinition {
  description: string;
  args?: Record<string, { type: string; description?: string; required?: boolean }>;
  execute: (args?: any) => Promise<string | object>;
}

export interface OpenCodePluginHooks {
  event?: (payload: { event: { type: string; [key: string]: any } }) => Promise<void>;
  "experimental.chat.system.transform"?: (input: any, output: { system: string[] }) => Promise<void>;
  "tool.execute.before"?: (input: { tool: string; [key: string]: any }, output: { args: any }) => Promise<void>;
  tool?: Record<string, OpenCodeToolDefinition>;
}

export interface OpenCodePluginV2Definition {
  id: string;
  name: string;
  version: string;
  description: string;
  setup: (ctx?: OpenCodeContext) => Promise<OpenCodePluginHooks>;
  effect?: (ctx?: OpenCodeContext) => Promise<OpenCodePluginHooks>;
}

export declare const BOOTSTRAP_CONTEXT: string;
export declare function setup(ctx?: OpenCodeContext): Promise<OpenCodePluginHooks>;
export declare const PaddlrPlugin: OpenCodePluginV2Definition;
export declare const HolyShitItWorksPlugin: OpenCodePluginV2Definition;
export declare const Plugin: OpenCodePluginV2Definition;
export declare const plugin: OpenCodePluginV2Definition;
export default PaddlrPlugin;
