from tools.artifacts import ArtifactAdapter
from extractor import extract_skills
from models.schemas import PersonProfile


class TalentPlanner:
    def __init__(self, people, role_target, org_hint, adapter: ArtifactAdapter):
        self.people = people
        self.role_target = role_target
        self.org_hint = org_hint
        self.adapter = adapter

    def execute_plan(self):
        self.plan_steps = [
            "retrieve_artifacts",
            "extract_skills",
            "aggregate_signals",
            "detect_risks",
        ]

        profiles = []

        for person in self.people:
            artifacts = self.adapter.get_artifacts(person)
            skills = extract_skills(person, artifacts)
            profiles.append(PersonProfile(name=person, skills=skills))

        return profiles


def infer_domain_ownership(profiles):
    domain_map = {}

    for p in profiles:
        for s in p.skills:
            domain_map.setdefault(s.skill, []).append(p.name)

    return domain_map


def detect_risk_areas(domain_map):
    risks = []
    for skill, owners in domain_map.items():
        if len(owners) == 1:
            risks.append(f"{skill} primarily owned by {owners[0]}")
    return risks
