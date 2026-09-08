from scripts.story_character_pressure import compile_character_pressure


def test_core_character_requires_independent_motion_and_scene_agency():
    result = compile_character_pressure({
        "id": "region-1",
        "characters": [
            {
                "id": "greg",
                "name": "Greg",
                "tier": "core",
                "want": "keep the job",
                "off_camera_motion": ["trains alone before work"],
                "competence": ["reads leverage and physical systems"],
                "cost_or_limit": ["current body cannot execute remembered timing"],
                "scene_vectors": ["changes route when the original plan fails"],
                "relationship_specificity": ["with Jorren, resists being treated as fragile"],
            }
        ],
    })

    assert result["warnings"] == []
    assert result["checks"]["core_cast_has_independent_motion"] is True
    assert result["checks"]["core_cast_has_scene_agency"] is True


def test_flat_recurring_character_is_flagged():
    result = compile_character_pressure({
        "id": "region-2",
        "characters": [
            {
                "id": "helper",
                "name": "Mira",
                "tier": "recurring",
                "want": "help Greg",
                "off_camera_motion": [],
                "competence": [],
                "cost_or_limit": [],
                "scene_vectors": [],
                "relationship_specificity": [],
            }
        ],
    })

    joined = " ".join(result["warnings"])
    assert "character_without_off_camera_life:helper" in joined
    assert "character_without_scene_agency:helper" in joined
    assert "character_without_distinguishing_leverage:helper" in joined
    assert "character_relationship_too_generic:helper" in joined


def test_minor_extra_is_not_forced_to_carry_core_character_depth():
    result = compile_character_pressure({
        "id": "region-3",
        "characters": [
            {
                "id": "clerk-1",
                "name": "Pela",
                "tier": "extra",
                "want": "finish the queue",
            }
        ],
    })

    assert not any(warning.startswith("character_without_") for warning in result["warnings"])


def test_similar_names_are_flagged_against_local_and_active_roster():
    result = compile_character_pressure({
        "id": "region-4",
        "active_roster": [
            {"id": "jorren", "name": "Jorren"},
            {"id": "hessa", "name": "Hessa"},
        ],
        "characters": [
            {
                "id": "joran",
                "name": "Joran",
                "tier": "recurring",
                "want": "win control of the yard",
                "off_camera_motion": ["recruits two fighters between scenes"],
                "competence": ["organizes people quickly"],
                "cost_or_limit": ["cannot tolerate public loss of status"],
                "scene_vectors": ["offers a deal before Greg can frame the conflict"],
                "relationship_specificity": ["treats Greg as useful labor, not a rival"],
            },
            {
                "id": "torren",
                "name": "Torren",
                "tier": "local",
                "want": "get paid and leave",
            },
        ],
    })

    warnings = " ".join(result["warnings"])
    assert "name_similarity_collision:joran:jorren" in warnings
    assert "name_similarity_collision:torren:jorren" in warnings


def test_distinct_names_do_not_trigger_similarity_warning():
    result = compile_character_pressure({
        "id": "region-5",
        "active_roster": [
            {"id": "jorren", "name": "Jorren"},
            {"id": "hessa", "name": "Hessa"},
        ],
        "characters": [
            {"id": "sable", "name": "Sable", "tier": "local", "want": "buy the lease"},
            {"id": "ortho", "name": "Ortho", "tier": "local", "want": "keep his crew employed"},
        ],
    })

    assert not any(warning.startswith("name_similarity_collision:") for warning in result["warnings"])


def test_character_contract_asks_who_can_move_story_without_protagonist():
    result = compile_character_pressure({
        "id": "region-6",
        "characters": [],
    })

    joined = " ".join(result["questions"]).lower()
    assert "without the protagonist" in joined
    assert "off-camera" in joined
    assert "solve" in joined or "solution" in joined
