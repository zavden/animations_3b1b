"""Extracts scenes from a file of the 3b1b/videos repo as standalone files.

Each generated file contains only what its scene needs: the used imports,
and the classes/functions/constants it depends on (transitively),
including those that come from other modules of the repo (`from _2026.x.y import *`),
which are copied inline instead of imported.

Usage:
    python extract.py list <source.py>              # scenes and flags, in JSON
    python extract.py one <source.py> <Scene> <output.py>"""
from __future__ import annotations

import ast
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Clone of 3b1b/videos (by default, next to the converted/ folder)
VIDEOS_ROOT = Path(os.environ.get(
    "THREEB1B_VIDEOS", Path(__file__).resolve().parents[2] / "videos"
)).resolve()
# Packages that live in converted/_lib and are therefore left as a normal import
LIB_PACKAGES = {"custom", "once_useful_constructs", "manim_imports_ext", "manimlib"}
INTERACTIVE_METHODS = {
    "on_mouse_motion", "on_mouse_drag", "on_mouse_press", "on_mouse_release",
    "on_mouse_scroll", "on_key_press", "on_key_release", "on_resize",
}


# ---------------------------------------------------------------- references

class RefCollector(ast.NodeVisitor):
    """Free names that a node reads, with approximate handling of local scopes."""

    def __init__(self):
        self.refs: set[str] = set()
        # (names, is_class): the names of a class body are only seen directly in that body, not in
        # its methods (a method get_x can call the global function get_x)
        self.scopes: list[tuple[set[str], bool]] = []

    def is_local(self, name):
        last = len(self.scopes) - 1
        return any(
            name in names and (not is_class or i == last)
            for i, (names, is_class) in enumerate(self.scopes)
        )

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and not self.is_local(node.id):
            self.refs.add(node.id)

    def visit_Attribute(self, node):
        self.visit(node.value)

    def _function(self, node, args, body):
        if hasattr(node, "decorator_list"):
            for d in node.decorator_list:
                self.visit(d)
        for default in args.defaults + [d for d in args.kw_defaults if d is not None]:
            self.visit(default)
        if getattr(node, "returns", None) is not None:
            self.visit(node.returns)
        all_args = args.posonlyargs + args.args + args.kwonlyargs
        for a in all_args + [args.vararg, args.kwarg]:
            if a is not None and a.annotation is not None:
                self.visit(a.annotation)
        local = {a.arg for a in all_args}
        local |= {a.arg for a in (args.vararg, args.kwarg) if a is not None}
        body_nodes = body if isinstance(body, list) else [body]
        for b in body_nodes:
            local |= assigned_names(b, skip_globals=True)
        self.scopes.append((local, False))
        for b in body_nodes:
            self.visit(b)
        self.scopes.pop()

    def visit_FunctionDef(self, node):
        self._function(node, node.args, node.body)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Lambda(self, node):
        self._function(node, node.args, node.body)

    def visit_ClassDef(self, node):
        for d in node.decorator_list:
            self.visit(d)
        for b in node.bases:
            self.visit(b)
        for k in node.keywords:
            self.visit(k.value)
        # The names of the class body are not visible in its methods, but they are within the body
        # itself
        local = set()
        for b in node.body:
            local |= assigned_names(b)
        self.scopes.append((local, True))
        for b in node.body:
            self.visit(b)
        self.scopes.pop()

    def _comprehension(self, node, elts):
        local = set()
        for gen in node.generators:
            local |= target_names(gen.target)
        # The first iterable is evaluated in the outer scope
        self.visit(node.generators[0].iter)
        self.scopes.append((local, False))
        for i, gen in enumerate(node.generators):
            if i > 0:
                self.visit(gen.iter)
            for cond in gen.ifs:
                self.visit(cond)
        for e in elts:
            self.visit(e)
        self.scopes.pop()

    def visit_ListComp(self, node):
        self._comprehension(node, [node.elt])

    visit_SetComp = visit_ListComp
    visit_GeneratorExp = visit_ListComp

    def visit_DictComp(self, node):
        self._comprehension(node, [node.key, node.value])


def target_names(target) -> set[str]:
    return {n.id for n in ast.walk(target) if isinstance(n, ast.Name)}


