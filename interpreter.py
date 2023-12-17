from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


def tokenize(code):
    keywords = [
        'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const',
        'continue', 'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern',
        'false', 'finally', 'fixed', 'float', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'int', 'interface',
        'internal', 'is', 'lock', 'long', 'namespace', 'new', 'null', 'object', 'operator', 'out', 'override', 'params',
        'private', 'protected', 'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short', 'sizeof',
        'stackalloc', 'static', 'string', 'struct', 'switch', 'this', 'throw', 'true', 'try', 'typeof', 'uint', 'ulong',
        'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void', 'volatile', 'while', 'add', 'and', 'alias',
        'ascending', 'args', 'async', 'await', 'by', 'descending', 'dynamic', 'equals', 'file', 'from', 'get', 'global',
        'group', 'init', 'into', 'join', 'let', 'managed', 'nameof', 'nint',
        'not', 'notnull', 'nuint', 'on', 'or', 'orderby', 'partial', 'record', 'remove',
        'required', 'scoped', 'select', 'set',
        'unmanaged', 'value', 'var', 'when',
        'where', 'with', 'yield'
    ]
    token_specification = [
        ('COMMENT_SINGLE', r'\//'),  # Single-line comment '//'
        ('COMMENT_MULTI', r'(/\*.*?\*/)'),  # Multi-line comment '/*...*/'
        ('NUMBER', r'\b\d+(\.\d*)?\b'),  # Integer or decimal number
        ('ASSIGN', r'='),  # Assignment operator
        ('END', r';'),  # Statement terminator
        ('ID', r'[A-Za-z_]\w*'),  # Identifiers
        ('OP', r'[+\-*/%=&|!<>^~?]+'),  # Operators in C#
        ('LPAREN', r'\('),  # Left parenthesis '('
        ('RPAREN', r'\)'),  # Right parenthesis ')'
        ('LBRACK', r'\{'),  # Left brace '{'
        ('RBRACK', r'\}'),  # Right brace '}'
        ('COLON', r':'),  # Colon ':'
        ('QUOTES', r'"'),  # Double quotes '"'
        ('PERIOD', r'\.'),  # Period '.'
        ('DOLLAR_STRING', r'\$[\'"](.*?)(?<!\\)[\'"]'),
        ('LSQBRACK', r'\['),
        ('RSQBRACK', r'\]'),
        # Matches $'...' or $"...". This assumes nested quotes are not supported.
        ('NEWLINE', r'\n'),  # Line endings
        ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
        ('MISMATCH', r'.'),  # Any other character
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    valid = True
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'COMMENT_SINGLE' or kind == 'COMMENT_MULTI':
            valid = False
            continue
        if kind == 'NEWLINE':
            valid = True
            continue
        if valid:
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'ID' and value.lower() in keywords:
                kind = value.upper()
            elif kind == 'END':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                print(f'Unexpected character {value!r} on line {line_num}, column {column}')
                continue
            yield Token(kind, value, line_num, column)


