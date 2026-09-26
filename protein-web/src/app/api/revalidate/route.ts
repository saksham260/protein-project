import { revalidatePath } from "next/cache";
import { timingSafeEqual } from "node:crypto";

/**
 * Called by the ETL price poller after it writes new prices.
 * Marks every page stale so the next visit rebuilds it with fresh data.
 */
export async function POST(request: Request) {
  const secret = process.env.REVALIDATE_SECRET;
  if (!secret) {
    return Response.json({ error: "REVALIDATE_SECRET is not configured" }, { status: 500 });
  }

  const provided = Buffer.from(request.headers.get("authorization")?.replace(/^Bearer /, "") ?? "");
  const expected = Buffer.from(secret);
  if (provided.length !== expected.length || !timingSafeEqual(provided, expected)) {
    return Response.json({ error: "Unauthorized" }, { status: 401 });
  }

  revalidatePath("/", "layout");
  return Response.json({ revalidated: true, at: new Date().toISOString() });
}
