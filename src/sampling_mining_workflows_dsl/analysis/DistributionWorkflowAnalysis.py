
from typing import TYPE_CHECKING

from sampling_mining_workflows_dsl.analysis.kolmogorov_smirnov import kolmogorov_smirnov
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from sampling_mining_workflows_dsl.operator.clustering.GroupingOperator import GroupingOperator

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.element.EagerSet import EagerSet


class DistributionWorkflowAnalysis:
    def __init__(self, metadata: Metadata[int]):
        self.map: dict[str, EagerSet] = {}
        self.metadata = metadata

    def analyze(self, workflow):
        # Retrieve the root operator from the workflow
        root_operator = workflow.get_root()
        self.populate_map(root_operator, "")
        analyzer = kolmogorov_smirnov(self.metadata)
        entries = list(self.map.items())

        print("Kolmogorov-Smirnov Test:")

        for i in range(len(entries) - 1):
            for j in range(i + 1, len(entries)):
                name = f"{entries[i][0]} /// {entries[j][0]}"
                result = analyzer.analyze(entries[i][1], entries[j][1])

                print(name)
                print(result)
                print("------------------------------------------")

    def populate_map(self, workflow, prefix: str):
        op = workflow.get_workflow_root_operator()
        self.map[f"{prefix}input"] = op.get_input()
        count = 1

        while op is not None:
            if isinstance(op, GroupingOperator):
                grouping_operator: GroupingOperator = op
                self.map[f"{prefix}operator_{count}_merged"] = (
                    grouping_operator.get_merged_output()
                )

                child_count = 1
                for internal_w in grouping_operator.get_workflows():
                    self.populate_map(
                        internal_w, f"{prefix}operator_{count}_Child_{child_count}_"
                    )
                    child_count += 1
            else:
                self.map[f"{prefix}operator_{count}"] = op.get_output()

            count += 1
            op = op.get_next_operator()
