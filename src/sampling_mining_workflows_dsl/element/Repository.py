from sampling_mining_workflows_dsl.element.Element import Element
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata


class Repository(Element):
    def __init__(self, id_metadata: Metadata[str]):
        super().__init__()
        self.id = id_metadata

    def get_id(self) -> str:
        return self.get_metadata_value(self.id).get_value()

    def __hash__(self) -> int:
        return hash(self.get_id())

    def __eq__(self, other):
        if not isinstance(other, Repository):
            return False
        return self.get_id() == other.get_id()

    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, level: int = 0) -> str:
        indent = "    " * level
        return f"{indent}{self.get_metadata_value(self.id)}"
