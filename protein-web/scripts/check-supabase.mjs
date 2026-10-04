// @ts-check
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createClient } from "@supabase/supabase-js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const webDir = path.resolve(__dirname, "..");
const envFile = path.join(webDir, ".env.local");

console.log("\n\x1b[36m=== Supabase Web (Anon / Publishable) Connection Check ===\x1b[0m\n");

if (!fs.existsSync(envFile)) {
  console.error("\x1b[31m❌ .env.local not found in protein-web!\x1b[0m");
  console.error("   Please create protein-web/.env.local from .env.local.example");
  process.exit(1);
}

// Simple parser for .env.local
const envContent = fs.readFileSync(envFile, "utf-8");
/** @type {Record<string, string>} */
const env = {};
for (const rawLine of envContent.split("\n")) {
  const line = rawLine.trim();
  if (!line || line.startsWith("#")) continue;
  const eqIdx = line.indexOf("=");
  if (eqIdx !== -1) {
    const key = line.slice(0, eqIdx).trim();
    const val = line.slice(eqIdx + 1).trim().replace(/^["']|["']$/g, "");
    env[key] = val;
  }
}

const url = env.NEXT_PUBLIC_SUPABASE_URL || "";
const key = env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

const placeholders = [
  "",
  "https://your-project.supabase.co",
  "https://placeholder-project.supabase.co",
  "placeholder-anon-key",
  "your-anon-key-here",
];

const isPlaceholder = (val) =>
  placeholders.includes(val) ||
  val.includes("placeholder") ||
  val.includes("your-project") ||
  val.includes("your-anon-key");

if (!url || isPlaceholder(url)) {
  console.error("\x1b[31m❌ NEXT_PUBLIC_SUPABASE_URL is missing or contains placeholder values.\x1b[0m");
  console.error(`   Current value: "${url}"`);
  console.error("   Please update protein-web/.env.local with your real project URL.");
  process.exit(1);
}

if (!key || isPlaceholder(key)) {
  console.error("\x1b[31m❌ NEXT_PUBLIC_SUPABASE_ANON_KEY is missing or contains placeholder values.\x1b[0m");
  console.error("   Please update protein-web/.env.local with your real Publishable/anon key.");
  process.exit(1);
}

const maskedKey = key.length > 14 ? key.slice(0, 10) + "..." + key.slice(-4) : "***";
console.log(`Target URL: \x1b[32m${url}\x1b[0m`);
console.log(`Publishable Key: \x1b[90m${maskedKey}\x1b[0m\n`);

const client = createClient(url, key);

let hasErrors = false;

async function runChecks() {
  // Check 1: Categories
  try {
    const { data, count, error } = await client
      .from("categories")
      .select("slug, name", { count: "exact" });
    if (error) throw error;
    console.log(`\x1b[32m✅ Categories table readable:\x1b[0m ${count ?? data?.length} rows found`);
  } catch (err) {
    hasErrors = true;
    console.error(`\x1b[31m❌ Categories read failed:\x1b[0m`, err?.message || err);
  }

  // Check 2: Products
  try {
    const { data, count, error } = await client
      .from("products")
      .select("id, name", { count: "exact" })
      .eq("is_active", true);
    if (error) throw error;
    console.log(`\x1b[32m✅ Products table readable:\x1b[0m ${count ?? data?.length} active products found`);
  } catch (err) {
    hasErrors = true;
    console.error(`\x1b[31m❌ Products read failed:\x1b[0m`, err?.message || err);
  }

  // Check 3: Product Variants
  let sampleVariantId = null;
  try {
    const { data, count, error } = await client
      .from("product_variants")
      .select("id, slug", { count: "exact" })
      .eq("is_active", true)
      .limit(1);
    if (error) throw error;
    if (data && data.length > 0) {
      sampleVariantId = data[0].id;
    }
    console.log(`\x1b[32m✅ Product variants readable:\x1b[0m ${count ?? (data ? data.length : 0)} rows found`);
  } catch (err) {
    hasErrors = true;
    console.error(`\x1b[31m❌ Product variants read failed:\x1b[0m`, err?.message || err);
  }

  // Check 4: Availability Reports (Anonymous Insert test if variants exist)
  if (sampleVariantId) {
    try {
      const { error: insertErr } = await client
        .from("availability_reports")
        .insert({
          variant_id: sampleVariantId,
          platform: "zepto",
          pincode: "560034",
          is_available: true,
        });
      if (insertErr) throw insertErr;
      console.log(`\x1b[32m✅ Availability reports anonymous insert permitted\x1b[0m`);
    } catch (err) {
      hasErrors = true;
      console.error(`\x1b[31m❌ Availability report insert failed:\x1b[0m`, err?.message || err);
    }
  } else {
    console.log(`\x1b[33mℹ️  No variants in database yet; skipping availability_reports insert test.\x1b[0m`);
  }

  // Check 5: Availability Summary View
  try {
    const { error } = await client.from("availability_summary").select("*").limit(5);
    if (error) throw error;
    console.log(`\x1b[32m✅ availability_summary view readable\x1b[0m`);
  } catch (err) {
    hasErrors = true;
    console.error(`\x1b[31m❌ availability_summary read failed:\x1b[0m`, err?.message || err);
  }

  if (hasErrors) {
    console.error("\n\x1b[31mPre-flight check failed! Please verify your Supabase SQL grants and policies.\x1b[0m\n");
    process.exit(1);
  } else {
    console.log("\n\x1b[32mAll web client checks passed successfully!\x1b[0m\n");
    process.exit(0);
  }
}

runChecks();
