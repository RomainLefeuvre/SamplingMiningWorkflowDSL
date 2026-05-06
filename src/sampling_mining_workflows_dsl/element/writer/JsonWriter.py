import json
from datetime import datetime, date
from pathlib import Path

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.element.LazySet import LazySet


# Note: Can handle both flat sets (depth 1) and nested sets (depth > 1)
class JsonWriter:
    def __init__(self, set_path: str):
        self.set_path = Path(set_path)

    def write_set(self, set_obj: EagerSet):
        print(f"Writing set to JSON at: {self.set_path}")

        elements = [element for element in set_obj]

        if not elements:
            raise ValueError("The set is empty. Nothing to write.")

        rows = [self._serialize_element(elem) for elem in elements]

        try:
            with self.set_path.open("w", encoding="utf-8") as f:
                json.dump(rows, f, indent=4, ensure_ascii=False)
            print(f"JSON has been written to {self.set_path}")
        except OSError as e:
            raise RuntimeError("Error while saving file") from e

    def _serialize_element(self, element):
        """Serialize an element, which can be a Repository or a Set."""
        if isinstance(element, EagerSet):
            # Nested Set: serialize as an array of elements
            return [self._serialize_element(elem) for elem in element.elements.values()]
        elif isinstance(element, Repository):
            return self._serialize_repository(element)
        else:
            raise TypeError(f"Unexpected element type: {type(element)}")

    def _serialize_repository(self, repo: Repository):
        if not isinstance(repo, Repository):
            raise TypeError("Expected Repository elements in the set")

        result = {}
        for meta, val in repo.get_all_metadata_values().items():
            value = val.get_value()
            # Convert datetime/date to timestamp
            if isinstance(value, (datetime, date)):
                if isinstance(value, datetime):
                    value = int(value.timestamp())
                else:  # date object
                    value = int(datetime.combine(value, datetime.min.time()).timestamp())
            # Keep lists as lists in JSON (no need to join like CSV)
            result[meta.name] = value
        return result
