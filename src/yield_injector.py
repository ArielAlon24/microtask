from typing import List
import ast
import inspect
from micro_task import _Empty, Function, MicroTaskCreator


class YieldInjector(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        node.body = self._inject(node.body)
        return node

    def _inject(self, body: List[ast.stmt]) -> List[ast.stmt]:
        new_body = []
        for stmt in body:
            if isinstance(stmt, ast.Return):
                if len(new_body) == 0:
                    new_body.append(ast.Expr(ast.Yield(value=stmt.value)))
                else:
                    new_body[-1] = ast.Expr(ast.Yield(value=stmt.value))
                continue

            for attribute in ("body", "orelse"):
                if hasattr(stmt, attribute):
                    setattr(stmt, attribute, self._inject(getattr(stmt, attribute)))

            if hasattr(stmt, "handlers"):
                for handler in getattr(stmt, "handlers"):
                    handler.body = self._inject(handler.body)

            new_body.append(stmt)
            new_body.append(
                ast.Expr(ast.Yield(value=ast.Name(id=_Empty.__name__, ctx=ast.Load())))
            )
        return new_body


def inject(func: Function) -> MicroTaskCreator:
    # Stripping decorators for ast.parse to work
    func.__globals__[func.__name__] = func
    source_lines = inspect.getsource(func).splitlines()
    source_code = "\n".join(line for line in source_lines if not line.startswith("@"))

    tree = ast.parse(source_code)

    transformer = YieldInjector()
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)

    code = compile(transformed_tree, filename="<ast>", mode="exec")
    func_globals = func.__globals__.copy()

    func_globals[_Empty.__name__] = _Empty

    exec(code, func_globals)
    return func_globals[func.__name__]
