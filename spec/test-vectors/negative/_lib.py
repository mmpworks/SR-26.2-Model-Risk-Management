# -*- coding: utf-8 -*-
"""Shared primitives for the FFIEC v1 negative-vector generators.

Every negative vector under `negative/` derives the SAME valid baseline
audit file from the central `chain_vectors.json` inputs, then applies
exactly one documented mutation (the named tamper class). This module
holds the deterministic spec §4.1 / §4.2 / §4.3 / §5 constructions plus
the baseline audit-file builder, so each per-vector `_compute.py` reads
as "load baseline → apply one mutation → write input.json + the pinned
verifier output."

Never hand-craft a hash. A generator computes the baseline with these
primitives, mutates one field, and lets the recompute fall where it
falls — that is exactly what the verifier walks.

Run a generator with: python _compute.py  (use `python`, not python3)
"""

from __future__ import annotations

import base64
import copy
import hashlib
import hmac
import json
import os
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# ---------------------------------------------------------------------------
# Spec §4.1 constants (FFIEC-conformance posture)
# ---------------------------------------------------------------------------
HKDF_SALT = b"ffiec.chain-of-custody.v1.salt"
HKDF_INFO_BASE = b"ffiec.chain-of-custody.v1.info"
HKDF_LENGTH = 32
LENGTH_LE32 = (32).to_bytes(4, "little")  # 0x20 0x00 0x00 0x00
GENESIS_HASH = b"\x00" * 32  # prev_hash for seq=1 (§4.1 inviolate property 5)

# Magic + locked algorithm-string table (§4.1, README)
MAGIC = "ffiec.chain-of-custody.v1"

# Central corpus inputs (mirror chain_vectors.json `inputs`)
TENANT_ID = "tenant-ffiec-test-1"
RUN_ID = "RUN-FFIEC-VECTOR"
SEAL_DATE = "2026-05-06"
ALGORITHM = "ed25519"
FORMAT_VERSION = "v1"
CADENCE = "daily"
DEV_MODE = False
SIGN_PAYLOAD_VERSION = "v1.0a"  # consolidated amendment form (§4.3, 2026-05-07)

IKM_V1_HEX = (
    "66666965632d63726f73732d6c616e67756167652d746573742d766563"
    "746f722d696b6d2d76312d3332627974657321"
)
IKM_V2_HEX = (
    "66666965632d63726f73732d6c616e67756167652d746573742d766563"
    "746f722d696b6d2d76322d3332627974657321"
)
IKM_V1 = bytes.fromhex(IKM_V1_HEX)
IKM_V2 = bytes.fromhex(IKM_V2_HEX)

HERE_ROOT = os.path.dirname(os.path.abspath(__file__))
CORPUS_ROOT = os.path.dirname(HERE_ROOT)  # spec/test-vectors/


# ---------------------------------------------------------------------------
# HKDF-SHA-256 (RFC 5869), HMAC, fingerprint, digest (§4.1)
# ---------------------------------------------------------------------------
def _hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    return hmac.new(salt, ikm, hashlib.sha256).digest()


def _hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    """RFC 5869 expand. length=32 fits the first round; T(1) IS the output."""
    okm = b""
    t = b""
    counter = 1
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        okm += t
        counter += 1
    return okm[:length]


