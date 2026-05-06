import json
from pathlib import Path
from typing import TYPE_CHECKING, Any
import logging
from sampling_mining_workflows_dsl.element.Loader import Loader
from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue


class JsonLoader(Loader):
    def __init__(self, set_path: Path, *metadatas: Metadata):
        super().__init__(*metadatas)
        self.set_path = set_path
        self.set = EagerSet()

    def load_set(self) -> EagerSet:
        try:
            if self.set_path.is_dir():
                json_files = sorted(self.set_path.glob("*.json"))
                if not json_files:
                    raise RuntimeError(
                        f"No JSON files found in directory: {self.set_path}"
                    )
            else:
                if not self.set_path.exists():
                    raise RuntimeError(f"File not found: {self.set_path}")
                json_files = [self.set_path]

            for json_file in json_files:
                print(f"Loading JSON file: {json_file}")
                with json_file.open("r") as reader:
                    json_list: list[dict[str, Any]] = json.load(reader)
                    for json_obj in json_list:
                        try:
                            repository = self.create_repository_from_map(json_obj)
                            if repository is not None:
                                self.set.add_element(repository)
                        except Exception as e:
                            logging.info(f"Row skipped due to {e} : {json_obj}")
            return self.set
        except OSError as e:
            raise RuntimeError("Error reading the JSON file", e) from e

    @staticmethod
    def parse_args(args: list[str]) -> dict[str, str]:
        import argparse

        default_input_path = Path(__file__).parent / "input.json"

        parser = argparse.ArgumentParser(description="Sampling Workflow")
        parser.add_argument(
            "-i",
            "--inputPath",
            type=str,
            default=str(default_input_path),
            help="Input path file",
        )
        parsed_args = parser.parse_args(args)
        return vars(parsed_args)
