import csv
from pathlib import Path

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet


# Note that the depth of the set should be 1
class CsvWriter:
    def __init__(self, set_path: str):
        self.set_path = Path(set_path)

    def write_set(self, set_obj: EagerSet):
        if not isinstance(set_obj, EagerSet):
            raise TypeError("Expected a Set object")

        # Depth-1: elements are Repository instances
        repositories = set_obj.elements.values()

        if not repositories:
            raise ValueError("The set is empty. Nothing to write.")

        rows = [self._serialize_repository(repo) for repo in repositories]

        headers = sorted(rows[0].keys())

        try:
            with self.set_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
            print(f"CSV has been written to {self.set_path}")
        except OSError as e:
            raise RuntimeError("Error while saving file") from e

    def _serialize_repository(self, repo: Repository):
        if not isinstance(repo, Repository):
            raise TypeError("Expected Repository elements in the set")

        result = {}
        for meta, val in repo.get_all_metadata_values().items():
            value = val.get_value()
            if isinstance(value, list):
                value = ";".join(map(str, value))
            result[meta.name] = value
        return result
