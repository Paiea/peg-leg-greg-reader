import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = runpy.run_path(str(ROOT / "scripts" / "audio_score_claim.py"))


def test_push_created_branch_accepts_only_new_branch_result():
    parse = MOD["push_created_branch"]
    branch = "audio/v2-greg-again-ch014-auto"
    created = "*\tabc123:refs/heads/audio/v2-greg-again-ch014-auto\t[new branch]\nDone"
    up_to_date = "=\tabc123:refs/heads/audio/v2-greg-again-ch014-auto\t[up to date]\nDone"

    assert parse(created, branch) is True
    assert parse(up_to_date, branch) is False


def test_push_created_branch_requires_exact_target_branch():
    parse = MOD["push_created_branch"]
    output = "*\tabc123:refs/heads/audio/v2-greg-again-ch015-auto\t[new branch]\nDone"

    assert parse(output, "audio/v2-greg-again-ch014-auto") is False
