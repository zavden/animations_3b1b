"""Standalone version of `manim_imports_ext.py` from the 3b1b/videos repo.

Differences from the original:
- It points the assets directories (pi creatures, images, sounds, data)
  to `converted/_lib/assets` instead of Grant's Dropbox.
- It replicates the essentials of his `custom_config.yml`: black background and CMU Serif font.
  If you pass `-c <color>` on the command line, your color is respected.

This module is importable from any folder thanks to the file
`converted_lib.pth` installed in manimgl's venv (see INSTALL_LOG.md)."""
import inspect
import os
import sys
from pathlib import Path

from manimlib import *
from manimlib.mobject.svg.old_tex_mobject import *

_LIB_DIR = Path(__file__).resolve().parent
# THREEB1B_ASSETS allows rendering against another assets folder (e.g. the clean one, without Grant's
# videos/assets files, which _tools/make_clean_assets.py builds). If it is not set, the assets repo cloned
# inside animations_3b1b/ (assets_3b1b/) or next to it (../assets_3b1b) is used and, in converted/,
# _lib/assets.
_ASSETS = Path(os.environ.get("THREEB1B_ASSETS") or next(
    (d for d in (_LIB_DIR.parent / "assets_3b1b", _LIB_DIR.parent.parent / "assets_3b1b") if (d / "PiCreature").is_dir()),
    _LIB_DIR / "assets",
))

manim_config.directories.update(
    pi_creature_images=str(_ASSETS / "PiCreature"),
    vector_images=str(_ASSETS / "svg_images"),
    raster_images=str(_ASSETS / "raster_images"),
    three_d_models=str(_ASSETS / "models"),
    sounds=str(_ASSETS / "sounds"),
    data=str(_LIB_DIR / "data"),
)
if not {"-c", "--color"}.intersection(sys.argv):
    manim_config.camera.background_color = "#000000"
manim_config.text.font = "CMU Serif"


# Grant works on macOS, which is case-insensitive: his code asks for "IMO_logo" even though the file
# is "imo_logo.png". If the normal lookup fails, it is retried ignoring case (and, for paths from
# his Dropbox, by file name). It also accepts Path paths (the original only accepts str).
import manimlib.utils.file_ops as _file_ops
import manimlib.utils.images as _images
import manimlib.utils.sounds as _sounds

_original_find_file = _file_ops.find_file


def _resolve_ignoring_case(path: Path):
    current = Path(path.anchor) if path.is_absolute() else Path(".")
    for part in path.parts[1:] if path.is_absolute() else path.parts:
        exact = current / part
        if exact.exists():
            current = exact
            continue
        if not current.is_dir():
            return None
        matches = [p for p in current.iterdir() if p.name.lower() == part.lower()]
        if not matches:
            return None
        current = matches[0]
    return current if current.is_file() else None


def find_file(file_name, directories=None, extensions=None):
    file_name = str(file_name)
    try:
        return _original_find_file(file_name, directories, extensions)
    except IOError:
        names = [file_name]
        # Absolute paths from Grant's Dropbox (/Users/grant/...): the file is looked up by name in
        # the assets directories, where the placeholders are
        if file_name.startswith("/Users/grant/"):
            names += [Path(file_name).name, Path(file_name).stem]
        for name in names:
            for directory in directories or [""]:
                for extension in extensions or [""]:
                    found = _resolve_ignoring_case(Path(directory, name + extension))
                    if found is not None:
                        return found
        raise


_images.find_file = find_file
_sounds.find_file = find_file


# Since manimgl PR #2481 (2026-07-31), an updater receives dt if its signature accepts two
# arguments, so the pattern `lambda m, i=i: ...` receives dt in `i`. Almost the whole repo predates
# it and uses the old rule: it receives dt only if it has a "dt" parameter.
from manimlib.mobject.mobject import Updater


def _func_takes_dt(func) -> bool:
    try:
        return "dt" in inspect.signature(func).parameters
    except (TypeError, ValueError):
        return False


Updater.func_takes_dt = staticmethod(_func_takes_dt)


# manimgl bug: TexturedSurface.pointwise_become_partial uses `im_coords` without defining it, so
# ShowCreation of a textured surface raises NameError.
from manimlib.mobject.types.surface import TexturedSurface