def hkdf_sha256(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    return _hkdf_expand(_hkdf_extract(salt, ikm), info, length)


def info_for_tenant(tenant_id: str) -> bytes:
    return HKDF_INFO_BASE + b"|" + tenant_id.encode("utf-8")


def session_key(ikm: bytes, tenant_id: str) -> bytes:
    return hkdf_sha256(ikm, HKDF_SALT, info_for_tenant(tenant_id), HKDF_LENGTH)


def key_fingerprint(tenant_id: str, ikm: bytes) -> bytes:
    """SHA-256(utf8(tenant_id) || ikm)[:16] per §4.1."""
    return hashlib.sha256(tenant_id.encode("utf-8") + ikm).digest()[:16]


def hkdf_inputs_digest(tenant_id: str) -> bytes:
    return hashlib.sha256(
        HKDF_SALT + info_for_tenant(tenant_id) + LENGTH_LE32
    ).digest()


# ---------------------------------------------------------------------------
# JCS canonical event bytes + per-event MAC (§5, §4.1)
# ---------------------------------------------------------------------------
def jcs_canonicalize(value: Any) -> bytes:
    """JCS for the simple shapes the corpus events use: sorted keys, no
    whitespace, UTF-8, integer (not float) numerics. Matches the central
    corpus's per-event `event_canonical_hex` byte-for-byte for cases
    001/002/010 (verified idempotent against the RFC 8785 `jcs` library)."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def event_object(
    *,
    tenant_id: str,
    run_id: str,
    seq: int,
    name: str,
    timestamp_ns: int,
    span_id_b64: str,
    trace_id_b64: str,
    event_id: str,
    data: str,
    step: int,
    chain_kind: str = "audit",
    kind: str = "audit",
    severity: str = "AUDIT",
) -> dict:
    """The §5 canonical event shape, mirroring chain_vectors.json events."""
    return {
        "attributes": {"data": data, "step": step},
        "chain_kind": chain_kind,
        "duration_ns": None,
        "event_id": event_id,
        "kind": kind,
        "name": name,
        "parent_span_id": None,
        "resource": {},
        "run_id": run_id,
        "severity": severity,
        "span_id": span_id_b64,
        "tenant_id": tenant_id,
        "timestamp_ns": timestamp_ns,
        "trace_id": trace_id_b64,
    }


def payload_hash(session_key_bytes: bytes, prev_hash: bytes, canonical: bytes) -> bytes:
    """§4.1 per-event MAC: HMAC-SHA-256(session_key, prev_hash || canonical)."""
    return hmac.new(session_key_bytes, prev_hash + canonical, hashlib.sha256).digest()


# ---------------------------------------------------------------------------
# RFC 6962 Merkle (§4.2, right-promote balancing)
# ---------------------------------------------------------------------------
def _rfc6962_leaf_hash(leaf: bytes) -> bytes:
    return hashlib.sha256(b"\x00" + leaf).digest()


def _rfc6962_internal_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()


def merkle_root_rfc6962(payload_hashes: list[bytes]) -> bytes:
    """RFC 6962 §2.1 streaming Merkle over the ordered payload_hash leaves."""
    if not payload_hashes:
        return hashlib.sha256(b"").digest()
    level = [_rfc6962_leaf_hash(h) for h in payload_hashes]
    while len(level) > 1:
        nxt: list[bytes] = []
        i = 0
        while i + 1 < len(level):
            nxt.append(_rfc6962_internal_hash(level[i], level[i + 1]))
            i += 2
        if i < len(level):
            nxt.append(level[i])  # right-promote unpaired leaf
        level = nxt
    return level[0]


# ---------------------------------------------------------------------------
# sign_payload v1.0a (§4.3, consolidated amendment form — 10 lines)
# ---------------------------------------------------------------------------
def build_sign_payload_v1_0a(
    *,
    algorithm: str,
    format_version: str,
    tenant_id: str,
    seal_date: str,
    merkle_root_hex: str,
    hkdf_inputs_digest_hex: str,
    cadence: str = CADENCE,
    dev_mode: bool = DEV_MODE,
) -> bytes:
    dev_byte = "1" if dev_mode else "0"
    text = "\n".join([
        MAGIC,
        "v1.0a",
        algorithm,
        format_version,
        tenant_id,
        seal_date,
        merkle_root_hex,
        hkdf_inputs_digest_hex,
        cadence,
        dev_byte,  # terminal field — NO trailing newline
    ])
    return text.encode("utf-8")


# ---------------------------------------------------------------------------
# TesseraSeal TEST signing key (Ed25519, deterministic RFC 8032)
# ---------------------------------------------------------------------------
# The generators read the PRIVATE seed local-only; the verifier reads only
# the PUBLIC key. Seed handling is fail-loud: a signature-bearing generator
# that cannot find the key dir MUST error, never silently fall back to a
# placeholder. The published public key is pinned so a key rotation that
# forgets to regenerate a vector is caught here, not silently passed.
TEST_KEY_DIR_ENV = "TESSERASEAL_TEST_KEY_DIR"
DEFAULT_TEST_KEY_DIR = r"E:\dev\testing\private-keys\tesseraseal"
SEED_HEX_FILE = "test-signing-key.seed.hex"
PUBLISHED_PUB_HEX = (
    "0985603b6c0e099bac783bcd7801664ed376a7888eafbf191859854bf8ff7f35"
)


def test_key_dir() -> str:
    """Resolve the test-key directory: env override, then local-only default."""
    return os.environ.get(TEST_KEY_DIR_ENV) or DEFAULT_TEST_KEY_DIR


def load_test_signing_key() -> Ed25519PrivateKey:
    """Read the 32-byte private seed and return the Ed25519 signing key.

    FAILS LOUDLY when the key directory or seed file is absent — a
    signature-bearing vector must never materialize against placeholder
    bytes. When the seed IS present, a derived-public-key mismatch against
    the pinned PUBLISHED_PUB_HEX is a hard error: the key was rotated
    without regenerating the corpus.
    """
    seed_path = os.path.join(test_key_dir(), SEED_HEX_FILE)
    if not os.path.isfile(seed_path):
        raise FileNotFoundError(
            f"TesseraSeal test signing seed not found at {seed_path}. "
            f"Set {TEST_KEY_DIR_ENV} to the local-only key directory "
            f"(it holds {SEED_HEX_FILE}). The generator refuses to "
            f"materialize a signature-bearing vector against placeholder bytes."
        )
    with open(seed_path, "r", encoding="utf-8") as f:
        seed = bytes.fromhex(f.read().strip())
    if len(seed) != 32:
        raise ValueError(f"seed {seed_path} has {len(seed)} bytes, want 32")
    priv = Ed25519PrivateKey.from_private_bytes(seed)
    pub_hex = priv.public_key().public_bytes_raw().hex()
    if pub_hex != PUBLISHED_PUB_HEX:
        raise ValueError(
            f"loaded seed derives public key {pub_hex}, but the corpus "
            f"publishes {PUBLISHED_PUB_HEX} — the test key was rotated "
            f"without regenerating the corpus."
        )
    return priv


def sign_bytes(priv: Ed25519PrivateKey, message: bytes) -> str:
    """Ed25519-sign `message` and return base64-std of the 64-byte signature.

    Deterministic per RFC 8032 — the same (seed, message) reproduces the
    same signature bytes on every run and in every conforming library.
    """
    return base64.b64encode(priv.sign(message)).decode("ascii")


def sign_seal_in_place(audit: dict, priv: Ed25519PrivateKey) -> None:
    """Replace the baseline seal's placeholder signature with a REAL one.

    Signs the seal's already-built `sign_payload` (the v1.0a byte form on
    `sign_payload_hex`) so the seal carries a genuine Ed25519 signature the
    §7 step-11 walk verifies under the published public key.
    """
    sign_payload = bytes.fromhex(audit["seal"]["sign_payload_hex"])
    audit["seal"]["signature_b64"] = sign_bytes(priv, sign_payload)


# ---------------------------------------------------------------------------
# Baseline audit-file builder
# ---------------------------------------------------------------------------
def _span_trace(seq: int) -> tuple[str, str]:
    """The central corpus's seq-stamped span_id (8B) / trace_id (16B), b64."""
    span = bytes([seq]) * 8
    trace = bytes([seq]) * 16
    return (
        base64.b64encode(span).decode("ascii"),
        base64.b64encode(trace).decode("ascii"),
    )


