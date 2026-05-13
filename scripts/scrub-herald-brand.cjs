#!/usr/bin/env node
/**
 * scrub-herald-brand.cjs
 *
 * Editorial sweep: replace `Herald.Py`, `Herald.NET`,
 * `Herald.Core`, and `Herald.Compliance` references with
 * vendor-neutral phrasing. The shipped spec corpus shouldn't carry
 * a brand-specific implementation name for the reference SDK.
 *
 * Substitutions are applied per-line, longest-first, so multi-word
 * patterns ("Herald.Py reference implementation") win before bare
 * tokens ("Herald.Py") and the result doesn't double up
 * ("the Python SDK reference implementation").
 *
 * Skipped:
 *   - CHANGELOG.md — historical record; entries describe what was
 *     called what at the time, scrubbing rewrites history.
 *   - Lines inside fenced code blocks — those are typically
 *     filesystem paths or code snippets where mechanical
 *     substitution mangles the syntax. Reviewed manually after.
 *   - Lines starting with 4+ spaces (indented code).
 *
 * Run from the repo root:  node scripts/scrub-herald-brand.cjs
 * Review the resulting git diff before committing.
 */

const fs = require('node:fs')
const path = require('node:path')

const HERE = __dirname
const REPO_ROOT = path.resolve(HERE, '..')

const SUBS = [
  // Longest first so multi-word patterns claim their territory
  // before bare-token replacements can match part of them.
  [/Herald\.Compliance\.Audit\.Chain/g, "the .NET SDK's chain primitives"],
  [/Herald\.Py reference implementation/g, 'the Python reference implementation'],
  [/Herald\.NET reference implementation/g, 'the .NET reference implementation'],
  [/Herald\.Compliance reference/g, 'the .NET reference'],
  [/Herald\.Py's/g, "the Python SDK's"],
  [/Herald\.NET's/g, "the .NET SDK's"],
  [/Herald\.Compliance's/g, "the .NET SDK's"],
  [/Herald\.Core's/g, "the reference SDK's"],
  [/Herald\.Py/g, 'the Python SDK'],
  [/Herald\.NET/g, 'the .NET SDK'],
  [/Herald\.Compliance/g, 'the .NET SDK'],
  [/Herald\.Core/g, 'the reference SDK'],
]

// Lowercase post-fixes: when a sentence started with "Herald.X"
// (capital H) we end up with sentence-leading "the X" which is
// fine, but the preceding "The " variants need de-doubling.
const POST = [
  [/\bThe the\b/g, 'The'],
  [/\bthe the\b/g, 'the'],
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

function scrubFile(file) {
  const before = fs.readFileSync(file, 'utf-8')
  if (!/Herald\./.test(before)) return 0
  const rel = path.relative(REPO_ROOT, file).replace(/\\/g, '/')
  if (SKIP_FILES.has(rel) || SKIP_FILES.has(path.basename(file))) return 0

  const lines = before.split(/\r?\n/)
  let inFence = false
  let edits = 0
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    // Track fenced code blocks (```...```). Toggle state on any
    // line starting with three or more backticks. Skip content
    // inside the fence for substitution.
    if (/^```/.test(line)) {
      inFence = !inFence
      continue
    }
    if (inFence) continue
    // Skip indented code blocks (4+ leading spaces, no list bullet).
    if (/^ {4,}\S/.test(line) && !/^\s*[-*+]\s/.test(line)) continue

    let next = line
    for (const [re, repl] of SUBS) {
      next = next.replace(re, repl)
    }
    for (const [re, repl] of POST) {
      next = next.replace(re, repl)
    }
    if (next !== line) {
      lines[i] = next
      edits += 1
    }
  }

  if (edits === 0) return 0
  const trailing = before.endsWith('\n') ? '\n' : ''
  fs.writeFileSync(file, lines.join('\n').replace(/\n+$/, '') + trailing, 'utf-8')
  console.log(`  ${rel}  (${edits} lines edited)`)
  return edits
}

let filesTouched = 0
let totalEdits = 0
for (const file of walkMd(REPO_ROOT)) {
  const n = scrubFile(file)
  if (n > 0) {
    filesTouched += 1
    totalEdits += n
  }
}

console.log('')
console.log(`scrub-herald-brand: ${filesTouched} files touched, ${totalEdits} lines edited`)
