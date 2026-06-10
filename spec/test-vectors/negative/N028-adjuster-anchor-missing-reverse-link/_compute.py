# -*- coding: utf-8 -*-
"""N028-adjuster-anchor-missing-reverse-link — auto-generated from negative/_gen_all.py.

§10.45 bidirectional cross-anchor: the cedent-side anchor references the reinsurer entry, but the reinsurer-side anchor's peer_party_chain_entries is empty (Variant A). Check (a) fails.

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
ABOUT = "§10.45 bidirectional cross-anchor: the cedent-side anchor references the reinsurer entry, but the reinsurer-side anchor's peer_party_chain_entries is empty (Variant A). Check (a) fails."


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'missing reverse link','variant':'A empty peer list'},'cedent_anchor':{'peer_party_chain_entries':[{'peer_run_id':'reinsurer-claim-001','peer_seq':2}]},'reinsurer_anchor':{'peer_party_chain_entries':[]}}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§7 step 11', reason='adjuster anchor missing reverse link to insurer chain entry',
        reason_template='adjuster anchor missing reverse link to insurer chain entry',
        exit_code=1, anomaly=None,
    )
    print("[N028-adjuster-anchor-missing-reverse-link] materialized:", 'FAIL', '§7 step 11', 'adjuster anchor missing reverse link to insurer chain entry')


if __name__ == "__main__":
    main()