def build_baseline(
    *,
    n_events: int = 5,
    rotation: bool = False,
    tenant_id: str = TENANT_ID,
    run_id: str = RUN_ID,
    seal_date: str = SEAL_DATE,
) -> dict:
    """Build the valid baseline audit file: header + chained entries + seal.

    The single-IKM baseline (rotation=False) mirrors the central corpus's
    `single_chain`; the rotation baseline (rotation=True) mirrors
    `rotation_chain` (seq 1-3 under key_version=1, seq 4-5 under
    key_version=2). The returned dict is the on-disk audit-file shape the
    negative vectors tamper.
    """
    sk_v1 = session_key(IKM_V1, tenant_id)
    sk_v2 = session_key(IKM_V2, tenant_id)
    fp_v1 = key_fingerprint(tenant_id, IKM_V1)
    fp_v2 = key_fingerprint(tenant_id, IKM_V2)
    digest = hkdf_inputs_digest(tenant_id)

    entries: list[dict] = []
    prev = GENESIS_HASH
    key_versions_present: list[int] = []
    for offset in range(n_events):
        seq = offset + 1
        if rotation and seq >= 4:
            kv, ikm, sk, fp = 2, IKM_V2, sk_v2, fp_v2
        else:
            kv, ikm, sk, fp = 1, IKM_V1, sk_v1, fp_v1
        if kv not in key_versions_present:
            key_versions_present.append(kv)

        span_b64, trace_b64 = _span_trace(seq)
        ev = event_object(
            tenant_id=tenant_id,
            run_id=run_id,
            seq=seq,
            name=f"audit_event_{seq}",
            timestamp_ns=1735689601000000000 + offset * 1_000_000_000,
            span_id_b64=span_b64,
            trace_id_b64=trace_b64,
            event_id=f"01HFFIEC0000000000000000000{seq}",
            data=f"payload-{seq}",
            step=seq,
        )
        canonical = jcs_canonicalize(ev)
        ph = payload_hash(sk, prev, canonical)
        entries.append({
            "seq": seq,
            "tenant_id": tenant_id,
            "run_id": run_id,
            "key_version": kv,
            "key_fingerprint_hex": fp.hex(),
            "format_version": FORMAT_VERSION,
            "event": ev,
            "event_canonical_hex": canonical.hex(),
            "prev_hash_hex": prev.hex(),
            "payload_hash_hex": ph.hex(),
        })
        prev = ph

    leaves = [bytes.fromhex(e["payload_hash_hex"]) for e in entries]
    merkle_root = merkle_root_rfc6962(leaves)
    sign_payload = build_sign_payload_v1_0a(
        algorithm=ALGORITHM,
        format_version=FORMAT_VERSION,
        tenant_id=tenant_id,
        seal_date=seal_date,
        merkle_root_hex=merkle_root.hex(),
        hkdf_inputs_digest_hex=digest.hex(),
    )

    header = {
        "format_version": FORMAT_VERSION,
        "tenant_id": tenant_id,
        "seal_date": seal_date,
        "genesis_hash_hex": GENESIS_HASH.hex(),
        "hkdf_inputs_digest_hex": digest.hex(),
    }
    seal = {
        "tenant_id": tenant_id,
        "seal_date": seal_date,
        "format_version": FORMAT_VERSION,
        "spec_version": "v1.0",
        "sign_payload_version": SIGN_PAYLOAD_VERSION,
        "algorithm": ALGORITHM,
        "cadence": CADENCE,
        "dev_mode": DEV_MODE,
        "key_versions": sorted(key_versions_present),
        "merkle_root_hex": merkle_root.hex(),
        "hkdf_inputs_digest_hex": digest.hex(),
        # The corpus carries no Ed25519 signature (README "Note on
        # signature" — signatures are implementation-produced against a
        # test key). A materialized negative that tampers the signature
        # carries a placeholder the verifier resolves against the test
        # key; for byte-form-only negatives the field stays a sentinel.
        "signature_b64": "TEST-SIGNATURE-PLACEHOLDER-not-an-ed25519-sig",
        "sign_payload_hex": sign_payload.hex(),
        "sign_payload_text": sign_payload.decode("utf-8"),
    }
    return {"header": header, "entries": entries, "seal": seal}


