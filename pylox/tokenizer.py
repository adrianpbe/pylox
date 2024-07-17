import re
from dataclasses import dataclass
from enum import Enum
from typing import  Any, Generator, List


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"
    STAR = "STAR"

    # One or two character tokens.
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"

    # Literals.
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    
    # Keywords
    AND = "AND"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FUN = "FUN"
    FOR = "FOR"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"

    EOF = "EOF"


KEYWORD_ID = {
        "and": "AND",
        "else": "ELSE",
        "false": "FALSE",
        "fun": "FUN",
        "for": "FOR",
        "if": "IF",
        "nil": "NIL",
        "or": "OR",
        "print": "PRINT",
        "return": "RETURN",
        "true": "TRUE",
        "var": "VAR",
        "while": "WHILE",
    }


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int

    def to_str(self):
        return self.type.value + " " + self.lexeme + " " + str(self.literal)


def tokenize_gen(code: str) -> Generator:
    # Beware of the order of patterns, double patterns such as "!="" and ""=="
    #  should be placed before "!" and "=", otherwise they'll be mismatched
    token_specification = [
        ("LEFT_PAREN",  r"\("),
        ("RIGHT_PAREN",  r"\)"),
        ("LEFT_BRACE",  r"{"),
        ("RIGHT_BRACE",  r"}"),
        ("COMMA",  r","),
        ("DOT",  r"\."),
        ("MINUS",  r"-"),
        ("PLUS",  r"\+"),
        ("SEMICOLON",  r";"),
        ("STAR",  r"\*"),
        # Before matching slash, an special skip pattern is used for comments, remember comments start with //
        ("COMMENT",  r"//.*?(\n|(?=\Z))"),
        ("SLASH",  r"/"),
        # double patterns with higher priority
        ("BANG_EQUAL",  r"!="),
        ("EQUAL_EQUAL",  r"=="),
        ("GREATER_EQUAL",  r">="),
        ("LESS_EQUAL",  r"<="),
        # lower priority
        ("BANG",  r"!"),
        ("EQUAL",  r"="),
        ("GREATER",  r">"),
        ("LESS",  r"<"),
        ("SKIP",     r'\s+'),       # Skip over spaces, tabs, uses special sequence \s that matches all kind of spaces
        ("NEWLINE",  r'\n'),           # Line endings (just for counting)
        ("NUMBER",   r'\d+(\.\d*)?'),  # Integer or decimal number
        ("STRING",   r"\".*?\""),  # String
        ("IDENTIFIER",       r'[A-Za-z_][A-Za-z0-9_]*'),   # Identifiers
        ("EOF", r"\Z"),
        ("mismatch", r'.'),            # Any other character
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    line_num = 1
    line_start = 0

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        literal = None
        # Literals (numbers, string or bool are saved with their Python type)
        # Skip is ignored, newline is ignored but used to keep track of position in text
        if kind == "NUMBER":
            literal = float(value) if '.' in value else int(value)
        elif kind == "STRING":
            literal = value.replace("\"", "")
        elif kind == "TRUE" or kind == "FALSE":
            literal = value == "true"
        elif kind == "IDENTIFIER":
            if value in KEYWORD_ID:
                kind = KEYWORD_ID[value]
                if kind == "TRUE" or kind == "FALSE":
                    literal = value == "true"
        elif kind == "SKIP" or kind == "COMMENT":
            continue

        elif kind == "NEWLINE":
            line_start = mo.end()
            line_num += 1
            continue

        elif kind == 'mismatch':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(
            TokenType(kind),
            value,
            literal,
            line_num
        )


def tokenize(code: str) -> List[Token]:
    return [t for t in tokenize_gen(code)]
