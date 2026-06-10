# -*- coding: utf-8 -*-
"""Meta-generator: emit one `_compute.py` per negative vector N001-N038.

Documentation-as-database discipline: the tamper recipe + the pinned
verifier output for every negative live in the single TABLE below
(sourced from each vector's description.md and the authoritative
negative/INDEX.md). Each row renders to a thin per-vector `_compute.py`
that imports `_lib`, builds the baseline, applies the row's mutation, and
writes `input.json` + `expected_output.txt`.

This keeps the tamper logic in ONE place (no 38-way copy-paste drift)
while still producing the per-vector `_compute.py` the corpus convention
expects. Re-run this generator, then run each `_compute.py`, to
regenerate the whole negative corpus deterministically.

Run: python _gen_all.py        # writes the 38 _compute.py files
     python _gen_all.py --run   # also runs each one
"""
from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Each row: slot dir, tamper-class label, the body of a `mutate(audit)`
# function (operating on the baseline dict in place, returning the
# concrete seq N where relevant), and the pinned output fields.
#
# `baseline` selects which baseline builder kwargs to use.
# `output` is (status, step, reason, exit_code, anomaly).
# `<N>` in reason is replaced with the row's `seq` before writing.
# `mutate` is Python source for the per-vector tamper, with `_lib` and
# `audit` in scope; it MUST set `tamper` (a dict) describing the change.

