from .base import Repository
import requests
import json
from pprint import pprint


class GithubApi:
    @staticmethod
    def repository_tree(owner, repository, tree_hash, recursive):
        url = "https://api.github.com/repos/{}/{}/git/trees/{}?recursive={}".format(owner, repository, tree_hash, recursive)
        return requests.get(url)


class GithubRepository(Repository):
    def create_snippet(self, snippet_id):
        raise NotImplementedError()

    def __init__(self):
        pass

    def get_snippet(self, snippet_id):
        raise NotImplementedError()

    def list(self):
        self._recursive_path_explorer("dexpota", ".snippets", "HEAD", "0")

    def _recursive_path_explorer(self, owner, repository, tree_hash, recursive):
        response = GithubApi.repository_tree(owner, repository, tree_hash, recursive)

        tree_response = json.loads(response.content.decode(response.encoding))

        current_tree = tree_response["tree"]
        current_tree_truncated = tree_response["truncated"]

        for child in current_tree:
            child_type = child["type"]
            if child_type == "tree" and current_tree_truncated:
                self._recursive_path_explorer(owner, repository, child["sha"], "0")
            elif child_type == "blob":
                pprint(child["path"])
