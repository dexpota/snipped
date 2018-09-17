"""snip.

Usage:
    snip <snippet>
    snip --info <snippet>
    snip --edit <snippet>
    snip --list
    snip --version|-v

Options:
    -v, --version  Show snipped version.

"""
from .commands import edit_snippet, snippet_info, show_snippet, list_snippets
from .repository.local import LocalRepository
from . import __version__
from docopt import docopt
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)

    arguments = docopt(__doc__)
    logging.debug("arguments: {}".format(arguments))

    repository = LocalRepository()

    if arguments["--version"]:
        # print program version
        print("Snipped version {}.".format(__version__))
    elif arguments["--list"]:
        # list all snippets
        list_snippets(repository)
    elif arguments["--info"]:
        # prints some info about the selected snippet
        snippet = arguments["<snippet>"]
        snippet_info(repository, snippet)
    elif arguments["--edit"]:
        snippet = arguments["<snippet>"]
        edit_snippet(repository, snippet)
    else:
        # show the snippet
        snippet = arguments["<snippet>"]
        show_snippet(repository, snippet)


if __name__ == "__main__":
    main()
