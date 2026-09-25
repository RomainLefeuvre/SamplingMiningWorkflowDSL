import os
import re
from typing import cast

from graphviz import Digraph

from sampling_mining_workflows_dsl.constraint.BoolConstraintString import BoolConstraintString
from sampling_mining_workflows_dsl.constraint.BoolConstraint import BoolConstraint

from sampling_mining_workflows_dsl.operator.clustering.GroupingOperator import GroupingOperator
from sampling_mining_workflows_dsl.operator.selection.filter.FilterOperator import FilterOperator


class WorkflowVisualizer:
    def __init__(self, workflow, output_dir: str = "output_workflow_graph", wrap_constraint_operators: bool = False):
        self.workflow = workflow
        self.global_set_counter = 0  # Global counter shared across all levels
        self.wrap_constraint_operators = wrap_constraint_operators
        if output_dir:
            self.output_dir = output_dir
            os.makedirs(self.output_dir, exist_ok=True)
        else:
            self.output_dir = os.path.dirname(__file__)

    def generate_graph(self, output_file: str = "workflow_graph"):
        svg_path = os.path.join(self.output_dir, output_file)
        dot = Digraph(format="svg")
        dot.attr(rankdir="LR")

        # Add input node
        input_size = self.workflow.get_workflow_input().flatten_set().size()
        formatted_input_size = f"{input_size:,}".replace(',', ' ')
        dot.node(
            "InputSet",
            label=f"INITIAL\nSAMPLING FRAME\nSize : {formatted_input_size}",
            shape="box",
        )

        # Traverse and draw the workflow
        self.global_set_counter = 0  # Reset counter for each graph generation
        last_nodes = self._add_nodes_and_edges(
            dot, self.workflow, parent_names=["InputSet"]
        )

        # Add output node
        output_set = self.workflow.get_workflow_output().flatten_set()
        output_size = output_set.size()
        formatted_output_size = f"{output_size:,}".replace(',', ' ')
        dot.node("OutputSet", label=f"SAMPLE\nSize : {formatted_output_size}", shape="box")

        # Link last operator(s) to output
        for node in last_nodes:
            dot.edge(node, "OutputSet")

        # Render
        dot_path = dot.save(f"{svg_path}.dot")
        dot.render(svg_path, format="svg", cleanup=False)
        print(f"Workflow graph saved to {svg_path}")
        print(f"Editable Graphviz source saved to {dot_path}")

        # HTML wrapper
        self.create_html_page(svg_path)

    def _add_nodes_and_edges(
        self,
        dot,
        workflow,
        level: int = 0,
        workflow_number: int = 0,
        op_number: int = 0,
        parent_names=None,
    ) -> list[str]:
        if parent_names is None:
            parent_names = []

        op = workflow.get_root()
        last_nodes = []

        while op is not None:
            output_set = op.get_output()
            node_name = f"{op.__class__.__name__}_{level}_{workflow_number}_{op_number}"

            # Only increment counter for non-grouping operators
            if not isinstance(op, GroupingOperator):
                self.global_set_counter += 1
            
            # Label formatting with global set number
            if isinstance(op, FilterOperator) :
                if isinstance(op.get_constraint(), BoolConstraintString):
                    constraint = cast(
                        "BoolConstraintString", op.get_constraint()
                    ).get_string_constraint()
                    if self.wrap_constraint_operators:
                        constraint = re.sub(r'\s+(and|or)\s+', r'\n\1 ', constraint, flags=re.IGNORECASE)
                    formatted_size = f"{output_set.flatten_set().size():,}".replace(',', ' ')
                    label = f"Filter Operator\n{constraint}\n\nSET#{self.global_set_counter}\n Size : {formatted_size}"
                elif isinstance(op.get_constraint(), BoolConstraint):
                        constraint = cast(
                        "BoolConstraint", op.get_constraint()
                    )
                        function=constraint.constraint
                        
                        metadata=constraint.targeted_metadatas[0].name
                        # Get method name from qualname
                        method_name = "unknown"
                        if hasattr(function, '__qualname__'):
                            qualname = function.__qualname__
                            # Extract method name (e.g., "MetadataDate.is_after.<locals>.<lambda>" -> "is_after")
                            parts = qualname.split('.')
                            for part in parts:
                                if part.startswith('is_') or part in ['greater_than', 'less_than', 'equal']:
                                    method_name = part
                                    break
                        
                        # Get argument from closure
                        argument_value = "unknown"
                        if hasattr(function, '__closure__') and function.__closure__:
                            for cell in function.__closure__:
                                try:
                                    cell_content = cell.cell_contents
                                    # Skip metadata objects, look for actual values
                                    if not hasattr(cell_content, 'name') and not hasattr(cell_content, 'type'):
                                        # This might be the argument value
                                        if isinstance(cell_content, (str, int, float, bool)):
                                            argument_value = str(cell_content)
                                        elif hasattr(cell_content, '__class__'):
                                            # For dates, objects, etc.
                                            argument_value = str(cell_content)
                                        break
                                except (ValueError, AttributeError):
                                    continue
                        formatted_size = f"{output_set.flatten_set().size():,}".replace(',', ' ')

                        label = f"Filter Operator\n{metadata}.{method_name}({argument_value})\n\nSET#{self.global_set_counter}\n Size : {formatted_size}"
            elif isinstance(op, GroupingOperator):
                label = f"Grouping\nOperator"  # No number for grouping
            else:
                formatted_size = f"{output_set.flatten_set().size():,}".replace(',', ' ')
                label = f"{op.__class__.__name__.replace('Operator', '')}\nOperator\n\nSET#{self.global_set_counter}\n Size : {formatted_size}"

            dot.node(node_name, label=label, shape="box")

            # Link all incoming parent nodes
            for parent in parent_names:
                dot.edge(parent, node_name)

            # Handle grouping
            if isinstance(op, GroupingOperator):
                sub_last_nodes = []
                for i, sub_workflow in enumerate(op.get_workflows()):
                    sub_nodes = self._add_nodes_and_edges(
                        dot,
                        sub_workflow,
                        level=level + 1,
                        workflow_number=i,
                        op_number=0,
                        parent_names=[node_name],
                    )
                    sub_last_nodes.extend(sub_nodes)

                parent_names = (
                    sub_last_nodes  # They become the parents of the next operator
                )
                last_nodes = sub_last_nodes
            else:
                parent_names = [node_name]
                last_nodes = [node_name]

            op = op.get_next_operator()
            op_number += 1

        return last_nodes

    def create_html_page(self, svg_file: str, output_html: str = "workflow.html"):
        html_path = os.path.join(self.output_dir, output_html)

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Workflow Visualization</title>
        </head>
        <body>
            <h1>Workflow Visualization</h1>
            <div>
                <embed src="{os.path.basename(svg_file)}.svg" type="image/svg+xml" style="width:100%; height:90vh;"></embed>
            </div>
        </body>
        </html>
        """
        with open(html_path, "w") as f:
            f.write(html_content)
        print(f"HTML page saved to {html_path}")
