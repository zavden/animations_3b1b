"""Compatibility with the manim API of 2020 (early OpenGL era, before the x_range ranges).

Imported at the end of `manim_imports_ext.py` (with `from legacy_2020 import *`). All the patches
only add behavior where the current manimgl gave an error (kwargs it did not know, methods that
were missing), so they do not change the already rendered 2021-2026 scenes.

What is there:
- `Mobject.shift(*vectores)` (adds several vectors).
- `Axes`/`NumberPlane`/`ComplexPlane`/`ThreeDAxes` with `x_min, x_max, y_min, y_max`,
  `number_line_config`, and `tick_frequency` / `x_min` / `x_max` inside `*axis_config`;
  `NumberLine(x_min=, x_max=, tick_frequency=, ...)`; `x_min`, `x_max`, `y_min`,
  `y_max` properties of the coordinate systems; `get_graph(f, x_min=, x_max=, step_size=)`;
  `add_coordinates`; `NumberLine.tick_marks`; `NumberLine.add_numbers(*numeros, ...)`.
- `DecimalNumber(height=)`.
- `FadeInFrom`, `FadeOutAndShift`, `fix_percent` (no-op).
- `Brace.get_text/get_tex` return OldTexText/OldTex if the caller is from 2020 or earlier
  (`is_legacy_caller()`, reusable for other per-era patches).
- `get_color()` of a group without points; `Tex(1)` / `OldTex(1)` with non-str arguments.
- `Scene.update_frame(ignore_skipping=)`, `CameraFrame.euler_angles`, `ArrowTip(start_angle=)`."""
import inspect
import re
import sys
from collections.abc import Iterable

import numpy as np

from manimlib import *
from manimlib.animation.fading import FadeIn, FadeOut
from manimlib.camera.camera_frame import CameraFrame
from manimlib.mobject.coordinate_systems import Axes, CoordinateSystem
from manimlib.mobject.mobject import Mobject
from manimlib.mobject.number_line import NumberLine
from manimlib.mobject.numbers import DecimalNumber
from manimlib.scene.scene import Scene

__all__ = ["FadeInFrom", "FadeOutAndShift", "fix_percent", "is_legacy_caller"]


# ---------------------------------------------------------------- Mobject.shift(*vectores)
_original_shift = Mobject.shift


def _shift(self, *vectors):
    if len(vectors) != 1:
        vectors = (np.sum([np.asarray(v, dtype=float) for v in vectors], axis=0),)
    return _original_shift(self, vectors[0])


Mobject.shift = _shift


# ---------------------------------------------------------------- DecimalNumber(height=)
_original_decimal_init = DecimalNumber.__init__


def _decimal_number_init(self, *args, height=None, width=None, **kwargs):
    _original_decimal_init(self, *args, **kwargs)
    if height is not None:
        self.set_height(height)
    elif width is not None:
        self.set_width(width)


DecimalNumber.__init__ = _decimal_number_init


# ---------------------------------------------------------------- NumberLine
_original_number_line_init = NumberLine.__init__
_OLD_NUMBER_LINE_KEYS = (
    "x_min", "x_max", "tick_frequency", "leftmost_tick", "numbers_with_elongated_ticks",
    "label_direction", "line_to_number_vect", "numbers_to_show", "number_at_center",
    "numbers_with_elongated_ticks", "include_numbers_to_show", "exclude_zero_from_default_numbers",
)


def _clean_axis_kwargs(cfg):
    """Returns (kwargs without the old keys, (x_min, x_max, tick_frequency))."""
    cfg = dict(cfg)
    lo = cfg.pop("x_min", None)
    hi = cfg.pop("x_max", None)
    step = cfg.pop("tick_frequency", None)
    cfg.pop("leftmost_tick", None)
    cfg.pop("numbers_to_show", None)
    cfg.pop("number_at_center", None)
    cfg.pop("include_numbers_to_show", None)
    cfg.pop("exclude_zero_from_default_numbers", None)
    if "numbers_with_elongated_ticks" in cfg:
        cfg["big_tick_numbers"] = list(cfg.pop("numbers_with_elongated_ticks"))
    for old in ("label_direction", "line_to_number_vect"):
        if old in cfg:
            cfg["line_to_number_direction"] = cfg.pop(old)
    return cfg, (lo, hi, step)