def _textured_pointwise_become_partial(self, tsmobject, a, b, axis=None):
    if axis is None:
        axis = self.preferred_creation_axis
    super(TexturedSurface, self).pointwise_become_partial(tsmobject, a, b, axis)
    with self.data.being_written() as data:
        im_coords = data["im_coords"]
        im_coords[:] = tsmobject.data["im_coords"]
        if a <= 0 and b >= 1:
            return self
        nu, nv = tsmobject.get_resolution()
        im_coords[:] = self.get_partial_points_array(im_coords, a, b, (nu, nv, 2), axis)
    return self


TexturedSurface.pointwise_become_partial = _textured_pointwise_become_partial


# manimgl bug (same PR #2481): the scene calls mobject.update(dt, frame_rate=...), but
# AnimatedStreamLines redefines update(self, dt) without that parameter -> TypeError.
from manimlib.mobject.vector_field import AnimatedStreamLines

_original_stream_lines_update = AnimatedStreamLines.update


def _stream_lines_update(self, dt=0, recurse=True, frame_rate=None):
    _original_stream_lines_update(self, dt)
    return self


AnimatedStreamLines.update = _stream_lines_update


# manimgl bug: AnimationGroup consumes a generator when building self.animations and then evaluates
# `all(isinstance(anim.mobject, VMobject) for anim in animations)` over the already-empty generator
# (gives True), so LaggedStart(FadeTransform(...) for ...) builds a VGroup with Groups and fails.
# The generator is converted to a list first.
from collections.abc import Iterator
from manimlib.animation.composition import AnimationGroup

_original_animation_group_init = AnimationGroup.__init__


def _animation_group_init(self, *args, **kwargs):
    if len(args) == 1 and isinstance(args[0], Iterator):
        args = (list(args[0]),)
    # manimgl bug (since 2024): AnimationGroup() with no arguments raises IndexError (it reads
    # args[0]); it works with LaggedStart(*anims) of an empty list.
    if not args:
        args = ([],)
    _original_animation_group_init(self, *args, **kwargs)


AnimationGroup.__init__ = _animation_group_init


# manimgl bug (since 2023): point_from_proportion on a zero-length curve (e.g. Arc(angle=0)) asks
# for a curve out of range and fails an assert.
_original_curve_and_prop = VMobject.curve_and_prop_of_partial_point


def _curve_and_prop_of_partial_point(self, alpha):
    index, residue = _original_curve_and_prop(self, alpha)
    if index >= self.get_num_curves():
        return 0, 0.0
    return index, residue


VMobject.curve_and_prop_of_partial_point = _curve_and_prop_of_partial_point


# Since August 2024, set_stroke(background=...) is called set_stroke(behind=...), and
# set_style(stroke_background=...) is called set_style(stroke_behind=...). The old names, widely
# used in the 2020-2023 videos, are accepted.
_original_set_stroke = VMobject.set_stroke
_original_set_style = VMobject.set_style


def _set_stroke(self, *args, background=None, **kwargs):
    if background is not None:
        kwargs.setdefault("behind", background)
    return _original_set_stroke(self, *args, **kwargs)


def _set_style(self, *args, stroke_background=None, reflectiveness=None, gloss=None, shadow=None,
               **kwargs):
    if stroke_background is not None:
        kwargs.setdefault("stroke_behind", stroke_background)
    # Until 2022 shading was passed as reflectiveness/gloss/shadow; now it is shading=(r, g, s)
    if (reflectiveness, gloss, shadow) != (None, None, None):
        self.set_shading(reflectiveness, gloss, shadow, recurse=kwargs.get("recurse", True))
    return _original_set_style(self, *args, **kwargs)


VMobject.set_stroke = _set_stroke
VMobject.set_style = _set_style


# PR #2481: the scene calls mobject.update(dt, frame_rate=...) and Mobject.update passes it to the
# children as a third argument. The repo's classes that redefine update(self, dt=0, recurse=True)
# fail with TypeError. When such a subclass is defined, its update is wrapped to receive only the
# arguments it accepts.
import functools


def _update_without_frame_rate(update):
    try:
        params = list(inspect.signature(update).parameters.values())[1:]
    except (TypeError, ValueError):
        return update
    kinds = {p.kind for p in params}
    if inspect.Parameter.VAR_KEYWORD in kinds or any(p.name == "frame_rate" for p in params):
        return update
    names = {p.name for p in params}
    positional = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    max_args = None if inspect.Parameter.VAR_POSITIONAL in kinds else sum(
        p.kind in positional for p in params
    )

    @functools.wraps(update)
    def wrapped(self, *args, **kwargs):
        if max_args is not None:
            args = args[:max_args]
        kwargs = {k: v for k, v in kwargs.items() if k in names}
        return update(self, *args, **kwargs)
    return wrapped