# ---------------------------------------------------------------------------
# Phase 1 — core MAC / fingerprint / signature / header integrity
# (derivable from the single / rotation baseline; real walkable fixtures)
# ---------------------------------------------------------------------------
TABLE = [
    dict(
        slot="N001-payload-hash-bit-flip",
        seq=3, baseline=dict(n_events=5),
        about="One byte of seq=3's payload_hash flipped post-capture; §7 step 9 recomputes the real MAC and rejects the stored value.",
        mutate=(
            "e = audit['entries'][2]\n"
            "ph = bytearray.fromhex(e['payload_hash_hex']); ph[0] ^= 0x01\n"
            "e['payload_hash_hex'] = ph.hex()\n"
            "tamper = {'class':'payload_hash bit-flip','seq':3,'byte_index':0,'xor':'0x01'}\n"
        ),
        output=("FAIL", "9", "payload_hash MAC mismatch at seq <N>", 1, None),
    ),
    dict(
        slot="N002-events-reordered",
        seq=2, baseline=dict(n_events=5),
        about="Entries seq=2 and seq=3 swapped in file order without re-chaining; the structural walk at §7 step 6 finds the chain link broken.",
        mutate=(
            "audit['entries'][1], audit['entries'][2] = audit['entries'][2], audit['entries'][1]\n"
            "tamper = {'class':'events reordered','swapped':[2,3]}\n"
        ),
        output=("FAIL", "6", "chain link broken at seq <N>", 1, None),
    ),
    dict(
        slot="N003-merkle-root-altered",
        seq=None, baseline=dict(n_events=5),
        about="The seal's merkle_root is set to garbage; §7 step 10 recomputes the root over the ledger and it does not match the sealed value.",
        mutate=(
            "audit['seal']['merkle_root_hex'] = '00'*32\n"
            "tamper = {'class':'merkle root altered','new':'00'*32}\n"
        ),
        output=("FAIL", "10", "merkle root mismatch — ledger contents do not produce sealed root", 1, None),
    ),
    dict(
        slot="N004-signature-garbage",
        seq=None, baseline=dict(n_events=5),
        about="The seal's signature is replaced with garbage bytes; §7 step 11 signature verification fails.",
        mutate=(
            "audit['seal']['signature_b64'] = 'Z' * 88\n"
            "tamper = {'class':'signature garbage'}\n"
        ),
        output=("FAIL", "11", "signature verification failed", 1, None),
    ),
    dict(
        slot="N005-signature-wrong-tenant",
        seq=None, baseline=dict(n_events=5),
        about="The seal is signed for a different tenant_id; tenant_id is bound into sign_payload, so §7 step 11 signature verification fails.",
        mutate=(
            "wrong = 'tenant-ffiec-test-OTHER'\n"
            "sp = _lib.build_sign_payload_v1_0a(algorithm=_lib.ALGORITHM, format_version=_lib.FORMAT_VERSION,\n"
            "    tenant_id=wrong, seal_date=audit['seal']['seal_date'],\n"
            "    merkle_root_hex=audit['seal']['merkle_root_hex'], hkdf_inputs_digest_hex=audit['seal']['hkdf_inputs_digest_hex'])\n"
            "audit['seal']['sign_payload_hex'] = sp.hex(); audit['seal']['sign_payload_text'] = sp.decode('utf-8')\n"
            "audit['seal']['signed_for_tenant_id'] = wrong\n"
            "tamper = {'class':'signature wrong tenant','signed_for':wrong}\n"
        ),
        output=("FAIL", "11", "signature verification failed", 1, None),
    ),
    dict(
        slot="N006-key-fingerprint-flipped",
        seq=2, baseline=dict(n_events=5),
        about="Entry seq=2's key_fingerprint flipped to arbitrary 16 bytes; §7 step 8 short-circuits BEFORE any MAC compute — the load-bearing ordering property.",
        mutate=(
            "e = audit['entries'][1]\n"
            "e['key_fingerprint_hex'] = 'ab'*16\n"
            "tamper = {'class':'key_fingerprint flipped','seq':2,'new':'ab'*16}\n"
        ),
        output=("FAIL", "8", "key_fingerprint mismatch at seq <N>: looked-up IKM does not match the entry's recorded fingerprint", 1, None),
    ),
    dict(
        slot="N007-unknown-key-version",
        seq=4, baseline=dict(n_events=5),
        about="Entry seq=4's key_version set to 99 (not in the test IKM registry); §7 step 7 rejects with no MAC compute.",
        mutate=(
            "e = audit['entries'][3]\n"
            "e['key_version'] = 99\n"
            "tamper = {'class':'unknown key_version','seq':4,'key_version':99}\n"
        ),
        output=("FAIL", "7", "unknown key_version: no IKM for (tenant=tenant-ffiec-test-1, key_version=99) at seq <N>", 1, None),
    ),
    dict(
        slot="N008-entry-format-version-mismatch",
        seq=2, baseline=dict(n_events=5),
        about="Entry seq=2's format_version set to v2; §7 step 5 rejects the per-entry format mismatch.",
        mutate=(
            "audit['entries'][1]['format_version'] = 'v2'\n"
            "tamper = {'class':'entry format_version mismatch','seq':2,'value':'v2'}\n"
        ),
        output=("FAIL", "5", "format_version mismatch at seq <N>", 1, None),
    ),
    dict(
        slot="N009-header-format-version-v2",
        seq=None, baseline=dict(n_events=5),
        about="Header format_version set to v2; §7 step 1 pre-flight rejects. Per §10.12, a step-1 value rejection still reached §7 so the exit code is Fail (1), not StructuralInputError.",
        mutate=(
            "audit['header']['format_version'] = 'v2'\n"
            "tamper = {'class':'header format_version','value':'v2'}\n"
        ),
        output=("FAIL", "1", "format_version v2 not supported by this verifier (running v1)", 1, None),
    ),
    dict(
        slot="N010-header-hkdf-digest-flipped",
        seq=None, baseline=dict(n_events=5),
        about="Header hkdf_inputs_digest flipped; §7 step 2 recomputes the digest from the §4.1 byte values and it no longer matches.",
        mutate=(
            "d = bytearray.fromhex(audit['header']['hkdf_inputs_digest_hex']); d[0] ^= 0x01\n"
            "audit['header']['hkdf_inputs_digest_hex'] = d.hex()\n"
            "tamper = {'class':'header hkdf digest flipped','byte_index':0}\n"
        ),
        output=("FAIL", "2", "header HKDF inputs do not match running v1 inputs", 1, None),
    ),
    dict(
        slot="N011-header-genesis-nonzero",
        seq=None, baseline=dict(n_events=5),
        about="Header genesis_hash set to non-zero bytes; §7 step 3 rejects (§4.1 inviolate property 5: seq=1 prev_hash is 32 zero bytes).",
        mutate=(
            "audit['header']['genesis_hash_hex'] = '01' + '00'*31\n"
            "tamper = {'class':'header genesis nonzero','value':'01'+'00'*31}\n"
        ),
        output=("FAIL", "3", "header genesis_hash does not match v1 constant", 1, None),
    ),
    dict(
        slot="N012-cross-chain-tenant-mismatch",
        seq=3, baseline=dict(n_events=5),
        about="Entry seq=3's event.tenant_id differs from the header's; §7 step 4 detects a cross-chain lift.",
        mutate=(
            "e = audit['entries'][2]\n"
            "e['event']['tenant_id'] = 'tenant-ffiec-test-OTHER'\n"
            "e['event_canonical_hex'] = _lib.jcs_canonicalize(e['event']).hex()\n"
            "tamper = {'class':'cross-chain tenant mismatch','seq':3,'event_tenant':'tenant-ffiec-test-OTHER'}\n"
        ),
        output=("FAIL", "4", "cross-chain lift detected at seq <N> (event.tenant_id mismatch)", 1, None),
    ),
    dict(
        slot="N015-prev-hash-substituted",
        seq=4, baseline=dict(n_events=5),
        about="Entry seq=4's prev_hash substituted, payload_hash left alone; the §7 step 6 structural walk catches the broken link before the MAC step.",
        mutate=(
            "e = audit['entries'][3]\n"
            "ph = bytearray.fromhex(e['prev_hash_hex']); ph[0] ^= 0x01\n"
            "e['prev_hash_hex'] = ph.hex()\n"
            "tamper = {'class':'prev_hash substituted','seq':4,'byte_index':0}\n"
        ),
        output=("FAIL", "6", "chain link broken at seq <N>", 1, None),
    ),
    dict(
        slot="N016-prev-hash-and-payload-recomputed-by-attacker",
        seq=4, baseline=dict(n_events=5),
        about="Attacker substitutes seq=4's prev_hash AND recomputes payload_hash WITHOUT the IKM (using a wrong key); the §7 step 6 structural walk catches the prev_hash substitution, and even if relaxed the MAC step would catch the attacker's MAC.",
        mutate=(
            "e = audit['entries'][3]\n"
            "fake_prev = bytes([0x42])*32\n"
            "# Attacker has no IKM; recompute the MAC under a wrong key so the\n"
            "# stored payload_hash is internally consistent with fake_prev but\n"
            "# not with the verifier's real session key.\n"
            "wrong_key = bytes([0x99])*32\n"
            "canonical = bytes.fromhex(e['event_canonical_hex'])\n"
            "fake_mac = _lib.hmac.new(wrong_key, fake_prev + canonical, _lib.hashlib.sha256).digest()\n"
            "e['prev_hash_hex'] = fake_prev.hex(); e['payload_hash_hex'] = fake_mac.hex()\n"
            "tamper = {'class':'prev_hash + payload recomputed by attacker','seq':4}\n"
        ),
        output=("FAIL", "6", "chain link broken at seq <N>", 1, None),
    ),
    dict(
        slot="N020-algorithm-key-type-mismatch",
        seq=None, baseline=dict(n_events=1),
        about="Seal claims algorithm ed25519 but the resolved public key for public_key_id is RSA-3072; §7 step 11 reports the specific algorithm/key-type mismatch, NOT the generic signature-verification-failed.",
        mutate=(
            "audit['seal']['public_key_id'] = 'tenant-ffiec-test-1.rsa-3072-misconfigured'\n"
            "audit['seal']['resolved_public_key_type'] = 'rsa-3072'\n"
            "tamper = {'class':'algorithm/key-type mismatch','seal_algorithm':'ed25519','resolved_key_type':'rsa-3072'}\n"
        ),
        output=("FAIL", "11", "algorithm/key-type mismatch at signature verification", 1, None),
    ),
    dict(
        slot="N022-format-version-v1-1",
        seq=None, baseline=dict(n_events=5),
        about="Header format_version set to v1.1 (unrecognized minor within the v1 family); §7 step 1 rejects.",
        mutate=(
            "audit['header']['format_version'] = 'v1.1'\n"
            "tamper = {'class':'header format_version','value':'v1.1'}\n"
        ),
        output=("FAIL", "1", "format_version v1.1 not supported by this verifier (running v1)", 1, None),
    ),
    dict(
        slot="N023-format-version-case-variant",
        seq=None, baseline=dict(n_events=5),
        about="Header format_version set to V1 (uppercase; case-variant of the recognized lowercase v1); §7 step 1 rejects on the exact byte form.",
        mutate=(
            "audit['header']['format_version'] = 'V1'\n"
            "tamper = {'class':'header format_version case-variant','value':'V1'}\n"
        ),
        output=("FAIL", "1", 'format_version "V1" not supported by this verifier (running v1)', 1, None),
    ),
    # -----------------------------------------------------------------------
    # N013 — file pre-flight truncation. Structural input error (exit 2).
    # The tamper produces an NDJSON rendering whose final byte is not \n.
    # -----------------------------------------------------------------------
    dict(
        slot="N013-mid-write-truncation",
        seq=None, baseline=dict(n_events=5),
        about="The audit file ends mid-line (writer-crash simulation): the NDJSON rendering of the file has its trailing newline removed AND the final event line is truncated mid-serialization. The verifier refuses at file pre-flight BEFORE parsing the header — §10.12 StructuralInputError (exit 2).",
        mutate=(
            "import json as _json\n"
            "lines = [_json.dumps(audit['header'], separators=(',',':'))]\n"
            "for e in audit['entries']:\n"
            "    lines.append(_json.dumps(e, separators=(',',':')))\n"
            "lines.append(_json.dumps(audit['seal'], separators=(',',':')))\n"
            "ndjson = '\\n'.join(lines) + '\\n'\n"
            "# Simulate the crash: drop the trailing newline and chop the last 17 bytes\n"
            "truncated = ndjson[:-1][:-17]\n"
            "audit['_ndjson_truncated'] = truncated\n"
            "audit['_ndjson_full_byte_len'] = len(ndjson.encode('utf-8'))\n"
            "audit['_truncated_byte_len'] = len(truncated.encode('utf-8'))\n"
            "tamper = {'class':'mid-write truncation','dropped_trailing_newline':True,'chopped_bytes':17}\n"
        ),
        output=("FAIL", "pre-flight", "audit file ends mid-line — possible mid-write crash", 2, None),
    ),
]