def _merge_range(base, lo, hi, step):
    base = list(base) if base is not None else [-8, 8, 1]
    if len(base) == 2:
        base.append(1)
    if lo is not None:
        base[0] = lo
    if hi is not None:
        base[1] = hi
    if step is not None:
        base[2] = step
    return tuple(base)


def _number_line_init(self, *args, **kwargs):
    if any(key in kwargs for key in _OLD_NUMBER_LINE_KEYS):
        # numbers_to_show: in Cairo, add_numbers() with no arguments only placed these numbers (ValueSlider, sir)
        if kwargs.get("numbers_to_show") is not None:
            self._legacy_numbers_to_show = [float(x) for x in kwargs["numbers_to_show"]]
        kwargs, (lo, hi, step) = _clean_axis_kwargs(kwargs)
        if args:
            base, args = args[0], args[1:]
        else:
            base = kwargs.pop("x_range", None)
        kwargs["x_range"] = _merge_range(base, lo, hi, step)
    _original_number_line_init(self, *args, **kwargs)


NumberLine.__init__ = _number_line_init

NumberLine.tick_marks = property(lambda self: self.ticks)

_original_add_numbers = NumberLine.add_numbers


def _is_number(x):
    return isinstance(x, (int, float, np.integer, np.floating))


def _add_numbers(self, *args, **kwargs):
    # Old version: add_numbers(*numbers, **config). The current one: add_numbers(values, excluding)
    legacy_numbers = getattr(self, "_legacy_numbers_to_show", None)
    if legacy_numbers is not None and not args and "x_values" not in kwargs:
        args = (list(legacy_numbers),)
    if len(args) > 1 and all(_is_number(a) for a in args):
        args = (list(args),)
    elif len(args) == 1 and _is_number(args[0]):
        args = ([args[0]],)
    return _original_add_numbers(self, *args, **kwargs)


NumberLine.add_numbers = _add_numbers


# ---------------------------------------------------------------- Axes and coordinate systems
_original_axes_init = Axes.__init__
_axes_signature = inspect.signature(_original_axes_init).parameters


def _axes_init(self, *args, **kwargs):
    old = {"x_min", "x_max", "y_min", "y_max", "number_line_config", "z_min", "z_max"}
    cfg_keys = ("axis_config", "x_axis_config", "y_axis_config", "z_axis_config")
    needs = old.intersection(kwargs) or any(
        any(k in kwargs.get(c, {}) for k in _OLD_NUMBER_LINE_KEYS) for c in cfg_keys
    )
    if not needs:
        return _original_axes_init(self, *args, **kwargs)

    args = list(args)
    base = {}
    for i, name in enumerate(("x_range", "y_range")):
        if len(args) > i:
            base[name] = args[i]
        else:
            base[name] = kwargs.pop(name, _axes_signature[name].default)
    args = args[2:]

    axis_config = dict(kwargs.pop("number_line_config", {}))
    axis_config.update(kwargs.pop("axis_config", {}))
    axis_config, (_, _, common_step) = _clean_axis_kwargs(axis_config)
    ranges = {}
    for axis, name in (("x", "x_range"), ("y", "y_range")):
        cfg, (lo, hi, step) = _clean_axis_kwargs(kwargs.pop(f"{axis}_axis_config", {}))
        kwargs[f"{axis}_axis_config"] = cfg
        lo = kwargs.pop(f"{axis}_min", lo)
        hi = kwargs.pop(f"{axis}_max", hi)
        ranges[name] = _merge_range(base[name], lo, hi, step if step is not None else common_step)
    if "z_axis_config" in kwargs:
        kwargs["z_axis_config"], _ = _clean_axis_kwargs(kwargs["z_axis_config"])
    kwargs["axis_config"] = axis_config
    return _original_axes_init(self, ranges["x_range"], ranges["y_range"], *args, **kwargs)


Axes.__init__ = _axes_init


def _range_property(attr, index):
    def getter(self):
        return getattr(self, attr)[index]

    def setter(self, value):
        values = list(getattr(self, attr))
        values[index] = value
        setattr(self, attr, tuple(values))
    return property(getter, setter)


for _name, _attr, _index in [("x_min", "x_range", 0), ("x_max", "x_range", 1),
                             ("y_min", "y_range", 0), ("y_max", "y_range", 1)]:
    setattr(CoordinateSystem, _name, _range_property(_attr, _index))

_original_get_graph = CoordinateSystem.get_graph


