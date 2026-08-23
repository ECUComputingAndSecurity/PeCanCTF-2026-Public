import type { BunFile } from "bun";

const DIST_PATH = process.env.DIST_PATH || `${import.meta.dir}/dist`;
let wordData: { word: string; pos: string; definition: string }[] | null = null;

async function loadWordData() {
  if (!wordData) {
    const file = Bun.file(`${DIST_PATH}/__words_.json`);
    wordData = await file.json();
  }
  return wordData;
}

async function getRoutes() {
  const routes: Record<string, Response | BunFile> = {};
  const glob = new Bun.Glob("**/*");
  const start = performance.now();

  for await (const filename of glob.scan({ cwd: DIST_PATH })) {
    if (filename === "__words_.json") continue;
    try {
      const path = `/${filename.replace(/\\/g, "/")}`;
      const file = Bun.file(`${DIST_PATH}/${filename}`);

      if (path.endsWith("/index.html")) {
        routes[path.replace("/index.html", "") || "/"] = file;
      } else if (path.endsWith(".html")) {
        routes[path.replace(".html", "") || "/"] = file;
      } else {
        routes[path] = file || "/";
      }
    } catch (e) {
      console.error(e);
    }
  }

  console.info(`Loaded ${Object.keys(routes).length} static routes in ${((performance.now() - start) / 1000).toFixed(1)}s`);
  return routes;
}


const routes = await getRoutes();

Bun.serve({
  port: parseInt(process.env.PORT || "3000"),
  routes: {
    ...routes,
    "/search": async (req) => {
      const url = new URL(req.url);
      const q = url.searchParams.get("q")?.toLowerCase().trim() || "";
      if (!q) {
        return Response.json({ results: [] }, { headers: { "Access-Control-Allow-Origin": "*" } });
      }

      const data = await loadWordData();
      const results = data!
        .filter((e) => e.word.toLowerCase().includes(q))
        .slice(0, 20);

      return Response.json({ results }, {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Cache-Control": "public, max-age=60",
        },
      });
    },
  }
});

console.info(`Server running on http://0.0.0.0:${parseInt(process.env.PORT || "3000")}`);
