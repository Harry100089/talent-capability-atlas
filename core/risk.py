def compute_domain_ownership(profiles):
    domain_map = {}

    for p in profiles:
        for s in p.skills:
            domain_map.setdefault(s.skill, []).append(
                {
                    "owner": p.name,
                    "confidence": s.confidence,
                    "relevance": s.relevance_to_role,
                }
            )

    return domain_map


def score_risks(domain_map, critical_skills):
    scored_risks = []

    for skill, owners in domain_map.items():

        num_owners = len(owners)
        avg_conf = sum(o["confidence"] for o in owners) / num_owners
        avg_relevance = sum(o["relevance"] for o in owners) / num_owners

        critical_weight = 1.5 if skill in critical_skills else 1.0

        risk_score = (
            critical_weight
            * avg_relevance
            * (1 / num_owners)
            * (1 - avg_conf)
        )

        if risk_score > 0.5:
            severity = "HIGH"
        elif risk_score > 0.25:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        scored_risks.append(
            {
                "skill": skill,
                "severity": severity,
                "risk_score": round(risk_score, 3),
                "owners": [o["owner"] for o in owners],
            }
        )

    return sorted(
        scored_risks,
        key=lambda x: x["risk_score"],
        reverse=True
    )
