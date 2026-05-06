from sampling_mining_workflows_dsl.constraint.Constraint import Constraint
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.operator.Operator import Operator
from tqdm import tqdm


class FilterOperator(Operator):
    def __init__(self, workflow, constraint: Constraint):
        super().__init__(workflow)
        self._constraint = constraint
        constraint.set_workflow(workflow)

    def execute(self):
        self._output = self._input.filter(self._constraint)
        super().execute()
        return self

    def get_constraint(self) -> Constraint:
        return self._constraint

    def short_str(self) -> str:
        return str(self._constraint)+" "+super().short_str()