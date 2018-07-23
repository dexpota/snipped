"""snip.

Usage: 
    snip <snippet>
    snip --info <snippet>
    snip --edit <snippet>
    snip --list
    snip --version|-v

"""
from .commands import edit_snippet, snippet_info, show_snippet, list_snippets
from .configuration import get_snippets_home_path
from docopt import docopt
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)

    arguments = docopt(__doc__)
    logging.debug("arguments: {}".format(arguments))

    snippets_home_path = get_snippets_home_path()
    logging.debug("root directory: {}".format(snippets_home_path))

    if arguments["--list"]:
        # list all snippets
        list_snippets(snippets_home_path)
    elif arguments["--info"]:
        # prints some info about the selected snippet
        snippet = arguments["<snippet>"]
        snippet_info(snippets_home_path, snippet)
    elif arguments["--edit"]:
        snippet = arguments["<snippet>"]
        edit_snippet(snippet)
    else:
        # show the snippet
        snippet = arguments["<snippet>"]
        show_snippet(snippets_home_path, snippet)


if __name__ == "__main__":
    main()
