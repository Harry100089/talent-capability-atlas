# Talent Capability Atlas

AI agent that builds a structured capability map and gives recommendations from engineering artifacts.

## Input

`input.json`

```json
{
  "people_list": ["Alice", "Bob", "Charlie"],
  "role_target": "Senior Applied Scientist",
  "org_hint": "Search relevance team"
}
```

## Output

`capability_atlas.json` containing:

* Role requirements (LLM-defined)
* Per-person skill profile (confidence + evidence)
* Domain ownership map
* Collaboration graph
* Risk ranking (coverage + criticality aware)
* Personalized growth plans
* New experiment with staffing recommendations
* Timestamp

---

# Architecture

```
- Input
- LLM: define role requirements
- Retrieve artifacts (budgeted, adapter-based)
- LLM: extract skills
- LLM: normalize to canonical taxonomy
- Ownership aggregation
- Collaboration graph
- Risk scoring
- LLM: generate growth plans
- LLM: Recommend staffing for a new experiment
- Persist snapshot
```

Most logic lives in `engine`, `planner`, `llm`, and `tools`.

---

# Key Design Decisions

### Decision Making by LLM

LLM is used for:

* Role capability definition
* Skill extraction
* Skill normalization
* Growth planning
* Experiment suggestion & staffing

### Artifact Adapter and Data Tools

Artifacts accessed via:

```python
class ArtifactAdapter:
```

Current: `MockArtifactAdapter`
Late can be swapped with GitHub/Jira/etc. integrations


### Canonical Taxonomy

```python
CANONICAL_TAXONOMY = [...]
```

This is a predefined list organizational skill vocabulary. Used to normalize skills output from the LLM. The assumption is in production this would  come from config or an org-level competency framework.


### Ownership & Risk

Ownership inferred from:

* Skill frequency
* Confidence
* Artifact signals (RFC > commit)

Risk considers:

* Single-owner concentration
* Whether skill is critical to role_target


### Collaboration Graph

Edge weight = number of shared normalized skills.
Approximates knowledge overlap.

## Refresh Strategy

Profiles can be updated over time by re-running the agent on fresh artifact data.

### Approach

1. **Schedule**: Re-run periodically (e.g., weekly/monthly) to capture new commits, RFCs, and tickets
2. **Versioning**: Archive outputs with timestamps in `storage/` to track changes
3. **Delta detection**: Compare skill confidence across runs to identify growth or risk shifts
4. **Staleness**: Flag people with no recent artifacts (>30 days) as potential coverage gaps

### Future Work to Improve refresh / learning
- Automated diff comparison across versions
- Scheduled refresh via cron
- Alerts on risk elevation (e.g., single-owner skills becoming unavailable)

---

# Assumptions / Mocks

* Artifacts are mocked (commits, RFCs, tickets)
* Skills are inferred, not pre-labeled
* Retrieval is budget-limited (API / scraper costs)
* LLM JSON output assumed to be well-formed
* No real API integration

---

# To Run
Create an .env with the following:
```
HF_API_KEY=hugging_face_api_key_goes_here
```
Run the following:

```bash
# optionally but recommended to use a venv
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python main.py
```
