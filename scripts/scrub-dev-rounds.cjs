#!/usr/bin/env node
/**
 * scrub-dev-rounds.cjs
 *
 * Editorial sweep: dev-cycle labels ("Round-17", "Round 18", etc.)
 * are development cadence markers, not part of the shipped spec
 * language. This script removes them from every *.md file in the
 * repo, line-by-line, leaving any line without a Round-N reference
 * untouched.
 *
 * Per matching line:
 *
 *   1. Drop entire `(Round-NN …)` parentheticals.
 *   2. Strip inline `Round-NN ` prefixes (with trailing space).
 *   3. Clean up artifacts the above left ON THAT LINE only —
 *      double-spaces, " ." / " ," / " ;" gaps. Lines that didn't
 *      match Round-N are not touched, so pre-existing whitespace
 *      conventions elsewhere stay intact.
 *
 * Run from the repo root:  node scripts/scrub-dev-rounds.cjs
 * Review the resulting diff in git before committing.
 */

const fs = require('node:fs')
const path = require('node:path')

const HERE = __dirname
const REPO_ROOT = path.resolve(HERE, '..')

const ROUND_RE = /Round[ -]\d+/
const PAREN_RE = / *\(Round[ -]\d+[^)]*\)/g
// Catch the possessive form ("Round-17's") plus the bare prefix
// case ("Round-17 …"). Drop the whole token including possessive
// 's so the surrounding sentence reads cleanly.
const POSS_RE = /Round[ -]\d+'s /g
const PREFIX_RE = /Round[ -]\d+ /g

function scrubLine(line) {
  if (!ROUND_RE.test(line)) return line
  let out = line
  out = out.replace(PAREN_RE, '')
  out = out.replace(POSS_RE, '')
  out = out.replace(PREFIX_RE, '')
  // Local whitespace cleanup. Only runs on lines that we already
  // know matched a Round-N pattern — pre-existing double-spaces in
  // other lines stay untouched.
  out = out
    .replace(/ {2,}/g, ' ')
    .replace(/ +\./g, '.')
    .replace(/ +,/g, ',')
    .replace(/ +;/g, ';')
    .replace(/\( +/g, '(')
    .replace(/ +\)/g, ')')
  return out
}

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

let filesTouched = 0
let totalLineEdits = 0

for (const file of walkMd(REPO_ROOT)) {
  const before = fs.readFileSync(file, 'utf-8')
  if (!ROUND_RE.test(before)) continue
  const lines = before.split(/\r?\n/)
  let fileEdits = 0
  for (let i = 0; i < lines.length; i++) {
    const next = scrubLine(lines[i])
    if (next !== lines[i]) {
      lines[i] = next
      fileEdits += 1
    }
  }
  if (fileEdits === 0) continue
  // Preserve trailing newline if the original had one.
  const trailingNewline = before.endsWith('\n') ? '\n' : ''
  // Use \n as the join separator; the source files are LF-terminated
  // per `.gitattributes` / git autocrlf handling, and git will
  // normalize on commit.
  fs.writeFileSync(file, lines.join('\n').replace(/\n+$/, '') + trailingNewline, 'utf-8')
  filesTouched += 1
  totalLineEdits += fileEdits
  const rel = path.relative(REPO_ROOT, file).replace(/\\/g, '/')
  console.log(`  ${rel}  (${fileEdits} lines edited)`)
}

console.log('')
console.log(`scrub-dev-rounds: ${filesTouched} files touched, ${totalLineEdits} lines edited`)
