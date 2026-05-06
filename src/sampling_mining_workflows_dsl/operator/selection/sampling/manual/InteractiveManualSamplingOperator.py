from typing import TypeVar

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.operator.Operator import Operator
from sampling_mining_workflows_dsl.operator.selection.sampling.manual.ManualSamplingOperator import (
    ManualSamplingOperator,
)
from sampling_mining_workflows_dsl.Workflow import Workflow

T = TypeVar("T")


class InteractiveManualSamplingOperator[T](ManualSamplingOperator):
    def __init__(self, workflow: Workflow):
        super().__init__(workflow)

    def execute(self) -> Operator:
        self._output = EagerSet()

        print(f"input : \n{self._input.to_string() if self._input else 'None'}")
        for element in self._input.get_elements():
            if isinstance(element, Repository):
                user_input = (
                    input(
                        f"Do you want to keep the project with ID {element.get_id()}? (yes/no/stop): "
                    )
                    .strip()
                    .lower()
                )
                if user_input in {"yes", "y"}:
                    self._output.add_element(element)
                elif user_input in {"stop"}:
                    return self
            else:
                raise RuntimeError(
                    "Interactive manual sampling not implemented for sets"
                )

        return self
