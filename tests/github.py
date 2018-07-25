from snip.repository.github import GithubRepository


def test_github():
    repository = GithubRepository("dexpota", ".snippets")

    for snippet_id in repository.list():
        print(snippet_id)

    repository.get_snippet("java/javadoc-method")
