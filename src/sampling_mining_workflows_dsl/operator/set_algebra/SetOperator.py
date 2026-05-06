from typing import TypeVar

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.operator.Operator import Operator
from sampling_mining_workflows_dsl.operator.selection.sampling.SamplingOperator import (
    SamplingOperator,
)

T = TypeVar("T")


class SetOperator(Operator):
    set_function = None
    def __init__(self, workflow,other:EagerSet):
        self.other = other
        super().__init__(workflow)
        
      
    def execute(self) -> Operator:
        if not self._output.size()==0:
            print("Warning: output set is not empty, clearing it")
            self.output_set.remove_all_elements()

        self.output_set.add(self.input_set)
        self.set_function(self.output_set,set)
        super().execute()
        return self
    
   