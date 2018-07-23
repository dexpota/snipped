from .base import Repository
from ..configuration import get_snippets_home_path
from ..snippet import parse_snippet
import logging
import os


class LocalRepository(Repository):
    def create_snippet(self, snippet_id):
        raise NotImplementedError()

    def __init__(self):
        self._root = get_snippets_home_path()
        logging.debug("root directory: {}".format(self._root))

    def get_snippet_local_path(self, snippet_id):
        local_path = snippet_id
        path = os.path.join(self._root, local_path)
        return path

    def get_snippet(self, snippet_id):
        local_path = snippet_id
        path = os.path.join(self._root, local_path)

        if os.path.isfile(path):
            with open(path, "r") as fp:
                file_content = fp.read()

            return parse_snippet(file_content)
        else:
            logging.error("snippet doesn't exist: {}".format(path))

    def list(self):
        for root, dirs, files in os.walk(self._root):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            files[:] = [file for file in files if not file.startswith(".")]

            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, self._root)
                yield relative_path
