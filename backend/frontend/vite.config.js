import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  root: 'app', // Your HTML lives here
  base: './',  // Makes relative paths work for favicon, CSS, JS
  server: {
    port: 5173,      // Local dev server port
    open: true,      // Automatically opens browser
    strictPort: true // Fails if port is taken
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'app') // Optional: use @ to reference app/ folder
    }
  },
  build: {
    outDir: '../dist', // Output folder relative to frontend/
    emptyOutDir: true, // Clear folder on rebuild
  }
});
