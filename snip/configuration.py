import os
import logging


def get_snippets_home_path():
    snippets_home_path = os.environ.get("SNIPPETS_DIR", "~/.snippets")
    snippets_home_path = os.path.expanduser(
        os.path.expandvars(snippets_home_path))

    if not os.path.isdir(snippets_home_path):
        logging.warning("Snippets home directory doesn't exist!")
        os.mkdir(snippets_home_path)
    else:
        write_permission = os.access(snippets_home_path, os.W_OK)
        read_permission = os.access(snippets_home_path, os.R_OK)

        if not write_permission or not read_permission:
            logging.error("Doesn't seems you have the rights to access this directory, "
                          "something wrong with permissions?")

    return snippets_home_path


def get_snippets_editor():
    return os.environ.get("SNIPPET_EDITOR") or os.environ.get("VISUAL") or os.environ.get("EDITOR")
