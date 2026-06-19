import { type NextRequest } from "next/server";
import { updateSession } from "@/lib/supabase/middleware";

// Edge middleware (NOT Next 16's nodejs `proxy.ts`): OpenNext/Cloudflare only
// supports Edge middleware, and Supabase's SSR session-refresh is edge-safe
// (fetch + cookies). Refreshes the auth cookie on every matched request.
export async function middleware(request: NextRequest) {
  return await updateSession(request);
}

export const config = {
  matcher: [
    /*
     * All paths except static assets and image files, so the auth session
     * cookie stays fresh while skipping cheap static requests.
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};
