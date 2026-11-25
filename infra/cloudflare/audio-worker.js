// quranayat-audio: serves the tajweed lesson audio from the R2 bucket `quranayat-audio`
// on Cloudflare's free workers.dev address (docs/MAKHRAJ_3D_PLAN.md §9), instead of the
// rate-limited r2.dev link. Read-only, tajweed/ only, with range requests for seeking.
// Deployed by hand in the Cloudflare dashboard (Workers & Pages → quranayat-audio) with
// an R2 binding named AUDIO; TAJWEED_AUDIO_BASE_URL on Koyeb points at
// https://quranayat-audio.<account>.workers.dev/tajweed/muallimi-soniy

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-headers": "range",
  "access-control-expose-headers": "content-range, content-length, accept-ranges, etag",
};

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") return new Response(null, { headers: CORS });
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405, headers: CORS });
    }
    const key = decodeURIComponent(new URL(request.url).pathname.slice(1));
    if (!key.startsWith("tajweed/") || key.includes("..")) {
      return new Response("Not found", { status: 404, headers: CORS });
    }
    const ranged = request.headers.has("range");
    const object = await env.AUDIO.get(key, ranged ? { range: request.headers } : {});
    if (!object) return new Response("Not found", { status: 404, headers: CORS });

    const headers = new Headers(CORS);
    object.writeHttpMetadata(headers);
    headers.set("etag", object.httpEtag);
    headers.set("accept-ranges", "bytes");
    // file names never change meaning (new encodes go under a new prefix), so a
    // browser can keep each one for good
    headers.set("cache-control", "public, max-age=31536000, immutable");
    const body = request.method === "HEAD" ? null : object.body;
    if (ranged && object.range) {
      // R2 reports either {offset, length} or {suffix}; the other keys may be present
      // but undefined, so test the values, not the keys
      const r = object.range;
      const suffix = typeof r.suffix === "number" ? r.suffix : null;
      const offset = suffix !== null ? object.size - suffix : r.offset ?? 0;
      const length = suffix !== null ? suffix : r.length ?? object.size - offset;
      headers.set("content-range", `bytes ${offset}-${offset + length - 1}/${object.size}`);
      headers.set("content-length", String(length));
      return new Response(body, { status: 206, headers });
    }
    headers.set("content-length", String(object.size));
    return new Response(body, { headers });
  },
};
