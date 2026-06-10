# Conformance-corpus test signing key (public material)

This directory publishes the **public** half of the Ed25519 test key that
signs the signature-bearing vectors in this corpus. The private seed is
**never** stored here — it lives local-only at
`E:\dev\testing\private-keys\tesseraseal\` and is read by the vector
generators at materialization time.

| File | What | Handling |
|---|---|---|
| `test-signing-key.pub.hex` | 32-byte Ed25519 public key, lowercase hex | publishable |
| `test-signing-key.ed25519.pub.pem` | the same key, PKIX `BEGIN PUBLIC KEY` PEM | publishable |

Public key (hex): `0985603b6c0e099bac783bcd7801664ed376a7888eafbf191859854bf8ff7f35`

## Why a public key lives in the corpus

A verifier consumes only public-key material. Step 11 of the §7 walk
(daily-seal signature verification) Ed25519-verifies the seal's signature
over the reconstructed `sign_payload` under this key. The corpus publishes
the key so any verifier — in any language — can run the step-11 path
against the pinned signatures without holding the private seed.

Ed25519 signing is deterministic (RFC 8032), so the pinned signature bytes
are reproducible. Anyone holding the local-only seed regenerates the exact
same signatures; everyone else verifies them with the public key above.

## Provenance

- Generated 2026-06-10 for the chain-of-custody conformance corpus.
- Key generator: `E:\dev\testing\private-keys\tesseraseal\keygen.go` (one-shot,
  refuses overwrite). The seed and the private PEM stay in that local-only
  directory and are never committed to any repo.
- The generators read the seed via the `TESSERASEAL_TEST_KEY_DIR`
  environment variable (default `E:\dev\testing\private-keys\tesseraseal`).
  A generator FAILS with a clear message when the key directory is absent —
  it never falls back to placeholder bytes.

## Rotation warning

Rotating the key invalidates every pinned signature in the corpus. A
rotation MUST regenerate all signature-bearing vectors in the same change.
The Go verifier's signature tests cross-check a loaded seed against the
published hex above and fail hard on a mismatch, so a rotation that misses
a vector is caught at the gate, not silently passed.
