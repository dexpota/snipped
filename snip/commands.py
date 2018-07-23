from .utilities import highlight
import logging

def list_snippets(repository):
    # list all snippets
    for snippet in repository.list():
        print(snippet)


def show_snippet(repository, snippet):
    # show the snippet
    snippet = repository.get_snippet(snippet)
    language = snippet.metadata["language"]

    print(highlight(language, snippet.snippet))


def snippet_info(repository, snippet):
    snippet = repository.get_snippet(snippet)
    print(snippet.metadata)


def edit_snippet(snippet):
    # edit the snippet
    logging.debug("snippet: {}".format(snippet))
    raise NotImplementedError("edit functionality is not yet implemented.")