# Until 2022 classes declared their default values in a CONFIG dict, which digest_config turned into
# attributes (merging the dicts with those of the base classes). manimgl no longer reads it, so
# those values were silently ignored. When a scene or mobject with CONFIG is defined, its keys
# become class attributes, and a dict is merged with the inherited one. In a scene, `camera_config`
# goes to `default_camera_config`, and `camera_class` is ignored (every camera is 3D). It does not
# reach the __init__ parameters of manimgl's classes (e.g. a mobject's `color`).
def _apply_config(cls):
    config = cls.__dict__.get("CONFIG")
    if not isinstance(config, dict):
        return
    config = dict(config)
    if issubclass(cls, Scene):
        if "camera_config" in config:
            camera_config = dict(config.pop("camera_config"))
            # samples is now an attribute of the scene, and anti_alias_width no longer exists
            if "samples" in camera_config:
                config["samples"] = camera_config.pop("samples")
            camera_config.pop("anti_alias_width", None)
            config["default_camera_config"] = camera_config
        config.pop("camera_class", None)
    for key, value in config.items():
        inherited = getattr(cls, key, None)
        if isinstance(value, dict) and isinstance(inherited, dict):
            value = merge_dicts_recursively(inherited, value)
        setattr(cls, key, value)
    cls._config_keys = frozenset(config).union(getattr(cls, "_config_keys", ()))


# The construction kwargs that match a CONFIG key (`Person(person_type=...)`,
# `Coin(numeric_labels=True)`, `CoinsOnBoard(coin_config={...})`) were consumed by digest_config in
# Mobject.__init__. Those that reach Mobject.__init__ without anyone claiming them (before they gave
# TypeError) become instance attributes; a dict is merged with the class's one.
_original_mobject_init = Mobject.__init__


def _digest_config_kwargs(self, kwargs):
    keys = getattr(type(self), "_config_keys", ())
    for key in [k for k in kwargs if k in keys]:
        value = kwargs.pop(key)
        inherited = getattr(self, key, None)
        if isinstance(value, dict) and isinstance(inherited, dict):
            value = merge_dicts_recursively(inherited, value)
        setattr(self, key, value)


_MOBJECT_INIT_PARAMS = frozenset(inspect.signature(_original_mobject_init).parameters) - {"self"}
_warned_ignored_kwargs = set()


def _mobject_init(self, *args, **kwargs):
    _digest_config_kwargs(self, kwargs)
    # digest_config in the old version stored any leftover kwarg as an attribute (and ignored it if
    # nobody read it); now it is a TypeError. It is imitated, warning once per class and kwarg.
    for key in [k for k in kwargs if k not in _MOBJECT_INIT_PARAMS]:
        value = kwargs.pop(key)
        marker = (type(self).__name__, key)
        if marker not in _warned_ignored_kwargs:
            _warned_ignored_kwargs.add(marker)
            print(f"[legacy] {type(self).__name__}(...{key}=) no es un parametro de manimgl: se guarda como atributo", file=sys.stderr)
        try:
            setattr(self, key, value)
        except AttributeError:
            pass
    _original_mobject_init(self, *args, **kwargs)


Mobject.__init__ = _mobject_init


# CONFIG of the Animation subclasses (e.g. `class FlipCoin(Animation): CONFIG = {"axis": RIGHT}`). The
# keys that are parameters of Animation (run_time, rate_func, lag_ratio...) are passed as default
# value; the others become instance attributes.
_original_animation_init = Animation.__init__
_ANIMATION_INIT_PARAMS = frozenset(inspect.signature(_original_animation_init).parameters) - {"self", "mobject"}


def _animation_init(self, *args, **kwargs):
    keys = getattr(type(self), "_config_keys", ())
    if keys:
        for key in keys & _ANIMATION_INIT_PARAMS:
            if key not in kwargs and len(args) <= 1:
                kwargs[key] = getattr(type(self), key)
        for key in [k for k in kwargs if k in keys and k not in _ANIMATION_INIT_PARAMS]:
            setattr(self, key, kwargs.pop(key))
    _original_animation_init(self, *args, **kwargs)