# ---------------------------------------------------------------------------
# N014 — botched rotation (key_version=1 re-used for a DIFFERENT IKM).
# Needs its own builder: build a chain where seq=4 stamps key_version=1
# but its MAC/fingerprint were produced under ikm_v2. §7 step 8 catches it.
# ---------------------------------------------------------------------------
TABLE.append(dict(
    slot="N014-botched-rotation",
    seq=4, baseline=dict(n_events=5),
    about="key_version=1 re-used for a different IKM (ikm_v2) at seq=4 (same tenant). The entry stamps key_version=1 but its fingerprint is ikm_v2's; §7 step 8 catches the fingerprint mismatch — the load-bearing per-tenant rotation defence.",
    mutate=(
        "e = audit['entries'][3]\n"
        "# Operator botched rotation: kept key_version=1 but the entry was\n"
        "# produced under ikm_v2. The fingerprint is ikm_v2's; key_version is 1.\n"
        "fp_v2 = _lib.key_fingerprint(_lib.TENANT_ID, _lib.IKM_V2)\n"
        "e['key_fingerprint_hex'] = fp_v2.hex()  # ikm_v2 fingerprint\n"
        "e['key_version'] = 1                      # but stamps generation 1\n"
        "tamper = {'class':'botched rotation','seq':4,'stamped_key_version':1,'actual_ikm':'v2'}\n"
    ),
    output=("FAIL", "8", "key_fingerprint mismatch at seq <N>", 1, None),
))

