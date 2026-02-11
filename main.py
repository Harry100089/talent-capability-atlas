import json
from datetime import datetime
from planner import TalentPlanner, infer_domain_ownership, detect_risk_areas
from models.schemas import CapabilityAtlas
from tools.artifacts import MockArtifactAdapter

STORAGE_PATH = "storage/latest_atlas.json"

def save_atlas(atlas):
    with open(STORAGE_PATH, "w") as f:
        f.write(atlas.model_dump_json(indent=2))

def load_previous_atlas():
    try:
        with open(STORAGE_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def load_input():
    with open("input.json") as f:
        return json.load(f)


def detect_gaps(profiles):
    required = [
        "Machine Learning",
        "Ranking",
        "Evaluation",
        "Infrastructure",
        "Data Pipelines"
    ]

    present = {skill.skill for p in profiles for skill in p.skills}
    return [r for r in required if r not in present]

def detect_skill_changes(previous, current_profiles):
    if not previous:
        return "No previous snapshot available."

    previous_skills = {
        p["name"]: {s["skill"] for s in p["skills"]}
        for p in previous["profiles"]
    }

    growth_notes = []

    for p in current_profiles:
        old = previous_skills.get(p.name, set())
        new = {s.skill for s in p.skills}

        added = new - old

        if added:
            growth_notes.append(
                f"{p.name} shows new signals in: {', '.join(added)}"
            )

    if not growth_notes:
        return "No major skill changes detected."

    return " | ".join(growth_notes)

def recommend_staffing(profiles):
    return [
        "Assign ranking experiments to Alice",
        "Infra scaling to Bob",
        "Pipeline reliability to Charlie",
        "Encourage cross-training on evaluation frameworks"
    ]


def main():
    inputs = load_input()

    previous_atlas = load_previous_atlas()

    planner = TalentPlanner(
        inputs["people_list"],
        inputs["role_target"],
        inputs["org_hint"],
        MockArtifactAdapter()
    )

    profiles = planner.execute_plan()

    growth_summary = detect_skill_changes(previous_atlas, profiles)

    domain_map = infer_domain_ownership(profiles)
    risks = detect_risk_areas(domain_map)
    gaps = detect_gaps(profiles)

    atlas = CapabilityAtlas(
        org_hint=inputs["org_hint"],
        role_target=inputs["role_target"],
        profiles=profiles,
        domain_ownership=domain_map,
        risk_areas=risks,
        gaps=gaps,
        recommendations=recommend_staffing(profiles),
        uncertainty_note=(
            "Artifacts limited to top recent items per person. "
            "Skill extraction derived from LLM and may contain classification noise."
        ),
        growth_summary=growth_summary,
        generated_at=str(datetime.now())
    )

    json_output = atlas.model_dump_json(indent=2)

    print(json_output)

    with open("capability_atlas.json", "w", encoding="utf-8") as f:
        f.write(json_output)

    save_atlas(atlas)

if __name__ == "__main__":
    main()
