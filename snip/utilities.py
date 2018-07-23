import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter


def highlight(language, code):
    lexer = get_lexer_by_name(language)
    return pygments.highlight(code, lexer, TerminalFormatter())