Animation.__init__ = _animation_init


def _animation_init_subclass(cls, **kwargs):
    super(Animation, cls).__init_subclass__(**kwargs)
    _apply_config(cls)


Animation.__init_subclass__ = classmethod(_animation_init_subclass)


def _mobject_init_subclass(cls, **kwargs):
    super(Mobject, cls).__init_subclass__(**kwargs)
    _apply_config(cls)
    update = cls.__dict__.get("update")
    if inspect.isfunction(update):
        cls.update = _update_without_frame_rate(update)


def _scene_init_subclass(cls, **kwargs):
    super(Scene, cls).__init_subclass__(**kwargs)
    _apply_config(cls)


Mobject.__init_subclass__ = classmethod(_mobject_init_subclass)
Scene.__init_subclass__ = classmethod(_scene_init_subclass)


# In August 2024 FillArrow was renamed Arrow, and `thickness` stopped being measured in scene units
# (0.05 by default) and is instead multiplied by Arrow.tickness_multiplier.
class FillArrow(Arrow):
    def __init__(self, *args, thickness: float = 0.05, **kwargs):
        super().__init__(*args, thickness=thickness / Arrow.tickness_multiplier, **kwargs)


# manimgl bug (since June 2024): LaggedStartMap(anim, list) fails with "Animation only works for
# Mobjects", because it uses the list as the animation's mobject. It is grouped first.
_original_lagged_start_map_init = LaggedStartMap.__init__


def _lagged_start_map_init(self, anim_func, group, *args, **kwargs):
    # Until 2021: LaggedStartMap(Class, group, arg_creator, **kwargs), where arg_creator(m) returns
    # the animation arguments of each member (e.g. lambda m: (m.shift, v)). It goes as the third
    # positional argument or with that name.
    arg_creator = kwargs.pop("arg_creator", None)
    if args and callable(args[0]) and not isinstance(args[0], (int, float)):
        arg_creator, args = args[0], args[1:]
    if arg_creator is not None:
        _anim_class = anim_func

        def anim_func(m, **kw):
            return _anim_class(*arg_creator(m), **kw)
    if not isinstance(group, Mobject):
        group = list(group)
        group_type = VGroup if all(isinstance(m, VMobject) for m in group) else Group
        group = group_type(*group)
    _original_lagged_start_map_init(self, anim_func, group, *args, **kwargs)


LaggedStartMap.__init__ = _lagged_start_map_init


# manimgl bugs (memory): the scene keeps a reference to every mobject ever added to it
# (id_to_mobject_map), and the SVG cache (each distinct Text/Tex) has no limit. A scene that redraws
# a growing paragraph 300 times went over 5 GB. The map is made weak and the cache is bounded (the
# same fixes as in the fork).
import weakref
import manimlib.mobject.svg.svg_mobject as _svg_module
from manimlib.utils.iterables import hash_obj as _hash_obj

_original_scene_init = Scene.__init__


def _scene_init(self, *args, **kwargs):
    _original_scene_init(self, *args, **kwargs)
    if not isinstance(self.id_to_mobject_map, weakref.WeakValueDictionary):
        self.id_to_mobject_map = weakref.WeakValueDictionary(self.id_to_mobject_map)


Scene.__init__ = _scene_init

_SVG_CACHE_MAX_SUBMOBJECTS = 10000


def _init_svg_mobject(self):
    cache = _svg_module.SVG_HASH_TO_MOB_MAP
    hash_val = _hash_obj(self.hash_seed)
    if hash_val in cache:
        # At the end, as the most recently used
        cache[hash_val] = cache.pop(hash_val)
        submobs = [sm.copy() for sm in cache[hash_val]]
    else:
        submobs = self.mobjects_from_svg_string(self.svg_string)
        cache[hash_val] = [sm.copy() for sm in submobs]
        cached = sum(map(len, cache.values()))
        while cached > _SVG_CACHE_MAX_SUBMOBJECTS and len(cache) > 1:
            cached -= len(cache.pop(next(iter(cache))))
    self.add(*submobs)
    self.flip(RIGHT)


SVGMobject.init_svg_mobject = _init_svg_mobject


# In March 2024 Bubble/SpeechBubble/ThoughtBubble began to take the size of their content (or of
# filler_shape) and stopped accepting width/height, widely used until 2023. They are accepted again:
# the body takes that size and the content shrinks to fit in it, as before.
_original_bubble_init = Bubble.__init__


