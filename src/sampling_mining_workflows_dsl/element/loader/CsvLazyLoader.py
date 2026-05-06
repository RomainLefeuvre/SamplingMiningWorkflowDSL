import csv
from pathlib import Path
import logging

from sampling_mining_workflows_dsl.element.Element import Element
from sampling_mining_workflows_dsl.element.Loader import Loader
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from sampling_mining_workflows_dsl.element.LazySet import LazySet

class CsvLazyLoader(Loader):
    def __init__(self, set_path: Path, *metadatas: Metadata):
        super().__init__(*metadatas)
        self.set_path = set_path

    def load_set(self) -> LazySet:
        try:
            if self.set_path.is_dir():
                csv_files = sorted(self.set_path.glob("*.csv"))
                if not csv_files:
                    raise RuntimeError(
                        f"No CSV files found in directory: {self.set_path}"
                    )
            else:
                if not self.set_path.exists():
                    raise RuntimeError(f"File not found: {self.set_path}")
                csv_files = [self.set_path]
        except OSError as e:
            raise RuntimeError("Error reading the CSV file", e) from e

        def iterator():
            for csv_file in csv_files:
                print(f"Loading CSV file: {csv_file}")
                with csv_file.open("r", newline="") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            repository = self.create_repository_from_map(row)
                            if repository is not None:
                                yield repository
                        except Exception as e:
                            logging.info(f"Row skipped due to {e} : {row}")

        the_set = LazySet(iterator())
        self.set = the_set
        return the_set

