#!/usr/bin/env node
/**
 * scrub-close-out-codes.cjs
 *
 * Editorial sweep: agency-prefixed close-out codes ("NIST-G2",
 * "M&A-P3", "CFPB-N2", "NAIC-P4", "NIST-lineage", "G-fix") are
 * internal review-cycle labels that don't belong in shipped spec
 * prose. Strip them in place, keeping the surrounding substance.
 *
 * Passes per matching line (longest-first):
 *
 *   1. Trailing-qualifier patterns:
 *        " — NIST-G2 close"
 *        "(NIST-G2 close)"
 *        "(normative — NIST-P2)"
 *      The qualifier gets dropped along with the surrounding
 *      dash / parens / "close".
 *
 *   2. Lead-then-explanation patterns:
 *        "Closes NIST-G1 — the …"  → "Closes the …"
 *        "Closes NIST-G2."          → "Closes." (only when at end)
 *      Em-dash explanations stay; the code disappears.
 *
 *   3. Bare-token cleanup. Any remaining "NIST-G2", "M&A-P3",
 *      "G-fix", "NIST-lineage", etc. that didn't match a richer
 *      pattern. Token-only strip; whitespace cleanup at the end.
 *
 *   4. Whitespace cleanup ON THE EDITED LINE ONLY — collapse
 *      doubled spaces, strip " ." / " ," / " ;" artifacts left
 *      by the prior passes.
 *
 * Skipped:
 *   - CHANGELOG.md (historical record).
 *   - Fenced code blocks and indented code (paths / code).
 *   - docs/future-needs/ (gitignored already).
 *
 * Run from the repo root:  node scripts/scrub-close-out-codes.cjs
 */

const fs = require('node:fs')
const path = require('node:path')

const HERE = __dirname
const REPO_ROOT = path.resolve(HERE, '..')

// Core agency-prefixed identifier — letter + digits, or "lineage".
// G-fix is a special case that doesn't follow the prefix pattern.
const AGENCY = '(?:NIST|NAIC|CFPB|M&A)'
const SUFFIX = '(?:G\\d+|P\\d+|N\\d+|lineage)'
const CODE = `${AGENCY}-${SUFFIX}`
const CODE_RE = new RegExp(`\\b${CODE}\\b`, 'g')

const PASSES = [
  // Subject-replacement patterns: where the close-out code IS the
  // sentence's subject, replace with "the <agency> reviewer" so the
  // verb still has a subject. "NIST-P1 surfaces this" becomes
  // "the NIST reviewer surfaces this".
  [
    new RegExp(`\\b(NIST|NAIC|CFPB|M&A)-(?:G\\d+|P\\d+|N\\d+|lineage)\\s+(surfaces|surfaced|surface)\\b`, 'g'),
    'the $1 reviewer $2',
  ],
  // " — NIST-G2 close" — em-dash trailing qualifier.
  [new RegExp(`\\s+\\—\\s+${CODE}\\s+close\\b`, 'g'), ''],
  [new RegExp(`\\s+-\\s+${CODE}\\s+close\\b`, 'g'), ''],
  // "(NIST-G2 close)" — parenthetical qualifier.
  [new RegExp(` *\\(${CODE}\\s+close\\)`, 'g'), ''],
  // "(normative — NIST-P2)" — keep "(normative)", drop the code.
  [new RegExp(`\\s+\\—\\s+${CODE}\\)`, 'g'), ')'],
  [new RegExp(`\\s+-\\s+${CODE}\\)`, 'g'), ')'],
  // "Closes NIST-G1 — the …" — code-then-dash lead. Drop the code
  // and the em-dash so the explanation reads as continuation.
  [new RegExp(`\\b${CODE}\\s+\\—\\s+`, 'g'), ''],
  [new RegExp(`\\b${CODE}\\s+-\\s+`, 'g'), ''],
  // Possessive: "NIST-G1's reviewer" → "the reviewer".
  [new RegExp(`\\b${CODE}'s\\s+`, 'g'), 'the '],
  // "NIST-lineage reviewer" → "the NIST reviewer".
  [/\bNIST-lineage\s+reviewer\b/g, 'the NIST reviewer'],
  // "G-fix close-out" → "close-out" (G-fix is the cycle name).
  [/\bG-fix\s+close-out\b/g, 'close-out'],
  // Standalone G-fix mentions.
  [/\bG-fix\b/g, ''],
  // Bare code token — last resort, drops the code with trailing
  // space if any.
  [new RegExp(`\\b${CODE}\\s+`, 'g'), ''],
  [new RegExp(`\\b${CODE}\\b`, 'g'), ''],
]

const POST = [
  [/ {2,}/g, ' '],
  [/ +\./g, '.'],
  [/ +,/g, ','],
  [/ +;/g, ';'],
  [/ +:/g, ':'],
  [/\( +/g, '('],
  [/ +\)/g, ')'],
  [/\(\)/g, ''],
  // Capitalize sentence-leading "the <agency> reviewer" after a
  // period that ends the previous sentence. Specifically lifts
  // the substitution we make above when the code was sentence-
  // initial (e.g. "MAC. NIST-P1 surfaces" → "MAC. the NIST
  // reviewer surfaces" → "MAC. The NIST reviewer surfaces").
  [/(\.\s+)the (NIST|NAIC|CFPB|M&A) reviewer\b/g, '$1The $2 reviewer'],
]

const SKIP_FILES = new Set(['CHANGELOG.md'])

function walkMd(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue
    if (entry.name === 'node_modules') continue
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) walkMd(full, out)
    else if (entry.isFile() && entry.name.toLowerCase().endsWith('.md')) out.push(full)
  }
  return out
}

function scrubLine(line) {
  if (!CODE_RE.test(line) && !/\bG-fix\b/.test(line) && !/\bNIST-lineage\b/.test(line)) {
    return line
  }
  // Reset lastIndex from the test above
  CODE_RE.lastIndex = 0
  let out = line
  for (const [re, repl] of PASSES) {
    out = out.replace(re, repl)
  }
  for (const [re, repl] of POST) {
    out = out.replace(re, repl)
  }
  return out
}

let filesTouched = 0
let totalEdits = 0

for (const file of walkMd(REPO_ROOT)) {
  const rel = path.relative(REPO_ROOT, file).replace(/\\/g, '/')
  if (SKIP_FILES.has(path.basename(file))) continue
  const before = fs.readFileSync(file, 'utf-8')
  if (
    !CODE_RE.test(before) &&
    !/\bG-fix\b/.test(before) &&
    !/\bNIST-lineage\b/.test(before)
  ) {
    continue
  }
  const lines = before.split(/\r?\n/)
  let inFence = false
  let edits = 0
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    if (/^```/.test(line)) {
      inFence = !inFence
      continue
    }
    if (inFence) continue
    if (/^ {4,}\S/.test(line) && !/^\s*[-*+]\s/.test(line)) continue
    const next = scrubLine(line)
    if (next !== line) {
      lines[i] = next
      edits += 1
    }
  }
  if (edits === 0) continue
  const trailing = before.endsWith('\n') ? '\n' : ''
  fs.writeFileSync(file, lines.join('\n').replace(/\n+$/, '') + trailing, 'utf-8')
  filesTouched += 1
  totalEdits += edits
  console.log(`  ${rel}  (${edits} lines edited)`)
}

console.log('')
console.log(`scrub-close-out-codes: ${filesTouched} files touched, ${totalEdits} lines edited`)
