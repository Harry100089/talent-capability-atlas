from pydantic import BaseModel
from typing import List, Dict, Optional, Any


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

class StaffingRecommendation(BaseModel):
    experiment_name: str
    experiment_description: str
    recommended_staff: List[str]
    mentor_suggestions: Dict[str, str]
    rationale: List[str]
    risks: List[str]
    confidence: float

class CapabilityAtlas(BaseModel):
    org_hint: str
    role_target: str
    role_requirements: RoleRequirements
    profiles: List[PersonProfile]
    domain_ownership: Dict[str, List[Dict[str, Any]]]
    collaboration_graph: Dict[str, Dict[str, int]]
    risk_areas: List[Dict[str, Any]]
    critical_coverage: Dict[str, float]
    staffing_recommendation: Optional[StaffingRecommendation] = None
    generated_at: str
