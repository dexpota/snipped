from .utilities import highlight, open_with_editor
from .configuration import get_snippets_editor
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


def edit_snippet(repository, snippet):
    # edit the snippet
    logging.debug("snippet: {}".format(snippet))
    editor = get_snippets_editor()

    path = repository.get_snippet_local_path(snippet)

    if not editor:
        logging.error("editor not available.")
    else:
        open_with_editor(editor, path)
