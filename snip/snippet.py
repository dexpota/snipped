import os
import yaml
import re
import logging


def parse_snippet(path):
    if os.path.isfile(path):
        with open(path, "r") as fp:
            file_content = fp.read()
            file_content = file_content.strip()

            splitter = re.compile(r'^-{3,}$', re.MULTILINE)
            _, metadata_content, snippet_content = splitter.split(file_content, 2)

        metadata = yaml.load(metadata_content)
        return metadata, snippet_content
    else:
        logging.error("snippet doesn't exist: {}".format(path))


class Snippet:
    def __init__(self, header, content):
        pass