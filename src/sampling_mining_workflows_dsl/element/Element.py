from abc import ABC, abstractmethod
from typing import TypeVar

from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue

T = TypeVar("T")


class Element(ABC):
    def __init__(self):
        self.metadata: dict[Metadata, MetadataValue] = {}

    def __hash__(self) -> int:
        return hash(frozenset(self.metadata.items()))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Element):
            return False
        return self.metadata == other.metadata

    def get_metadata_value(self, metadata: Metadata[T]) -> MetadataValue[T]:
        if metadata not in self.metadata:
            raise RuntimeError(f"Missing metadata {metadata.name}")
        return self.metadata[metadata]

    def add_metadata_values(self, metadata_values: list[MetadataValue]):
        for metadata_value in metadata_values:
            self.metadata[metadata_value.get_metadata()] = metadata_value

    def add_metadata_value(self, metadata_value: MetadataValue):
        self.metadata[metadata_value.get_metadata()] = metadata_value

    def get_all_metadata_values(self) -> dict[Metadata, MetadataValue]:
        return self.metadata.copy()

    @abstractmethod
    def get_id(self) -> str:
        raise NotImplementedError("Subclasses must implement get_id method")

    @abstractmethod
    def to_string(self, level: int) -> str:
        pass
