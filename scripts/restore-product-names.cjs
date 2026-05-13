#!/usr/bin/env node
/**
 * restore-product-names.cjs
 *
 * The earlier Herald-brand scrub replaced "Herald.Py" with "the
 * Python SDK" and "Herald.NET / Herald.Compliance / Herald.Core"
 * with "the .NET SDK" / "the reference SDK". That was too
 * aggressive: shipped prose should use the product names —
 * Vidimus (the Python product) and TesseraSeal (the .NET product
 * comprising the receiver and adjacent components). Herald.X
 * stays where the engineering codebase is being named
 * specifically (manual review after this script's mechanical
 * pass).
 *
 * Substitutions:
 *   the Python SDK            -> Vidimus
 *   The Python SDK            -> Vidimus
 *   the Python SDK's          -> Vidimus's
 *   The Python SDK's          -> Vidimus's
 *   the Python reference implementation -> Vidimus
 *   The Python reference implementation -> Vidimus
 *   the .NET SDK              -> TesseraSeal
 *   The .NET SDK              -> TesseraSeal
 *   the .NET SDK's            -> TesseraSeal's
 *   The .NET SDK's            -> TesseraSeal's
 *   the .NET SDK's chain primitives -> TesseraSeal's chain primitives
 *   the .NET reference implementation -> TesseraSeal
 *   The .NET reference implementation -> TesseraSeal
 *   the reference SDK         -> TesseraSeal
 *   The reference SDK         -> TesseraSeal
 *
 * Run from the repo root:  node scripts/restore-product-names.cjs
 * Review the resulting git diff; manually fix any edge cases
 * where double-substitution or context-mismatch arise (e.g.,
 * "the TesseraSeal / TesseraSeal split" should become
 * "the TesseraSeal / Herald.Compliance split").
 */

const fs = require('node:fs')
const path = require('node:path')

const HERE = __dirname
const REPO_ROOT = path.resolve(HERE, '..')

const SUBS = [
  // Multi-word longer forms first so the bare-token replacement
  // doesn't catch them partially.
  [/the \.NET SDK's chain primitives/g, "TesseraSeal's chain primitives"],
  [/The \.NET SDK's chain primitives/g, "TesseraSeal's chain primitives"],
  [/the Python reference implementation/g, 'Vidimus'],
  [/The Python reference implementation/g, 'Vidimus'],
  [/the \.NET reference implementation/g, 'TesseraSeal'],
  [/The \.NET reference implementation/g, 'TesseraSeal'],
  // Possessives.
  [/the Python SDK's/g, "Vidimus's"],
  [/The Python SDK's/g, "Vidimus's"],
  [/the \.NET SDK's/g, "TesseraSeal's"],
  [/The \.NET SDK's/g, "TesseraSeal's"],
  [/the reference SDK's/g, "TesseraSeal's"],
  [/The reference SDK's/g, "TesseraSeal's"],
  // Bare forms.
  [/the Python SDK/g, 'Vidimus'],
  [/The Python SDK/g, 'Vidimus'],
  [/the \.NET SDK/g, 'TesseraSeal'],
  [/The \.NET SDK/g, 'TesseraSeal'],
  [/the reference SDK/g, 'TesseraSeal'],
  [/The reference SDK/g, 'TesseraSeal'],
  // Short-form internal labels that survived the original Herald
  // scrub. "HPy" is shorthand for Herald.Py; "HCp.Chain" is
  // shorthand for Herald.Compliance.Audit.Chain. Used in
  // cross-impl byte-equivalence prose.
  [/\bHCp\.Chain\b/g, "TesseraSeal's chain primitives"],
  [/\bHPy\b/g, 'Vidimus'],
  [/\bHCp\b/g, 'TesseraSeal'],
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

let filesTouched = 0
let totalEdits = 0

for (const file of walkMd(REPO_ROOT)) {
  if (SKIP_FILES.has(path.basename(file))) continue
  const before = fs.readFileSync(file, 'utf-8')
  let after = before
  for (const [re, repl] of SUBS) after = after.replace(re, repl)
  if (after === before) continue
  fs.writeFileSync(file, after, 'utf-8')
  // Count substitutions by comparing line counts of the two strings.
  const linesBefore = before.split('\n')
  const linesAfter = after.split('\n')
  let edits = 0
  for (let i = 0; i < Math.max(linesBefore.length, linesAfter.length); i++) {
    if (linesBefore[i] !== linesAfter[i]) edits += 1
  }
  filesTouched += 1
  totalEdits += edits
  const rel = path.relative(REPO_ROOT, file).replace(/\\/g, '/')
  console.log(`  ${rel}  (${edits} lines edited)`)
}

console.log('')
console.log(`restore-product-names: ${filesTouched} files touched, ${totalEdits} lines edited`)
