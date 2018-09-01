from snipped.repository.github import GithubRepository, RateLimitReached


def test_github():
    try:
        repository = GithubRepository("dexpota", ".snippets")
    except RateLimitReached as r:
        # When we reach the limit there is nothing we can do except tell the user and wait.
        return

    for snippet_id in repository.list():
        print(snippet_id)

    repository.get_snippet("java/javadoc-method")
