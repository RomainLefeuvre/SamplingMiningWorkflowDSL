from typing import TypeVar, cast

from sampling_mining_workflows_dsl import CompleteWorkflow
from sampling_mining_workflows_dsl.analysis.DistributionWorkflowAnalysis import (
    DistributionWorkflowAnalysis,
)
from sampling_mining_workflows_dsl.analysis.HistWorkflowAnalysis import HistWorkflowAnalysis
from sampling_mining_workflows_dsl.analysis.YamaneWorkflowAnalysis import YamaneWorkflowAnalysis
from sampling_mining_workflows_dsl.constraint.Constraint import Constraint
from sampling_mining_workflows_dsl.element.Element import Element
from sampling_mining_workflows_dsl.element.Loader import Loader
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.element.Writer import Writer
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from sampling_mining_workflows_dsl.operator.clustering.GroupingOperator import GroupingOperator
from sampling_mining_workflows_dsl.operator.Operator import Operator
from sampling_mining_workflows_dsl.operator.selection.filter.FilterOperator import FilterOperator
from sampling_mining_workflows_dsl.operator.selection.sampling.automatic.RandomSelectionOperator import (
    RandomSelectionOperator,
)
from sampling_mining_workflows_dsl.operator.selection.sampling.manual.ManualSamplingOperator import (
    ManualSamplingOperator,
)

T = TypeVar("T")


class Workflow:
    def __init__(self):
        self._input: EagerSet | None = None
        self._output: EagerSet | None = None
        self._output_writer: Writer | None = None
        self._root: Operator | None = None
        self._last_operator: Operator | None = None
        self._metadata: list[Metadata] = []

    def get_all_Metadata(self) -> list[Metadata]:
        return self._metadata

    def add_metadata_type(self, metadata: Metadata) -> "Workflow":
        self._metadata.append(metadata)
        return self

    def grouping_operator(self, *workflows: "Workflow") -> "Workflow":
        if not workflows:
            raise ValueError("At least one workflow must be provided.")

        # Create a GroupingOperator with the provided sub workflows
        grouping_operator = GroupingOperator(self, *workflows)

        # Add the grouping operator to the current workflow
        self.add_operator(cast("Operator", grouping_operator))
        return self

    def random_selection_operator(self, cardinality: int, seed: int = -1) -> "Workflow":
        random_selection_operator = RandomSelectionOperator(
            self, cardinality=cardinality, seed=seed
        )
        self.add_operator(cast("Operator", random_selection_operator))
        return self

    def filter_operator(self, constraint: Constraint):
        filter_operator = FilterOperator(self, constraint)
        self.add_operator(cast("Operator", filter_operator))
        return self

    def manual_sampling_operator(self, *ids: T) -> "Workflow":
        if not ids:
            raise ValueError(
                "At least one element must be provided for manual sampling."
            )

        manual_sampling_operator = ManualSamplingOperator(self, *ids)
        self.add_operator(cast("Operator", manual_sampling_operator))
        return self
    
    def get_all_set_from_workflow(self, index=0):
        sets = {}
        if index==0:
            sets[index] = (self._input,None)
            index += 1

        op = self.get_root()
        while op is not None:
            if not isinstance(op, GroupingOperator):
                if hasattr(op, "_output") and op._output is not None:
                    sets[index] = (op._output,op)  # Fix: use index as key, not the Set object
                    index += 1
            else:
                for internal_w in op.get_workflows():
                    grouping_sets = internal_w.get_all_set_from_workflow(index)
                    index = index + len(grouping_sets)
                    sets.update(grouping_sets)  # Fix: use update() instead of extend()
            op = op.get_next_operator()
        return sets
    
    def get_internal_set_by_index(self,index):
        return self.get_all_set_from_workflow()[index]
        
    def get_internal_set_by_id(self, set_id: str) -> EagerSet | None:
        current: Operator= self._root
        while current is not None:
            output:EagerSet = current.get_output()
            if not output is None and output.get_id() == set_id:
                return output
            if current.isinstance(GroupingOperator):
                for w in current.get_workflows():
                    internal_set = w.get_internal_set_by_id(set_id)
                    if internal_set is not None:
                        return internal_set
            current = current._next_operator
        return None

    def input(self, loader: Loader) -> "Workflow":
        self._metadata = list(loader.metadatas.values())
        self._input = loader.load_set()
        return self

    def add_metadata(self, loader: Loader) -> "Workflow":
        # Add metadata value to last declared operator
        current_operator: Operator = self.get_last_operator()
        if current_operator:
            current_operator.add_metadata_loader(loader)
        return self

    def output(self, writer: Writer) -> "Workflow":
        self._output_writer = writer
        last_operator = self.get_last_operator()
        if last_operator:
            last_operator.output(writer)
        return self

    def is_complete(self) -> bool:
        return (
            self._root is not None
            and self._input is not None
            and self._output_writer is not None
        )

    def add_operator(self, operator: Operator):
        # If the workflow is empty, set the root operator
        if self._root is None:
            self._root = operator
            self._last_operator = operator

        # If the workflow already has operators, append the new operator to the end
        else:
            self._last_operator._next_operator = operator
            operator._previous_operator = self._last_operator
            operator.input_set(self._last_operator.get_output())
            self._last_operator.output_set(operator.get_output())
            self._last_operator = operator

        if self.is_complete():
            return CompleteWorkflow(self)
        return None

    def set_workflow_input(self, input_set: EagerSet | None) -> "Workflow":
        self._input = input_set
        if self._root is not None:
            self._root.input_set(input_set)
        return self

    def set_root_input(self, input_set: EagerSet | None) -> "Workflow":
        if self._root is None:
            raise ValueError("Cannot set root input when no root operator is defined.")
        self._root.input_set(input_set)
        return self

    def get_workflow_input(self) -> Element | None:
        return self._input

    def set_workflow_output(self, output_element: Element) -> "Workflow":
        self._output = output_element
        return self

    def get_workflow_output(self) -> EagerSet | None:
        return self._output

    def get_root(self) -> Operator | None:
        return self._root

    def get_last_operator(self) -> Operator | None:
        if self._root is None:
            return None
        current = self._root
        while current._next_operator is not None:
            current = current._next_operator
        return current

    def get_operator_by_position(self, position: int) -> Operator | None:
        if position < 0:
            return None
        current = self._root
        index = 0
        while current is not None:
            if index == position:
                return current
            current = current._next_operator
            index += 1
        return None

    def execute_workflow(self) -> "Workflow":
        root = self._root
        root.input_set(self._input)
        root.execute()
        self._output = self._last_operator.get_output()
        return self

    def print(self) -> "Workflow":
        print(self)
        return self

    def analyze_workflow(self, metadata: Metadata[T]) -> "Workflow":
        # Perform analysis on a given metadata
        # workflow_analysis = HistWorkflowAnalysis(metadata)
        workflow_distrib_analysis = DistributionWorkflowAnalysis(metadata=metadata)
        workflow_distrib_analysis.analyze(self)

        workflow_yamane_analysis = YamaneWorkflowAnalysis()
        workflow_yamane_analysis.analyze(self)

        workflow_hist_analysis = HistWorkflowAnalysis(metadata=metadata)
        workflow_hist_analysis.analyze(self)
        return self

    # --- Methods for workflow printing ---

    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, level: int):
        indent = "    " * level
        res = f"{indent}Workflow: [[[\n"
        # res = ""
        if self._root is not None:
            res += self._root.to_string(level)
        else:
            res += f"{indent}No operators defined in this workflow.\n"

        res += "\n" + indent + "]]]\n"
        return res
