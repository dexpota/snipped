from ..snippet import parse_snippet
from .base import Repository
import requests
import json
import base64


class GithubApi:
    @staticmethod
    def repository_tree(owner, repository, tree_hash, recursive):
        url = "https://api.github.com/repos/{}/{}/git/trees/{}?recursive={}".format(
            owner, repository, tree_hash, recursive)
        return requests.get(url)

    @staticmethod
    def repository_content(owner, repository, path):
        url = "https://api.github.com/repos/{}/{}/contents/{}".format(
            owner, repository, path)
        return requests.get(url)


class GithubNode:
    @property
    def path(self):
        return self._path

    def __init__(self, sha, path):
        self._sha = sha
        self._path = path


class GithubTree:
    def __init__(self):
        self._children = []

    def add_node(self, node):
        self._children.append(node)


class GithubRepository(Repository):
    @property
    def owner(self):
        return self._owner

    @property
    def repository(self):
        return self._repository

    @property
    def refs(self):
        return self._refs

    def __init__(self, owner, repository, refs="HEAD"):
        self._owner = owner
        self._repository = repository
        self._refs = refs
        self._root = GithubTree()

    def create_snippet(self, snippet_id):
        raise NotImplementedError()

    def get_snippet(self, snippet_id):
        if not self._root:
            raise NotImplementedError()
        else:
            for child in self._root._children:
                if child.path == snippet_id:
                    response = GithubApi.repository_content(
                        self.owner, self.repository, child.path)
                    content_response = json.loads(
                        response.content.decode(response.encoding))
                    content = base64.b64decode(
                        content_response["content"]).decode("utf-8")
                    return parse_snippet(content)

    def list(self):
        self._root = GithubTree()
        return self._recursive_path_explorer(self._root, self.owner, self.repository, self.refs, "1")

    def _recursive_path_explorer(self, root, owner, repository, tree_hash, recursive):
        response = GithubApi.repository_tree(
            owner, repository, tree_hash, recursive)

        tree_response = json.loads(response.content.decode(response.encoding))

        current_tree = tree_response["tree"]
        current_tree_truncated = tree_response["truncated"]

        for child in current_tree:
            child_type = child["type"]
            if child_type == "tree" and current_tree_truncated:
                subtree = GithubTree(child["sha"], child["path"])
                root.add_node(subtree)
                self._recursive_path_explorer(
                    subtree, owner, repository, child["sha"], "1")
            elif child_type == "blob":
                root.add_node(GithubNode(child["sha"], child["path"]))
                yield child["path"]
