from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from sampling_mining_workflows_dsl.element.LazySet import LazySet
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from sampling_mining_workflows_dsl.element.Repository import Repository

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue

class Loader(ABC):
    def __init__(self, *metadatas: Metadata | None):
        # Assuming the first metadata is the ID, store its name for further use
        self.metadata_id_name = metadatas[0].name
        self.metadatas: dict[str, Metadata] = {}
        for metadata in metadatas:
            self.metadatas[metadata.name] = metadata

    @abstractmethod
    def load_set(self) -> LazySet:
        pass

    def create_repository_from_map(self, map_object: dict[str, Any]) -> Repository:
        id_metadata_value = map_object.get(self.metadata_id_name)

        if id_metadata_value is None or id_metadata_value == "":
            raise ValueError(f"Invalid ID {self.metadata_id_name}")

        repo = Repository(self.metadatas.get(self.metadata_id_name))

        metadata_values: list[MetadataValue] = []
        for metadata in self.metadatas.values():
            try:
                metadata_value = metadata.create_metadata_value(map_object.get(metadata.name))
                metadata_values.append(metadata_value)
            except Exception as e:
                raise ValueError(
                    f"Error creating metadata value for '{metadata.name}' with value '{map_object.get(metadata.name)}'",
                ) from e

        repo.add_metadata_values(metadata_values)
        return repo