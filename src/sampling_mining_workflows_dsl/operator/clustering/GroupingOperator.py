
from typing import TYPE_CHECKING

from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.operator.Operator import Operator

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.Workflow import Workflow


class GroupingOperator(Operator):
    def __init__(self, root_workflow, workflows):
        super().__init__(root_workflow)

        self.workflows = workflows

    def execute(self) -> Operator:
        self._output = EagerSet()
        for w in self.workflows:
            # The input of the workflow is the input of the grouping operator
            w.set_workflow_input(self._input)

            w.execute_workflow()
            self._output.add_element(w.get_workflow_output())
        super().execute()
        return self

    def get_workflows(self) -> list["Workflow"]:
        return self.workflows

    def extra_to_string(self, level: int) -> str:
        indent = "    " * (level + 1)
        res = f"\n{indent}Internal Workflows:"
        for w in self.workflows:
            res += f"\n{w.to_string(level + 1)}"
        return res
