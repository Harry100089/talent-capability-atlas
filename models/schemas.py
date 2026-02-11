from pydantic import BaseModel
from typing import List, Dict, Optional


class Evidence(BaseModel):
    source: str
    id: str
    snippet: str
    timestamp: Optional[str]


class SkillSignal(BaseModel):
    skill: str
    confidence: float
    relevance_to_role: float  
    evidence: List[Evidence]


class PersonProfile(BaseModel):
    name: str
    skills: List[SkillSignal]
    growth_plan: List[str]


class RoleRequirements(BaseModel):
    critical_skills: List[str]


class CapabilityAtlas(BaseModel):
    org_hint: str
    role_target: str
    role_requirements: RoleRequirements
    profiles: List[PersonProfile]
    domain_ownership: Dict[str, Dict]
    collaboration_graph: Dict[str, Dict[str, int]]
    risk_areas: List[str]
    critical_coverage: dict
    generated_at: str
