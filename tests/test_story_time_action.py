from scripts.story_time_action import compile_time_action_contract


def test_continuous_scene_does_not_require_elapsed_time_evidence():
    contract = compile_time_action_contract({
        "id": "scene-1",
        "time": {"gap_mode": "continuous_scene"},
        "action": {
            "pressure_sources": ["argument while carrying a broken prop"],
            "state_changes": ["prop becomes unusable"],
            "residue": ["repair obligation"],
        },
    })

    assert contract["time"]["gap_mode"] == "continuous_scene"
    assert "time_gap_without_state_change" not in contract["warnings"]
    assert "action_without_residue" not in contract["warnings"]


def test_elapsed_gap_requires_visible_or_structural_residue():
    contract = compile_time_action_contract({
        "id": "gap-1",
        "time": {
            "gap_mode": "off_camera_gap",
            "elapsed_hint": "six weeks",
        },
        "action": {},
    })

    assert "time_gap_without_state_change" in contract["warnings"]
    assert contract["checks"]["temporal_weight"] is False


def test_elapsed_gap_can_earn_large_progress_and_large_cost():
    contract = compile_time_action_contract({
        "id": "gap-2",
        "time": {
            "gap_mode": "deliberate_skip",
            "elapsed_hint": "three months",
            "growth_allowed": ["sword footwork becomes automatic"],
            "decay_risks": ["friendship cools after avoidance"],
            "missed_opportunities": ["job offered to someone else"],
            "routine_changes": ["training no longer needs supervision"],
        },
        "action": {
            "state_changes": ["protagonist can now execute the old technique"],
            "residue": ["the original reason for learning it has disappeared"],
        },
    })

    assert contract["checks"]["temporal_weight"] is True
    assert contract["checks"]["action_residue"] is True
    assert contract["warnings"] == []


def test_pressure_without_changed_state_is_flagged_as_empty_action():
    contract = compile_time_action_contract({
        "id": "fight-1",
        "time": {"gap_mode": "continuous_scene"},
        "action": {
            "pressure_sources": ["knife fight"],
            "state_changes": [],
            "residue": [],
        },
    })

    assert "action_without_residue" in contract["warnings"]
    assert contract["checks"]["action_residue"] is False


def test_contract_asks_about_off_camera_causality_and_changed_win_conditions():
    contract = compile_time_action_contract({
        "id": "mixed-1",
        "time": {
            "gap_mode": "compressed_repetition",
            "elapsed_hint": "two weeks",
            "off_camera_changes": ["customers begin recognizing the worker"],
        },
        "action": {
            "pressure_sources": ["theft turns into knife threat"],
            "win_condition_changes": ["catch thief -> recover what is safe and let thief leave"],
            "state_changes": ["money is partially lost"],
            "residue": ["cash handling procedure changes"],
        },
    })

    joined = " ".join(contract["questions"]).lower()
    assert "camera" in joined or "off-camera" in joined
    assert "waiting" in joined
    assert "win condition" in joined
