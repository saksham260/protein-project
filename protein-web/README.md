# Protein Discovery Engine — Web Frontend

Consumer-facing web application built with **Next.js 16 (App Router)**, **React 19**, **TypeScript**, and **Tailwind CSS**.

---

## Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Environment Configuration
Copy the template:
```bash
cp .env.local.example .env.local
```
Fill in your Supabase project credentials:
```env
NEXT_PUBLIC_SUPABASE_URL=https://<your-project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-publishable-or-anon-key>
REVALIDATE_SECRET=<shared-secret-with-etl>
```
*(Note: If credentials are not supplied, the app transparently falls back to the local seed catalog).*

### 3. Verify Connection
Run the pre-flight connection check to ensure your Supabase Data API and RLS policies are reachable:
```bash
npm run check:supabase
```

### 4. Run Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 5. Running Tests & Quality Checks
```bash
npm test              # Run Vitest test suite
npx tsc --noEmit      # Type-check TypeScript
npm run build         # Validate Next.js production build & SSG prerendering
```