def assigned_names(node, skip_globals=False) -> set[str]:
    """Names that a statement assigns in its scope (without entering nested defs)."""
    names = set()
    stack = [node]
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(n.name)
            continue
        if isinstance(n, ast.Lambda):
            continue
        if isinstance(n, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            continue
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            names.add(n.id)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for alias in n.names:
                if alias.name != "*":
                    names.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(n, ast.ExceptHandler) and n.name:
            names.add(n.name)
        elif isinstance(n, (ast.Global, ast.Nonlocal)) and skip_globals:
            continue
        stack.extend(ast.iter_child_nodes(n))
    if skip_globals:
        for n in ast.walk(node):
            if isinstance(n, ast.Global):
                names -= set(n.names)
    return names


def references(node) -> set[str]:
    rc = RefCollector()
    rc.visit(node)
    return rc.refs


# ---------------------------------------------------------------- units

@dataclass
class Unit:
    module: Path          # source file
    node: ast.stmt
    text: str
    defines: set[str]
    refs: set[str]
    kind: str             # "future", "import", "def", "effect"
    order: int = 0
    lines: tuple = (0, 0)


@dataclass
class ModuleIndex:
    units: list[Unit] = field(default_factory=list)
    modules_seen: set[Path] = field(default_factory=set)
    unresolved: list[str] = field(default_factory=list)
    redirects: list[str] = field(default_factory=list)


def resolve_local_module(name: str, level: int, current: Path, index: ModuleIndex) -> Path | None:
    """Returns the .py file of a repo module, or None if it is external."""
    if level > 0:
        base = current.parent
        for _ in range(level - 1):
            base = base.parent
        candidate = base.joinpath(*name.split(".")) if name else base
        if candidate.with_suffix(".py").exists():
            return candidate.with_suffix(".py")
        if (candidate / "__init__.py").exists():
            return candidate / "__init__.py"
        index.unresolved.append(f"{'.' * level}{name}")
        return None
    top = name.split(".")[0]
    if not (top.startswith("_20") or top.startswith("_19")):
        return None
    candidate = VIDEOS_ROOT.joinpath(*name.split(".")).with_suffix(".py")
    if candidate.exists():
        return candidate
    # Files that Grant moved to another year (e.g. _2025/hairy_ball -> _2026/hairy_ball)
    rest = Path(*name.split(".")[1:]).with_suffix(".py")
    matches = sorted(VIDEOS_ROOT.glob(f"_20*/{rest}"))
    if matches:
        index.redirects.append(f"{name} -> {matches[-1].relative_to(VIDEOS_ROOT)}")
        return matches[-1]
    # Folders renamed within the same year (e.g. _2025/blocks_and_grover -> _2025/grover)
    year_dir = VIDEOS_ROOT / top
    matches = sorted(year_dir.rglob(rest.name)) if year_dir.is_dir() else []
    if len(matches) == 1:
        index.redirects.append(f"{name} -> {matches[0].relative_to(VIDEOS_ROOT)}")
        return matches[0]
    index.unresolved.append(name)
    return None


def unit_text(source_lines: list[str], node: ast.stmt) -> tuple[str, tuple]:
    start = node.lineno
    if getattr(node, "decorator_list", None):
        start = min(start, *(d.lineno for d in node.decorator_list))
    # Include comments stuck right above
    while start > 1 and source_lines[start - 2].lstrip().startswith("#"):
        start -= 1
    end = node.end_lineno
    return "".join(source_lines[start - 1:end]).rstrip() + "\n", (start, end)


def is_main_guard(node) -> bool:
    return (
        isinstance(node, ast.If)
        and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == "__name__"
    )


def index_module(path: Path, index: ModuleIndex):
    path = path.resolve()
    if path in index.modules_seen:
        return
    index.modules_seen.add(path)
    source = path.read_text(encoding="utf-8")
    source_lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    for node in tree.body:
        if is_main_guard(node):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue  # module docstring
        if isinstance(node, ast.ImportFrom):
            if node.module == "__future__":
                text, lines = unit_text(source_lines, node)
                index.units.append(Unit(path, node, text, set(), set(), "future", lines=lines))
                continue
            local = resolve_local_module(node.module or "", node.level, path, index)
            if local is not None:
                index_module(local, index)
                aliases = [a for a in node.names if a.name != "*" and a.asname and a.asname != a.name]
                for a in aliases:
                    text = f"{a.asname} = {a.name}\n"
                    index.units.append(Unit(path, node, text, {a.asname}, {a.name}, "def"))
                continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            text, lines = unit_text(source_lines, node)
            star = any(a.name == "*" for a in node.names)
            kind = "import"
            defines = set() if star else assigned_names(node)
            unit = Unit(path, node, text, defines, set(), kind, lines=lines)
            unit.always = star
            index.units.append(unit)
            continue
        text, lines = unit_text(source_lines, node)
        defines = assigned_names(node)
        refs = references(node)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defines = {node.name}
        kind = "def" if defines else "effect"
        index.units.append(Unit(path, node, text, defines, refs, kind, lines=lines))
    for i, u in enumerate(index.units):
        u.order = i


def build_index(source: Path) -> ModuleIndex:
    index = ModuleIndex()
    index_module(source, index)
    return index


def closure(index: ModuleIndex, seeds: set[str]) -> list[Unit]:
    by_name: dict[str, list[Unit]] = {}
    for u in index.units:
        for name in u.defines:
            by_name.setdefault(name, []).append(u)
    included: set[int] = set()
    work = list(seeds)
    for u in index.units:
        if u.kind == "future" or getattr(u, "always", False) or u.kind == "effect":
            included.add(id(u))
            work.extend(u.refs)
    seen = set()
    while work:
        name = work.pop()
        if name in seen:
            continue
        seen.add(name)
        for u in by_name.get(name, []):
            if id(u) not in included:
                included.add(id(u))
                work.extend(u.refs)
    return [u for u in index.units if id(u) in included]


def render_units(units: list[Unit], main_module: Path) -> str:
    future = [u for u in units if u.kind == "future"]
    imports = [u for u in units if u.kind == "import"]
    rest = [u for u in units if u.kind not in ("future", "import")]

    out = []
    seen_text = set()
    for u in future + imports:
        if u.text not in seen_text:
            seen_text.add(u.text)
            out.append(u.text)
    out.append("\n")
    current_module = None
    show_origin = len({u.module for u in rest}) > 1
    for u in rest:
        if u.module != current_module and show_origin:
            current_module = u.module
            rel = u.module.relative_to(VIDEOS_ROOT)
            out.append(f"\n# ----- Desde {rel} -----\n\n")
        out.append(u.text)
        out.append("\n\n")
    return "".join(out).rstrip() + "\n"


# ---------------------------------------------------------------- scenes

def manim_scene_bases() -> dict[str, bool]:
    """Names of Scene classes available via manim_imports_ext -> do they have their own construct?"""
    sys.argv = sys.argv[:1]
    import manim_imports_ext as mie
    from manimlib.scene.scene import Scene
    result = {}
    for name in dir(mie):
        obj = getattr(mie, name)
        if isinstance(obj, type) and issubclass(obj, Scene):
            result[name] = obj.construct is not Scene.construct
    return result


def base_name(expr) -> str | None:
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return expr.attr
    return None


def list_scenes(source: Path) -> dict:
    index = build_index(source)
    source = source.resolve()
    external = manim_scene_bases()
    classes: dict[str, ast.ClassDef] = {}
    for u in index.units:
        if isinstance(u.node, ast.ClassDef):
            classes[u.node.name] = u.node  # the last definition wins

    memo: dict[str, tuple[bool, bool]] = {}

    def info(name, depth=0) -> tuple[bool, bool]:
        """(is_scene, has_construct)"""
        if name in memo:
            return memo[name]
        if name not in classes:
            res = (name in external, external.get(name, False))
            memo[name] = res
            return res
        if depth > 50:
            return (False, False)
        node = classes[name]
        own_construct = any(
            isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef)) and b.name == "construct"
            for b in node.body
        )
        is_scene, has_construct = False, own_construct
        for b in node.bases:
            bn = base_name(b)
            if bn is None or bn == name:
                continue
            s, c = info(bn, depth + 1)
            is_scene |= s
            has_construct |= c
        memo[name] = (is_scene, has_construct)
        return memo[name]

    def class_methods(name, depth=0) -> set[str]:
        if name not in classes or depth > 50:
            return set()
        node = classes[name]
        methods = {b.name for b in node.body if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for b in node.bases:
            bn = base_name(b)
            if bn and bn != name:
                methods |= class_methods(bn, depth + 1)
        return methods

    scenes = []
    for u in index.units:
        node = u.node
        if u.module != source or not isinstance(node, ast.ClassDef):
            continue
        is_scene, has_construct = info(node.name)
        if not is_scene:
            continue
        flags = []
        if not has_construct:
            flags.append("sin_construct")
        methods = class_methods(node.name)
        if methods & INTERACTIVE_METHODS:
            flags.append("eventos_mouse_teclado")
        body_src = u.text
        for pattern, flag in [
            ("self.embed(", "embed"),
            ("wait_until", "wait_until"),
            ("while True", "while_true"),
            ("input(", "input"),
            ("tkinter", "tkinter"),
            ("checkpoint_paste", "checkpoint_paste"),
        ]:
            if pattern in body_src:
                flags.append(flag)
        scenes.append({
            "scene": node.name,
            "lines": list(u.lines),
            "flags": flags,
        })
    return {
        "source": str(source.relative_to(VIDEOS_ROOT)),
        "scenes": scenes,
        "unresolved_imports": index.unresolved,
        "redirected_imports": index.redirects,
    }


def extract_one(source: Path, scene: str, out: Path) -> dict:
    index = build_index(source)
    units = closure(index, {scene})
    code = render_units(units, source.resolve())
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(code, encoding="utf-8")
    inlined = sorted(
        {str(u.module.relative_to(VIDEOS_ROOT)) for u in units if u.kind in ("def", "effect")}
        - {str(source.resolve().relative_to(VIDEOS_ROOT))}
    )
    return {
        "lines_out": code.count("\n"),
        "inlined_modules": inlined,
        "unresolved_imports": index.unresolved,
        "redirected_imports": index.redirects,
    }


def main():
    cmd = sys.argv[1]
    if cmd == "list":
        print(json.dumps(list_scenes(Path(sys.argv[2])), indent=1))
    elif cmd == "one":
        print(json.dumps(extract_one(Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]))))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
