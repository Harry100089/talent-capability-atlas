# Talent Capability Atlas

An AI agent that builds a capability map for a team based on engineering artifacts.

It:
* Aggregates skill signals from commits, RFCs, and tickets
* Infers ownership and detects single points of failure
* Identifies gaps relative to a target role
* Suggests staffing and growth opportunities
* Tracks skill changes over time

## Input

Provided via `input.json`:

```json
{
  "people_list": ["Alice", "Bob", "Charlie"],
  "role_target": "Senior Applied Scientist",
  "org_hint": "Search relevance team"
}
```

## Output

The agent produces a structured `CapabilityAtlas` including:

* Skill profile per person (with confidence + evidence)
* Domain ownership map
* Risk flags (single-owner domains)
* Skill gaps vs target role
* Staffing suggestions
* Growth summary (if previous snapshot exists)
* Uncertainty note


## How It Works

### 1. Retrieval (Budgeted)

For each person:

* Fetch most recent artifacts (mocked GitHub, RFCs, Jira)
* Prioritize recency
* Limit to top-N per person to simulate cost constraints

### 2. Skill Extraction

* Use HuggingFace LLM to extract structured skill signals
* Return JSON with confidence scores
* Attach artifact-backed evidence

### 3. Aggregation

* Merge skill signals across team
* Infer domain ownership
* Flag single points of failure
* Compare against role target to detect gaps

### 4. Refresh & Change Detection

* Save snapshot of last run
* On next run:

  * Compare skill sets
  * Detect new expertise
  * Recompute risk areas

## Data Model

Artifacts are mocked with this structure:

```json
{
  "id": "unique-id",
  "type": "github_commit | rfc | jira_ticket",
  "author | assignee": "person-name",
  "message | summary": "text with skill signals",
  "timestamp": "YYYY-MM-DD",
  "url": "source-link"
}
```

Care was taken so skills are inferred from the mocks and not pre-labeled.

## Refresh Strategy

* Store previous `CapabilityAtlas` snapshot
* On re-run:

  * Diff skill sets per person
  * Flag newly emerged skills
  * Update risk and ownership signals
* Designed for periodic execution (e.g., weekly)

## Uncertainty Handling

* Per-skill confidence score from LLM
* Explicit uncertainty note in output
* Limited artifact budget per person
* Evidence attached to every skill

## Run
Create a .env
```
HF_API_KEY=hugging_face_api_key_here
```

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python main.py
```
