import os.path
from textwrap import dedent

import pytest
from pytest import CaptureFixture

from pylox.interpreter import Interpreter
from pylox.lexer import Lexer
from pylox.nodes import (
    Assignment,
    Binary,
    Block,
    Expr,
    ExprStmt,
    Literal,
    Print,
    Program,
    VarDeclaration,
    Variable,
)
from pylox.parser import Parser
from pylox.tokens import Token, TokenType


@pytest.mark.parametrize(
    ("tree", "expected"),
    (
        (
            Binary(
                left=Literal(value=2.0),
                operator=Token(token_type=TokenType.PLUS, string="+", value=None),
                right=Binary(
                    left=Literal(value=3.0),
                    operator=Token(token_type=TokenType.STAR, string="*", value=None),
                    right=Literal(value=5.0),
                ),
            ),
            17.0,
        ),
        # TODO: add more tests
    ),
)
def test_interpreter_expr(tree: Expr, expected: object) -> None:
    output = Interpreter().visit(tree)
    assert output == expected


@pytest.mark.parametrize(
    ("tree", "output"),
    (
        (
            Program(
                body=[
                    VarDeclaration(
                        name=Token(TokenType.IDENTIFIER, "greeting"),
                        initializer=Literal("hello lox!"),
                    ),
                    Print(Variable(Token(TokenType.IDENTIFIER, "greeting"))),
                ]
            ),
            "hello lox!",
        ),
        (
            Program(
                body=[
                    VarDeclaration(
                        name=Token(TokenType.IDENTIFIER, "a"),
                        initializer=Literal("Something"),
                    ),
                    VarDeclaration(
                        name=Token(TokenType.IDENTIFIER, "b"),
                        initializer=Literal("Another thing"),
                    ),
                    ExprStmt(
                        Assignment(
                            name=Token(TokenType.IDENTIFIER, "a"),
                            value=Assignment(
                                name=Token(TokenType.IDENTIFIER, "b"),
                                value=Binary(
                                    left=Literal(2.0),
                                    operator=Token(TokenType.PLUS, "+"),
                                    right=Literal(3.0),
                                ),
                            ),
                        ),
                    ),
                    Print(Variable(Token(TokenType.IDENTIFIER, "a"))),
                    Print(Variable(Token(TokenType.IDENTIFIER, "b"))),
                ],
            ),
            "5.0\n5.0",
        ),
        (
            Program(
                body=[
                    VarDeclaration(
                        name=Token(TokenType.IDENTIFIER, "a"),
                        initializer=Literal(value="ga"),
                    ),
                    VarDeclaration(
                        name=Token(TokenType.IDENTIFIER, "b"),
                        initializer=Literal(value="gb"),
                    ),
                    VarDeclaration(
                        name=Token(TokenType.IDENTIFIER, "c"),
                        initializer=Literal(value="gc"),
                    ),
                    Block(
                        body=[
                            VarDeclaration(
                                name=Token(TokenType.IDENTIFIER, "a"),
                                initializer=Literal(value="ea"),
                            ),
                            VarDeclaration(
                                name=Token(TokenType.IDENTIFIER, "b"),
                                initializer=Literal(value="eb"),
                            ),
                            Block(
                                body=[
                                    VarDeclaration(
                                        name=Token(TokenType.IDENTIFIER, "a"),
                                        initializer=Literal(value="la"),
                                    ),
                                    Print(
                                        value=Variable(
                                            name=Token(TokenType.IDENTIFIER, "a")
                                        )
                                    ),
                                    Print(
                                        value=Variable(
                                            name=Token(TokenType.IDENTIFIER, "b")
                                        )
                                    ),
                                    Print(
                                        value=Variable(
                                            name=Token(TokenType.IDENTIFIER, "c")
                                        )
                                    ),
                                ]
                            ),
                            Print(
                                value=Variable(name=Token(TokenType.IDENTIFIER, "a"))
                            ),
                            Print(
                                value=Variable(name=Token(TokenType.IDENTIFIER, "b"))
                            ),
                            Print(
                                value=Variable(name=Token(TokenType.IDENTIFIER, "c"))
                            ),
                        ]
                    ),
                    Print(value=Variable(name=Token(TokenType.IDENTIFIER, "a"))),
                    Print(value=Variable(name=Token(TokenType.IDENTIFIER, "b"))),
                    Print(value=Variable(name=Token(TokenType.IDENTIFIER, "c"))),
                ]
            ),
            "la\neb\ngc\nea\neb\ngc\nga\ngb\ngc",
        )
        # TODO: add more tests
    ),
)
def test_interpreter(
    tree: Program,
    output: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    Interpreter().visit(tree)

    stdout, stderr = capsys.readouterr()
    assert stdout.rstrip() == output
    assert stderr == ""


# TODO: add failing tests


@pytest.mark.parametrize(
    ("filename", "output"),
    (
        (
            "control_flow.lox",
            """\
            Number is positive
            Number is small
            Should run
            """,
        ),
    ),
)
def test_interpreter_files(
    filename: str,
    output: str,
    capsys: CaptureFixture[str],
) -> None:
    test_dir = os.path.join(os.path.dirname(__file__), "testdata")
    filepath = os.path.join(test_dir, filename)
    with open(filepath) as file:
        source = file.read()

    tokens = Lexer(source).tokens
    parser = Parser(tokens)
    program, errors = parser.parse()
    assert not errors
    Interpreter().visit(program)

    stdout, stderr = capsys.readouterr()
    assert stdout.rstrip() == dedent(output).rstrip()
    assert stderr == ""
