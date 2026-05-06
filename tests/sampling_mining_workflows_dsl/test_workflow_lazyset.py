import math

from sampling_mining_workflows_dsl.element.LazySet import LazySet
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata



from sampling_mining_workflows_dsl.element.loader.LoaderFactory import LoaderFactory

from sampling_mining_workflows_dsl.element.loader.CsvLazyLoader import CsvLazyLoader
from sampling_mining_workflows_dsl.element.writer.WriterFactory import WriterFactory
from sampling_mining_workflows_dsl.exec_visualizer.WorkflowVisualizer import WorkflowVisualizer
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from sampling_mining_workflows_dsl.operator.clustering.SubWorkflowOperatorBuilder import (
    SubWorkflowOperatorBuilder,
)
from sampling_mining_workflows_dsl.WorkflowBuilder import WorkflowBuilder

json_writer = WriterFactory.json_writer
filter_operator = SubWorkflowOperatorBuilder.filter_operator



def test_workflow_lazyset():
    import os

    input_path = os.path.join(os.path.dirname(__file__), "input.csv")

    language = Metadata.of_string("language")
    id_ = Metadata.of_string("id")
    commit_nb = Metadata.of_integer("commitNb")

    w = (
        WorkflowBuilder()
        .input(LoaderFactory.csv_lazy_loader(input_path, id_, commit_nb, language))
        .filter_operator("commitNb > 20000 and commitNb < 700000")
        .random_selection_operator(40)
        .output(json_writer("out_lazy.json"))
    )

    w.execute_workflow()

    import json
    with open("out_lazy.json", 'r') as f:
        written_data = json.load(f)
        assert(len(written_data) == 40)
        assert(all(20000 < d["commitNb"] < 700000 for d in written_data))
    
    WorkflowVisualizer(w, ".").generate_graph()

