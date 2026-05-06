from typing import TypeVar

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.operator.Operator import Operator
from sampling_mining_workflows_dsl.operator.selection.sampling.SamplingOperator import (
    SamplingOperator,
)
from sampling_mining_workflows_dsl.operator.set_algebra import ExternalSetOperator

T = TypeVar("T")


class UnionOperator(ExternalSetOperator):
    def __init__(self, workflow, indexes=[-1]):
        super().__init__(workflow)
    def set_function(self, a, b):
        return a.union(b)
