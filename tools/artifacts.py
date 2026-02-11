import json

DATA_PATH = "data/mock_artifacts.json"


class ArtifactAdapter:
    def get_artifacts(self, person, budget):
        raise NotImplementedError


class MockArtifactAdapter(ArtifactAdapter):
    def load_all(self):
        with open(DATA_PATH) as f:
            return json.load(f)

    def get_artifacts(self, person, budget=5):
        artifacts = self.load_all()

        results = [
            a for a in artifacts
            if a.get("author") == person or a.get("assignee") == person
        ]

        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return results[:budget]