def _get_graph(self, function, x_range=None, *args, x_min=None, x_max=None, step_size=None, **kwargs):
    if x_min is not None or x_max is not None or step_size is not None:
        base = x_range if x_range is not None else self.x_range
        step = None if step_size is None else step_size * self.num_sampled_graph_points_per_tick
        x_range = _merge_range(base, x_min, x_max, step)
    return _original_get_graph(self, function, x_range, *args, **kwargs)


CoordinateSystem.get_graph = _get_graph
CoordinateSystem.add_coordinates = lambda self, *args, **kwargs: self.add_coordinate_labels(*args, **kwargs)


# ---------------------------------------------------------------- Animations and scene
class FadeInFrom(FadeIn):
    """Cairo/GL 2020: the animation enters from the given direction."""
    def __init__(self, mobject, direction=DOWN, **kwargs):
        super().__init__(mobject, shift=-np.array(direction), **kwargs)


class FadeOutAndShift(FadeOut):
    """Cairo/GL 2020: the animation exits by shifting in the given direction."""
    def __init__(self, mobject, direction=DOWN, **kwargs):
        super().__init__(mobject, shift=np.array(direction), **kwargs)


def fix_percent(sym):
    # It used to recompose the "%" glyph (two curves in the same subpath); manimgl already draws it correctly
    return sym


_original_update_frame = Scene.update_frame


def _update_frame(self, dt=0, force_draw=False, ignore_skipping=None):
    return _original_update_frame(self, dt, force_draw)


Scene.update_frame = _update_frame

CameraFrame.euler_angles = property(lambda self: self.get_euler_angles())

_original_arrow_tip_init = ArrowTip.__init__


def _arrow_tip_init(self, *args, start_angle=None, **kwargs):
    if start_angle is not None:
        kwargs.setdefault("angle", start_angle)
    _original_arrow_tip_init(self, *args, **kwargs)


ArrowTip.__init__ = _arrow_tip_init


# ---------------------------------------------------------------- Brace.get_text / get_tex
# Until 2020 they returned OldTexText / OldTex (LaTeX, with [0] = the whole string); now they return
# Text and Tex. So as not to change the 2021+ scenes, the old version is only used if the caller is
# a 2020-or-earlier file (the path has a _2015 ... _2020 / 2015 ... 2020 folder).
from manimlib.mobject.svg.brace import Brace
from manimlib.mobject.svg.old_tex_mobject import OldTex, OldTexText

_LEGACY_PATH = re.compile(r"/_?(201\d|2020)/")


def is_legacy_caller(depth=2):
    """True if the calling scene's file is from 2020 or earlier. The frames of
    manimlib and _lib are skipped (a subclass like IntegerMatrix calls Matrix.__init__ from the library)."""
    try:
        frame = sys._getframe(depth)
    except ValueError:
        return False
    while frame is not None:
        filename = frame.f_code.co_filename.replace("\\", "/")
        if "/manimlib/" not in filename and "/_lib/" not in filename:
            return bool(_LEGACY_PATH.search(filename))
        frame = frame.f_back
    return False


_original_brace_get_text = Brace.get_text
_original_brace_get_tex = Brace.get_tex


def _brace_get_text(self, *text, **kwargs):
    if not is_legacy_caller():
        return _original_brace_get_text(self, *text, **kwargs)
    mob = OldTexText(*text)
    self.put_at_tip(mob, **kwargs)
    return mob


def _brace_get_tex(self, *tex, **kwargs):
    if not is_legacy_caller():
        return _original_brace_get_tex(self, *tex, **kwargs)
    mob = OldTex(*tex)
    self.put_at_tip(mob, **kwargs)
    return mob


Brace.get_text = _brace_get_text
Brace.get_tex = _brace_get_tex


# ---------------------------------------------------------------- get_color of a group
# In 2020 get_color() of a Group/Cube returned the color of its family; now it reads data["rgba"][0]
# and a mobject with no points gives IndexError. If it has no points the first submobject is asked.
from manimlib.mobject.types.vectorized_mobject import VMobject


def _wrap_get_color(cls):
    original = cls.get_color

    def get_color(self):
        try:
            return original(self)
        except IndexError:
            for submob in self.submobjects:
                try:
                    return submob.get_color()
                except IndexError:
                    continue
            raise
    cls.get_color = get_color


_wrap_get_color(Mobject)
_wrap_get_color(VMobject)

