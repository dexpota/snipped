import yaml
import re


def parse_snippet(file_content):
    splitter = re.compile(r'^-{3,}$', re.MULTILINE)
    _, metadata_content, snippet_content = splitter.split(file_content, 2)
    metadata = yaml.load(metadata_content)
    return Snippet(metadata, snippet_content)


class Snippet:
    @property
    def metadata(self):
        return self._metadata

    @property
    def snippet(self):
        return self._snippet

    def __init__(self, metadata, snippet):
        self._metadata = metadata
        self._snippet = snippet
