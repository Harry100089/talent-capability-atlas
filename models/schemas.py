from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Evidence(BaseModel):
    source: str
    id: str
    snippet: str
    timestamp: Optional[str]


class SkillSignal(BaseModel):
    skill: str
    confidence: float
    evidence: List[Evidence]


class PersonProfile(BaseModel):
    name: str
    skills: List[SkillSignal]


class CapabilityAtlas(BaseModel):
    org_hint: str
    role_target: str
    profiles: List[PersonProfile]
    domain_ownership: dict
    risk_areas: List[str]
    gaps: List[str]
    recommendations: List[str]
    uncertainty_note: str
    growth_summary: str
    generated_at: str
