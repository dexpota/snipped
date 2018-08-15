from .utilities import highlight, open_with_editor
from .configuration import get_snippets_editor
import logging
import tempfile
import yaml
import os


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


def edit_snippet(repository, snippet_id):
    # edit the snippet
    logging.debug("snippet: {}".format(snippet_id))
    editor = get_snippets_editor()

    snippet = repository.get_snippet(snippet_id)
    snippet_path = repository.get_snippet_local_path(snippet_id)

    # copy snippet to temporary file, without the header
    os_descriptor, path = tempfile.mkstemp()
    with os.fdopen(os_descriptor, "w") as fh:
        fh.write(snippet.snippet)

    if not editor:
        logging.error("editor not available.")
    else:
        open_with_editor(editor, path)

    with open(path, "r") as fh:
        new_snippet = fh.read()

    with open(snippet_path, "w") as fh:
        fh.write("---\n")
        fh.write(yaml.dump(snippet.metadata, default_flow_style=False))
        fh.write("---\n")
        fh.write(new_snippet)
