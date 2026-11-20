// Entry program for make.fun bounty "news-image-20261120" (v2 rebuild).
//
// The image is the finished front page: a 1024x1024 dense newspaper front
// page with 35 verified stories from Friday 20 November 2026 — a masthead,
// numbers strip, UTC timeline, three lead stories (Russia's overnight
// barrage on Kyiv, Cyclone Akvan's landfall in Odisha, the markets slide),
// ten pictured cards, a dotted world map with numbered pins, a 20-story
// "also on" list, a date-check box and a sources footer. The Akvan lead
// uses a real satellite photo (JTWC/NASA, public domain); every other
// visual is a flat illustration drawn in code and every word is drawn with
// a real font, so nothing is garbled. This program copies the finished
// image to the output directory the grader reads.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
