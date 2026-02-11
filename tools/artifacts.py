import json

DATA_PATH = "data/mock_artifacts.json"

class ArtifactAdapter:
    def get_artifacts(self, person, budget):
        raise NotImplementedError

class MockArtifactAdapter(ArtifactAdapter):
    def load_all_artifacts(self):
        with open(DATA_PATH) as f:
            return json.load(f)

    def get_artifacts(self, person: str, budget: int = 5):
        artifacts = self.load_all_artifacts()

        results = [
            a for a in artifacts
            if a.get("author") == person or a.get("assignee") == person
        ]

        # Sort newest first
        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return results[:budget]