# ---------------------------------------------------------------------------
# Phase: dual-algorithm (N017/N018/N019) — DEFERRED-v1.x.
# v1.0 ships single-algorithm Ed25519 only; these need Dilithium3 keys +
# signatures that do not exist at v1.0. We pin the verifier-output triple
# (the reason strings are deterministic) and ship a structural seal fixture
# carrying the posture descriptor, so the gate executes and asserts the
# INDEX-pinned reason. The PQ signatures land in the v1.x materialization.
# ---------------------------------------------------------------------------
TABLE.append(dict(
    slot="N017-dual-algo-partial-coverage",
    seq=None, baseline=dict(n_events=5, rotation=True),
    about="DEFERRED-v1.x: dual-algorithm posture. Seal carries only the ed25519 signature while the institution's declared posture is [ed25519, dilithium3]. PASS-WITH-ANOMALY (control-completeness, regardless of --strict). The Dilithium3 keypair is a v1.x materialization dependency; this fixture pins the posture descriptor + the normative anomaly reason.",
    mutate=(
        "audit['seal']['declared_algorithm_posture'] = ['ed25519','dilithium3']\n"
        "audit['seal']['signatures'] = [{'algorithm':'ed25519','public_key_id':'tenant-ffiec-test-1.ed25519','signature_b64':'TEST-ED25519-PLACEHOLDER'}]\n"
        "audit['seal']['_deferred_v1x'] = 'dilithium3 signature not materialized at v1.0'\n"
        "tamper = {'class':'dual-algo partial coverage','present':['ed25519'],'declared':['ed25519','dilithium3']}\n"
    ),
    output=("PASS-WITH-ANOMALY", "11", "partial-coverage seal: single-algorithm signature during institution's declared dual-algorithm posture", 0, "partial-coverage seal: single-algorithm signature during institution's declared dual-algorithm posture"),
))
TABLE.append(dict(
    slot="N018-dual-algo-not-in-posture",
    seq=None, baseline=dict(n_events=5, rotation=True),
    about="DEFERRED-v1.x: seal carries slh_dsa_shake_128s, not on the declared [ed25519, dilithium3] posture. --strict: FAIL (exit 1); non-strict: PASS-WITH-ANOMALY. Pins the --strict disposition (the conformance bar) + the normative reason. PQ signatures are a v1.x dependency.",
    mutate=(
        "audit['seal']['declared_algorithm_posture'] = ['ed25519','dilithium3']\n"
        "audit['seal']['signatures'] = [\n"
        "    {'algorithm':'ed25519','public_key_id':'tenant-ffiec-test-1.ed25519','signature_b64':'TEST-ED25519-PLACEHOLDER'},\n"
        "    {'algorithm':'dilithium3','public_key_id':'tenant-ffiec-test-1.dilithium3','signature_b64':'TEST-DILITHIUM3-PLACEHOLDER'},\n"
        "    {'algorithm':'slh_dsa_shake_128s','public_key_id':'tenant-ffiec-test-1.slhdsa','signature_b64':'TEST-SLHDSA-PLACEHOLDER'}]\n"
        "audit['seal']['_deferred_v1x'] = 'PQ signatures not materialized at v1.0'\n"
        "tamper = {'class':'dual-algo not in posture','unexpected':['slh_dsa_shake_128s'],'declared':['ed25519','dilithium3']}\n"
    ),
    output=("FAIL", "11", "algorithm not on institution's declared posture list at seal_date 2026-05-06", 1, "unknown_algorithms: [slh_dsa_shake_128s]"),
))
TABLE.append(dict(
    slot="N019-dual-algo-one-valid-one-invalid",
    seq=None, baseline=dict(n_events=5, rotation=True),
    about="DEFERRED-v1.x: co-signed seal, ed25519 validates, dilithium3 does not (one byte flipped). --strict: FAIL (exit 1); non-strict: PASS-WITH-ANOMALY. Pins the --strict disposition + the normative co-signed-failure reason. PQ signatures are a v1.x dependency.",
    mutate=(
        "audit['seal']['declared_algorithm_posture'] = ['ed25519','dilithium3']\n"
        "audit['seal']['signatures'] = [\n"
        "    {'algorithm':'ed25519','public_key_id':'tenant-ffiec-test-1.ed25519','signature_b64':'TEST-ED25519-VALID-PLACEHOLDER'},\n"
        "    {'algorithm':'dilithium3','public_key_id':'tenant-ffiec-test-1.dilithium3','signature_b64':'TEST-DILITHIUM3-INVALID-PLACEHOLDER'}]\n"
        "audit['seal']['per_algorithm_results'] = {'ed25519':'PASS','dilithium3':'FAIL'}\n"
        "audit['seal']['_deferred_v1x'] = 'PQ signatures not materialized at v1.0'\n"
        "tamper = {'class':'dual-algo one valid one invalid','valid':'ed25519','invalid':'dilithium3'}\n"
    ),
    output=("FAIL", "11", "co-signed seal failure: algorithm ed25519 validated, algorithm dilithium3 did not", 1, None),
))

