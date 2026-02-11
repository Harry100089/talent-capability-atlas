def compute_domain_ownership(profiles):
    domain_map = {}

    for p in profiles:
        for s in p.skills:
            domain_map.setdefault(s.skill, []).append(
                {"owner": p.name, "confidence": s.confidence}
            )

    return domain_map


def score_risks(domain_map, critical_skills):
    risks = []

    for skill, owners in domain_map.items():
        if skill in critical_skills:
            if len(owners) == 1:
                risks.append(f"HIGH RISK: {skill} owned by single person ({owners[0]['owner']})")
            elif len(owners) == 2:
                risks.append(f"MEDIUM RISK: {skill} has limited coverage")

    return risks
