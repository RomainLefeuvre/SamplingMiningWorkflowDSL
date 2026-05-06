

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



def main():
    import os

    input_path = os.path.join(os.path.dirname(__file__), "input.csv")

    language = Metadata.of_string("language")
    id_ = Metadata.of_string("id")
    commit_nb = Metadata.of_integer("commitNb")


    w = (
        WorkflowBuilder()
        .input(LoaderFactory.csv_lazy_loader(input_path, id_, commit_nb, language))
        .filter_operator("commitNb > 2000 and commitNb < 7000")
        .random_selection_operator(40)
        .output(json_writer("out.json"))
    )


    w.execute_workflow()
    

if __name__ == "__main__":
    main()

