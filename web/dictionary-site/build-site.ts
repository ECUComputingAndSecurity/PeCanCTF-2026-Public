#!/usr/bin/env bun
import { mkdir, writeFile, readFile, rmdir } from "node:fs/promises";

const FLAG = "pecan{als0_n0t4_w0rd}";
const SKIP_COMMON = 50;
const FEATURED_COUNT = 12;
const FLAGS_PER_CHUNK = 10;
const CHUNK_SIZE = 1000;
const WORD_COUNT = 5000;
const TPL = `${import.meta.dir}/templates`;
const OUT = `${import.meta.dir}/dist`;

const WORD_LIST_URL =
  "https://raw.githubusercontent.com/hermitdave/FrequencyWords/refs/heads/master/content/2018/en/en_50k.txt";

const POS = ["noun", "verb", "adjective", "adverb"];

type Entry = {
  word: string;
  pos: string[];
  definitions: string[];
  examples: string[];
  synonyms: string[];
  alsoSee: string[];
};

const defTemplates: Record<string, string[]> = {
  noun: [
    "The state or quality of being {word}.",
    "A person or thing associated with {word}.",
    "The act or process of {word}ing.",
    "A particular instance or type of {word}.",
  ],
  verb: [
    "To engage in or perform {word}.",
    "To cause to become {word}.",
    "To relate to or be connected with {word}.",
  ],
  adjective: [
    "Of or relating to {word}.",
    "Having the characteristics of {word}.",
    "Pertaining to or associated with {word}.",
  ],
  adverb: [
    "In a manner that is {word}.",
    "To the extent or degree of {word}.",
    "With respect to or concerning {word}.",
  ],
};

const examples = [
  "The concept of {word} has been studied extensively.",
  "Her understanding of {word} was remarkable.",
  "The principles of {word} are widely accepted.",
  "A thorough analysis of {word} reveals its complexity.",
  "The relevance of {word} cannot be overstated.",
];

function pick<T>(a: T[]): T {
  return a[Math.floor(Math.random() * a.length)];
}

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function shuffle<T>(a: T[]): T[] {
  const b = [...a];
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [b[i], b[j]] = [b[j], b[i]];
  }
  return b;
}