def clone_baseline(**kwargs) -> dict:
    """A deep copy of a fresh baseline, for safe in-place mutation."""
    return copy.deepcopy(build_baseline(**kwargs))


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------
def write_input_json(here: str, record: dict) -> None:
    with open(os.path.join(here, "input.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_expected_output(
    here: str,
    *,
    status: str,
    step: str,
    reason: str,
    exit_code: int,
    anomaly: str | None = None,
    reason_template: str | None = None,
) -> None:
    """Write the §7 normative verifier-output pin.

    Format (§7 "Verifier output format (normative)"):
        Status: <status>
        Step: <step>
        Reason-Template: <verbatim INDEX reason, tokens intact>
        Reason: <reason with <N>/<X>/<date> substituted to this input>
        Anomaly: <text>     (PASS-with-anomaly cases only)
        ExitCode: <code>     (§10.12 contract; not part of the line-oriented
                              §7 form but pinned here so the future §7-walk
                              wiring asserts the exit code too)

    Two reason lines on purpose. `Reason-Template` is the byte-verbatim
    negative/INDEX.md cell (e.g. `payload_hash MAC mismatch at seq <N>`) —
    the conformance contract the gate matches against. `Reason` is the
    rendered instance the verifier actually emits for THIS fixture (e.g.
    `payload_hash MAC mismatch at seq 3`), with the position-dependent
    token substituted per INDEX.md's token-substitution rule. Keeping
    both means the gate's literal contract check passes AND the pin stays
    truthful about the concrete per-input output.
    """
    lines = [f"Status: {status}"]
    if step:
        lines.append(f"Step: {step}")
    if reason_template and reason_template != reason:
        lines.append(f"Reason-Template: {reason_template}")
    lines.append(f"Reason: {reason}")
    if anomaly:
        lines.append(f"Anomaly: {anomaly}")
    lines.append(f"ExitCode: {exit_code}")
    with open(os.path.join(here, "expected_output.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def here_of(file: str) -> str:
    return os.path.dirname(os.path.abspath(file))
