// Entry program for make.fun bounty "news-image-20261120".
//
// The image itself is drawn ahead of time by compose.py (flat illustrations
// plus text set with real fonts) and committed here as entry.png. This
// program only places that finished image where the grader expects it, so
// the run needs no network and always produces the same bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

copyFileSync(source, join(outDir, "entry.png"));