def _bubble_init(self, *args, width=None, height=None, **kwargs):
    _original_bubble_init(self, *args, **kwargs)
    if width is None and height is None:
        return
    body = self.body
    body.set_shape(width or body.get_width(), height or body.get_height())
    body.move_to(self.content)
    body.shift(self.bubble_center_adjustment_factor * body.get_height() * DOWN)
    # With the fixed margin of position_mobject_inside, a short body leaves the content without height
    buff = min(MED_LARGE_BUFF, body.get_width() / 8, body.get_height() / 8)
    self.position_mobject_inside(self.content, buff=buff)


Bubble.__init__ = _bubble_init


# Since August 2026 (#2482) a surface's resolution lives only in its uniforms and is read with
# get_resolution(); the 2020-2024 code uses the attribute `surface.resolution`.
Surface.resolution = property(Surface.get_resolution, Surface.set_resolution)


# Since October 2025 (#2402) NumberLine does not store unit_size: it is measured with get_unit_size().
# Assigning it after building the line had no effect before either, so it is ignored.
NumberLine.unit_size = property(
    NumberLine.get_unit_size,
    lambda self, value: None,
)


# Grant used a local version of manimgl in which set_opacity also accepted border_width (it never
# reached the published version): it is passed to set_fill, which does accept it.
_original_set_opacity = VMobject.set_opacity


def _set_opacity(self, opacity, recurse=True, border_width=None):
    _original_set_opacity(self, opacity, recurse)
    if border_width is not None:
        self.set_fill(border_width=border_width, recurse=recurse)
    return self


VMobject.set_opacity = _set_opacity


# manimgl bug (since December 2024, #2259): SVGMobject requires the SVG or a file, and
# SingleStringTex (base of OldTex/OldTexText, with which the LaTeX of the 2022-and-earlier videos is
# written) passes it neither. It is given a "virtual" file whose SVG is written from the tex.
SingleStringTex.file_name = "tex"
SingleStringTex.file_name_to_svg_string = lambda self, file_name: self.get_svg_string_by_content(
    self.get_tex_file_body(self.tex_string)
)


# manimgl bugs (also fixed in the fork): indexing a Text/Tex with a numpy integer (e.g. from
# np.argmin) treated it as a substring to search, and OldTex balanced braces badly in a chunk with an
# unmatched } (it added one { per remaining character), which misaligned its parts.
_original_string_mobject_getitem = StringMobject.__getitem__


def _string_mobject_getitem(self, value):
    if isinstance(value, np.integer):
        value = int(value)
    return _original_string_mobject_getitem(self, value)


def _balance_braces(self, tex):
    num_unclosed = 0
    num_unopened = 0
    for i, char in enumerate(tex):
        if i > 0 and tex[i - 1] == "\\":
            continue
        if char == "{":
            num_unclosed += 1
        elif char == "}":
            if num_unclosed == 0:
                num_unopened += 1
            else:
                num_unclosed -= 1
    return num_unopened * "{" + tex + num_unclosed * "}"


StringMobject.__getitem__ = _string_mobject_getitem
SingleStringTex.balance_braces = _balance_braces


# Until 2020 a method was animated by passing it with its arguments: self.play(mob.shift, UP).
# manimgl no longer accepts it (TypeError "cannot be converted to an animation"). The ApplyMethod
# that the old version built is built; the arguments of a method are the ones that follow until the
# next animation.
from manimlib.mobject.mobject import _AnimationBuilder

_original_play = Scene.play


def _is_mobject_method(arg):
    return inspect.ismethod(arg) and isinstance(arg.__self__, Mobject)


