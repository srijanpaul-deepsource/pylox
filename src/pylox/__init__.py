"""pylox - A Lox interpreter written in Python."""
from __future__ import annotations

import os.path
import sys

from pylox.lexer import Lexer, LexError
from pylox.parser import Parser


def read_file(filename: str) -> str:
    with open(filename) as file:
        source = file.read()

    return source


def get_snippet_line_col(source: str, index: int) -> tuple[int, int, str]:
    """Returns line number, column number and line of code at the given index."""
    line, col = 1, 0

    current = 0
    snippet_start_index = 0
    for char in source:
        if current == index:
            break

        if char == "\n":
            snippet_start_index = current + 1
            line += 1
            col = 0

        col += 1
        current += 1

    while current < len(source) and source[current] != "\n":
        current += 1

    snippet_end_index = current
    snippet = source[snippet_start_index:snippet_end_index]
    return line, col, snippet


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv

    if len(argv) > 2:
        print("Usage: pylox [filename]")
        raise SystemExit(1)

    if len(argv) == 1:
        raise SystemExit(run_interactive())

    filepath = argv[1]
    raise SystemExit(run(filepath))


def run_interactive() -> int:
    while True:
        try:
            text = input("> ")
        except KeyboardInterrupt:
            return 1

        run(text)


def run(filepath: str) -> int:
    source = read_file(filepath)

    try:
        tokens = Lexer(source).tokens
    except LexError as exc:
        filename = os.path.basename(filepath)
        line, col, snippet = get_snippet_line_col(source, exc.index)
        print(f"Error in {filename}:{line}:{col}")

        indent = "    "
        print()
        print(indent + snippet)
        print(indent + "^".rjust(col))
        print(f"Syntax Error: {exc.message}")
        return 1

    parser = Parser(tokens)
    tree = parser.parse()
    print(tree)
    # TODO: parse
    # TODO: run code

    return 0