# ---------------------------------------------------------------------------
# Phase 2 + 3 — extension-primitive vectors (N024-N038).
# These target §10.x extension primitives whose POSITIVE cases (034, 035,
# 037, 039, 040, ...) carry their own schema. Where the tamper is a
# self-contained structural mutation we encode it faithfully; the §7-walk
# wiring for these extension primitives is a known follow-up on the Go side
# (the gate today asserts the INDEX-pinned reason in expected_output.txt).
# Each fixture is a real JSON descriptor of the tamper per the recipe.
# ---------------------------------------------------------------------------
EXT = [
    dict(slot="N024-acquirer-hsm-signature-mismatch", seq=None,
         about="§10.39 successor-attestation: the envelope's declared acquirer_hsm_key_fingerprint does not match the key under which the to-entity dual_signatures entry actually verifies (Variant A: declared-fingerprint corruption).",
         struct=("{'_about':ABOUT,'tamper':{'class':'acquirer-HSM fingerprint mismatch','variant':'A declared-fingerprint corruption'},"
                 "'successor_envelope':{'acquirer_hsm_key_fingerprint':'00'+'ff'*31,"
                 "'dual_signatures':[{'role':'from_entity','signature_b64':'TEST-FROM-PLACEHOLDER'},"
                 "{'role':'to_entity','signature_b64':'TEST-TO-PLACEHOLDER-verifies-under-real-key'}],"
                 "'_note':'to_entity signature verifies under the real key; declared fingerprint points elsewhere'}}"),
         output=("FAIL", "§10.39 acquirer_hsm_key_fingerprint cross-binding to dual_signatures",
                 "acquirer-HSM signature verification failed at successor anchor", 1, None)),
    dict(slot="N025-backfill-merkle-root-corrupted", seq=None,
         about="§10.42 backfill seal: the seal's apex merkle_root is corrupted by a single-byte flip; the recomputed root over (baseline manifest leaves + metadata leaf) differs (Variant C: baseline manifest leaf path → step 2 / root recomputation).",
         struct=("{'_about':ABOUT,'tamper':{'class':'backfill merkle root corrupted','variant':'C baseline-manifest leaf'},"
                 "'backfill_seal':{'merkle_root_hex':'00'+'11'*31,'backfill_seq':1,"
                 "'baseline_manifest':[{'artifact':'pre-acq-day-01','sha256':'00'*32}],"
                 "'_note':'apex root corrupted; recomputed root over leaves differs'}}"),
         output=("FAIL", "§10.42 step 2 (Merkle root verification)",
                 "backfill merkle root mismatch at backfill seq <N>", 1, None), seq_lit=1),
    dict(slot="N027-state-machine-invalid-transition", seq=None,
         about="§10.43 / §1.5 state machine: a closed → opened transition (no transition out of a terminal state). The validator rejects at index 0.",
         struct=("{'_about':ABOUT,'tamper':{'class':'illegal state transition'},"
                 "'transitions_table':{'opened':['pending','closed'],'pending':['decided','closed'],'decided':['closed'],'closed':[]},"
                 "'walk':[{'from_state':'closed','to_state':'opened'}]}"),
         output=("FAIL", "§7 step 12", "state-machine illegal transition at seq <N>: closed → opened", 1, None), seq_lit=0),
    dict(slot="N028-adjuster-anchor-missing-reverse-link", seq=None,
         about="§10.45 bidirectional cross-anchor: the cedent-side anchor references the reinsurer entry, but the reinsurer-side anchor's peer_party_chain_entries is empty (Variant A). Check (a) fails.",
         struct=("{'_about':ABOUT,'tamper':{'class':'missing reverse link','variant':'A empty peer list'},"
                 "'cedent_anchor':{'peer_party_chain_entries':[{'peer_run_id':'reinsurer-claim-001','peer_seq':2}]},"
                 "'reinsurer_anchor':{'peer_party_chain_entries':[]}}"),
         output=("FAIL", "§7 step 11", "adjuster anchor missing reverse link to insurer chain entry", 1, None)),
    dict(slot="N029-bordereau-reconciled-before-received", seq=None,
         about="§10.46 lifecycle: a reconciled event for a bordereau_id has no prior received event from the same party (published → reconciled, skipping received).",
         struct=("{'_about':ABOUT,'tamper':{'class':'lifecycle out of order','skipped':'received'},"
                 "'bordereau_id':'polaris-bordereau-2026-05','reconciling_party_identifier':'polaris-reinsurance-bermuda',"
                 "'lifecycle':[{'seq':0,'event':'published'},{'seq':1,'event':'reconciled'}]}"),
         output=("FAIL", "§7 step 12", "bordereau lifecycle out of order at seq <N>", 1, None), seq_lit=1),
    dict(slot="N030-output-hash-mismatch", seq=2,
         about="§10.49 generative-AI output binding: a routing/output attribute inside the canonical bytes is altered post-capture; §7 step 9 re-MACs and rejects. Derived from the single baseline seq=2 with one attribute mutated.",
         struct=None,
         output=("FAIL", "9", "payload_hash MAC mismatch at seq <N>", 1, None),
         mutate=("e = audit['entries'][1]\n"
                 "e['event']['attributes']['ai_output_grounding'] = 'tampered-output-claim'\n"
                 "e['event_canonical_hex'] = _lib.jcs_canonicalize(e['event']).hex()\n"
                 "# §7 step 9 recomputes the MAC over the new canonical bytes; the stored\n"
                 "# payload_hash (over the original bytes) no longer matches.\n"
                 "tamper = {'class':'output hash mismatch','seq':2,'altered_attr':'ai_output_grounding'}\n")),
    dict(slot="N031-retrieval-merkle-tampered", seq=None,
         about="§10.49 retrieval-set Merkle: the retrieval-set Merkle root bound into the entry is tampered; recomputation over the retrieval set does not match.",
         struct=("{'_about':ABOUT,'tamper':{'class':'retrieval merkle tampered'},"
                 "'retrieval_set_merkle_root_hex':'00'+'22'*31,"
                 "'retrieval_set':[{'doc_id':'kb-001','sha256':'aa'*32},{'doc_id':'kb-002','sha256':'bb'*32}]}"),
         output=("FAIL", "§7 step 11", "retrieval set Merkle root mismatch", 1, None)),
    dict(slot="N032-hitl-signature-bad", seq=3,
         about="§10.50 human-in-the-loop: the HITL reviewer signature on the seq=3 entry fails verification. Derived from the single baseline with a HITL signature attribute injected + corrupted.",
         struct=None,
         output=("FAIL", "§7 step 11", "HITL reviewer signature verification failed at seq <N>", 1, None),
         mutate=("e = audit['entries'][2]\n"
                 "e['hitl_review'] = {'reviewer_id':'analyst-7','signature_b64':'Z'*88,'_note':'corrupted HITL signature'}\n"
                 "tamper = {'class':'HITL signature bad','seq':3}\n")),
    dict(slot="N033-dp-noise-seed-tampered", seq=2,
         about="§10.51 differential-privacy overlay: the DP noise seed inside the canonical bytes is altered post-capture; §7 step 9 re-MACs and rejects. Derived from the single baseline seq=2.",
         struct=None,
         output=("FAIL", "9", "payload_hash MAC mismatch at seq <N>", 1, None),
         mutate=("e = audit['entries'][1]\n"
                 "e['event']['attributes']['dp_noise_seed'] = 'tampered-seed-value'\n"
                 "e['event_canonical_hex'] = _lib.jcs_canonicalize(e['event']).hex()\n"
                 "tamper = {'class':'DP noise seed tampered','seq':2}\n")),
    dict(slot="N034-decadal-reseal-previous-anchor-mismatch", seq=None,
         about="§10.54 decadal re-sealing: the decadal re-seal's previous-anchor reference does not match the prior decade's seal apex; §7 step 11 rejects.",
         struct=("{'_about':ABOUT,'tamper':{'class':'decadal reseal previous-anchor mismatch'},"
                 "'decadal_reseal':{'seal_date':'2036-05-06','previous_anchor_hex':'00'+'33'*31,"
                 "'actual_prior_decade_apex_hex':'cc'*32,'_note':'previous_anchor does not match prior decade apex'}}"),
         output=("FAIL", "§7 step 11", "decadal re-seal previous-anchor mismatch at seal_date 2036-05-06", 1, None)),
    dict(slot="N035-challenge-response-disposition-out-of-order", seq=None,
         about="§10.55 audit-target challenge-response: a disposition event precedes its challenge (out of order). §7 step 12 lifecycle check rejects.",
         struct=("{'_about':ABOUT,'tamper':{'class':'challenge-response out of order'},"
                 "'sequence':[{'seq':0,'event':'disposition'},{'seq':1,'event':'challenge'}]}"),
         output=("FAIL", "§7 step 12", "challenge-response disposition out of order at seq <N>", 1, None), seq_lit=0),
    dict(slot="N036-otlp-json-bytes-encoding", seq=2,
         about="DEFERRED-v1.x receiver-decoder hardening: an OTLP/JSON emission encodes payload_hash under padding-stripped base64; the receiver decodes to different bytes and §7 step 9 re-MAC rejects. Derived from the single baseline seq=2; the malformed-encoding marker rides on the entry.",
         struct=None,
         output=("FAIL", "9", "payload_hash MAC mismatch at seq <N>", 1, None),
         mutate=("e = audit['entries'][1]\n"
                 "import base64 as _b64\n"
                 "raw = bytes.fromhex(e['payload_hash_hex'])\n"
                 "good = _b64.b64encode(raw).decode('ascii')\n"
                 "bad = good.rstrip('=')  # padding-stripped (non-conformant per §4.4)\n"
                 "e['otlp_json_payload_hash_b64'] = bad\n"
                 "e['_malformed_encoding'] = 'padding-stripped base64 (§4.4 violation)'\n"
                 "tamper = {'class':'OTLP/JSON bytes encoding','seq':2,'encoding':'padding-stripped base64'}\n")),
    dict(slot="N037-leap-second-captured-at", seq=2,
         about="§10.4 leap-second: two adjacent entries' captured_at straddle a leap second (23:59:60Z then 23:59:60.5Z). A CONFORMANT verifier emits PASS with a clock-skew anomaly (ordering preserved by seq), NOT a chain-link-broken FAIL. This vector pins the conformant PASS disposition; the non-conformant reaction is the false-positive it guards against.",
         struct=None,
         output=("PASS", "", "clock-skew anomaly at seq <N>: captured_at non-monotonic across leap-second boundary; ordering preserved by seq", 0,
                 "clock-skew anomaly at seq <N>: captured_at non-monotonic across leap-second boundary; ordering preserved by seq"),
         mutate=("audit['entries'][0]['event']['captured_at'] = '2026-12-31T23:59:60Z'\n"
                 "audit['entries'][1]['event']['captured_at'] = '2026-12-31T23:59:60.5Z'\n"
                 "# captured_at is provenance-only (NOT in the canonical MAC bytes), so\n"
                 "# adding it does not change payload_hash; ordering stays seq-driven.\n"
                 "tamper = {'class':'leap-second captured_at','conformant_disposition':'PASS with anomaly'}\n")),
    dict(slot="N021-routing-event-tampered", seq=2,
         about="DEFERRED-v1.x: §4.4.1 routing. A routing attribute (audit.routing.provider_chosen) inside the canonical bytes is altered post-capture; §7 step 9 re-MACs and rejects — proving routing attributes are inside the chain-MAC-covered canonical bytes. Derived from the single baseline seq=2.",
         struct=None,
         output=("FAIL", "9", "payload_hash MAC mismatch at seq <N>", 1, None),
         mutate=("e = audit['entries'][1]\n"
                 "e['event']['attributes']['audit.routing.provider_chosen'] = 'tampered-provider-route'\n"
                 "e['event_canonical_hex'] = _lib.jcs_canonicalize(e['event']).hex()\n"
                 "# The stored payload_hash was MAC'd over the original canonical bytes;\n"
                 "# the §7 step 9 recompute over the tampered routing attribute differs.\n"
                 "tamper = {'class':'routing event tampered','seq':2,'altered_attr':'audit.routing.provider_chosen'}\n")),
    dict(slot="N026-additional-verifications-invalid-string", seq=None,
         about="DEFERRED-v1.x: §10.12 strict-mode post-§7 verdict-output validation. The verdict object's additional_verifications array carries an unknown marker (Variant B: uppercase case-variant of a spec string). Under --strict the verifier rejects with exit code 3 (configuration/strict-mode); the chain itself PASSes §7. This is verifier-OUTPUT validation, not chain integrity.",
         struct=("{'_about':ABOUT,'tamper':{'class':'additional_verifications invalid string','variant':'B uppercase case-variant'},"
                 "'chain_status':'PASS (§7 integrity intact)',"
                 "'verdict_object':{'exit_code':0,'posture':'ffiec','additional_verifications':['BACKFILL_SEAL_VERIFIED'],"
                 "'_note':'BACKFILL_SEAL_VERIFIED is an uppercase variant of the lowercase spec string; not in the v1.0 closed enumeration'}}"),
         output=("FAIL", "§10.12 strict-mode (post-§7)", 'additional_verifications marker "BACKFILL_SEAL_VERIFIED" not in v1.0 enumeration', 3, None)),
    dict(slot="N038-discovery-production-form", seq=None,
         about="DEFERRED-v1.x: §10.13.1 discovery production form. The production packet omits the per-entry canonical-bytes/ artifact; the production-manifest pre-flight refuses. Pins the missing-artifact reason.",
         struct=("{'_about':ABOUT,'tamper':{'class':'discovery production form missing artifact','missing':'canonical-bytes/'},"
                 "'production_manifest':{'artifacts_present':['ndjson','verdict-object','seal-records','hsm-pubkey','trust-anchor-manifest'],"
                 "'artifacts_missing':['canonical-bytes/']}}"),
         output=("FAIL", "pre-flight", "production manifest missing required artifact: canonical-bytes/", 1, None)),
]

# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
COMPUTE_TEMPLATE = '''# -*- coding: utf-8 -*-
"""{slot} — auto-generated from negative/_gen_all.py.

{about}

This generator builds the valid baseline from the central corpus inputs,
applies the single documented mutation, and writes input.json (the
tampered fixture) plus expected_output.txt (the §7 Status/Step/Reason +
§10.12 exit code the verifier MUST emit). Never hand-crafts a hash.

Run: python _compute.py
"""
from __future__ import annotations
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _lib  # noqa: E402

HERE = _lib.here_of(__file__)
ABOUT = {about!r}


def main() -> None:
{body}
    _lib.write_expected_output(
        HERE, status={status!r}, step={step!r}, reason={reason!r},
        reason_template={reason_template!r},
        exit_code={exit_code}, anomaly={anomaly!r},
    )
    print("[{slot}] materialized:", {status!r}, {step!r}, {reason!r})


if __name__ == "__main__":
    main()
'''


def _sub_seq(text: str, seq) -> str:
    if seq is None:
        return text
    return text.replace("<N>", str(seq))


def parse_index_reasons() -> dict[str, str]:
    """Extract each negative vector's expected-reason cell from INDEX.md
    EXACTLY as the Go gate does: split the table row on '|', trim each
    cell, drop the empty outer cells, then trim a single layer of
    backticks off the reason cell (cells[2]). This is the byte-verbatim
    contract string the gate matches `expected_output.txt` against."""
    reasons: dict[str, str] = {}
    index_path = os.path.join(HERE, "INDEX.md")
    with open(index_path, encoding="utf-8") as f:
        for line in f.read().split("\n"):
            if not line.strip().startswith("|"):
                continue
            parts = [c.strip() for c in line.strip().split("|")]
            if parts and parts[0] == "":
                parts = parts[1:]
            if parts and parts[-1] == "":
                parts = parts[:-1]
            if len(parts) < 5:
                continue
            slot = parts[0]
            if not (len(slot) >= 2 and slot[0] == "N" and slot[1].isdigit()):
                continue
            reasons[slot] = parts[2].strip("`")
    return reasons


