import pygments
import subprocess
import logging
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter


def highlight(language, code):
    lexer = get_lexer_by_name(language)
    return pygments.highlight(code, lexer, TerminalFormatter())


def open_with_editor(editor, filepath):
    try:
        subprocess.call([editor, filepath])
    except OSError:
        logging.error('Could not launch ' + editor)
