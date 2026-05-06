import os
import pickle
from abc import ABC
from typing import TYPE_CHECKING, Optional

from sampling_mining_workflows_dsl.element.Loader import Loader
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.element.Writer import Writer

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue


class Operator(ABC):
    def __init__(self, worflow):
        self.workflow = worflow
        self._input: EagerSet | None = None
        self._output: EagerSet | None = None
        self._output_writer: Writer | None = None
        self._next_operator: Operator | None = None
        self._previous_operator: Operator | None = None
        # Loader to add metadata on output during the execution
        self._loader: Loader | None = None

    def add_metadata_loader(self, loader) -> "Operator":
        self._loader = loader
        return self
    
    def set_output_set_id(self, set_id: str) -> "Operator":
        if self._output is not None:
            self._output.set_id(set_id)
        return self
    
    def set_input_set_id(self, set_id: str) -> "Operator":
        if self._input is not None:
            self._input.set_id(set_id)
        return self

    def add_metadata(self) -> "Operator":
        # Add the new metadata to the existing workflow metadata list
        for metadata in self._loader.metadatas.values():
            if metadata != self._loader.metadata_id_name:
                self.workflow.add_metadata_type(metadata)

        # Load new metadata set
        new_metadata_set: EagerSet = self._loader.load_set()
        # Add metadata value to current output set
        for element in self._output.get_elements():
            if not isinstance(element, EagerSet):
                id = element.get_id()
                try:
                    new_element = new_metadata_set.get_element(id)
                    metadata_values: list[MetadataValue] = (
                        new_element.get_all_metadata_values().values()
                    )
                    metadata_values_filtered = [
                        x for x in metadata_values if x.get_value() != id
                    ]
                    element.add_metadata_values(metadata_values_filtered)

                except ValueError:
                    print(f"Element with id {id} not found in the metadata set")

    def execute(self) -> "Operator":
        if self._loader:
            self.add_metadata()

        if self._next_operator:
            self._next_operator._input = self._output
            self._next_operator.execute()
        elif self._output_writer:
            self._output_writer.write_set(self._output)
        return self

    def get_workflow_root_operator(self) -> "Operator":
        if self._previous_operator is None:
            return self
        return self._previous_operator.get_workflow_root_operator()

    def execute_workflow(self) -> "Operator":
        root = self.get_workflow_root_operator()
        root.input_set(self._input).execute()
        return self

    def get_next_operator(self) -> Optional["Operator"]:
        return self._next_operator

    def get_output(self) -> EagerSet | None:
        return self._output

    def get_merged_output(self) -> EagerSet:
        result = EagerSet()
        for element in self._output.get_elements():
            if isinstance(element, EagerSet):
                # Recursively flatten nested Sets
                result.union(element.flatten_set())
            else:
                # Add non-Set elements directly
                result.add_element(element)
        return result

    def output(self, writer: Writer) -> "Operator":
        self._output_writer = writer
        return self

    def input_set(self, input_set: EagerSet) -> "Operator":
        self._input = input_set
        return self

    def output_set(self, output_set: EagerSet) -> "Operator":
        self._output = output_set
        return self
    

    def get_input(self) -> EagerSet | None:
        return self._input

    def input(self, loader: Loader) -> "Operator":
        self._input = loader.load_set()
        return self

    def chain(self, operator: "Operator") -> "Operator":
        self._next_operator = operator
        operator._previous_operator = self
        return operator

    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, level: int = 0) -> str:
        indent = "    " * level
        double_indent = "    " * (level + 1)
        formatted_next_operator = (
            self._next_operator.to_string(level + 3)
            if self._next_operator
            else double_indent
        )

        class_name = self.__class__.__name__
        return (
            f"{indent}{class_name}\n"
            f"{double_indent}{self.extra_to_string(level)}\n"
            f"{double_indent}input:\n"
            f"{double_indent}{self._input.to_string(level + 2) if self._input else 'None'}\n"
            f"{double_indent}output:\n"
            f"{double_indent}{self._output.to_string(level + 2) if self._output else 'None'}\n"
            f"{double_indent}nextOperator:\n"
            f"{formatted_next_operator}"
        )

    def extra_to_string(self, level: int) -> str:
        return ""

    def short_str(self) -> str:
        return f"{self.__class__.__name__} (input size: {self._input.size() if self._input else 'None'}, output size: {self._output.size() if self._output else 'None'})"

    def serialize(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def deserialize(path: str) -> "Operator":
        with open(path, "rb") as file:
            return pickle.load(file)
