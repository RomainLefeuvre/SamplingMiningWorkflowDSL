from pathlib import Path
from typing import TYPE_CHECKING, Any

from sampling_mining_workflows_dsl.element.loader.CsvLoader import CsvLoader
from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.EagerSet import EagerSet
from sampling_mining_workflows_dsl.github_seart.metadata import all_metadatas

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue

class SEARTGithubLoader(CsvLoader):
    def __init__(self, set_path: Path):
        super().__init__(*all_metadatas)
        self.set_path = set_path
        self.set = EagerSet()

