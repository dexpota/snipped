from .snippet import parse_snippet
import logging
import os
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter


def list_snippets(snippets_home_path):
    if not os.path.isdir(snippets_home_path):
        logging.error("snippet directory doesn't exist: {}".format(snippets_home_path))
        exit(-1)

    for root, dirs, files in os.walk(snippets_home_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        files[:] = [file for file in files if not file.startswith(".")]

        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, snippets_home_path)
            print(relative_path)


def show_snippet(snippets_home_path, snippet):
    # show the snippet
    logging.debug("snippet: {}".format(snippet))

    full_path = os.path.join(snippets_home_path, snippet)
    logging.debug("snippet full path: {}".format(full_path))

    yaml_header, content = parse_snippet(full_path)
    language = yaml_header["language"]

    lexer = get_lexer_by_name(language)
    print(highlight(content, lexer, TerminalFormatter()))


def snippet_info(snippets_home_path, snippet):
    full_path = os.path.join(snippets_home_path, snippet)
    logging.debug("snippet full path: {}".format(full_path))

    yaml_header, _ = parse_snippet(full_path)
    print(yaml_header)


def edit_snippet(snippet):
    # edit the snippet
    logging.debug("snippet: {}".format(snippet))
    raise NotImplementedError("edit functionality is not yet implemented.")
