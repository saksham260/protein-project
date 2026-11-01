import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    environment: "node",
    globals: true,
  },
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "./src"),
      // Next.js handles this guard when bundling; plain Node has nothing to resolve it to.
      "server-only": path.resolve(import.meta.dirname, "./src/lib/testing/emptyModule.ts"),
    },
  },
});
