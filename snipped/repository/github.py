from ..snippet import parse_snippet
from .base import Repository
import requests
import json
import base64


class GithubApiException(BaseException):
    @property
    def response(self):
        return self._response

    def __init__(self, response, message):
        super(GithubApiException, self).__init__(message)
        self._response = response


class RateLimitReached(GithubApiException):
    def __init__(self, response, message):
        super(GithubApiException, self).__init__(response, message)


class GithubApi:
    @staticmethod
    def check_response(response):
        status_code = response.status_code
        headers = response.headers

        if (status_code == requests.codes.forbidden
                and headers is not None and "X-RateLimit-Remaining" in headers
                and int(response.headers.get("X-RateLimit-Remaining")) == 0):
            raise RateLimitReached(response, response.text)
        elif response.status_code != requests.codes.ok:
            raise GithubApiException(response,
                                     "Response code is {}".format(response.status_code))
        return response

    @staticmethod
    def repository_tree(owner, repository, tree_hash, recursive):
        url = "https://api.github.com/repos/{}/{}/git/trees/{}?recursive={}".format(
            owner, repository, tree_hash, recursive)
        return GithubApi.check_response(requests.get(url))

    @staticmethod
    def repository_content(owner, repository, path):
        url = "https://api.github.com/repos/{}/{}/contents/{}".format(
            owner, repository, path)
        return GithubApi.check_response(requests.get(url))


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
