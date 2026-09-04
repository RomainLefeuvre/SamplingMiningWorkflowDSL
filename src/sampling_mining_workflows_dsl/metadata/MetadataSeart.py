
import json
from typing import TypedDict

from sampling_mining_workflows_dsl.metadata.Metadata import Metadata
from sampling_mining_workflows_dsl.metadata.MetadataValue import MetadataValue


class LanguageMetrics(TypedDict):
    commentLines: int
    codeLines: int
    blankLines: int

class MetadataMetrics(Metadata[dict[str, LanguageMetrics]]):
    def __init__(self, name: str):
        super().__init__(name, dict[str, LanguageMetrics])

    def create_metadata_value(self, value):
        # the raw value is list[dict[str, str|int]], convert it to dict[str, LanguageMetrics]
        typed_value = {}
        for item in json.loads(value):
            lang = item["language"]
            metrics = LanguageMetrics(
                commentLines=item.get("commentLines", 0),
                codeLines=item.get("codeLines", 0),
                blankLines=item.get("blankLines", 0),
            )
            typed_value[lang] = metrics

        return MetadataValue(self, typed_value)



id = Metadata.of_string("id")
name = Metadata.of_string("name")
isFork = Metadata.of_boolean("isFork")
commits = Metadata.of_integer("commits")
branches = Metadata.of_integer("branches")
releases = Metadata.of_integer("releases")
forks = Metadata.of_integer("forks")
mainLanguage = Metadata.of_string("mainLanguage")
defaultBranch = Metadata.of_string("defaultBranch")
license = Metadata.of_string("license")
homepage = Metadata.of_string("homepage")
watchers = Metadata.of_integer("watchers")
stargazers = Metadata.of_integer("stargazers")
contributors = Metadata.of_integer("contributors")
size = Metadata.of_integer("size")
createdAt = Metadata.of_date("createdAt")
pushedAt = Metadata.of_date("pushedAt")
updatedAt = Metadata.of_date("updatedAt")
totalIssues = Metadata.of_integer("totalIssues")
openIssues = Metadata.of_integer("openIssues")
totalPullRequests = Metadata.of_integer("totalPullRequests")
openPullRequests = Metadata.of_integer("openPullRequests")
blankLines = Metadata.of_integer("blankLines")
codeLines = Metadata.of_integer("codeLines")
commentLines = Metadata.of_integer("commentLines")
metrics = MetadataMetrics("metrics")
lastCommit = Metadata.of_date("lastCommit")
lastCommitSHA = Metadata.of_string("lastCommitSHA")
hasWiki = Metadata.of_boolean("hasWiki")
isArchived = Metadata.of_boolean("isArchived")
isDisabled = Metadata.of_boolean("isDisabled")
isLocked = Metadata.of_boolean("isLocked")
languages = Metadata.of_dict("languages", str, int, lambda s: json.loads(s) if s else {})
labels = Metadata.of_list("labels", list[str], lambda s: s.split(";") if s else [])
topics = Metadata.of_list("topics", list[str], lambda s: s.split(";") if s else [])

all_metadatas = [
    id,
    name,
    isFork,
    commits,
    branches,
    releases,
    forks,
    mainLanguage,
    defaultBranch,
    license,
    homepage,
    watchers,
    stargazers,
    contributors,
    size,
    createdAt,
    pushedAt,
    updatedAt,
    totalIssues,
    openIssues,
    totalPullRequests,
    openPullRequests,
    blankLines,
    codeLines,
    commentLines,
    metrics,
    lastCommit,
    lastCommitSHA,
    hasWiki,
    isArchived,
    isDisabled,
    isLocked,
    languages,
    labels,
    topics
]
