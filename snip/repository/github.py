from .base import Repository


class GithubRepository(Repository):
    def __init__(self):
        raise NotImplementedError()

    def get_snippet(self, snippet_id):
        raise NotImplementedError()

    def list(self):
        raise NotImplementedError()
