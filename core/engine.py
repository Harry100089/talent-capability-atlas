import json
from datetime import datetime

from tools.artifacts import MockArtifactAdapter
from core.planner import TalentPlanner
from core.risk import compute_domain_ownership, score_risks
from core.collaboration import build_collaboration_graph

from llm.extractor import extract_skills
from llm.normalizer import normalize_skills
from llm.growth import generate_growth_plan

from models.schemas import PersonProfile, CapabilityAtlas


class TalentAtlasEngine:
    def __init__(self, input_path):
        with open(input_path) as f:
            self.inputs = json.load(f)

        self.adapter = MockArtifactAdapter()

    def run(self):
        people = self.inputs["people_list"]
        role_target = self.inputs["role_target"]
        org_hint = self.inputs["org_hint"]

        planner = TalentPlanner(role_target, org_hint)
        role_requirements = planner.define_role_requirements()

        profiles = []

        for person in people:
            artifacts = self.adapter.get_artifacts(person, budget=5)

            raw_skills = extract_skills(artifacts)
            raw_skill_names = [s.skill for s in raw_skills]

            normalized = normalize_skills(raw_skill_names)

            growth_plan = generate_growth_plan(
                person,
                normalized,
                role_target,
                role_requirements.critical_skills,
            )

            profiles.append(
                PersonProfile(
                    name=person,
                    skills=raw_skills,
                    growth_plan=growth_plan,
                )
            )

        domain_map = compute_domain_ownership(profiles)
        risks = score_risks(domain_map, role_requirements.critical_skills)
        collaboration = build_collaboration_graph(profiles)

        return CapabilityAtlas(
            org_hint=org_hint,
            role_target=role_target,
            role_requirements=role_requirements,
            profiles=profiles,
            domain_ownership=domain_map,
            collaboration_graph=collaboration,
            risk_areas=risks,
            generated_at=str(datetime.now()),
        )

    def save(self, atlas):
        with open("capability_atlas.json", "w") as f:
            f.write(atlas.model_dump_json(indent=2))
