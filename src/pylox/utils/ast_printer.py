from pylox.expr import Binary, Grouping, Literal, Unary
from pylox.lexer import Lexer
from pylox.parser import Parser
from pylox.utils.visitor import Visitor


class AstPrinter(Visitor):
    def visit_Literal(self, literal: Literal) -> str:
        if literal.value is None:
            return "nil"

        if isinstance(literal.value, bool):
            return f"{literal.value}".lower()

        return f"{literal.value}"

    def visit_Unary(self, unary: Unary) -> str:
        return f"({unary.operator.string} {self.visit(unary.right)})"

    def visit_Binary(self, binary: Binary) -> str:
        return (
            f"({self.visit(binary.left)} "
            f"{binary.operator.string} "
            f"{self.visit(binary.right)})"
        )

    def visit_Grouping(self, grouping: Grouping) -> str:
        return f"(group {self.visit(grouping.expression)})"


def main() -> None:
    tokens = Lexer("(8 / 2) + 3 * 5").tokens
    parser = Parser(tokens)
    tree = parser.parse()
    tree_str = AstPrinter().visit(tree)
    print(tree_str)


if __name__ == "__main__":
    main()