import yaml
import re


class Snippet:
    @property
    def metadata(self):
        return self._metadata

    @property
    def snippet(self):
        return self._snippet

    def __init__(self, metadata: str, snippet: str):
        self._metadata = metadata
        self._snippet = snippet


def parse_snippet(file_content: str) -> Snippet:
    splitter = re.compile(r'^-{3}[\s\S]', re.MULTILINE)
    _, metadata_content, snippet_content = splitter.split(file_content, 2)
    metadata = yaml.load(metadata_content)
    return Snippet(metadata, snippet_content)
