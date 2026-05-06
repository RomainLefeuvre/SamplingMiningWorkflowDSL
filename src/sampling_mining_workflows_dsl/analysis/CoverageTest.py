from collections import Counter

from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata


class CoverageTest:
    def __init__(self, metadata: Metadata, set_1: EagerSet, set_2: EagerSet):
        self.metadata = metadata
        self.set_1 = set_1
        self.set_2 = set_2

    def compute_coverage(self, top_x: int = None) -> float:
        counter = Counter()
        for element in self.set_1.get_elements():
            values = element.get_metadata_value(self.metadata).get_value()
            counter.update(self.flatten(values))

        if top_x is not None:
            top_values = {item for item, _ in counter.most_common(top_x)}
        else:
            top_values = set(counter.elements())

        set_1_unique = {
            v
            for element in self.set_1.get_elements()
            for v in self.flatten(element.get_metadata_value(self.metadata).get_value())
            if v in top_values
        }

        set_2_unique = {
            v
            for element in self.set_2.get_elements()
            for v in self.flatten(element.get_metadata_value(self.metadata).get_value())
        }

        if not set_1_unique:
            print(
                f"No value for {self.metadata.name}. Couverture = 0.0"
            )
            return 0.0

        intersection = set_1_unique.intersection(set_2_unique)
        coverage = len(intersection) / len(set_1_unique)

        print(
            f"Coverage for {self.metadata.name} (top {top_x if top_x is not None else 'all'}): {coverage:.2f}"
        )
        return coverage

    def flatten(self, values):
        if isinstance(values, list):
            result = []
            for v in values:
                if isinstance(v, list):
                    result.extend(v)
                else:
                    result.append(v)
            return result
        return [values]
