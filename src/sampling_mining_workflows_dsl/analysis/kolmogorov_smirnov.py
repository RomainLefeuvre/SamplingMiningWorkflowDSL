
from scipy.stats import ks_2samp

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata


class kolmogorov_smirnov:
    def __init__(self, metadata: Metadata[int]):
        self.metadata = metadata

    def analyze(self, a: EagerSet, sample: EagerSet) -> float:
        first_list = self.extract_list(a)
        second_list = self.extract_list(sample)

        # Perform the Kolmogorov-Smirnov test
        res = ks_2samp(first_list, second_list)
        return res

    def extract_list(self, s: EagerSet) -> list[int]:
        metadata_values = []

        for element in s.get_elements():
            if isinstance(element, Repository):
                repo: Repository = element
                metadata_value = repo.get_metadata_value(self.metadata)
                if metadata_value:
                    metadata_values.append(metadata_value.get_value())

        return metadata_values