INDEX_REASONS = parse_index_reasons()


def render_baseline_vector(row: dict) -> str:
    seq = row.get("seq")
    seq_for_reason = seq if seq is not None else row.get("seq_lit")
    reason = _sub_seq(row["output"][2], seq_for_reason)
    anomaly = row["output"][4]
    if anomaly is not None:
        anomaly = _sub_seq(anomaly, seq_for_reason)
    body_lines = [
        f"    audit = _lib.clone_baseline(**{row['baseline']!r})",
    ]
    for ln in row["mutate"].rstrip("\n").split("\n"):
        body_lines.append("    " + ln)
    body_lines.append("    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}")
    body_lines.append("    _lib.write_input_json(HERE, record)")
    body = "\n".join(body_lines)
    return COMPUTE_TEMPLATE.format(
        slot=row["slot"], about=row["about"], body=body,
        status=row["output"][0], step=row["output"][1], reason=reason,
        reason_template=INDEX_REASONS[row["slot"]],
        exit_code=row["output"][3], anomaly=anomaly,
    )


def render_ext_vector(row: dict) -> str:
    seq_for_reason = row.get("seq") if row.get("seq") is not None else row.get("seq_lit")
    reason = _sub_seq(row["output"][2], seq_for_reason)
    anomaly = row["output"][4]
    if anomaly is not None:
        anomaly = _sub_seq(anomaly, seq_for_reason)
    if row.get("struct"):
        body = (
            f"    record = {row['struct']}\n"
            f"    _lib.write_input_json(HERE, record)"
        )
    else:
        # mutate-from-baseline ext vector (N030/N032/N033/N036/N037)
        body_lines = ["    audit = _lib.clone_baseline(n_events=5)"]
        for ln in row["mutate"].rstrip("\n").split("\n"):
            body_lines.append("    " + ln)
        body_lines.append("    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}")
        body_lines.append("    _lib.write_input_json(HERE, record)")
        body = "\n".join(body_lines)
    return COMPUTE_TEMPLATE.format(
        slot=row["slot"], about=row["about"], body=body,
        status=row["output"][0], step=row["output"][1], reason=reason,
        reason_template=INDEX_REASONS[row["slot"]],
        exit_code=row["output"][3], anomaly=anomaly,
    )


def main() -> None:
    run = "--run" in sys.argv
    written = []
    for row in TABLE:
        src = render_baseline_vector(row)
        path = os.path.join(HERE, row["slot"], "_compute.py")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
        written.append(row["slot"])
    for row in EXT:
        src = render_ext_vector(row)
        path = os.path.join(HERE, row["slot"], "_compute.py")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
        written.append(row["slot"])

    print(f"wrote {len(written)} _compute.py files")
    if run:
        for slot in written:
            cp = os.path.join(HERE, slot, "_compute.py")
            r = subprocess.run([sys.executable, cp], capture_output=True, text=True)
            tag = "OK " if r.returncode == 0 else "ERR"
            print(f"  [{tag}] {slot}: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[:200]}")


if __name__ == "__main__":
    main()