async function main() {
  const start = performance.now();

  await rmdir(OUT).catch(() => { });

  console.log("Fetching word list...");
  const res = await fetch(WORD_LIST_URL);
  const text = await res.text();
  const allWords = text
    .split("\n")
    .map((l) => l.trim().split(" ")[0])
    .filter((w) => w && /^[a-z-]+$/.test(w));
  console.log(`Got ${allWords.length} words`);

  const words = allWords.slice(SKIP_COMMON, SKIP_COMMON + WORD_COUNT);
  const total = words.length;
  console.log(`Using ${total} words`);

  const synPool = shuffle(words);
  const alsoPool = shuffle(words);

  console.log("Generating entries...");
  const entries: Entry[] = words.map((word, i) => {
    const posCount = 1 + Math.floor(Math.random() * 2);
    const posList: string[] = [];
    const avail = [...POS];
    for (let p = 0; p < posCount; p++) {
      const idx = Math.floor(Math.random() * avail.length);
      posList.push(avail[idx]);
      avail.splice(idx, 1);
    }

    const definitions = posList.map(
      (p) => pick(defTemplates[p] || defTemplates.noun).replace(/\{word\}/g, word)
    );
    const examplesList = posList.map(
      () => pick(examples).replace(/\{word\}/g, word)
    );

    const seen = new Set([word]);
    const synonymCount = 2 + Math.floor(Math.random() * 3);
    const synonyms: string[] = [];
    for (let j = 0; synonyms.length < synonymCount && j < synPool.length; j++) {
      const s = synPool[(i * 7 + j * 13 + 3) % synPool.length];
      if (!seen.has(s)) {
        seen.add(s);
        synonyms.push(s);
      }
    }

    const alsoSeeCount = 1 + Math.floor(Math.random() * 3);
    const alsoSee: string[] = [];
    for (let j = 0; alsoSee.length < alsoSeeCount && j < alsoPool.length; j++) {
      const a = alsoPool[(i * 11 + j * 17 + 5) % alsoPool.length];
      if (!seen.has(a)) {
        seen.add(a);
        alsoSee.push(a);
      }
    }

    return { word, pos: posList, definitions, examples: examplesList, synonyms, alsoSee };
  });

  console.log("Injecting flag entries...");
  const restricted = new Set<number>();
  const N = entries.length;
  for (let i = 0; i < 500 && i < N; i++) restricted.add(i);
  for (let i = Math.max(0, N - 500); i < N; i++) restricted.add(i);
  const mid = Math.floor(N / 2);
  for (let i = mid - 250; i <= mid + 249; i++) {
    if (i >= 0 && i < N) restricted.add(i);
  }

  const flagWords = new Set<string>();
  const numChunks = Math.ceil(entries.length / CHUNK_SIZE);
  for (let chunk = 0; chunk < numChunks; chunk++) {
    const chunkStart = chunk * CHUNK_SIZE;
    const chunkEnd = Math.min(chunkStart + CHUNK_SIZE, entries.length);
    const available: number[] = [];
    for (let i = chunkStart; i < chunkEnd; i++) {
      if (!restricted.has(i)) available.push(i);
    }
    const shuffled = shuffle(available);
    const count = Math.min(FLAGS_PER_CHUNK, shuffled.length);
    for (let f = 0; f < count; f++) {
      entries[shuffled[f]].alsoSee.push(FLAG);
      flagWords.add(entries[shuffled[f]].word);
    }
  }
  console.log(`Flag injected into ${flagWords.size} entries`);

  const featured: Entry[] = [];
  const shuffled = shuffle(entries);
  for (const e of shuffled) {
    if (!flagWords.has(e.word) && featured.length < FEATURED_COUNT) {
      featured.push(e);
    }
  }

  console.log("Reading templates...");
  const wordTpl = await readFile(`${TPL}/word.html`, "utf-8");
  const homeTpl = await readFile(`${TPL}/home.html`, "utf-8");
  const robotsTpl = await readFile(`${TPL}/robots.txt`, "utf-8");
  const css = await readFile(`${TPL}/style.css`, "utf-8");

  const replaceAll = (t: string, k: string, v: string) => t.replaceAll(k, v);

  console.log("Writing pages...");
  const BATCH = 500;
  for (let i = 0; i < entries.length; i += BATCH) {
    const batch = entries.slice(i, i + BATCH);
    await Promise.all(batch.map(async (e) => {
      const dir = `${OUT}/word/${encodeURIComponent(e.word)}`;
      await mkdir(dir, { recursive: true });
      let html = wordTpl;
      html = replaceAll(html, "{{WORD}}", esc(e.word));
      html = replaceAll(html, "{{POS}}", esc(e.pos.join(", ")));
      html = replaceAll(html, "{{DEFINITIONS}}", e.definitions.map((d) => `<li>${esc(d)}</li>`).join("\n"));
      html = replaceAll(html, "{{EXAMPLES}}", e.examples.map((d) => `<li><em>${esc(d)}</em></li>`).join("\n"));
      html = replaceAll(html, "{{SYNONYMS}}", e.synonyms.map((w) => `<li><a href="/word/${encodeURIComponent(w)}">${esc(w)}</a></li>`).join("\n"));
      html = replaceAll(html, "{{ALSO_SEE}}", e.alsoSee.map((w) => `<li><a href="/word/${encodeURIComponent(w)}">${esc(w)}</a></li>`).join("\n"));
      html = replaceAll(html, "{{WORD_COUNT}}", String(total));
      await writeFile(`${dir}/index.html`, html);
    }));
    if ((i / BATCH) % 10 === 0) console.log(`  ${Math.min(i + BATCH, entries.length)}/${entries.length}`);
  }

  let homeHtml = homeTpl;
  homeHtml = replaceAll(homeHtml, "{{WORD_COUNT}}", String(total));
  homeHtml = replaceAll(homeHtml, "{{FEATURED_WORDS}}",
    featured.map((e) =>
      `<article class="word-card">
<h3><a href="/word/${encodeURIComponent(e.word)}">${esc(e.word)}</a></h3>
<p class="pos">${esc(e.pos.join(", "))}</p>
<p>${esc((e.definitions[0] || "").length > 100 ? e.definitions[0].slice(0, 100) + "..." : e.definitions[0] || "")}</p>
</article>`
    ).join("\n")
  );

  await writeFile(`${OUT}/index.html`, homeHtml);
  await writeFile(`${OUT}/style.css`, css);

  let robots = robotsTpl;
  robots = replaceAll(robots, "{{WORD_COUNT}}", String(total));
  await writeFile(`${OUT}/robots.txt`, robots);

  const wordData = entries.map((e) => ({
    word: e.word,
    pos: e.pos.join(", "),
    definition: (e.definitions[0] || "").length > 120 ? e.definitions[0].slice(0, 120) + "..." : e.definitions[0] || "",
  }));
  await writeFile(`${OUT}/__words_.json`, JSON.stringify(wordData));

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>/</loc></url>
${words.map((w) => `  <url><loc>/word/${encodeURIComponent(w)}</loc></url>`).join("\n")}
</urlset>`;
  await writeFile(`${OUT}/sitemap.xml`, sitemap);

  const elapsed = ((performance.now() - start) / 1000).toFixed(1);
  console.log(`Done! ${words.length} pages in ${elapsed}s`);
  console.log(`Flag: ${FLAG}`);
}

await main();