def _play(self, *proto_animations, run_time=None, rate_func=None, lag_ratio=None, **extra):
    animations = []
    args = list(proto_animations)
    while args:
        arg = args.pop(0)
        if _is_mobject_method(arg) and arg.__func__ is Mobject.restore:
            # ApplyMethod(m.restore) copies the mobject and the copy does not keep saved_state
            arg = Restore(arg.__self__)
        elif _is_mobject_method(arg):
            method_args = []
            while args and not (isinstance(args[0], (Animation, _AnimationBuilder))
                                or _is_mobject_method(args[0])):
                method_args.append(args.pop(0))
            arg = ApplyMethod(arg, *method_args)
        animations.append(arg)
    # Until 2021 play passed any other kwarg (path_arc, ...) to each animation; now it only accepts
    # these three. It goes to mob.animate(...) or is set on the animation, as the old version did
    if extra:
        for anim in animations:
            if isinstance(anim, _AnimationBuilder):
                anim.set_anim_args(**extra)
            elif isinstance(anim, Animation):
                for key, value in extra.items():
                    setattr(anim, key, value)
                if isinstance(anim, Transform) and ("path_arc" in extra or "path_func" in extra):
                    anim.path_func = extra.get("path_func")
                    anim.init_path_func()
    return _original_play(self, *animations, run_time=run_time, rate_func=rate_func, lag_ratio=lag_ratio)


Scene.play = _play


# manimgl bugs (also fixed in the fork): a zero-step NewtonFractal came out a single color, and
# NumberPlane(background_line_style=dict(stroke_width=1)), without color, gave KeyError.
_original_newton_fractal_init = NewtonFractal.__init__


def _newton_fractal_init(self, *args, **kwargs):
    _original_newton_fractal_init(self, *args, **kwargs)
    self.replace_shader_code("var step_size = 0.0;", "var step_size = 1.0;")


_original_number_plane_init = NumberPlane.__init__


def _number_plane_init(self, *args, background_line_style=None, **kwargs):
    if background_line_style is not None:
        background_line_style = dict(background_line_style)
        background_line_style.setdefault("stroke_color", BLUE_D)
        kwargs["background_line_style"] = background_line_style
    _original_number_plane_init(self, *args, **kwargs)


NewtonFractal.__init__ = _newton_fractal_init
NumberPlane.__init__ = _number_plane_init


# Until 2021 ParametricCurve completed an incomplete t_range with (0, 1, 0.1) and accepted t_min,
# t_max and step_size; now it requires all three values.
_original_parametric_curve_init = ParametricCurve.__init__


def _parametric_curve_init(self, t_func, t_range=(0, 1, 0.1), *args, t_min=None, t_max=None,
                           step_size=None, **kwargs):
    full_range = [0, 1, 0.1]
    full_range[:len(t_range)] = t_range
    for i, value in enumerate([t_min, t_max, step_size]):
        if value is not None:
            full_range[i] = value
    _original_parametric_curve_init(self, t_func, tuple(full_range), *args, **kwargs)


ParametricCurve.__init__ = _parametric_curve_init


# TransformMatchingTex only accepts current Tex/Text (StringMobject). The 2021-2022 code uses it
# with OldTex or groups, which used to be matched by parts; there TransformMatchingShapes is used,
# which matches by shape.
def _transform_matching_tex_new(cls, source, target, *args, **kwargs):
    if isinstance(source, StringMobject) and isinstance(target, StringMobject):
        return object.__new__(cls)
    for key in ("key_map", "matched_keys", "fade_transform_mismatches", "transform_mismatches"):
        kwargs.pop(key, None)
    return TransformMatchingShapes(source, target, *args, **kwargs)


# The class is patched (not the name): the `from custom... import *` statements below re-export manimgl's
TransformMatchingTex.__new__ = staticmethod(_transform_matching_tex_new)


# manimgl bug (also fixed in the fork): Sector(outer_radius=...), as its own docstring and the pre-2023
# code write it, gave "multiple values for keyword argument". And `circle.radius` (an earlier
# attribute; now get_radius()) is defined as a property.
_original_sector_init = Sector.__init__


def _sector_init(self, *args, outer_radius=None, **kwargs):
    if outer_radius is not None:
        kwargs["radius"] = outer_radius
    _original_sector_init(self, *args, **kwargs)


Sector.__init__ = _sector_init
Circle.radius = property(Circle.get_radius, lambda self, value: None)


# Until 2023 the thickness of Arrow/Vector was given in scene units (0.025-0.15); since August 2024
# it is multiplied by Arrow.tickness_multiplier (0.015), and those values give invisible arrows. A
# thickness that small only makes sense on the old scale, so it is converted.
_original_arrow_init = Arrow.__init__


