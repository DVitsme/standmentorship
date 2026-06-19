import { defineCloudflareConfig } from "@opennextjs/cloudflare";

// No incremental cache configured yet. If/when we adopt ISR or `use cache`,
// add an R2 (or KV) incremental-cache override here and the matching binding
// in wrangler.jsonc.
export default defineCloudflareConfig({});