# ---------------------------------------------------------------- Tex(1, 2): non-str arguments
# TexMobject used to call str() on each argument; now " ".join(...) fails with int.
from manimlib.mobject.svg.tex_mobject import Tex


def _stringify_tex_args(cls):
    original = cls.__init__

    def __init__(self, *args, **kwargs):
        args = tuple(str(a) if isinstance(a, (int, float, np.integer, np.floating)) else a for a in args)
        original(self, *args, **kwargs)
    cls.__init__ = __init__


_stringify_tex_args(Tex)
_stringify_tex_args(OldTex)

# ---------------------------------------------------------------- Matrix.mob_matrix as a numpy array
# Until 2020 it was an np.ndarray (mob_matrix[n, :], .shape); now it is a list of lists. Only for
# 2020-or-earlier scenes (the caller), so as not to change the type in 2021+ ones.
from manimlib.mobject.matrix import Matrix

_original_matrix_init = Matrix.__init__


def _matrix_init(self, *args, **kwargs):
    _original_matrix_init(self, *args, **kwargs)
    if is_legacy_caller():
        rows = self.mob_matrix
        array = np.empty((len(rows), len(rows[0])), dtype=object)
        for i, row in enumerate(rows):
            for j, elem in enumerate(row):
                array[i, j] = elem
        self.mob_matrix = array


Matrix.__init__ = _matrix_init

# ---------------------------------------------------------------- Bubble text
# Until 2020 the text of a bubble (`says("a\\\\b")`, `bubble.write(...)`) was OldTexText, with `\\`
# line breaks and $...$ formulas; now a str is drawn as Text (and `\\` comes out literally). Only
# for 2020-or-earlier scenes (the caller).
from manimlib.mobject.svg.drawings import Bubble

_original_bubble_init = Bubble.__init__
_original_bubble_write = Bubble.write


def _bubble_init(self, content=None, *args, **kwargs):
    if isinstance(content, str) and is_legacy_caller():
        content = OldTexText(content)
    _original_bubble_init(self, content, *args, **kwargs)


def _bubble_write(self, text):
    if isinstance(text, str) and is_legacy_caller():
        self.add_content(OldTexText(text))
        return self
    return _original_bubble_write(self, text)


Bubble.__init__ = _bubble_init
Bubble.write = _bubble_write

# ---------------------------------------------------------------- OldTex as the 2020 TexMobject
# (proposed by E3) In 2020 TexMobject joined its arguments with " " (arg_separator), and
# break_up_by_substrings kept the parts without glyphs ("{", "}", "", "\\,") as empty parts, so the
# scenes' tex[i] indices counted them. manimgl skips them and shifts the indices. Only if whoever
# builds the OldTex is a 2020-or-earlier scene.
from manimlib.mobject.svg.old_tex_mobject import SingleStringTex

_original_old_tex_init = OldTex.__init__
_original_break_up = OldTex.break_up_by_substrings


def _old_tex_init(self, *tex_strings, **kwargs):
    legacy = is_legacy_caller()
    self._legacy_tex = legacy
    if legacy and "arg_separator" not in kwargs:
        kwargs["arg_separator"] = " "
    _original_old_tex_init(self, *tex_strings, **kwargs)


def _break_up_by_substrings(self, tex_strings):
    if not getattr(self, "_legacy_tex", False):
        return _original_break_up(self, tex_strings)
    tex_strings = list(tex_strings)
    if len(tex_strings) == 1:
        self.set_submobjects([self.copy()])
        return self
    new_submobjects = []
    curr_index = 0
    for tex_string in tex_strings:
        tex_string = tex_string.strip()
        sub_tex_mob = SingleStringTex(tex_string, math_mode=self.math_mode) if tex_string else SingleStringTex("")
        num_submobs = len(sub_tex_mob) if tex_string else 0
        if num_submobs == 0:
            sub_tex_mob.set_submobjects([])
            if self.submobjects:
                sub_tex_mob.move_to(self.submobjects[min(curr_index, len(self.submobjects) - 1)], RIGHT)
        else:
            sub_tex_mob.set_submobjects(self.submobjects[curr_index:curr_index + num_submobs])
        new_submobjects.append(sub_tex_mob)
        curr_index += num_submobs
    self.set_submobjects(new_submobjects)
    return self


OldTex.__init__ = _old_tex_init
OldTex.break_up_by_substrings = _break_up_by_substrings
