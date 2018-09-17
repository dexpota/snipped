"""snip.

Usage:
    snip [options] <snippet>
    snip --info [options] <snippet>
    snip --edit [options] <snippet>
    snip --list [options]
    snip --version

Options:
    --version  Show snipped version.
    -d --debug  Enable debugging mode.

"""
from .commands import edit_snippet, snippet_info, show_snippet, list_snippets
from .repository.local import LocalRepository
from . import __version__
from docopt import docopt
import logging


def main():
    arguments = docopt(__doc__)

    if arguments["--debug"]:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.WARNING

    logging.basicConfig(level=logging_level)

    repository = LocalRepository()

    logging.debug("arguments: {}".format(arguments))

    if arguments["--version"]:
        # print program version
        print("Snipped version {}.".format(__version__))
    elif arguments["--list"]:
        logging.debug("Listing")
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