def _arrow_init(self, *args, thickness=None, **kwargs):
    # Arguments of the 2020 stroke-based Arrow (now it is a filled arrow)
    if "max_stroke_width_to_length_ratio" in kwargs:
        kwargs.setdefault("max_width_to_length_ratio", kwargs.pop("max_stroke_width_to_length_ratio"))
    tip_length = kwargs.pop("tip_length", None)
    for old_key in ("tip_width", "tip_config", "preserve_tip_size_when_scaling"):
        kwargs.pop(old_key, None)
    if tip_length is not None:
        base = (thickness if thickness is not None else 3.0)
        if base < 0.3:
            base = base / Arrow.tickness_multiplier
        kwargs.setdefault("tip_width_ratio", tip_length / (0.866 * base * Arrow.tickness_multiplier))
        kwargs.setdefault("max_tip_length_to_length_ratio", 1.0)
    if thickness is not None:
        if thickness < 0.3:
            thickness = thickness / Arrow.tickness_multiplier
        kwargs["thickness"] = thickness
    _original_arrow_init(self, *args, **kwargs)


Arrow.__init__ = _arrow_init


# manimgl bug (since November 2022; also fixed in the fork): in a play, an animation shorter than the
# longest one receives alphas greater than 1 when it finishes, and those that read the alpha directly
# (UpdateFromAlphaFunc, MoveAlongPath, ChangingDecimal...) kept going. It is clipped to [0, 1].
Animation.interpolate = lambda self, alpha: self.interpolate_mobject(clip(alpha, 0, 1))


# manimgl bug (since August 2026; also fixed in the fork): mob.deepcopy() copied the StructuredArray's
# floats/bytes views as separate arrays, so the moved or restyled copy was drawn as it was when copied.
from manimlib.utils.structured_array import StructuredArray as _StructuredArray


def _structured_array_deepcopy(self, memo):
    result = self.copy()
    memo[id(self)] = result
    return result


_StructuredArray.__deepcopy__ = _structured_array_deepcopy


# manimgl bug (since August 2026; also fixed in the fork): Rotating copies the initial points straight
# into the data without updating the bounding boxes, and rotates around an old center. If an updater
# reorders the parts every frame (faces sorted by depth), the group drifted away.
_original_rotating_interpolate = Rotating.interpolate_mobject


def _rotating_interpolate(self, alpha):
    pairs = zip(
        self.mobject.family_members_with_points(),
        self.starting_mobject.family_members_with_points(),
    )
    for sm1, sm2 in pairs:
        for key in sm1.pointlike_data_keys:
            sm1.data[key] = sm2.data[key]
    self.mobject.refresh_bounding_box(recurse_down=True)
    self.mobject.rotate(
        self.rate_func(self.time_spanned_alpha(alpha)) * self.angle,
        axis=self.axis,
        about_point=self.about_point,
        about_edge=self.about_edge,
    )


Rotating.interpolate_mobject = _rotating_interpolate


# Fonts: some scenes ask for fonts that cannot be redistributed (Consolas is Microsoft's, and the
# license of Better Grade and Simplo Soft is unclear). Free fonts (OFL) from _lib/assets/fonts are
# registered (assets/generated/fonts/get_fonts.py downloads them) and the old names are translated.
import manimpango as _manimpango

FONT_ALIASES = {
    "Consolas": "JetBrains Mono",
    "Better Grade": "Caveat",
    "Simplo Soft Medium": "Nunito",
}
for _font_file in sorted((_ASSETS / "fonts").glob("*.ttf")):
    _manimpango.register_font(str(_font_file))
_original_markup_text_init = MarkupText.__init__


def _markup_text_init(self, text, *args, font="", **kwargs):
    _original_markup_text_init(self, text, *args, font=FONT_ALIASES.get(font, font), **kwargs)


MarkupText.__init__ = _markup_text_init


# numpy 2 removed these aliases, which the 2020-2024 code uses
for _name, _value in [("product", np.prod), ("float", float), ("infty", np.inf), ("complex", complex)]:
    if not hasattr(np, _name):
        setattr(np, _name, _value)

from custom.backdrops import *
from custom.banner import *
from custom.characters.pi_creature import *
from custom.characters.pi_creature_animations import *
from custom.characters.pi_creature_scene import *
from custom.deprecated import *
from custom.drawings import *
from custom.end_screen import *
from custom.filler import *
from custom.logo import *
from custom.opening_quote import *

# Compatibility with the 2020 API (early GL): separate module, see its docstring
from legacy_2020 import *

# Compatibility with the Cairo era (2015-2019): separate module, see its docstring
from cairo_compat import *
