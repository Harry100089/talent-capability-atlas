import json
from llm.client import call_llm
from llm.prompts import role_requirement_prompt
from models.schemas import RoleRequirements


class TalentPlanner:
    def __init__(self, role_target, org_hint):
        self.role_target = role_target
        self.org_hint = org_hint

    def define_role_requirements(self):
        prompt = role_requirement_prompt(self.role_target, self.org_hint)
        output = call_llm(prompt)
        data = json.loads(output)
        return RoleRequirements(**data)
