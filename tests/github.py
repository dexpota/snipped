from snip.repository.github import GithubRepository


def test_github():
    repository = GithubRepository()
    repository.list()
