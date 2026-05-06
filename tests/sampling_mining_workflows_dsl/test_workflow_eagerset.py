from sampling_mining_workflows_dsl.element.loader.LoaderFactory import LoaderFactory
from sampling_mining_workflows_dsl.element.writer.WriterFactory import WriterFactory
from sampling_mining_workflows_dsl.exec_visualizer.WorkflowVisualizer import WorkflowVisualizer
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from sampling_mining_workflows_dsl.operator.clustering.SubWorkflowOperatorBuilder import (
    SubWorkflowOperatorBuilder,
)
from sampling_mining_workflows_dsl.WorkflowBuilder import WorkflowBuilder

json_loader = LoaderFactory.json_loader
json_writer = WriterFactory.json_writer
filter_operator = SubWorkflowOperatorBuilder.filter_operator


def test_workflow_eagerset_simple():
    import os

    input_path = os.path.join(os.path.dirname(__file__), "input.json")

    language = Metadata.of_string("language")
    id_ = Metadata.of_string("id")
    commit_nb = Metadata.of_integer("commitNb")

    w = (
        WorkflowBuilder()
        .input(json_loader(input_path, id_, commit_nb, language))
        .filter_operator("commitNb > 2000 and commitNb < 7000")
        .random_selection_operator(40)
        .output(json_writer("out_eager.json"))
    )

    w.execute_workflow()

    import json
    with open("out_eager.json", 'r') as f:
        written_data = json.load(f)
        assert(len(written_data) == 40)
        assert(all(2000 < d["commitNb"] < 7000 for d in written_data))

