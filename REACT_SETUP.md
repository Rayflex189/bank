# React, Tailwind CSS, and shadcn/ui Setup Guide

This guide explains how to configure a React project structure with TypeScript, Tailwind CSS, and shadcn/ui in this codebase to run the integrated `glassmorphism-trust-hero.tsx` and `demo.tsx` components.

---

## 1. Project Initialization

If you are setting up a new React project in this repository, you can initialize a Vite + React + TypeScript app:

```bash
# Initialize Vite in a 'frontend' subdirectory
npx -y create-vite@latest frontend --template react-ts
cd frontend
npm install
```

---

## 2. Install Tailwind CSS

Install Tailwind CSS and its peer dependencies, then generate the configuration files:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Configure Tailwind Paths
Add the paths to all of your template files in your `tailwind.config.js` file:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}", // include components directory
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Add the Tailwind directives to your main CSS file (e.g., `src/index.css`):

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## 3. Configure TypeScript Path Aliases

To support path aliases (like `@/components/ui/...`), modify your `tsconfig.json` and `tsconfig.app.json` (or `tsconfig.paths.json`):

Update `tsconfig.app.json` under `compilerOptions`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*", "./*"]
    }
  }
}
```

If using Vite, install the `vite-tsconfig-paths` plugin or define paths in `vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./"),
    },
  },
})
```

---

## 4. Initialize shadcn/ui CLI

Run the shadcn-ui initialization command to configure your project structure:

```bash
npx shadcn-ui@latest init
```

During initialization, you will be prompted to configure paths. Make sure you set:
- **TypeScript**: Yes
- **Style sheet location**: `src/index.css`
- **Components alias**: `@/components`
- **Utility helper alias**: `@/lib/utils`

---

## 5. The Importance of the `/components/ui/` Directory

### Why we create `/components/ui/`
In a shadcn project, the default path for components is configured under `/components/ui/`. 

It is important to preserve this exact folder structure for the following reasons:
1. **Separation of Concerns**: It distinguishes low-level, reusable **UI primitive components** (e.g., buttons, dialogs, inputs, badges) from high-level, application-specific **composite layouts** (e.g., product cards, profile forms, hero sections).
2. **shadcn CLI Automation**: The `shadcn-ui` CLI is designed to automatically write newly added elements directly to the `components/ui` folder. If this folder is missing or incorrectly mapped, the CLI commands (like `npx shadcn-ui add button`) will fail or scatter components across your codebase.
3. **Consistency**: It standardizes import paths across the engineering team (e.g., `import { Button } from "@/components/ui/button"`), making code sharing and updates seamless.

---

## 6. Install NPM Dependencies

Run the following command in your React project root to install the icons library required by the hero component:

```bash
npm install lucide-react
```
