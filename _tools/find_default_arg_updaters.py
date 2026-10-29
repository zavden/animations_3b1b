"""Lists scenes in _work/ that pass add_updater a function whose second parameter
has a default value and is not called "dt" (e.g. `lambda m, i=i: ...`).
With manimgl's updater rule after Jul 2026 those functions receive dt
in that parameter; _lib restores the old rule, so their previous renders may
be wrong and it is worth re-rendering them.

Usage: python find_default_arg_updaters.py [folder inside _work]"""
import ast
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[1] / "_work"


def second_param_has_default(args: ast.arguments) -> bool:
    positional = args.posonlyargs + args.args
    if len(positional) < 2 or positional[1].arg == "dt":
        return False
    n_without_default = len(positional) - len(args.defaults)
    return 1 >= n_without_default


def scan(path: Path) -> bool:
    tree = ast.parse(path.read_text())
    funcs = {
        n.name: n for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr not in ("add_updater", "insert_updater") or not node.args:
            continue
        arg = node.args[0]
        if isinstance(arg, ast.Lambda) and second_param_has_default(arg.args):
            return True
        if isinstance(arg, ast.Name) and arg.id in funcs:
            fn = funcs[arg.id]
            if second_param_has_default(fn.args):
                return True
    return False


def main():
    root = WORK / sys.argv[1] if len(sys.argv) > 1 else WORK
    for path in sorted(root.rglob("*.py")):
        if path.name.endswith(".orig.py"):
            continue
        try:
            if scan(path):
                print(path.parent.relative_to(WORK), path.stem)
        except SyntaxError:
            pass


if __name__ == "__main__":
    main()
