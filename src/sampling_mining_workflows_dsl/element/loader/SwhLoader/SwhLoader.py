from datetime import date, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

from sampling_mining_workflows_dsl.element.Loader import Loader
from sampling_mining_workflows_dsl.element.loader.CsvLoader import CsvLoader
from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.Set import Set
from sampling_mining_workflows_dsl.element.loader.SwhLoader.SwhGraphApiClient import SWHGraphAPIClient
from sampling_mining_workflows_dsl.metadata.MetadataDate import MetadataDate
from sampling_mining_workflows_dsl.metadata.MetadataNumber import MetadataNumber
from sampling_mining_workflows_dsl.metadata.MetadataString import MetadataString
from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue
from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from tqdm import tqdm


if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue

class SwhLoader(Loader):
    def __init__(self,*all_metadatas:Metadata):
        super().__init__(*all_metadatas)
        self.swh_api_client :SWHGraphAPIClient=SWHGraphAPIClient()

    def load_set(self) -> Set:
        print("Loading SWH repositories...")
        swh_set = Set()
        repos_id = self.swh_api_client.get_all_origin_ids()
        with tqdm(repos_id, desc="Filtering elements", unit="repo_id") as pbar:
            for repo_id in pbar:
                repository = Repository(self.metadatas[self.metadata_id_name])
                for metadata in self.metadatas.values():
                    if metadata is swh_url:
                        metadata_value = SwhUrlMetadataValue(metadata,self.swh_api_client,repo_id)
                    elif metadata is swh_commit_count:
                        metadata_value = SwhCommitCountMetadataValue(metadata,self.swh_api_client,repo_id)
                    elif metadata is swh_id:
                        metadata_value = metadata.create_metadata_value(repo_id)
                    elif metadata is swh_commiter_count:
                        metadata_value = SwhCommitterCountMetadataValue(metadata,self.swh_api_client,repo_id)
                    elif metadata is swh_latest_commit_date:
                        metadata_value = SwhLatestCommitDateMetadataValue(metadata,self.swh_api_client,repo_id)
                    else:
                        raise ValueError(f"Unsupported metadata type: {metadata.name}")
                    repository.add_metadata_value(metadata_value)
                swh_set.add_element(repository)
        print("SWH repositories loaded.")
       # print("cache")
        #self.swh_api_client.cache_latest_commit_dates()
        self.swh_api_client.cache_commit_counts()
        self.swh_api_client.cache_committer_counts()
        #print("SWH repositories cached.")
        return swh_set


swh_url :MetadataString = MetadataString(
    name="swh_url",
)

swh_commit_count:MetadataNumber = MetadataNumber(
    name="swh_commit_count",
    type_=int,
)

swh_id :MetadataNumber = MetadataNumber(
    name="swh_id",
    type_=int,
)

swh_commiter_count:MetadataNumber = MetadataNumber(
    name="swh_commiter_count",
    type_=int,
)

swh_latest_commit_date:MetadataDate = MetadataDate(
    name="swh_latest_commit_date",
)

class SwhUrlMetadataValue(MetadataValue[str]):
    def __init__(self, metadata ,swh_api_client:SWHGraphAPIClient,id_value:int):
        super().__init__(metadata, "default_value")
        self.swh_api_client=swh_api_client
        self.id_value=id_value
    
    def get_value(self):
        return self.swh_api_client.get_origin_url(self.id_value)

class SwhCommitCountMetadataValue(MetadataValue[int]):
    def __init__(self, metadata ,swh_api_client:SWHGraphAPIClient,id_value:int):
        super().__init__(metadata, 0)
        self.swh_api_client=swh_api_client
        self.id_value=id_value
    
    def get_value(self):
        return self.swh_api_client.get_commit_count(self.id_value)
    
class SwhCommitterCountMetadataValue(MetadataValue[int]):
    def __init__(self, metadata ,swh_api_client:SWHGraphAPIClient,id_value:int):
        super().__init__(metadata, 0)
        self.swh_api_client=swh_api_client
        self.id_value=id_value
    
    def get_value(self):
        return self.swh_api_client.get_committer_count(self.id_value)
    
class SwhLatestCommitDateMetadataValue(MetadataValue[Union[datetime, date]]):
    def __init__(self, metadata ,swh_api_client:SWHGraphAPIClient,id_value:int):
        super().__init__(metadata, 0)
        self.swh_api_client=swh_api_client
        self.id_value=id_value
    
    def get_value(self):
        timestamp = self.swh_api_client.get_latest_commit_date(self.id_value)
        if timestamp is None:
            return datetime.min
        return datetime.fromtimestamp(timestamp)