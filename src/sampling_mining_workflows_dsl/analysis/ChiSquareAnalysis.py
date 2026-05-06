from collections import Counter

from scipy.stats import chisquare

from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

class ChiSquareAnalysis:
    def __init__(self, metadata: Metadata[str]):
        self.metadata = metadata

    def analyze(self, set_1: EagerSet, set_2: EagerSet):
        # Extract keywords from both sets
        keywords_1 = self.extract_keywords(set_1)
        keywords_2 = self.extract_keywords(set_2)

        all_labels = sorted(set(keywords_1 + keywords_2))

        pop_counts = [Counter(keywords_1).get(label, 0) for label in all_labels]
        sample_counts = [Counter(keywords_2).get(label, 0) for label in all_labels]

        total_pop = sum(pop_counts)
        total_sample = sum(sample_counts)
        scaled_pop = [x * (total_sample / total_pop) for x in pop_counts]

        chi2, p = chisquare(f_obs=sample_counts, f_exp=scaled_pop)

        print("Chi2:", chi2)
        print("p-value:", p)

    def extract_keywords(self, s: EagerSet):
        keywords = []
        for element in s.get_elements():
            metadata_value = element.get_metadata_value(self.metadata)
            if metadata_value:
                keywords.extend(metadata_value.get_value())
        return keywords
