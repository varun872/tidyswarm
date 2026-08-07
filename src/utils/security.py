"""AST Code Security Engine for Scrub Swarm."""

import ast
from src.config import ALLOWED_MODULES, FORBIDDEN_BUILTINS


class CodeSecurityError(Exception):
    """Raised when generated code violates AST security policies."""

    pass


class ASTSecurityValidator(ast.NodeVisitor):
    """Walks Python AST to catch unauthorized imports and system calls."""

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            base_module = alias.name.split(".")[0]
            if base_module not in ALLOWED_MODULES:
                raise CodeSecurityError(
                    f"Security Error: Unauthorized import '{alias.name}'. "
                    f"Only {ALLOWED_MODULES} are permitted."
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            base_module = node.module.split(".")[0]
            if base_module not in ALLOWED_MODULES:
                raise CodeSecurityError(
                    f"Security Error: Unauthorized import from '{node.module}'. "
                    f"Only {ALLOWED_MODULES} are permitted."
                )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Direct calls to forbidden builtins (e.g., open(), eval())
        if isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_BUILTINS:
                raise CodeSecurityError(
                    f"Security Error: Call to forbidden builtin '{node.func.id}()' is prohibited."
                )

        # Attribute calls on forbidden system modules (e.g., os.system())
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id in {
                "os",
                "sys",
                "subprocess",
                "shutil",
            }:
                raise CodeSecurityError(
                    f"Security Error: Call to system library '{node.func.value.id}.{node.func.attr}()' is prohibited."
                )

        self.generic_visit(node)


def validate_code_security(code_str: str) -> None:
    """Parses code into AST and runs security validation checks."""
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        raise CodeSecurityError(f"SyntaxError in code block: {e}")

    validator = ASTSecurityValidator()
    validator.visit(tree)