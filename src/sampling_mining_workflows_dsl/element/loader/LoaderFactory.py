from pathlib import Path

from sampling_mining_workflows_dsl.element.loader.JsonLoader import JsonLoader
from sampling_mining_workflows_dsl.element.loader.CsvLazyLoader import CsvLazyLoader
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata


class LoaderFactory:
    @staticmethod
    def json_loader(set_path: str, *metadatas: Metadata):
        return JsonLoader(Path(set_path), *metadatas)

    @staticmethod
    def json_loader_from_path(set_path: Path, *metadatas: Metadata):
        return JsonLoader(set_path, *metadatas)
    
    @staticmethod
    def csv_lazy_loader(set_path: str, *metadatas: Metadata):
        return CsvLazyLoader(Path(set_path), *metadatas)
