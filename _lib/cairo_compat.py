"""Compatibility with the code of 3b1b's Cairo era (2015-2019) on ManimGL 1.7.2.

It is imported by `manim_imports_ext.py` at the end, so it is available in all scenes. What it only adds
(names, aliases, missing methods) applies to all. The patches that wrap methods that already exist are installed
only if the scene being rendered is from 2015-2020 (`_CAIRO_ERA`; 2020 included because its early GL code uses the
same old arguments), so as not to change anything from 2021 onward. Each
patch carries a line saying which old code needs it.

It was started by the Codex instance that converted part of 2019 (`_tools/CODEX_2019.md`, `handoff/CX19*.md`); now it belongs
to the agent that continues with 2015-2019. The general shims remain in `manim_imports_ext.py`."""
from manimlib import *
from manimlib.mobject.svg.old_tex_mobject import OldTex, OldTexText
from once_useful_constructs.dict_shenanigans import digest_config, digest_locals, DictAsObject
from once_useful_constructs.graph_scene import GraphScene as _OriginalGraphScene
import inspect as _inspect
import os as _os
import re as _re
import sys as _sys
import types as _types

# Cairo-era or 2020 scene: the path of the file being rendered (_work/_2015 ... _work/_2020, or <category>/2015 ... <category>/2020) or
# CAIRO_COMPAT=1 (the file can be given with a relative path, e.g. `cd 2_modified/2019/windmill; manimgl X.py X`: its absolute path is
# checked too)
_ARGV_PATHS = [str(arg) for arg in _sys.argv] + [_os.path.abspath(arg) for arg in _sys.argv[1:] if str(arg).endswith(".py")]
_CAIRO_ERA = (_os.environ.get("CAIRO_COMPAT") == "1"
              or any(_re.search(r"[/\\]_?20(1[5-9]|20)[/\\]", str(arg)) for arg in _ARGV_PATHS))

# Only what this module adds is exported. Without __all__, the `import *` of manim_imports_ext would re-export
# the original names from manimlib and override the shims defined before it. Each new name goes in this list.
__all__ = [
    "MovingCameraScene", "SpecialThreeDScene", "GraphScene", "ParametricFunction",
    "digest_config", "digest_locals", "DictAsObject", "DoubleArrow", "ThreeDVMobject",
    "ShowPassingFlashWithThinningStrokeWidth", "ContinualChangingDecimal",
    "CairoHilbertCurve", "rotate", "SOUND_DIR",
    "cairo_svg_defaults",
    "CairoImageMobject",
    "CairoParametricSurface", "CairoSphere", "CairoCube",
    "CairoVectorField", "cairo_smooth", "cairo_rush_into",
    "cairo_arrange_in_grid",
    "CairoPMobject", "CairoPGroup",
]


# Cairo scenes read this legacy attribute; GL derives the angle from the curve.
if _CAIRO_ERA and not hasattr(Arc, "start_angle"):
    Arc.start_angle = property(lambda self: self.get_start_angle())


# Cairo 2019: these bases no longer exist in GL; the extractor also needs them.
class MovingCameraScene(Scene):
    @property
    def camera_frame(self):
        return self.frame


def cairo_arrange_in_grid(mobject, n_rows=None, n_cols=None, **kwargs):
    """Opt into sep19 grid order and spacing without changing GL's grid method."""
    submobjects = mobject.submobjects
    if not submobjects:
        return mobject
    if n_rows is None and n_cols is None:
        n_cols = max(1, int(np.sqrt(len(submobjects))))
    count = n_rows if n_rows is not None else n_cols
    if count <= 0:
        raise ValueError("Grid dimensions must be positive.")
    chunk_size = max(1, len(submobjects) // count)
    first, second = (RIGHT, DOWN) if n_rows is not None else (DOWN, RIGHT)
    Group(*[
        Group(*submobjects[index:index + chunk_size]).arrange(first, **kwargs)
        for index in range(0, len(submobjects), chunk_size)
    ]).arrange(second, **kwargs)
    return mobject


class CairoPMobject(DotCloud):
    """Opt into visible Cairo point clouds with fixed stroke size during scaling."""

    def __init__(self, points=None, stroke_width=4, **kwargs):
        self.stroke_width = stroke_width
        super().__init__(points=points, radius=self._stroke_radius(stroke_width), **kwargs)

    @staticmethod
    def _stroke_radius(width):
        # sep19 scales production (1440p) point thickness to the 720p reference.
        pixels = max(0, int(1 + (float(width) - 1) / 2))
        return pixels * FRAME_HEIGHT / (2 * 720)

    def add_points(self, points, rgbas=None, color=None, alpha=1, opacity=None):
        if color is None and rgbas is None:
            color = self.get_color() if self.get_num_points() else self.color
        super().add_points(points, rgbas=rgbas,
                           color=color,
                           opacity=alpha if opacity is None else opacity)
        self.set_radius(self._stroke_radius(self.stroke_width))
        return self

    def set_stroke_width(self, width, family=True):
        for mob in self.get_family(recurse=family):
            if isinstance(mob, CairoPMobject):
                mob.stroke_width = width
                mob.radius = self._stroke_radius(width)
                mob.set_radius(mob.radius)
        return self

    def get_stroke_width(self):
        return self.stroke_width

    def scale(self, scale_factor, **kwargs):
        kwargs.pop("scale_radii", None)
        return super().scale(scale_factor, scale_radii=False, **kwargs)


class CairoPGroup(CairoPMobject):
    """Group Cairo point clouds while retaining their legacy type checks."""

    def __init__(self, *mobjects, **kwargs):
        super().__init__(**kwargs)
        self.add(*mobjects)


# Grant removed MovingCameraScene from some files without migrating camera_frame.
if not hasattr(Scene, "camera_frame"):
    Scene.camera_frame = property(lambda self: self.frame)

from manimlib.camera.camera import Camera as _Camera
if not hasattr(_Camera, "frame_center"):
    _Camera.frame_center = property(lambda self: self.frame)
if not hasattr(_Camera, "set_distance"):
    def _set_distance(self, distance):
        self.frame.set_focal_distance(distance)
        return self
    _Camera.set_distance = _set_distance
if not hasattr(_Camera, "get_distance"):
    _Camera.get_distance = lambda self: self.frame.get_focal_distance()


# Cairo 2019: only the old methods convert the angles; the GL API stays intact.
def _set_camera_orientation(self, phi=None, theta=None, distance=None, gamma=None):
    angles = {}
    for key, value in (("phi", phi), ("theta", None if theta is None else theta + PI / 2),
                       ("gamma", None if gamma is None else -gamma)):
        if value is not None:
            angles[key] = value
    self.frame.set_euler_angles(**angles)
    if distance is not None:
        self.frame.set_focal_distance(distance)
    return self


def _move_camera(self, phi=None, theta=None, distance=None, gamma=None,
                 frame_center=None, added_anims=None, **kwargs):
    target = self.frame.copy()
    proxy = _types.SimpleNamespace(frame=target)
    _set_camera_orientation(proxy, phi, theta, distance, gamma)
    if frame_center is not None:
        target.move_to(frame_center)
    self.play(Transform(self.frame, target), *(added_anims or []), **kwargs)
    return self


def _begin_ambient_camera_rotation(self, rate=0.02):
    self.stop_ambient_camera_rotation()
    self._cairo_ambient_rotation = lambda frame, dt: frame.increment_theta(rate * dt)
    self.frame.add_updater(self._cairo_ambient_rotation)
    return self


def _stop_ambient_camera_rotation(self):
    updater = getattr(self, "_cairo_ambient_rotation", None)
    if updater is not None:
        self.frame.remove_updater(updater)
    return self


def _add_fixed_in_frame_mobjects(self, *mobjects):
    for mob in mobjects:
        mob.fix_in_frame()
    self.add(*mobjects)
    return self


for _name, _method in {
    "set_camera_orientation": _set_camera_orientation,
    "move_camera": _move_camera,
    "begin_ambient_camera_rotation": _begin_ambient_camera_rotation,
    "stop_ambient_camera_rotation": _stop_ambient_camera_rotation,
    "add_fixed_in_frame_mobjects": _add_fixed_in_frame_mobjects,
}.items():
    if not hasattr(ThreeDScene, _name):
        setattr(ThreeDScene, _name, _method)


class SpecialThreeDScene(ThreeDScene):
    default_frame_orientation = (0, 0)
    three_d_axes_config = dict(unit_size=2, axis_config=dict(stroke_width=2),
                              z_axis_config=dict(unit_size=2))
    sphere_config = dict(radius=2, resolution=(24, 48))
    default_angled_camera_position = dict(phi=70 * DEGREES, theta=-110 * DEGREES)

    def setup(self):
        super().setup()
        self.frame.set_focal_distance(20)

    def get_axes(self):
        return ThreeDAxes(**self.three_d_axes_config)

    def get_sphere(self, **kwargs):
        return CairoSphere(**merge_dicts_recursively(self.sphere_config, kwargs))

    def get_default_camera_position(self):
        return dict(self.default_angled_camera_position)

    def set_camera_to_default_position(self):
        return self.set_camera_orientation(**self.default_angled_camera_position)

    def set_to_default_angled_camera_orientation(self, **kwargs):
        return self.set_camera_orientation(**dict(self.default_angled_camera_position, **kwargs))


# Cairo 2019: the GraphScene port references OldTex/np without importing them. We clone the methods
# with their globals repaired, without editing the shared module or its classes.
class GraphScene(_OriginalGraphScene):
    pass


for _name, _method in vars(_OriginalGraphScene).items():
    if _inspect.isfunction(_method):
        _globals = dict(_method.__globals__, OldTex=OldTex, OldTexText=OldTexText, np=np)
        _clone = _types.FunctionType(_method.__code__, _globals, _method.__name__,
                                     _method.__defaults__, _method.__closure__)
        _clone.__kwdefaults__ = _method.__kwdefaults__
        setattr(GraphScene, _name, _clone)


# Cairo 2019: removed names, with GL equivalents that keep the interface.
ParametricFunction = ParametricCurve
ThreeDVMobject = VMobject


class DoubleArrow(Line):
    def __init__(self, *args, tip_length=0.35, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_tip(length=tip_length)
        self.add_tip(at_start=True, length=tip_length)


# Cairo 2019: set_variables_as_attrs deduced names in the caller's scope.
def _set_variables_as_attrs(self, *objects, **kwargs):
    caller = _inspect.currentframe().f_back
    try:
        for name, value in caller.f_locals.items():
            if name != "self" and any(value is obj for obj in objects):
                setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)
    finally:
        del caller
    return self


if not hasattr(Scene, "set_variables_as_attrs"):
    Scene.set_variables_as_attrs = _set_variables_as_attrs


# Cairo 2019: the old shininess has no exact equivalent; it is kept as GL shading only when the
# removed API is invoked.
def _set_sheen(self, factor, direction=None, family=True):
    self.set_gloss(factor, recurse=family)
    if direction is not None:
        self.sheen_direction = np.array(direction)
    return self


def _set_sheen_direction(self, direction, family=True):
    for mob in self.get_family() if family else (self,):
        mob.sheen_direction = np.array(direction)
    return self


def _set_shade_in_3d(self, value=True, z_index_as_group=False):
    if value:
        self.apply_depth_test()
    else:
        self.deactivate_depth_test()
    return self


for _name, _method in {
    "set_sheen": _set_sheen,
    "set_sheen_direction": _set_sheen_direction,
    "set_shade_in_3d": _set_shade_in_3d,
    "set_background_stroke": lambda self, *args, **kwargs: self.set_backstroke(*args, **kwargs),
}.items():
    if not hasattr(VMobject, _name):
        setattr(VMobject, _name, _method)

for _name, _method in {"set_sheen": _set_sheen, "set_sheen_direction": _set_sheen_direction,
                       "set_shade_in_3d": _set_shade_in_3d}.items():
    if not hasattr(Mobject, _name):
        setattr(Mobject, _name, _method)


# Cairo 2019 Pendulum: kwargs removed from set_style and from VMobject.__init__. Without these old
# arguments it delegates without changing values or results.
from functools import wraps as _wraps

_old_cairo_set_style = VMobject.set_style


@_wraps(_old_cairo_set_style)
def _cairo_set_style(self, *args, sheen_factor=None, sheen_direction=None,
                     background_stroke_color=None, background_stroke_width=None,
                     background_stroke_opacity=None, shade_in_3d=None, family=None, **kwargs):
    if family is not None:
        kwargs.setdefault("recurse", family)
    result = _old_cairo_set_style(self, *args, **kwargs)
    recurse = kwargs.get("recurse", True)
    if sheen_factor is not None:
        self.set_sheen(sheen_factor, sheen_direction, family=recurse)
    elif sheen_direction is not None:
        self.set_sheen_direction(sheen_direction, family=recurse)
    # GL has a single stroke per object. If the main stroke was also requested, preserve it:
    # replacing it with the black border would make the lines disappear.
    has_main_stroke = any(kwargs.get(key) is not None for key in ("stroke_color", "stroke_width", "stroke_opacity"))
    if not has_main_stroke and (background_stroke_color is not None or background_stroke_width is not None or background_stroke_opacity is not None):
        self.set_stroke(background_stroke_color, background_stroke_width, background_stroke_opacity,
                        behind=True, recurse=recurse)
    if shade_in_3d is not None:
        self.set_shade_in_3d(shade_in_3d)
    return result


if _CAIRO_ERA:
    VMobject.set_style = _cairo_set_style
_old_cairo_vmobject_init = VMobject.__init__
_cairo_style_keys = frozenset(("sheen_factor", "sheen_direction", "background_stroke_color",
                              "background_stroke_width", "background_stroke_opacity", "shade_in_3d"))


@_wraps(_old_cairo_vmobject_init)
def _cairo_vmobject_init(self, *args, **kwargs):
    legacy = {key: kwargs.pop(key) for key in tuple(kwargs) if key in _cairo_style_keys}
    # Cairo used this minimum tessellation in Brace. The current WGSL backend subdivides the curves
    # on its own and no longer uses that parameter.
    min_num_quads = kwargs.pop("min_num_quads", None)
    _old_cairo_vmobject_init(self, *args, **kwargs)
    if min_num_quads is not None:
        self.min_num_quads = min_num_quads
    if legacy:
        self.set_style(**legacy)


if _CAIRO_ERA:
    VMobject.__init__ = _cairo_vmobject_init

# The Cairo Bayes helpers query Brace.direction, now get_direction().
if not hasattr(Brace, "direction"):
    Brace.direction = property(lambda self: self.get_direction())


# Cairo Pendulum: DashedLine accepted the number of dashes instead of their length.
_old_cairo_dashed_line_init = DashedLine.__init__


@_wraps(_old_cairo_dashed_line_init)
def _cairo_dashed_line_init(self, start=LEFT, end=RIGHT, *args, num_dashes=None, **kwargs):
    if num_dashes is not None:
        if num_dashes <= 0:
            raise ValueError("num_dashes must be positive")
        line = Line(start, end, buff=kwargs.get("buff", 0), path_arc=kwargs.get("path_arc", 0))
        kwargs["dash_length"] = line.get_arc_length() * kwargs.get("positive_space_ratio", 0.5) / max(num_dashes - 1e-8, 1e-8)
    _old_cairo_dashed_line_init(self, start, end, *args, **kwargs)


if _CAIRO_ERA:
    DashedLine.__init__ = _cairo_dashed_line_init


# Cairo hyperdarts: unit_size in axis_config clashes with the argument that GL adds internally; the
# equivalent call uses the Axes' own unit_size.
_old_cairo_axes_init = Axes.__init__


@_wraps(_old_cairo_axes_init)
def _cairo_axes_init(self, *args, **kwargs):
    for name in ("number_line_config", "axis_config"):
        config = kwargs.get(name)
        if isinstance(config, dict) and "unit_size" in config:
            config = dict(config)
            kwargs.setdefault("unit_size", config.pop("unit_size"))
            kwargs[name] = config
    return _old_cairo_axes_init(self, *args, **kwargs)


if _CAIRO_ERA:
    Axes.__init__ = _cairo_axes_init

_old_cairo_three_axes_init = ThreeDAxes.__init__


@_wraps(_old_cairo_three_axes_init)
def _cairo_three_axes_init(self, *args, z_min=None, z_max=None, num_axis_pieces=None, **kwargs):
    if z_min is not None or z_max is not None:
        values = list(args[2] if len(args) > 2 else kwargs.pop("z_range", (-4, 4, 1)))
        if z_min is not None:
            values[0] = z_min
        if z_max is not None:
            values[1] = z_max
        if len(args) > 2:
            args = (*args[:2], values, *args[3:])
        else:
            kwargs["z_range"] = values
    _old_cairo_three_axes_init(self, *args, **kwargs)
    if num_axis_pieces is not None:
        self.num_axis_pieces = num_axis_pieces


if _CAIRO_ERA:
    ThreeDAxes.__init__ = _cairo_three_axes_init
for _name, _index in (("z_min", 0), ("z_max", 1)):
    if not hasattr(ThreeDAxes, _name):
        setattr(ThreeDAxes, _name, property(lambda self, i=_index: self.z_range[i]))
if not hasattr(NumberLine, "tick_frequency"):
    NumberLine.tick_frequency = property(lambda self: self.x_step)


# Cairo NumberLine used unit="\\%" as the decimal's suffix, now unit_tex.
_old_cairo_number_mobject = NumberLine.get_number_mobject


@_wraps(_old_cairo_number_mobject)
def _cairo_number_mobject(self, *args, **kwargs):
    if isinstance(kwargs.get("unit"), str):
        kwargs.setdefault("unit_tex", kwargs.pop("unit"))
    return _old_cairo_number_mobject(self, *args, **kwargs)


if _CAIRO_ERA:
    NumberLine.get_number_mobject = _cairo_number_mobject


# Cairo Rotating(radians=...) was renamed to angle.
_old_cairo_rotating_init = Rotating.__init__


@_wraps(_old_cairo_rotating_init)
def _cairo_rotating_init(self, *args, **kwargs):
    radians = kwargs.pop("radians", None)
    if radians is not None and len(args) < 2:
        kwargs.setdefault("angle", radians)
    return _old_cairo_rotating_init(self, *args, **kwargs)


if _CAIRO_ERA:
    Rotating.__init__ = _cairo_rotating_init


# Cairo 2019 accepted family instead of recurse in fill and stroke.
for _method_name in ("set_fill", "set_stroke"):
    def _with_family(original):
        @_wraps(original)
        def wrapped(self, *args, family=None, **kwargs):
            if family is not None:
                kwargs.setdefault("recurse", family)
            return original(self, *args, **kwargs)
        return wrapped
    if _CAIRO_ERA:
        setattr(VMobject, _method_name, _with_family(getattr(VMobject, _method_name)))


# DescribeSVG uses cubic controls; GL's are quadratic. This degree elevation preserves each curve
# exactly, it is not just an alias.
def _get_cubic_bezier_tuples(self):
    quadratics = np.asarray(list(self.get_bezier_tuples()))
    if len(quadratics) == 0:
        return np.empty((0, 4, 3))
    a, h, b = quadratics[:, 0], quadratics[:, 1], quadratics[:, 2]
    return np.stack((a, a + (2/3)*(h-a), b + (2/3)*(h-b), b), axis=1)


if not hasattr(VMobject, "get_cubic_bezier_tuples"):
    VMobject.get_cubic_bezier_tuples = _get_cubic_bezier_tuples


# Cairo gradient from an image: stroke sampled per vertex, fill interpolated between the vertical
# extremes. It does not replace global shaders.
def _color_using_background_image(self, filename):
    if filename is None:
        for mob in self.get_family():
            if hasattr(mob, "_cairo_before_background"):
                mob.set_style(**mob._cairo_before_background)
                del mob._cairo_before_background
        self.background_image_file = None
        return self
    from PIL import Image
    from manimlib.utils.images import get_full_raster_image_path
    pixels = np.asarray(Image.open(get_full_raster_image_path(filename)).convert("RGB")) / 255
    height, width = pixels.shape[:2]

    def sample(points):
        if len(points) == 0:
            return np.empty((0, 3))
        xs = np.clip((points[:, 0] / FRAME_WIDTH + 0.5) * (width-1), 0, width-1).astype(int)
        ys = np.clip((0.5 - points[:, 1] / FRAME_HEIGHT) * (height-1), 0, height-1).astype(int)
        return pixels[ys, xs]

    for mob in self.family_members_with_points():
        if not isinstance(mob, VMobject):
            continue
        if not hasattr(mob, "_cairo_before_background"):
            mob._cairo_before_background = dict(stroke_rgba=mob.data["stroke_rgba"].copy(),
                fill_rgba=mob.uniforms["fill_rgba"].copy(), fill_rgba_end=mob.uniforms["fill_rgba_end"].copy())
        colors = [rgb_to_hex(rgb) for rgb in sample(mob.get_points())]
        mob.set_stroke(color=colors, recurse=False)
        endpoints = np.array([mob.get_bottom(), mob.get_top()])
        mob.set_fill(color=[rgb_to_hex(rgb) for rgb in sample(endpoints)], gradient_direction=UP, recurse=False)
    self.background_image_file = filename
    return self


if not hasattr(VMobject, "color_using_background_image"):
    VMobject.color_using_background_image = _color_using_background_image


# Cairo grouped the emphasis rectangle's configuration in a dictionary.
from manimlib.animation.indication import AnimationOnSurroundingRectangle as _RectAnimation
_old_cairo_rect_animation_init = _RectAnimation.__init__


@_wraps(_old_cairo_rect_animation_init)
def _cairo_rect_animation_init(self, *args, surrounding_rectangle_config=None, **kwargs):
    config = dict(surrounding_rectangle_config or {})
    if "color" in config:
        config.setdefault("stroke_color", config.pop("color"))
    for key in ("stroke_color", "stroke_width", "buff"):
        if key in config:
            kwargs.setdefault(key, config.pop(key))
    _old_cairo_rect_animation_init(self, *args, **kwargs)


if _CAIRO_ERA:
    _RectAnimation.__init__ = _cairo_rect_animation_init


# Opt-in for the four Bayes SVG classes: CONFIG does not reach the arguments of the GL constructor.
# It is only called through decorators on 2019 copies.
def cairo_svg_defaults(cls):
    original_init = cls.__init__

    @_wraps(original_init)
    def init(self, *args, **kwargs):
        config = merge_dicts_recursively(*(base.__dict__.get("CONFIG", {}) for base in reversed(type(self).__mro__)))
        for name in ("fill_color", "fill_opacity", "stroke_color", "stroke_width", "stroke_opacity", "color"):
            if name in config and config[name] is not None:
                kwargs.setdefault(name, config[name])
        original_init(self, *args, **kwargs)

    cls.__init__ = init
    return cls


# Opt-in for the Cairo scenes: the original height was 2; GL uses 4. The numpy arrays are
# materialized in a content cache and the pixel API is read-only.
class CairoImageMobject(ImageMobject):
    def __init__(self, filename, height=2.0, **kwargs):
        if isinstance(filename, np.ndarray):
            from hashlib import sha256
            from pathlib import Path
            from PIL import Image
            from manimlib.utils.directories import get_cache_dir

            pixels = np.asarray(filename)
            if np.issubdtype(pixels.dtype, np.floating) and pixels.size and pixels.max() <= 1:
                pixels = pixels * 255
            pixels = np.clip(pixels, 0, 255).astype(np.uint8)
            folder = Path(get_cache_dir()) / "cairo_arrays"
            folder.mkdir(parents=True, exist_ok=True)
            key = sha256(str(pixels.shape).encode() + pixels.tobytes()).hexdigest()
            path = folder / (key + ".png")
            if not path.exists():
                Image.fromarray(pixels).save(path)
            filename = str(path)
        super().__init__(filename, height=height, **kwargs)

    @property
    def pixel_array(self):
        return np.asarray(self.image.convert("RGBA"))

    def get_pixel_array(self):
        return self.pixel_array


# Cairo surfaces were groups of VMobject faces, indexable and animatable with DrawBorderThenFill.
# Adaptation of manim sep19 (3b1b) to ManimGL polygons. They are opt-in by alias in the 2019 copies,
# without changing GL's Surface/Sphere/Cube.
class CairoParametricSurface(VGroup):
    def __init__(self, func, u_min=0, u_max=1, v_min=0, v_max=1, resolution=(32, 32),
                 u_range=None, v_range=None, fill_color=BLUE_D, fill_opacity=1,
                 checkerboard_colors=(BLUE_D, BLUE_E), stroke_color=GREY_A,
                 stroke_width=0.5, stroke_opacity=1, surface_piece_config=None,
                 should_make_jagged=False, pre_function_handle_to_anchor_scale_factor=None,
                 **kwargs):
        if u_range is not None:
            u_min, u_max = u_range[:2]
        if v_range is not None:
            v_min, v_max = v_range[:2]
        if np.isscalar(resolution):
            resolution = (int(resolution), int(resolution))
        self.func = func
        self.resolution = tuple(max(1, int(n)) for n in resolution)
        self.u_min, self.u_max, self.v_min, self.v_max = u_min, u_max, v_min, v_max
        super().__init__(**kwargs)
        us = np.linspace(u_min, u_max, self.resolution[0] + 1)
        vs = np.linspace(v_min, v_max, self.resolution[1] + 1)
        grid = [[np.asarray(func(u, v), dtype=float) for v in vs] for u in us]
        faces = []
        for i in range(len(us) - 1):
            for j in range(len(vs) - 1):
                color = checkerboard_colors[(i + j) % len(checkerboard_colors)] if checkerboard_colors else fill_color
                config = dict(fill_color=color, fill_opacity=fill_opacity, stroke_color=stroke_color,
                              stroke_width=stroke_width, stroke_opacity=stroke_opacity)
                config.update(surface_piece_config or {})
                face = Polygon(grid[i][j], grid[i+1][j], grid[i+1][j+1], grid[i][j+1], **config)
                face.u_index, face.v_index = i, j
                face.u1, face.u2, face.v1, face.v2 = us[i], us[i+1], vs[j], vs[j+1]
                face.apply_depth_test()
                faces.append(face)
        self.add(*faces)

    def set_fill_by_checkerboard(self, *colors, opacity=None):
        for face in self:
            face.set_fill(colors[(face.u_index + face.v_index) % len(colors)], opacity)
        return self


class CairoSphere(CairoParametricSurface):
    def __init__(self, radius=1, resolution=(12, 24), **kwargs):
        self.radius = radius
        kwargs.setdefault("u_min", 0.001)
        kwargs.setdefault("u_max", PI - 0.001)
        kwargs.setdefault("v_min", 0)
        kwargs.setdefault("v_max", TAU)
        super().__init__(lambda u, v: radius * np.array([np.cos(v)*np.sin(u), np.sin(v)*np.sin(u), np.cos(u)]),
                         resolution=resolution, **kwargs)


class CairoCube(VGroup):
    def __init__(self, side_length=2, fill_color=BLUE, fill_opacity=0.75, stroke_width=0, **kwargs):
        from manimlib.utils.space_ops import z_to_vector
        super().__init__(**kwargs)
        self.side_length = side_length
        for vector in (IN, OUT, LEFT, RIGHT, UP, DOWN):
            face = Square(side_length=side_length, fill_color=fill_color,
                          fill_opacity=fill_opacity, stroke_width=stroke_width)
            face.flip()
            face.shift(side_length * OUT / 2)
            face.apply_matrix(z_to_vector(vector))
            face.apply_depth_test()
            self.add(face)


# sep19 VectorField: VGroup of individual arrows; the current GL requires a coordinate system and no
# longer allows the API of these scenes.
class CairoVectorField(VGroup):
    def __init__(self, func, delta_x=0.5, delta_y=0.5,
                 x_min=None, x_max=None, y_min=None, y_max=None,
                 min_magnitude=0, max_magnitude=2, colors=(BLUE_E, GREEN, YELLOW, RED),
                 length_func=None, opacity=1, vector_config=None, **kwargs):
        self.func = func
        self.delta_x, self.delta_y = delta_x, delta_y
        self.x_min = np.floor(-FRAME_WIDTH / 2) if x_min is None else x_min
        self.x_max = np.ceil(FRAME_WIDTH / 2) if x_max is None else x_max
        self.y_min = np.floor(-FRAME_HEIGHT / 2) if y_min is None else y_min
        self.y_max = np.ceil(FRAME_HEIGHT / 2) if y_max is None else y_max
        self.min_magnitude, self.max_magnitude = min_magnitude, max_magnitude
        self.colors = list(colors)
        self.length_func = length_func or (lambda norm: 0.45 * sigmoid(norm))
        self.vector_config = dict(vector_config or {})
        super().__init__(**kwargs)
        for x in np.arange(self.x_min, self.x_max + 0.5*delta_x, delta_x):
            for y in np.arange(self.y_min, self.y_max + 0.5*delta_y, delta_y):
                self.add(self.get_vector(np.array([x, y, 0])))
        self.set_opacity(opacity)

    def get_vector(self, point, **kwargs):
        output = np.asarray(self.func(point), dtype=float)
        norm = np.linalg.norm(output)
        if norm > 0:
            output = output * self.length_func(norm) / norm
        config = dict(self.vector_config, **kwargs)
        vector = Vector(output, **config).shift(point)
        value = np.clip((norm - self.min_magnitude) / max(self.max_magnitude - self.min_magnitude, 1e-10), 0, 1)
        index = min(int(value * (len(self.colors)-1)), len(self.colors)-2)
        color = self.colors[0] if len(self.colors) == 1 else interpolate_color(self.colors[index], self.colors[index+1], value*(len(self.colors)-1)-index)
        vector.set_color(color)
        return vector


# Opt-in for the files that call the Cairo signature smooth(t, inflection).
_normal_smooth = smooth
_normal_rush_into = rush_into


def cairo_smooth(t, inflection=None):
    if inflection is None:
        return _normal_smooth(t)
    error = sigmoid(-inflection / 2)
    return np.clip((sigmoid(inflection * (t - 0.5)) - error) / (1 - 2*error), 0, 1)


def cairo_rush_into(t, inflection=None):
    if inflection is None:
        return _normal_rush_into(t)
    return 2 * cairo_smooth(t / 2, inflection)


# Cairo 2019 (pendulum/clacks): utilities removed from the public import.
from manimlib.utils.directories import get_sound_dir as _get_sound_dir

SOUND_DIR = _get_sound_dir()


def rotate(points, angle=PI, axis=OUT):
    if axis is None:
        return np.asarray(points)
    return np.dot(points, rotation_matrix(angle, axis).T)


# Cairo sep19 vector_field.py: several passes with decreasing stroke and window.
class ShowPassingFlashWithThinningStrokeWidth(AnimationGroup):
    def __init__(self, vmobject, n_segments=10, time_width=0.1, **kwargs):
        kwargs.setdefault("remover", True)
        widths = np.linspace(0, vmobject.get_stroke_width(), n_segments)
        windows = np.linspace(time_width, 0, n_segments)
        super().__init__(*(
            ShowPassingFlash(vmobject.copy().set_stroke(width=width), time_width=window, **kwargs)
            for width, window in zip(widths, windows)
        ))


# Cairo 3feb RabbitFoxEquation: the decimal changes continuously through an updater.
class ContinualChangingDecimal(Mobject):
    def __init__(self, decimal_mobject, number_update_func, position_update_func=None, **kwargs):
        kwargs.pop("start_up_time", None)
        kwargs.pop("wind_down_time", None)
        super().__init__(**kwargs)
        self.mobject = decimal_mobject
        self.internal_time = 0.0
        self.add(decimal_mobject)

        def update_decimal(container, dt):
            container.internal_time += dt
            decimal_mobject.set_value(number_update_func(container.internal_time))
            if position_update_func is not None:
                position_update_func(decimal_mobject)

        self.add_updater(update_decimal)


# FourierOfHilbert: the old fractals port is not imported in GL. Mathematical construction of
# Hilbert in a single VMobject; it depends neither on an SVG nor on the renderer.
class CairoHilbertCurve(VMobject):
    def __init__(self, order=5, radius=3, **kwargs):
        if not isinstance(order, int) or order < 0:
            raise ValueError("order must be a non-negative integer")
        super().__init__(**kwargs)
        self.order = order
        size = 2 ** order
        points = []
        for distance in range(size * size):
            x = y = 0
            t = distance
            scale = 1
            while scale < size:
                rx = (t // 2) & 1
                ry = (t ^ rx) & 1
                if ry == 0:
                    if rx:
                        x, y = scale - 1 - x, scale - 1 - y
                    x, y = y, x
                x += scale * rx
                y += scale * ry
                t //= 4
                scale *= 2
            points.append([x, y, 0])
        points = np.asarray(points, dtype=float)
        if size > 1:
            points[:, :2] = radius * (2 * points[:, :2] / (size - 1) - 1)
        if len(points) == 1:
            points = np.repeat(points, 2, axis=0)
        self.set_points_as_corners(points)


# CL19-CL1: NumberPlane(x_line_frequency=, y_line_frequency=) from Cairo (diffyq/part1 phase_space...). In Cairo
# the spacing of the background lines was independent of the spacing of the axis ticks (and, because of a Cairo
# quirk, x_line_frequency set the spacing of the lines parallel to the x axis, that is, the horizontal ones). GL
# takes them from the step of x_range/y_range, so they are stored separately and get_lines_parallel_to_axis uses
# them.
_cl19_old_plane_init = NumberPlane.__init__
_cl19_old_plane_lines = NumberPlane.get_lines_parallel_to_axis


@_wraps(_cl19_old_plane_init)
def _cl19_plane_init(self, *args, x_line_frequency=None, y_line_frequency=None, **kwargs):
    self._cairo_line_freq = {"x": x_line_frequency, "y": y_line_frequency}
    _cl19_old_plane_init(self, *args, **kwargs)


@_wraps(_cl19_old_plane_lines)
def _cl19_plane_lines(self, axis1, axis2, *args, **kwargs):
    freqs = getattr(self, "_cairo_line_freq", None) or {}
    freq = freqs.get("x" if axis1 is self.get_x_axis() else "y")
    if freq is None:
        return _cl19_old_plane_lines(self, axis1, axis2, *args, **kwargs)
    line = Line(axis1.get_start(), axis1.get_end())
    ratio = self.faded_line_ratio
    step = freq / (1 + ratio)
    lines1 = VGroup()
    lines2 = VGroup()
    for inputs in (np.arange(0, axis2.x_max + 1e-8, step), np.arange(0, axis2.x_min - 1e-8, -step)):
        for k, x in enumerate(inputs):
            if abs(x) < 1e-8:
                continue
            new_line = line.copy()
            new_line.shift(axis2.n2p(x) - axis2.n2p(0))
            (lines1 if k % (1 + ratio) == 0 else lines2).add(new_line)
    return lines1, lines2


if _CAIRO_ERA:
    NumberPlane.__init__ = _cl19_plane_init
    NumberPlane.get_lines_parallel_to_axis = _cl19_plane_lines


# CL19-CL1: FadeInFromPoint(mob, other_mobject) / FadeOutToPoint(mob, other_mobject). Cairo did move_to(point)
# and accepted a mobject as the "point"; GL subtracts point from get_center() and fails with "operands could not
# be broadcast".
_cl19_old_fade_in_from_point = FadeInFromPoint.__init__
_cl19_old_fade_out_to_point = FadeOutToPoint.__init__


@_wraps(_cl19_old_fade_in_from_point)
def _cl19_fade_in_from_point(self, mobject, point, *args, **kwargs):
    if isinstance(point, Mobject):
        point = point.get_center()
    _cl19_old_fade_in_from_point(self, mobject, point, *args, **kwargs)


@_wraps(_cl19_old_fade_out_to_point)
def _cl19_fade_out_to_point(self, mobject, point, *args, **kwargs):
    if isinstance(point, Mobject):
        point = point.get_center()
    _cl19_old_fade_out_to_point(self, mobject, point, *args, **kwargs)


if _CAIRO_ERA:
    FadeInFromPoint.__init__ = _cl19_fade_in_from_point
    FadeOutToPoint.__init__ = _cl19_fade_out_to_point


# CL19-CL1: Axes(center_point=...) from Cairo (position of the origin; diffyq/part1/staging SimpleProjectileEquation).
_cl19_old_axes_init = Axes.__init__


@_wraps(_cl19_old_axes_init)
def _cl19_axes_init(self, *args, center_point=None, **kwargs):
    _cl19_old_axes_init(self, *args, **kwargs)
    if center_point is not None:
        # In Cairo the origin of the axes ends up at center_point (GL centers the box of the axes)
        self.shift(np.array(center_point) - self.get_origin())


if _CAIRO_ERA:
    Axes.__init__ = _cl19_axes_init


# CL19-CL1: Cairo Matrix (include_background_rectangle, add_background_rectangles_to_entries, element_to_mobject,
# element_to_mobject_config and the default spacings v_buff=0.8 / h_buff=1.3 used by the 2019 Matrix and earlier).
# The old spacings only apply to 2019 scenes or earlier, so as not to change 2020.
from manimlib.mobject.matrix import Matrix as _ClMatrix

_cl19_old_matrix_init = _ClMatrix.__init__
_CL19_OLD_PATH = _re.compile(r"/_?(201[0-9])/")


def _cl19_is_2019_caller(depth=2):
    try:
        frame = _sys._getframe(depth)
    except ValueError:
        return False
    while frame is not None:
        filename = frame.f_code.co_filename.replace("\\", "/")
        if "/manimlib/" not in filename and "/_lib/" not in filename:
            return bool(_CL19_OLD_PATH.search(filename))
        frame = frame.f_back
    return False


@_wraps(_cl19_old_matrix_init)
def _cl19_matrix_init(self, matrix, *args, include_background_rectangle=False,
                      add_background_rectangles_to_entries=False, element_to_mobject=None,
                      element_to_mobject_config=None, **kwargs):
    if element_to_mobject_config is not None:
        kwargs.setdefault("element_config", element_to_mobject_config)
    legacy_2019 = _cl19_is_2019_caller()
    if element_to_mobject is not None:
        self.element_to_mobject = lambda element, **config: (
            element if isinstance(element, Mobject) else element_to_mobject(str(element), **config))
    elif legacy_2019 and type(self).element_to_mobject is _ClMatrix.element_to_mobject:
        # The elements were TexMobject (OldTex: e[-1][-2] is a glyph), not GL's new Tex. Only in the base Matrix:
        # IntegerMatrix/DecimalMatrix/MobjectMatrix bring their own (spirals PrimesAndPi uses get_value)
        self.element_to_mobject = lambda element, **config: (
            element if isinstance(element, Mobject) else OldTex(str(element), **config))
    if legacy_2019:
        # In Cairo v_buff/h_buff were the distance between the centers of the rows/columns (0.8 and 1.3 by
        # default); in GL they are the gap between elements (the maximum height/width is added)
        if not args:
            kwargs.setdefault("v_buff", 0.8)
            kwargs.setdefault("h_buff", 1.3)

        def create_mobject_matrix(rows, v_pitch, h_pitch, aligned_corner, **element_config):
            mob_matrix = [[self.element_to_mobject(element, **element_config) for element in row] for row in rows]
            for i, row in enumerate(mob_matrix):
                for j, elem in enumerate(row):
                    elem.move_to(i * v_pitch * DOWN + j * h_pitch * RIGHT, aligned_corner)
            return mob_matrix
        self.create_mobject_matrix = create_mobject_matrix
    _cl19_old_matrix_init(self, matrix, *args, **kwargs)
    if add_background_rectangles_to_entries:
        self.add_background_to_entries()
    if include_background_rectangle:
        self.add_background_rectangle()


if _CAIRO_ERA:
    _ClMatrix.__init__ = _cl19_matrix_init


# CL19-CL2: Axes(stroke_width=...) in Cairo's axes_config (diffyq/part3 discrete_case). Axes was a VGroup and
# the kwarg was stored in the empty VGroup without affecting the axes; GL's CoordinateSystem rejects it with
# TypeError.
_cl2_old_axes_init = Axes.__init__


@_wraps(_cl2_old_axes_init)
def _cl2_axes_init(self, *args, stroke_width=None, **kwargs):
    _cl2_old_axes_init(self, *args, **kwargs)


if _CAIRO_ERA:
    Axes.__init__ = _cl2_axes_init


# CL19-CL2: GL's Mobject.fade(...) does not return self (only VMobject.fade does), so `image.copy().fade(1).shift(...)` gives
# "NoneType has no attribute shift" with ImageMobject/Group (clacks IntroducePreviousTwoVideos).
_cl2_old_mobject_fade = Mobject.fade


@_wraps(_cl2_old_mobject_fade)
def _cl2_mobject_fade(self, *args, **kwargs):
    result = _cl2_old_mobject_fade(self, *args, **kwargs)
    return self if result is None else result


if _CAIRO_ERA:
    Mobject.fade = _cl2_mobject_fade


# CL19-CL1: ApplyMethod(m.restore) (e.g. LaggedStartMap(ApplyMethod, group, lambda m: (m.restore,))). Cairo
# restored the saved state; in GL the copy that ApplyMethod uses does not keep saved_state and raises "Trying
# to restore without having saved". (self.play(m.restore) is already handled by manim_imports_ext.)
_cl19_old_apply_method_target = ApplyMethod.create_target


@_wraps(_cl19_old_apply_method_target)
def _cl19_apply_method_target(self):
    method = self.method
    if (getattr(method, "__func__", None) is Mobject.restore
            and getattr(method.__self__, "saved_state", None) is not None):
        return method.__self__.saved_state.copy()
    return _cl19_old_apply_method_target(self)


if _CAIRO_ERA:
    ApplyMethod.create_target = _cl19_apply_method_target


# CL19-CL1: CubicBezier([x, y, 0], [..], [..], [..]) with lists (Cairo accepted them; GL subtracts
# vectors and fails with "unsupported operand type(s) for -: 'list' and 'list'").
_cl19_old_cubic_bezier_init = CubicBezier.__init__


@_wraps(_cl19_old_cubic_bezier_init)
def _cl19_cubic_bezier_init(self, *points, **kwargs):
    points = [np.array(p, dtype=float) if isinstance(p, (list, tuple)) else p for p in points]
    _cl19_old_cubic_bezier_init(self, *points, **kwargs)


if _CAIRO_ERA:
    CubicBezier.__init__ = _cl19_cubic_bezier_init


# CL19-CL2: Cairo's VMobject.append_points(other.get_points()). GL points are quadratic (2n+1, odd) and append_points
# requires an even number (AssertionError). An odd array is a complete subpath: it is added with add_subpath.
_cl2_old_append_points = VMobject.append_points


@_wraps(_cl2_old_append_points)
def _cl2_append_points(self, points, *args, **kwargs):
    if len(points) % 2 == 1:
        return self.add_subpath(points)
    return _cl2_old_append_points(self, points, *args, **kwargs)


if _CAIRO_ERA:
    VMobject.append_points = _cl2_append_points


# CL19-CL1: The 2019 TauCreature (diffyq LoveExample) had .eyes/.body/.mouth; in GL its init_structure is `pass`.
# The installed Tau SVG contains, in order: 2 eyes (white), 2 pupils, body, mouth and 2 anchors.
if _CAIRO_ERA:
    from custom.characters.pi_creature import TauCreature as _ClOriginalTauCreature

    class TauCreature(_ClOriginalTauCreature):
        def init_structure(self):
            parts = self.submobjects
            eyes = VGroup()
            for iris, pupil in ((parts[0], parts[2]), (parts[1], parts[3])):
                eye = VGroup(iris, pupil)
                eye.iris = iris
                eye.pupil = pupil
                eyes.add(eye)
            self.eyes = eyes
            self.body = parts[4]
            self.mouth = parts[5]
            self.set_submobjects([self.eyes, self.body, self.mouth])

    __all__.append("TauCreature")


# CL19-CL1: OldTexText("Essence of", "Calculus") in diffyq (April-July 2019). Until mid-2019 TextMobject joined its
# arguments with " " (like TexMobject); since Sep19 it uses "" and the later files (moduli, windmill, bayes,
# spirals) write the spaces by hand. GL's OldTexText always sets arg_separator="", so the legacy_2020 shim (which
# only acts when the kwarg is missing) does not reach it. Here " " is restored for the diffyq code; the rest of 2019
# keeps "".
_CL19_SPACED_TEXT_PATH = _re.compile(r"/_?2019/(diffyq|clacks)/")   # CL19-CL2: clacks (January 2019, 3feb) also used " "
_cl19_old_old_tex_text_init = OldTexText.__init__


def _cl19_caller_path(depth=2):
    try:
        frame = _sys._getframe(depth)
    except ValueError:
        return ""
    while frame is not None:
        filename = frame.f_code.co_filename.replace("\\", "/")
        if "/manimlib/" not in filename and "/_lib/" not in filename:
            return filename
        frame = frame.f_back
    return ""


@_wraps(_cl19_old_old_tex_text_init)
def _cl19_old_tex_text_init(self, *tex_strings, arg_separator=None, **kwargs):
    if arg_separator is None:
        arg_separator = " " if _CL19_SPACED_TEXT_PATH.search(_cl19_caller_path()) else ""
    _cl19_old_old_tex_text_init(self, *tex_strings, arg_separator=arg_separator, **kwargs)


if _CAIRO_ERA:
    OldTexText.__init__ = _cl19_old_tex_text_init


# CL19-CL2: Cairo's ThreeDScene.remove_fixed_in_frame_mobjects(*mobs) (diffyq/part3 temperature_graphs). It only removed
# the mobjects from the camera's list of "fixed in frame" ones (they stayed in the scene); in GL it is equivalent to
# unfix_from_frame().
if not hasattr(ThreeDScene, "remove_fixed_in_frame_mobjects"):
    def _remove_fixed_in_frame_mobjects(self, *mobjects):
        for mob in mobjects:
            mob.unfix_from_frame()
        return self

    ThreeDScene.remove_fixed_in_frame_mobjects = _remove_fixed_in_frame_mobjects


# CL19-CL2: Cairo's NumberLine.get_number_mobjects(*numbers, **config) (diffyq/part4: y_axis.get_number_mobjects(*np.arange(...), unit=...)):
# it returned a VGroup with one DecimalNumber per value. GL only has get_number_mobject (a single one) and add_numbers.
if not hasattr(NumberLine, "get_number_mobjects"):
    def _get_number_mobjects(self, *numbers, **kwargs):
        if len(numbers) == 0:
            numbers = self.get_tick_range()
        return VGroup(*[self.get_number_mobject(number, **kwargs) for number in numbers])

    NumberLine.get_number_mobjects = _get_number_mobjects


# CL19-CL1: Cairo's camera_config with keys that GL's Camera does not have (shading_factor, should_apply_shading,
# exponential_projection, use_z_coordinate_for_display_order, max_allowable_norm, ...): GL would raise TypeError.
# light_source_start_point and frame_rate are translated; the rest are discarded (GL's lighting is different).
from manimlib.camera.camera import Camera as _ClCamera

_cl19_old_camera_init = _ClCamera.__init__
_cl19_camera_params = frozenset(_inspect.signature(_cl19_old_camera_init).parameters)


@_wraps(_cl19_old_camera_init)
def _cl19_camera_init(self, *args, **kwargs):
    if "light_source_start_point" in kwargs:
        kwargs.setdefault("light_source_position", kwargs.pop("light_source_start_point"))
    if "frame_rate" in kwargs:
        kwargs.setdefault("fps", kwargs.pop("frame_rate"))
    for key in [k for k in kwargs if k not in _cl19_camera_params]:
        del kwargs[key]
    _cl19_old_camera_init(self, *args, **kwargs)


if _CAIRO_ERA:
    _ClCamera.__init__ = _cl19_camera_init


# CL19-CL1: `mob.submobjects = [...]` and `mob.submobjects.insert/append/remove(...)` (direct mutation, very common
# in Cairo: `y_axis_copy.submobjects = []`, `answer.submobjects.insert(4, VectorizedPoint(..))`). In GL the
# `family` list is cached and, if it does not go through add/remove, it gets out of sync: copy() fails with
# "IndexError: list index out of range" and transformations align badly ("could not broadcast ..."); the parents
# are not registered either. `submobjects` becomes a list that, when modified by code that is not part of manimlib,
# registers the parents and invalidates the family cache. Reading is still the normal attribute (the descriptor
# only defines __set__).
def _cl19_external(depth):
    try:
        return "/manimlib/" not in _sys._getframe(depth).f_code.co_filename.replace("\\", "/")
    except ValueError:
        return False


def _cl19_family_changed(owner, items):
    data = owner.__dict__
    if "family" not in data or "parents" not in data:
        return
    for submobject in items:
        if owner not in submobject.parents:
            submobject.parents.append(owner)
    owner.note_changed_family()


class _Cl19SubList(list):
    _owner = None

    def _touched(self):
        if self._owner is not None and _cl19_external(3):
            _cl19_family_changed(self._owner, self)


def _cl19_wrap_list_method(name):
    original = getattr(list, name)

    def method(self, *args, **kwargs):
        result = original(self, *args, **kwargs)
        self._touched()
        return result
    method.__name__ = name
    return method


for _name in ("append", "extend", "insert", "remove", "pop", "clear", "sort", "reverse",
              "__setitem__", "__delitem__", "__iadd__", "__imul__"):
    setattr(_Cl19SubList, _name, _cl19_wrap_list_method(_name))


class _Cl19SubmobjectsAssign:
    def __set__(self, obj, value):
        wrapped = _Cl19SubList(value)
        wrapped._owner = obj
        obj.__dict__["submobjects"] = wrapped
        if _cl19_external(2):
            _cl19_family_changed(obj, wrapped)


if _CAIRO_ERA:
    Mobject.submobjects = _Cl19SubmobjectsAssign()


# CL19-CL1: Cairo's StreamLines / AnimatedStreamLines (Sep19), used by diffyq/part1 (phase_space, staging) and part2.
# StreamLines(func, delta_x=.., start_points_generator_config={..}, virtual_time=..): func(point) -> vector, without
# coordinate_system (GL's version requires a different, vectorized func and a coordinate system). They are exported
# under the old name only in _CAIRO_ERA (in 2021+ the manimgl ones apply).
if _CAIRO_ERA:
    def _cl_rgb_gradient(min_value=0, max_value=1, colors=(BLUE, RED)):
        # Cairo's get_rgb_gradient_function (current manimgl uses a different signature)
        rgbs = np.array([color_to_rgb(c) for c in colors])

        def func(values):
            alphas = np.clip(inverse_interpolate(min_value, max_value, np.array(values)), 0, 1)
            scaled_alphas = alphas * (len(rgbs) - 1)
            indices = scaled_alphas.astype(int)
            next_indices = np.clip(indices + 1, 0, len(rgbs) - 1)
            inter_alphas = (scaled_alphas % 1).repeat(3).reshape((len(indices), 3))
            return interpolate(rgbs[indices], rgbs[next_indices], inter_alphas)
        return func

    class StreamLines(VGroup):
        _cairo_config = dict(
            x_min=-8, x_max=8, y_min=-5, y_max=5, delta_x=0.5, delta_y=0.5, n_repeats=1, noise_factor=None,
            dt=0.05, virtual_time=3, n_anchors_per_line=100, stroke_width=1, stroke_color=WHITE,
            color_by_arc_length=True, min_arc_length=0, max_arc_length=12, color_by_magnitude=False,
            min_magnitude=0.5, max_magnitude=1.5, colors=[BLUE_E, GREEN, YELLOW, RED], cutoff_norm=15,
        )

        def __init__(self, func, start_points_generator_config=None, **kwargs):
            super().__init__()
            config = dict(self._cairo_config)
            config.update(start_points_generator_config or {})
            config.update(kwargs)
            for key, value in config.items():
                setattr(self, key, value)
            self.func = func
            for point in self.get_start_points():
                points = [point]
                for t in np.arange(0, self.virtual_time, self.dt):
                    last_point = points[-1]
                    points.append(last_point + self.dt * np.array(func(last_point)))
                    if get_norm(last_point) > self.cutoff_norm:
                        break
                line = VMobject()
                step = max(1, int(len(points) / self.n_anchors_per_line))
                line.set_points_smoothly(np.array(points[::step]))
                line.virtual_time = self.virtual_time
                self.add(line)
            self.set_stroke(self.stroke_color, self.stroke_width)
            if self.color_by_arc_length:
                len_to_rgb = _cl_rgb_gradient(self.min_arc_length, self.max_arc_length, colors=self.colors)
                for line in self:
                    line.set_color(rgb_to_color(len_to_rgb([line.get_arc_length()])[0]))
            elif self.color_by_magnitude:
                # Cairo colored with a background image according to the norm of the field at each point
                mag_to_rgb = _cl_rgb_gradient(self.min_magnitude, self.max_magnitude, colors=self.colors)
                for line in self:
                    anchors = line.get_anchors()
                    rgbs = mag_to_rgb([get_norm(func(p)) for p in anchors])
                    line.set_stroke(color=[rgb_to_color(rgb) for rgb in rgbs])

        def get_start_points(self):
            noise_factor = self.noise_factor
            if noise_factor is None:
                noise_factor = self.delta_y / 2
            return np.array([
                x * RIGHT + y * UP + noise_factor * np.random.random(3)
                for n in range(self.n_repeats)
                for x in np.arange(self.x_min, self.x_max + self.delta_x, self.delta_x)
                for y in np.arange(self.y_min, self.y_max + self.delta_y, self.delta_y)
            ])

    class AnimatedStreamLines(VGroup):
        def __init__(self, stream_lines, lag_range=4, line_anim_class=ShowPassingFlash, line_anim_config=None,
                     **kwargs):
            super().__init__(**kwargs)
            config = dict(run_time=4, rate_func=linear, time_width=0.3)
            config.update(line_anim_config or {})
            self.stream_lines = stream_lines
            for line in stream_lines:
                line.anim = line_anim_class(line, **config)
                line.anim.begin()
                line.time = -lag_range * np.random.random()
                self.add(line.anim.mobject)
            self.add_updater(lambda m, dt: m._cairo_step(dt))

        def _cairo_step(self, dt):
            for line in self.stream_lines:
                line.time += dt
                adjusted_time = max(line.time, 0) % line.anim.run_time
                line.anim.update(adjusted_time / line.anim.run_time)
            return self

    __all__.extend(["StreamLines", "AnimatedStreamLines"])


# CL19-CL1: attributes of Cairo's ParametricFunction (t_min, t_max, function) on top of GL's ParametricCurve (t_range, t_func).
def _cl19_t_bound(index):
    def getter(self):
        return self.t_range[index]

    def setter(self, value):
        values = list(self.t_range)
        values[index] = value
        self.t_range = tuple(values)
    return property(getter, setter)


if not hasattr(ParametricCurve, "t_min"):
    ParametricCurve.t_min = _cl19_t_bound(0)
    ParametricCurve.t_max = _cl19_t_bound(1)
if not hasattr(ParametricCurve, "function"):
    # FunctionGraph assigns self.function = f(x); in a Cairo ParametricFunction it was the function t -> point
    ParametricCurve.function = property(lambda self: self.__dict__.get("_cl19_function", self.t_func),
                                        lambda self, value: self.__dict__.__setitem__("_cl19_function", value))


# CL19-CL2: ticks and background lines aligned to multiples of the step (2019 scenes only). In Cairo the first tick of a
# NumberLine was `leftmost_tick = step * ceil(x_min / step)` and the NumberPlane lines went from 0 outwards; GL counts them
# from x_min, so with ranges such as (-2.5, 2.5) (diffyq/part4: plane_config y_min=-1.25) everything is shifted by half a
# step and the numbers come out as "0", "0", "0i", "0i". Limited to 2019 so as not to change 2020 (E1 already rendered it).
_CL19_2019 = any(_re.search(r"[/\\]_?2019[/\\]", str(arg)) for arg in _ARGV_PATHS)
# CL18: 2018 scenes only (_work/_2018, <category>/2018). New 2018 patches go under `if _CL18_2018:` so the look of the already
# rendered 2019/2020 does not change. (New classes and functions that wrap nothing existing do not need it.)
_CL18_ONLY_2018 = any(_re.search(r"[/\\]_?2018[/\\]", str(arg)) for arg in _ARGV_PATHS)
# CL17: 2017 scenes (_work/_2017, <category>/2017). 2017 is the same Cairo code base as 2018 (sep19, a few 3feb), so it reuses ALL the
# `_CL18_2018` patches: `_CL18_2018` is True for 2017 AND 2018 (it is False for 2019+, so nothing already rendered changes). A patch that must
# apply to 2018 only goes under `if _CL18_ONLY_2018:`; one that must apply to 2017 only goes under `if _CL17_2017:`. Never widen either to 2019+.
_CL17_2017 = any(_re.search(r"[/\\]_?2017[/\\]", str(arg)) for arg in _ARGV_PATHS)
_CL18_2018 = _CL18_ONLY_2018 or _CL17_2017
# CL18 (closing agent): the two "Cairo semantics" patches for shapes (CL18-B: CONFIG of subclasses of Circle/Rectangle/Line/VMobject...,
# CL18-E: color= of Circle/Dot/Sector/Arrow) were written for 2018 but are not 2018-specific: 2019 (Cairo) and 2020 (early GL) code relies on
# the same behaviour and its renders showed default colours/sizes. `_CL18_GEOM` is True for 2018 and, unless CL18_GEOM_OFF=1 (only used to
# compare before/after), for 2019/2020. CL18_GEOM_PROBE=<file> appends one JSON line per construction the patches actually changed.
_CL18_GEOM = _CL18_2018 or (_CAIRO_ERA and _os.environ.get("CL18_GEOM_OFF") != "1"
                            and any(_re.search(r"[/\\]_?20(19|20)[/\\]", str(arg)) for arg in _ARGV_PATHS))
_CL18_GEOM_PROBE = _os.environ.get("CL18_GEOM_PROBE")
_cl18_geom_probe_seen = set()


def _cl18_geom_probe(kind, cls, key, value, default=None):
    """Debug aid for the 2019/2020 rescan: record (once per process) a construction changed by a CL18 shape patch."""
    if not _CL18_GEOM_PROBE:
        return
    marker = (kind, cls, key)
    if marker in _cl18_geom_probe_seen:
        return
    _cl18_geom_probe_seen.add(marker)
    try:
        import json as _json
        with open(_CL18_GEOM_PROBE, "a") as _f:
            _f.write(_json.dumps({"argv": _sys.argv[1:3], "kind": kind, "cls": cls, "key": key,
                                  "value": repr(value)[:80], "default": repr(default)[:80]}) + "\n")
    except Exception:
        pass
_cl2_old_tick_range = NumberLine.get_tick_range
_cl2_old_plane_lines2 = NumberPlane.get_lines_parallel_to_axis


@_wraps(_cl2_old_tick_range)
def _cl2_tick_range(self):
    step = self.x_step
    first = step * np.ceil(round(self.x_min / step, 9)) if step else self.x_min
    if np.isclose(first, self.x_min):
        return _cl2_old_tick_range(self)
    end = self.x_max if self.include_tip else self.x_max + step
    result = np.arange(first, end, step)
    return result[result <= self.x_max + 1e-8]


@_wraps(_cl2_old_plane_lines2)
def _cl2_plane_lines(self, axis1, axis2, *args, **kwargs):
    freqs = getattr(self, "_cairo_line_freq", None) or {}
    if freqs.get("x" if axis1 is self.get_x_axis() else "y") is not None:
        return _cl2_old_plane_lines2(self, axis1, axis2, *args, **kwargs)    # handled by the CL1 patch
    ratio = self.faded_line_ratio
    step = axis2.x_step / (1 + ratio)
    line = Line(axis1.get_start(), axis1.get_end())
    lines1 = VGroup()
    lines2 = VGroup()
    for inputs in (np.arange(0, axis2.x_max, step), np.arange(0, axis2.x_min, -step)):
        for k, x in enumerate(inputs):
            if abs(x) < 1e-8:
                continue
            new_line = line.copy()
            new_line.shift(axis2.n2p(x) - axis2.n2p(0))
            (lines1 if k % (1 + ratio) == 0 else lines2).add(new_line)
    return lines1, lines2


if _CL19_2019:
    NumberLine.get_tick_range = _cl2_tick_range
    NumberPlane.get_lines_parallel_to_axis = _cl2_plane_lines


# CL19-CL2: Cairo's NumberPlane had faded_line_ratio=1 (one faint line between two main ones); GL uses 4. 2019 only, and only if the
# scene does not pass it: the grids came out with 4 faint lines per unit instead of 1.
_cl2_old_plane_init2 = NumberPlane.__init__


@_wraps(_cl2_old_plane_init2)
def _cl2_plane_init(self, *args, **kwargs):
    kwargs.setdefault("faded_line_ratio", 1)
    _cl2_old_plane_init2(self, *args, **kwargs)


if _CL19_2019:
    NumberPlane.__init__ = _cl2_plane_init


# CL19-CL1: Cairo's ThreeDCamera had camera.phi_tracker / theta_tracker / gamma_tracker / distance_tracker
# (ValueTracker) that were animated with `self.play(self.camera.phi_tracker.set_value, 60 * DEGREES, ...)`. They
# are created on request and a frame updater synchronizes them in both directions: if the tracker changed, it
# applies the angle to the frame (theta_GL = theta_Cairo + 90 degrees, gamma_GL = -gamma_Cairo); otherwise it reads
# the frame (so they coexist with set_camera_orientation, move_camera and ambient rotation).
def _cl19_camera_trackers(self):
    trackers = self.__dict__.get("_cl19_trackers")
    if trackers is not None:
        return trackers
    frame = self.frame
    trackers = self.__dict__["_cl19_trackers"] = dict(
        phi=ValueTracker(frame.get_phi()),
        theta=ValueTracker(frame.get_theta() - PI / 2),
        gamma=ValueTracker(-frame.get_gamma()),
        distance=ValueTracker(frame.get_focal_distance()),
    )
    last = {key: tracker.get_value() for key, tracker in trackers.items()}

    def sync(frame_mob, dt=0):
        values = {key: tracker.get_value() for key, tracker in trackers.items()}
        if any(abs(values[key] - last[key]) > 1e-9 for key in values):
            frame_mob.set_euler_angles(theta=values["theta"] + PI / 2, phi=values["phi"], gamma=-values["gamma"])
            frame_mob.set_focal_distance(values["distance"])
            last.update(values)
        else:
            current = dict(phi=frame_mob.get_phi(), theta=frame_mob.get_theta() - PI / 2,
                           gamma=-frame_mob.get_gamma(), distance=frame_mob.get_focal_distance())
            for key, value in current.items():
                trackers[key].set_value(value)
            last.update(current)
        return frame_mob

    frame.add_updater(sync)
    return trackers


from manimlib.camera.camera import Camera as _ClCameraT

for _name in ("phi", "theta", "gamma", "distance"):
    if not hasattr(_ClCameraT, f"{_name}_tracker"):
        setattr(_ClCameraT, f"{_name}_tracker", property(lambda self, k=_name: _cl19_camera_trackers(self)[k]))


# CL19-CL1: Cairo's Camera.frame_rate (today fps; e.g. `circles.update(-1 / self.camera.frame_rate)`).
if not hasattr(_ClCameraT, "frame_rate"):
    _ClCameraT.frame_rate = property(lambda self: self.fps)


# CL19-CL2: the origin of Axes/ThreeDAxes/NumberPlane/ComplexPlane (2019 scenes only). In Cairo `Axes(x_min=0, x_max=TAU, ...)` left the
# point (0, 0) at `center_point` (ORIGIN by default), because each axis put its 0 at the origin; GL's `Axes.__init__` ends with
# `self.center()` and centers the box of the axes, so with asymmetric ranges the origin is shifted and everything the scene places with
# `axes.shift(...)`, `c2p` or the 3D camera ends up off-center or out of frame (diffyq/part3 temperature_graphs). Here the origin is
# returned to `center_point` (the one from CL1, which shifted the already centered group, has no effect: it is consumed here).
_cl2_old_axes_init3 = Axes.__init__


@_wraps(_cl2_old_axes_init3)
def _cl2_axes_origin_init(self, *args, center_point=None, **kwargs):
    _cl2_old_axes_init3(self, *args, **kwargs)
    target = np.zeros(3) if center_point is None else np.array(center_point, dtype=float)
    shift = target - np.array(self.x_axis.n2p(0))
    if np.abs(shift).max() > 1e-8:
        self.shift(shift)
        log = _os.environ.get("CL19_AXES_LOG")
        if log:
            try:
                with open(log, "a") as fp:
                    fp.write(f"{_sys.argv[1] if len(_sys.argv) > 1 else '?'}\t{type(self).__name__}\t{np.round(shift, 3).tolist()}\n")
            except OSError:
                pass


if _CL19_2019:
    Axes.__init__ = _cl2_axes_origin_init


# CL19-CL2: color_using_background_image in 3D scenes (2019 only). In Cairo the background image ("VerticalTempGradient") was applied
# in SCREEN coordinates, from top (red) to bottom (blue); the shim above samples by the scene's (x, y), which in a 3D graph of
# ThreeDAxes (the curve lies in the x-z plane, with constant y) gives a single color (white). If the figure varies more in z than in y,
# the on-screen height is z: a copy rotated 90 degrees (z -> y) is colored and the colors are copied over.
_cl2_old_color_bg = VMobject.color_using_background_image


@_wraps(_cl2_old_color_bg)
def _cl2_color_bg(self, filename):
    points = self.get_all_points() if filename is not None else None
    if points is None or len(points) == 0 or np.ptp(points[:, 2]) <= np.ptp(points[:, 1]) + 1e-8:
        return _cl2_old_color_bg(self, filename)
    proxy = self.copy()
    proxy.rotate(-90 * DEGREES, RIGHT, about_point=ORIGIN)
    _cl2_old_color_bg(proxy, filename)
    for original, colored in zip(self.family_members_with_points(), proxy.family_members_with_points()):
        if isinstance(original, VMobject):
            original.data["stroke_rgba"][:] = colored.data["stroke_rgba"]
            for key in colored.uniforms:
                if "fill" in key or "gradient" in key:
                    original.uniforms[key] = np.array(colored.uniforms[key]).copy()
    self.background_image_file = filename
    return self


if _CL19_2019:
    VMobject.color_using_background_image = _cl2_color_bg


# CL19-CL2: Cairo's VMobject(background_image_file="VerticalTempGradient") (diffyq: default_graph_style of temperature_graphs, etc.). It painted
# the stroke with that image on screen; in GL the kwarg was stored as an attribute and the curve came out white. 2019 only:
# color_using_background_image is applied when the constructor finishes.
_cl2_old_vmobject_init = VMobject.__init__


@_wraps(_cl2_old_vmobject_init)
def _cl2_vmobject_init(self, *args, background_image_file=None, **kwargs):
    _cl2_old_vmobject_init(self, *args, **kwargs)
    if background_image_file and self.has_points():
        self.color_using_background_image(background_image_file)


if _CL19_2019:
    VMobject.__init__ = _cl2_vmobject_init


# CL19-CL3: DecimalNumber(complex(2, 1), num_decimal_places=0) (diffyq/part4 AskAboutComplexNotVector). In Cairo it gave "2+1i"; GL
# formats the real and imaginary parts (always float in a complex) with "d" and raises "Unknown format code 'd' for object of type
# 'float'". With 0 decimals the parts are rounded to int before formatting (same format as GL's get_num_string).
_cl3_old_get_num_string = DecimalNumber.get_num_string


@_wraps(_cl3_old_get_num_string)
def _cl3_get_num_string(self, number):
    if isinstance(number, complex) and self.num_decimal_places == 0:
        parts = _types.SimpleNamespace(real=int(round(number.real)), imag=int(round(number.imag)))
        if self.hide_zero_components_on_complex and parts.imag == 0:
            text = self.get_formatter().format(parts.real)
        elif self.hide_zero_components_on_complex and parts.real == 0:
            text = (self.get_formatter() + "i").format(parts.imag)
        else:
            text = self.get_complex_formatter().format(parts)
        return text.replace("-", "–")
    return _cl3_old_get_num_string(self, number)


if _CAIRO_ERA:
    DecimalNumber.get_num_string = _cl3_get_num_string


# CL19-CL3: scene inside another scene (clacks/solution2/simple_scenes ClacksSolution2Thumbnail). In Cairo, `Scene(skip_animations=True,
# end_at_animation_number=18, center=ORIGIN)` ran construct() in __init__, accepted the CONFIG values as kwargs and the nested scene stored
# its mobjects in `.mobjects`. In GL __init__ does not build and rejects kwargs that are not its own. This function creates the scene with
# Scene's own kwargs, assigns the rest as attributes (dictionaries are merged with those of CONFIG), calls setup()/construct() without
# writing video and removes the camera frame from `.mobjects`. Usage: scene2 = cairo_nested_scene(Class, center=ORIGIN).
def cairo_nested_scene(scene_class, **kwargs):
    from manimlib.scene.scene import EndScene
    from manimlib.utils.dict_ops import merge_dicts_recursively
    # (Scene.__init__ is wrapped in manim_imports_ext without functools.wraps, so its signature cannot be read)
    init_params = {"window", "camera_config", "file_writer_config", "skip_animations", "always_update_mobjects",
                   "start_at_animation_number", "end_at_animation_number", "show_animation_progress",
                   "leave_progress_bars", "preview_while_skipping", "presenter_mode", "default_wait_time",
                   "invert_zoom_scroll"}
    init_kwargs = {key: kwargs.pop(key) for key in list(kwargs) if key in init_params}
    init_kwargs.setdefault("skip_animations", True)
    init_kwargs["file_writer_config"] = {**init_kwargs.get("file_writer_config", {}), "write_to_movie": False, "save_last_frame": False}
    scene = scene_class(**init_kwargs)
    for key, value in kwargs.items():
        old = getattr(scene, key, None)
        if isinstance(old, dict) and isinstance(value, dict):
            value = merge_dicts_recursively(old, value)
        setattr(scene, key, value)
    scene.virtual_animation_start_time = 0
    scene.real_animation_start_time = 0
    scene.setup()
    try:
        scene.construct()
    except EndScene:
        pass
    scene.mobjects = [mob for mob in scene.mobjects if mob is not scene.camera.frame]
    return scene


__all__.append("cairo_nested_scene")


# CL19-CL3: Cairo's Arc.arc_center (attribute; GL only has get_arc_center()). Clacks solution2: `center = arc.arc_center` in an updater.
if _CAIRO_ERA and not hasattr(Arc, "arc_center"):
    Arc.arc_center = property(lambda self: self.get_arc_center())


# CL19-CL3: anim.update(alpha) without having called begin() (clacks solution2 ClacksSolution2Thumbnail: `for beam in beams: beam.update(0.5)` to
# leave a snapshot of the flashes). In Cairo the Animation already had what it needed since __init__; in GL `families` is built in begin() and
# `update` fails with "'ApplyMethod' object has no attribute 'families'". If the animation has not started, begin() is called first.
if _CAIRO_ERA:
    _cl3_old_animation_update = Animation.update

    @_wraps(_cl3_old_animation_update)
    def _cl3_animation_update(self, alpha):
        if not hasattr(self, "families"):
            self.begin()
        return _cl3_old_animation_update(self, alpha)

    Animation.update = _cl3_animation_update


# CL19-CL1: Cairo's ThreeDScene (2019) started with the camera at phi=0, theta=-90 degrees (view from above, the z=0 plane at
# 2D scale); GL starts at (-30, 70) and a flat scene that does not call set_camera_orientation (diffyq/part2
# TwoDBodyWithManyTemperatures: plate, arrow and text in 2D) comes out tilted and cut off at the edges. 2019 only (2020 uses
# the ThreeDScene of the GL of that time, already rendered by E1/E2); SpecialThreeDScene already started at (0, 0).
if _CL19_2019:
    ThreeDScene.default_frame_orientation = (0, 0)


# CL19-CL1: GL's camera frame (self.camera.frame) is the first mobject of the scene. That broke Cairo code in two ways
# (diffyq/part2 heat_equation: ContrastXChangesToTChanges, TransitionToTempVsTime, ShowDelTermsAsTinyNudges): 1)
# `Group(*self.get_mobjects())` and `for m in self.get_mobjects(): m.clear_updaters()` included the camera: when "rotating
# everything on screen" (orient_mobject_for_3d) the camera was rotated too (the view came out wrong) and its updaters were erased
# (the angle trackers and the ambient rotation). get_mobjects() no longer returns it. 2) `self.clear()` removed the frame from
# the list, and its updaters stopped running; now it is kept. And `self.camera.frame_center` was the frame itself, so
# `move_camera(..., added_anims=[self.camera.frame_center.move_to, p])` or `self.play(theta_tracker.set_value, a,
# self.camera.frame_center.shift, v)` animated the whole frame twice (the order of the animations erased the rotation and the
# frame's updaters were suspended). In Cairo it was a separate point: here it is a Point that pushes its position to the frame
# every time it moves or interpolates, and reads the frame's position on every frame. 2019 only (_CL19_2019): 2020 is the GL of
# that time and is already rendered.
if _CL19_2019:
    from manimlib.scene.scene import Scene as _ClScene

    _cl19_old_get_mobjects = _ClScene.get_mobjects
    _cl19_old_scene_clear = _ClScene.clear

    @_wraps(_cl19_old_get_mobjects)
    def _cl19_get_mobjects(self):
        return [m for m in _cl19_old_get_mobjects(self) if m is not self.camera.frame]

    @_wraps(_cl19_old_scene_clear)
    def _cl19_scene_clear(self, *args, **kwargs):
        result = _cl19_old_scene_clear(self, *args, **kwargs)
        if self.camera.frame not in self.mobjects:
            self.mobjects.insert(0, self.camera.frame)
        return result

    _ClScene.get_mobjects = _cl19_get_mobjects
    _ClScene.clear = _cl19_scene_clear

    class _ClFrameCenter(Point):
        """Point representing the center of the camera frame (Cairo's camera.frame_center)."""

        def _is_live(self):
            frame = self.__dict__.get("_cl19_frame")
            return frame is not None and frame.__dict__.get("_cl19_center_proxy") is self

        def _push(self):
            if self._is_live():
                self._cl19_frame.move_to(self.get_location())
            return self

        def _pull(self):
            if self._is_live():
                self.set_location(self._cl19_frame.get_center())
            return self

        def shift(self, *vectors):
            super().shift(*vectors)
            return self._push()

        def move_to(self, *args, **kwargs):
            super().move_to(*args, **kwargs)
            return self._push()

        def interpolate(self, *args, **kwargs):
            super().interpolate(*args, **kwargs)
            return self._push()

        def update(self, dt=0, recurse=True, frame_rate=None):
            # Called by the frame updater; if it is also in the scene (an animation adds it), it only runs once per frame
            if self._is_live():
                if self._cl19_last_tick == self._cl19_tick:
                    return self
                self._cl19_last_tick = self._cl19_tick
            return super().update(dt, recurse, frame_rate)

    def _cl19_frame_center(self):
        frame = self.frame
        proxy = frame.__dict__.get("_cl19_center_proxy")
        if proxy is None:
            proxy = _ClFrameCenter(frame.get_center())
            proxy._cl19_frame = frame
            proxy._cl19_tick = 0
            proxy._cl19_last_tick = -1
            frame.__dict__["_cl19_center_proxy"] = proxy

            def drive(frame_mob, dt=0, *args):
                proxy._pull()
                proxy._cl19_tick += 1
                proxy.update(dt)
                return frame_mob

            frame.add_updater(drive)
        else:
            proxy._pull()
        return proxy

    _ClCameraT.frame_center = property(_cl19_frame_center)


# CL18-C: kwargs and attributes of the Cairo-era NumberPlane/ComplexPlane (2018 only, scenes of fourier, div_curl, pi_day).
# 3feb NumberPlane took x_radius/y_radius (extent of the plane in coordinate units, each side of the origin), x_unit_size/y_unit_size
# (scene units per coordinate unit), center_point, secondary_line_ratio; ComplexPlane took unit_size. ManimGL has none of them
# (TypeError / AttributeError). Mapped onto x_range/y_range + x_axis_config["unit_size"]; the old values are readable afterwards.
_cl18c_old_plane_init = NumberPlane.__init__


@_wraps(_cl18c_old_plane_init)
def _cl18c_plane_init(self, *args, x_radius=None, y_radius=None, x_unit_size=None, y_unit_size=None, unit_size=None,
                      center_point=None, secondary_line_ratio=None, color=None, secondary_color=None, axes_color=None,
                      secondary_stroke_width=None, stroke_width=None, stroke_opacity=None, written_coordinate_height=None,
                      propagate_style_to_family=None, **kwargs):
    uni = 1.0 if unit_size is None else unit_size
    ux = uni if x_unit_size is None else x_unit_size
    uy = uni if y_unit_size is None else y_unit_size
    cx, cy = (0.0, 0.0) if center_point is None else (float(center_point[0]), float(center_point[1]))
    if len(args) < 1 and "x_range" not in kwargs:
        rx = (FRAME_X_RADIUS + abs(cx)) / ux if x_radius is None else x_radius
        kwargs["x_range"] = (-rx, rx, 1)
    if len(args) < 2 and "y_range" not in kwargs:
        ry = (FRAME_Y_RADIUS + abs(cy)) / uy if y_radius is None else y_radius
        kwargs["y_range"] = (-ry, ry, 1)
    for axis, size in (("x", ux), ("y", uy)):
        cfg = dict(kwargs.get(f"{axis}_axis_config", {}))
        cfg.setdefault("unit_size", size)
        kwargs[f"{axis}_axis_config"] = cfg
    kwargs["faded_line_ratio"] = kwargs.get("faded_line_ratio", 1) if secondary_line_ratio is None else secondary_line_ratio
    # colors/widths of the 3feb NumberPlane: main lines, faded lines, axes
    for key, value, style in (("background_line_style", color, "stroke_color"), ("background_line_style", stroke_width, "stroke_width"), ("background_line_style", stroke_opacity, "stroke_opacity"),
                              ("faded_line_style", secondary_color, "stroke_color"),
                              ("faded_line_style", secondary_stroke_width, "stroke_width")):
        if value is not None:
            base = kwargs.get(key) or ({"stroke_width": 1, "stroke_opacity": 0.5} if key == "faded_line_style" else {})
            kwargs[key] = {**base, style: value} if style not in base else base
    if axes_color is not None:
        kwargs["axis_config"] = {"stroke_color": axes_color, **kwargs.get("axis_config", {})}
    _cl18c_old_plane_init(self, *args, **kwargs)
    if center_point is not None and (cx or cy):
        self.shift(np.array([cx, cy, 0.0]) - np.array(self.get_x_axis().n2p(0)))


if _CAIRO_ERA and _CL18_2018:
    NumberPlane.__init__ = _cl18c_plane_init
    for _name, _getter in (
        ("x_unit_size", lambda self: self.x_axis.get_unit_size()),
        ("y_unit_size", lambda self: self.y_axis.get_unit_size()),
        ("unit_size", lambda self: self.x_axis.get_unit_size()),
        ("x_radius", lambda self: (self.x_range[1] - self.x_range[0]) / 2),
        ("y_radius", lambda self: (self.y_range[1] - self.y_range[0]) / 2),
    ):
        if not hasattr(Axes, _name):
            setattr(Axes, _name, property(_getter))


# CL18-D: the ContinualAnimation family of manim_3feb (manimlib/continual_animation/*). sep19 removed it in favour of
# updaters, GL never had it. Port: the continual animation is a plain object that drives its mobject through a GL updater
# that is attached when the scene adds it (`scene.add(ca)`) and detached on `scene.remove(ca)` / `scene.clear()`.
# Same semantics as 3feb: start_up_time / wind_down_time scale dt, `ca.mobject` is the managed mobject, `update_mobject(dt)`
# is the hook of subclasses. Scene.add/remove/clear/wind_down are extended under `_CL18_2018` (2019/2020 never use them).
def _cl18_instantiate(item):
    return item() if isinstance(item, type) else item


class ContinualAnimation(object):
    CONFIG = {
        "start_up_time": 1,
        "wind_down_time": 1,
        "end_time": np.inf,
    }

    def __init__(self, mobject, **kwargs):
        mobject = _cl18_instantiate(mobject)
        assert isinstance(mobject, Mobject)
        digest_config(self, kwargs, locals())
        self.internal_time = 0
        self.external_time = 0
        self._cl18_driver = None
        self.setup()
        self.update(0)

    def setup(self):
        # To implement in subclass
        pass

    def begin_wind_down(self, wind_down_time=None):
        if wind_down_time is not None:
            self.wind_down_time = wind_down_time
        self.end_time = self.external_time + self.wind_down_time

    def update(self, dt):
        # Time runs slower during start up / wind down (as in 3feb)
        self.external_time += dt
        if self.external_time < self.start_up_time:
            dt *= float(self.external_time) / self.start_up_time
        elif self.external_time > self.end_time - self.wind_down_time:
            dt *= np.clip(
                float(self.end_time - self.external_time) / max(self.wind_down_time, 1e-9), 0, 1
            )
        self.internal_time += dt
        self.update_mobject(dt)

    def update_mobject(self, dt):
        # To implement in subclass
        pass

    def copy(self):
        import copy as _copy
        return _copy.deepcopy(self)

    # GL glue: the scene attaches/detaches the driver
    def _cl18_attach(self):
        if self._cl18_driver is not None:
            return

        def driver(mob, dt=0):
            self.update(dt)
        self._cl18_driver = driver
        self.mobject.add_updater(driver, call=False)

    def _cl18_detach(self):
        if self._cl18_driver is not None:
            self.mobject.remove_updater(self._cl18_driver)
            self._cl18_driver = None


class ContinualAnimationGroup(ContinualAnimation):
    CONFIG = {
        "start_up_time": 0,
        "wind_down_time": 0,
    }

    def __init__(self, *continual_animations, **kwargs):
        digest_config(self, kwargs, locals())
        self.group = Group(*[ca.mobject for ca in continual_animations])
        ContinualAnimation.__init__(self, self.group, **kwargs)

    def update_mobject(self, dt):
        for continual_animation in self.continual_animations:
            continual_animation.update(dt)


class ContinualRotation(ContinualAnimation):
    CONFIG = {
        "axis": OUT,
        "rate": np.pi / 12,  # radians per second
        "in_place": True,
        "about_point": None,
    }

    def update_mobject(self, dt):
        if self.about_point is not None:
            about_point = self.about_point
        elif self.in_place:
            about_point = self.mobject.get_center()
        else:
            about_point = ORIGIN
        self.mobject.rotate(dt * self.rate, axis=self.axis, about_point=about_point)


class ContinualMovement(ContinualAnimation):
    CONFIG = {
        "direction": RIGHT,
        "rate": 0.05,  # units per second
    }

    def update_mobject(self, dt):
        self.mobject.shift(dt * self.rate * self.direction)


class NormalAnimationAsContinualAnimation(ContinualAnimation):
    CONFIG = {
        "start_up_time": 0,
        "wind_down_time": 0,
    }

    def __init__(self, animation, **kwargs):
        self.animation = animation
        animation.begin()
        ContinualAnimation.__init__(self, animation.mobject, **kwargs)

    def update_mobject(self, dt):
        self.animation.update(min(float(self.internal_time) / self.animation.run_time, 1))


class CycleAnimation(ContinualAnimation):
    def __init__(self, animation, **kwargs):
        self.animation = animation
        animation.begin()
        ContinualAnimation.__init__(self, animation.mobject, **kwargs)

    def update_mobject(self, dt):
        mod_value = self.internal_time % self.animation.run_time
        self.animation.update(mod_value / float(self.animation.run_time))


class ContinualUpdate(ContinualAnimation):
    CONFIG = {
        "function_depends_on_dt": False,
    }

    def __init__(self, mobject, func, **kwargs):
        self.func = func
        ContinualAnimation.__init__(self, mobject, **kwargs)

    def update_mobject(self, dt):
        if self.function_depends_on_dt:
            self.func(self.mobject, dt)
        else:
            self.func(self.mobject)


class ContinualUpdateFromFunc(ContinualUpdate):
    pass


class ContinualUpdateFromTimeFunc(ContinualUpdate):
    CONFIG = {
        "function_depends_on_dt": True,
    }


class ContinualMaintainPositionRelativeTo(ContinualAnimation):
    def __init__(self, mobject, tracked_mobject, **kwargs):
        self.anim = MaintainPositionRelativeTo(mobject, tracked_mobject, **kwargs)
        self.anim.begin()
        ContinualAnimation.__init__(self, mobject, **kwargs)

    def update_mobject(self, dt):
        self.anim.update(0)


class ContinualGrowValue(ContinualAnimation):
    CONFIG = {
        "rate": 1,
    }

    def __init__(self, value_tracker, **kwargs):
        if not isinstance(value_tracker, ValueTracker):
            raise Exception("ContinualGrowValue must take a ValueTracker as its mobject")
        self.value_tracker = value_tracker
        ContinualAnimation.__init__(self, value_tracker, **kwargs)

    def update_mobject(self, dt):
        self.value_tracker.set_value(self.value_tracker.get_value() + self.rate * dt)


__all__ += [
    "ContinualAnimation", "ContinualAnimationGroup", "ContinualRotation", "ContinualMovement",
    "NormalAnimationAsContinualAnimation", "CycleAnimation", "ContinualUpdate", "ContinualUpdateFromFunc",
    "ContinualUpdateFromTimeFunc", "ContinualMaintainPositionRelativeTo", "ContinualGrowValue",
]


if _CL18_2018:
    _cl18_scene_add = Scene.add
    _cl18_scene_remove = Scene.remove
    _cl18_scene_clear = Scene.clear

    def _cl18_split_cas(items):
        mobs, cas = [], []
        for item in items:
            (cas if isinstance(item, ContinualAnimation) else mobs).append(item)
        return mobs, cas

    def _cl18_scene_cas(self):
        return self.__dict__.setdefault("continual_animations", [])

    @_wraps(_cl18_scene_add)
    def _cl18_add(self, *items):
        mobs, cas = _cl18_split_cas(items)
        # Scene.add calls self.remove(*mobjects) first: do not let that detach the animations being added
        self.__dict__["_cl18_adding"] = True
        try:
            _cl18_scene_add(self, *mobs, *[ca.mobject for ca in cas])
        finally:
            self.__dict__["_cl18_adding"] = False
        for ca in cas:
            ca._cl18_attach()
            if ca not in _cl18_scene_cas(self):
                _cl18_scene_cas(self).append(ca)
        # CL18-D: Cairo kept foreground mobjects on top: every add() re-appends them at the end of the draw order
        foreground = self.__dict__.get("foreground_mobjects")
        if foreground:
            self.__dict__["_cl18_adding"] = True
            try:
                _cl18_scene_add(self, *foreground)
            finally:
                self.__dict__["_cl18_adding"] = False
        return self

    @_wraps(_cl18_scene_remove)
    def _cl18_remove(self, *items):
        mobs, cas = _cl18_split_cas(items)
        mobs = mobs + [ca.mobject for ca in cas]
        if not self.__dict__.get("_cl18_adding", False):
            registered = _cl18_scene_cas(self)
            gone = [ca for ca in registered if ca in cas or any(ca.mobject is m for m in mobs)]
            for ca in gone:
                ca._cl18_detach()
            self.continual_animations = [ca for ca in registered if ca not in gone]
            if self.__dict__.get("foreground_mobjects"):
                self.foreground_mobjects = [m for m in self.foreground_mobjects if not any(m is r for r in mobs)]
        return _cl18_scene_remove(self, *mobs)

    @_wraps(_cl18_scene_clear)
    def _cl18_clear(self):
        for ca in _cl18_scene_cas(self):
            ca._cl18_detach()
        self.continual_animations = []
        self.foreground_mobjects = []
        return _cl18_scene_clear(self)

    # CL18-D: Cairo foreground mobjects (scene.add_foreground_mobject(s) / remove_foreground_mobject(s)), always drawn on top
    def _cl18_add_foreground_mobjects(self, *mobjects):
        fg = [m for m in self.__dict__.get("foreground_mobjects", []) if not any(m is n for n in mobjects)]
        self.foreground_mobjects = fg + list(mobjects)
        self.add(*mobjects)
        return self

    def _cl18_remove_foreground_mobjects(self, *to_remove):
        self.remove(*to_remove)
        return self

    def _cl18_clear_foreground_mobjects(self):
        self.foreground_mobjects = []
        return self

    def _cl18_wind_down(self, *continual_animations, **kwargs):
        wind_down_time = kwargs.pop("wind_down_time", 1)
        for ca in continual_animations:
            ca.begin_wind_down(wind_down_time)
        self.wait(wind_down_time)
        # Remove only the animations that were wound down (3feb kept the others by mistake)
        self.remove(*continual_animations)

    Scene.add = _cl18_add
    Scene.remove = _cl18_remove
    Scene.clear = _cl18_clear
    Scene.wind_down = _cl18_wind_down
    Scene.add_foreground_mobjects = _cl18_add_foreground_mobjects
    Scene.add_foreground_mobject = lambda self, mobject: _cl18_add_foreground_mobjects(self, mobject)
    Scene.remove_foreground_mobjects = _cl18_remove_foreground_mobjects
    Scene.remove_foreground_mobject = lambda self, mobject: _cl18_remove_foreground_mobjects(self, mobject)
    Scene.clear_foreground_mobjects = _cl18_clear_foreground_mobjects


# CL18-B: Cairo's `constants.MEDIA_DIR` no longer exists in ManimGL; 2018 scenes build asset paths from it
# (os.path.join(MEDIA_DIR, "3b1b_videos", ...)). Grant's Dropbox-style prefix makes manim_imports_ext.find_file
# search the file by name in converted/_lib/assets/*, where the replacement assets live.
MEDIA_DIR = "/Users/grant/Dropbox/3Blue1Brown/media"
__all__.append("MEDIA_DIR")


# CL18-E: Cairo's VGroup/VMobject.add accepted any Mobject (e.g. VGroup(ellipse, ImageMobject("sun"))); ManimGL raises
# "Only VMobjects can be passed into VGroup" / "All submobjects must be of type VMobject". 2018 scenes only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.mobject.mobject import Mobject as _ClEMobject, Group as _ClEGroup
    from manimlib.mobject.types.vectorized_mobject import VMobject as _ClEVMobject, VGroup as _ClEVGroup

    _cl18e_vmobject_add = _ClEVMobject.add
    _cl18e_vgroup_init = _ClEVGroup.__init__

    def _cl18e_vmobject_add_any(self, *mobjects):
        if all(isinstance(m, _ClEVMobject) for m in mobjects):
            return _cl18e_vmobject_add(self, *mobjects)
        return _ClEMobject.add(self, *mobjects)

    def _cl18e_vgroup_init_any(self, *mobjects, **kwargs):
        if not any(isinstance(m, _ClEMobject) and not isinstance(m, _ClEVMobject) for m in mobjects):
            return _cl18e_vgroup_init(self, *mobjects, **kwargs)
        _cl18e_vgroup_init(self, **kwargs)
        self._ingest_args(*mobjects)
        first = self.submobjects[0] if self.submobjects else None
        if isinstance(first, _ClEVMobject):
            self.uniforms.update(first.uniforms)

    _cl18e_vgroup_new = _ClEVGroup.__new__

    def _cl18e_vgroup_new_mixed(cls, *mobjects, **kwargs):
        # A plain VGroup holding an ImageMobject (etc.) becomes a real Group: VMobject.set_fill/set_opacity (FadeIn...)
        # iterate the whole family and need VMobject uniforms, which an ImageMobject lacks.
        if cls is _ClEVGroup and any(isinstance(m, _ClEMobject) and not isinstance(m, _ClEVMobject) for m in mobjects):
            return _ClEGroup(*mobjects, **kwargs)
        return _cl18e_vgroup_new(cls)

    _ClEVMobject.add = _cl18e_vmobject_add_any
    _ClEVGroup.__init__ = _cl18e_vgroup_init_any
    _ClEVGroup.__new__ = _cl18e_vgroup_new_mixed


# CL18-E: Axes(color=TEAL, ...) in Cairo: Axes was a VGroup, so `color` recolored the whole group (axes, ticks) after
# construction. GL's CoordinateSystem.__init__ rejects the kwarg (TypeError). Apply it with set_color afterwards. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    _cl18e_axes_init = Axes.__init__

    @_wraps(_cl18e_axes_init)
    def _cl18e_axes_init_color(self, *args, color=None, **kwargs):
        _cl18e_axes_init(self, *args, **kwargs)
        if color is not None:
            self.set_color(color)

    Axes.__init__ = _cl18e_axes_init_color


# CL18-B: Cairo ChangingDecimal(decimal, func, position_update_func=...) called position_update_func(decimal) after every
# value update (to keep the label next to a moving point); ManimGL's ChangingDecimal rejects the kwarg. Wrapping the base
# class also covers ChangeDecimalToValue / CountInFrom. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.animation.numbers import ChangingDecimal as _ClBChangingDecimal

    _clb_cd_init = _ClBChangingDecimal.__init__
    _clb_cd_interp = _ClBChangingDecimal.interpolate_mobject

    @_wraps(_clb_cd_init)
    def _clb_changing_decimal_init(self, *args, position_update_func=None, **kwargs):
        self.position_update_func = position_update_func
        _clb_cd_init(self, *args, **kwargs)

    @_wraps(_clb_cd_interp)
    def _clb_changing_decimal_interp(self, alpha):
        _clb_cd_interp(self, alpha)
        if getattr(self, "position_update_func", None) is not None:
            self.position_update_func(self.mobject)

    _ClBChangingDecimal.__init__ = _clb_changing_decimal_init
    _ClBChangingDecimal.interpolate_mobject = _clb_changing_decimal_interp


# CL18-A: one-time port of once_useful_constructs scene bases (VectorScene, LinearTransformationScene,
# SampleSpaceScene, ReconfigurableScene, TODOStub, PatreonThanks, LogoGenerationTemplate, ShowShadows + helpers).
# New names only (nothing existing is wrapped), so no era flag. Source: _lib/once_useful_gl.py.
import once_useful_gl as _cl18a_gl
from once_useful_gl import *
__all__.extend(_cl18a_gl.__all__)


# CL18-E: Line.put_start_and_end_on_with_projection (Cairo, manim_3feb geometry.py): rescales and rotates the line (keeping
# a DashedLine's dash pattern) instead of rebuilding it. New method, nothing wrapped, so no era flag.
def _cl18e_put_start_and_end_on_with_projection(self, new_start, new_end):
    new_start = np.array(new_start, dtype=float)
    target_vect = np.array(new_end, dtype=float) - new_start
    curr_vect = self.get_vector()
    curr_norm = get_norm(curr_vect)
    if curr_norm == 0:
        self.put_start_and_end_on(new_start, new_end)
        return self
    target_norm = get_norm(target_vect)
    if target_norm == 0:
        self.scale(0.001 / curr_norm)
        self.move_to(new_start)
        return self
    unit_target = target_vect / target_norm
    unit_curr = curr_vect / curr_norm
    normal = np.cross(unit_target, unit_curr)
    if get_norm(normal) == 0:
        normal = UP if (unit_curr[0] == 0 and unit_curr[1] == 0) else OUT
    angle_diff = np.arccos(np.clip(np.dot(unit_target, unit_curr), -1, 1))
    self.scale(target_norm / curr_norm)
    self.rotate(-angle_diff, normal)
    self.shift(new_start - self.get_start())
    return self


Line.put_start_and_end_on_with_projection = _cl18e_put_start_and_end_on_with_projection


# CL18-C: VectorField(func, **config) of Cairo (div_curl, others): GL's VectorField needs a coordinate_system and a vectorized func.
# 2018 only: the name VectorField is the Cairo-style CairoVectorField (VGroup of Vector arrows), as 2019 scenes already got via CairoVectorField.
if _CAIRO_ERA and _CL18_2018:
    class VectorField(CairoVectorField):
        def __init__(self, func, delta_x=0.5, delta_y=0.5, **kwargs):
            # delta_x/delta_y = np.inf (div_curl DivergenceAsNewFunction: the field is only used through get_vector): old numpy's arange gave one
            # sample for an infinite step; a huge finite step keeps it to the first sample (plus one far away) without erroring.
            delta_x = 1e6 if np.isinf(delta_x) else delta_x
            delta_y = 1e6 if np.isinf(delta_y) else delta_y
            super().__init__(func, delta_x=delta_x, delta_y=delta_y, **kwargs)

    __all__.append("VectorField")


# CL18-A: Cairo's Matrix accepted a flat list/array as a column vector (`Matrix(["x", "y"])`, `Matrix(np.array(chars))`) and kept
# `matrix.elements` as a VGroup (`.elements.set_color_by_gradient(...)`, `ReplacementTransform(..., col.elements)`). GL's Matrix treats
# a flat list as rows of characters and keeps `elements` as a plain list. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    _cl18a_old_matrix_init = _ClMatrix.__init__

    @_wraps(_cl18a_old_matrix_init)
    def _cl18a_matrix_init(self, matrix, *args, **kwargs):
        if (isinstance(matrix, (list, tuple, np.ndarray)) and len(matrix) > 0
                and not isinstance(matrix[0], (list, tuple, np.ndarray))):
            matrix = [[element] for element in matrix]
        custom_e2m = kwargs.get("element_to_mobject")
        if callable(custom_e2m) and not isinstance(custom_e2m, type):
            # CL18-A: the CL19 shim passes Mobject entries through untouched, but Cairo called element_to_mobject on them too
            # (`Matrix(mob_matrix, element_to_mobject=lambda m: m.copy())` in cramer made copies; without it the new matrix steals the entries)
            matrix = [[custom_e2m(el) if isinstance(el, Mobject) else el for el in row] for row in matrix]
        number_class = kwargs.get("element_to_mobject")
        if isinstance(number_class, type) and issubclass(number_class, DecimalNumber):
            # CL18-A: the CL19 shim above calls element_to_mobject(str(element)); Integer/DecimalNumber need the number back
            def element_to_mobject(text, _cls=number_class, **config):
                try:
                    value = int(text)
                except ValueError:
                    value = float(text)
                return _cls(value, **config)
            kwargs["element_to_mobject"] = element_to_mobject
        _cl18a_old_matrix_init(self, matrix, *args, **kwargs)
        if isinstance(self.elements, list):
            self.elements = VGroup(*self.elements)

    _ClMatrix.__init__ = _cl18a_matrix_init


# CL18-C: Animation(rate_func=None) meant "linear" in 3feb (Animation.__init__ replaced None with identity); GL calls None and crashes
# ("'NoneType' object is not callable"). 2018 only. Affects fourier (DrawFrequencyPlot family), possibly other 2018 scenes.
if _CAIRO_ERA and _CL18_2018:
    _cl18c_old_animation_init = Animation.__init__

    @_wraps(_cl18c_old_animation_init)
    def _cl18c_animation_init(self, *args, **kwargs):
        if "rate_func" in kwargs and kwargs["rate_func"] is None:
            kwargs["rate_func"] = linear
        _cl18c_old_animation_init(self, *args, **kwargs)

    Animation.__init__ = _cl18c_animation_init


# CL18-C: Succession(ApplyMethod, mob.shift, UP, {"run_time": 2}, FadeOut, mob, ...) of 3feb: "each arg is an animation, or an animation
# class followed by its arguments (and optionally a config dict)". GL's Succession only takes animation instances. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    _cl18c_old_succession_init = Succession.__init__

    @_wraps(_cl18c_old_succession_init)
    def _cl18c_succession_init(self, *args, **kwargs):
        if any(isinstance(a, type) and issubclass(a, Animation) for a in args):
            animations, cls, cls_args, cls_config = [], None, [], {}

            def flush():
                if cls is not None:
                    animations.append(cls(*cls_args, **cls_config))
            for arg in args:
                if isinstance(arg, Animation):
                    flush()
                    cls, cls_args, cls_config = None, [], {}
                    animations.append(arg)
                elif isinstance(arg, type) and issubclass(arg, Animation):
                    flush()
                    cls, cls_args, cls_config = arg, [], {}
                elif isinstance(arg, dict):
                    cls_config = arg
                else:
                    cls_args.append(arg)
            flush()
            args = tuple(animations)
        _cl18c_old_succession_init(self, *args, **kwargs)

    Succession.__init__ = _cl18c_succession_init


# CL18-C: NumberPlane/ComplexPlane.get_coordinate_labels / add_coordinates of 3feb (2018 only). GL only has add_coordinate_labels, which skips
# the first tick and has other label sizes; scenes index plane.coordinate_labels[:7] (reals) / [7:] (imaginaries) and pop the last one.
# Labels: one per integer in [-int(radius), int(radius)] on x (including 0) and, for ComplexPlane, nonzero integers on y written "<n>i".
def _cl18c_label(self, text, point):
    label = OldTex(text)
    label.add_background_rectangle()
    label.set_height(0.2)
    label.next_to(point, DOWN + LEFT, SMALL_BUFF)
    return label


def _cl18c_plane_coordinate_labels(self, x_vals=None, y_vals=None):
    labels = VGroup()
    if x_vals is None:
        x_vals = list(range(-int(self.x_radius), int(self.x_radius) + 1))
    if y_vals is None:
        y_vals = list(range(-int(self.y_radius), int(self.y_radius) + 1))
    for index, vals in enumerate([x_vals, y_vals]):
        for val in vals:
            if val == 0:
                continue
            pair = [0, 0]
            pair[index] = val
            labels.add(_cl18c_label(self, str(val), self.coords_to_point(*pair)))
    self.coordinate_labels = labels
    return labels


def _cl18c_complex_coordinate_labels(self, *numbers):
    labels = VGroup()
    if len(numbers) == 0:
        numbers = list(range(-int(self.x_radius), int(self.x_radius) + 1))
        numbers += [complex(0, y) for y in range(-int(self.y_radius), int(self.y_radius) + 1) if y != 0]
    for number in numbers:
        text = str(number).replace("j", "i")
        if text.startswith("0"):
            text = "0"
        elif text in ("1i", "-1i"):
            text = text.replace("1", "")
        labels.add(_cl18c_label(self, text, self.number_to_point(number)))
    self.coordinate_labels = labels
    return labels


if _CAIRO_ERA and _CL18_2018:
    NumberPlane.get_coordinate_labels = _cl18c_plane_coordinate_labels
    NumberPlane.add_coordinates = lambda self, x_vals=None, y_vals=None: self.add(self.get_coordinate_labels(x_vals, y_vals))
    ComplexPlane.get_coordinate_labels = _cl18c_complex_coordinate_labels
    ComplexPlane.add_coordinates = lambda self, *numbers: self.add(self.get_coordinate_labels(*numbers))


# CL18-C: ThreeDScene.add_fixed_orientation_mobjects(*mobs) / remove_fixed_orientation_mobjects(*mobs) of Cairo. The mobjects keep their 3D position
# but are drawn as if the camera looked straight at them (labels in a 3D scene). In GL a per-frame updater re-orients the points into the camera basis
# (world offset = camera orientation matrix @ screen-aligned offset) around the mobject's own position; removing it restores the original points.
# Not era-gated: new methods only.
def _cl18c_billboard(frame, mob):
    members = list(mob.family_members_with_points())
    center0 = np.array(mob.get_center())
    rels = [m.get_points().copy() - center0 for m in members]
    mean_rel = np.concatenate(rels).mean(axis=0)
    state = {"Q": np.eye(3)}

    def update(_mob, dt=0):
        Q = frame.get_orientation().as_matrix()
        cur_mean = np.concatenate([m.get_points() for m in members]).mean(axis=0)
        center = cur_mean - mean_rel @ state["Q"].T
        for m, rel in zip(members, rels):
            m.set_points(center + rel @ Q.T)
        state["Q"] = Q

    def restore():
        cur_mean = np.concatenate([m.get_points() for m in members]).mean(axis=0)
        center = cur_mean - mean_rel @ state["Q"].T
        for m, rel in zip(members, rels):
            m.set_points(center + rel)
        state["Q"] = np.eye(3)

    mob._cl18c_billboard = (update, restore)
    mob.add_updater(update)
    update(mob)


def _cl18c_add_fixed_orientation_mobjects(self, *mobjects, use_static_center_func=False, center_func=None, **kwargs):
    self.add(*mobjects)
    for mob in mobjects:
        if getattr(mob, "_cl18c_billboard", None) is None:
            _cl18c_billboard(self.frame, mob)
    return self


def _cl18c_remove_fixed_orientation_mobjects(self, *mobjects):
    for mob in mobjects:
        pair = getattr(mob, "_cl18c_billboard", None)
        if pair is not None:
            mob.remove_updater(pair[0])
            pair[1]()
            mob._cl18c_billboard = None
    return self


if not hasattr(ThreeDScene, "add_fixed_orientation_mobjects"):
    ThreeDScene.add_fixed_orientation_mobjects = _cl18c_add_fixed_orientation_mobjects
    ThreeDScene.remove_fixed_orientation_mobjects = _cl18c_remove_fixed_orientation_mobjects


# CL18-C: VMobject.copy() of a VGroup that contains a plain Mobject (ImageMobject, allowed by CL18-E's VGroup shim) reads mob.fill_group for every
# family member and raises AttributeError on the non-VMobject ones (ApplyMethod(VGroup(image, ...).to_edge, ...) in quaternions IntroduceHamilton). 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.mobject.mobject import Mobject as _ClCMobject
    if not hasattr(_ClCMobject, "fill_group"):
        _ClCMobject.fill_group = None


# CL18-C: Cairo (sep19/3feb) ParametricSurface and Sphere for 2018 scenes. They were VGroups of ThreeDVMobject faces (u_index/v_index, set_fill_by_checkerboard,
# faces that can be sorted, faded, indexed and animated), `self.func` replaceable by subclasses, `Sphere.func(self, u, v)` callable unbound
# (quaternions StereoProjectedSphere*). GL's Surface/Sphere are single shader meshes with a different API, so in 2018 the names are the faces version
# (the 2019 scenes used the opt-in aliases CairoParametricSurface/CairoSphere, which differ in constructor structure). New classes, 2018 only.
if _CAIRO_ERA and _CL18_2018:
    class ParametricSurface(VGroup):
        CONFIG = {
            "u_min": 0,
            "u_max": 1,
            "v_min": 0,
            "v_max": 1,
            "resolution": 32,
            "surface_piece_config": {},
            "fill_color": BLUE_D,
            "fill_opacity": 1.0,
            "checkerboard_colors": [BLUE_D, BLUE_E],
            "stroke_color": GREY_B,
            "stroke_width": 0.5,
            "stroke_opacity": 1.0,
            "should_make_jagged": False,
            "pre_function_handle_to_anchor_scale_factor": 0.00001,
        }

        def __init__(self, func, **kwargs):
            VGroup.__init__(self)
            digest_config(self, kwargs)
            self.func = func
            self.setup_in_uv_space()
            for face in self:
                face.set_points(np.array([func(p[0], p[1]) for p in face.get_points()], dtype=float).reshape(-1, 3))

        def get_u_values_and_v_values(self):
            res = self.resolution
            u_res, v_res = (res, res) if np.isscalar(res) else res
            return (np.linspace(self.u_min, self.u_max, int(u_res) + 1),
                    np.linspace(self.v_min, self.v_max, int(v_res) + 1))

        def setup_in_uv_space(self):
            u_values, v_values = self.get_u_values_and_v_values()
            faces = VGroup()
            for i in range(len(u_values) - 1):
                for j in range(len(v_values) - 1):
                    u1, u2 = u_values[i:i + 2]
                    v1, v2 = v_values[j:j + 2]
                    face = VMobject()
                    face.set_points_as_corners([[u1, v1, 0], [u2, v1, 0], [u2, v2, 0], [u1, v2, 0], [u1, v1, 0]])
                    face.apply_depth_test()
                    faces.add(face)
                    face.u_index, face.v_index = i, j
                    face.u1, face.u2, face.v1, face.v2 = u1, u2, v1, v2
            faces.set_fill(color=self.fill_color, opacity=self.fill_opacity)
            faces.set_stroke(color=self.stroke_color, width=self.stroke_width, opacity=self.stroke_opacity)
            self.add(*faces)
            if self.checkerboard_colors:
                self.set_fill_by_checkerboard(*self.checkerboard_colors)

        def set_fill_by_checkerboard(self, *colors, opacity=None):
            n_colors = len(colors)
            for face in self:
                face.set_fill(colors[(face.u_index + face.v_index) % n_colors], opacity=opacity)

    class Sphere(ParametricSurface):
        CONFIG = {
            "resolution": (12, 24),
            "radius": 1,
            "u_min": 0.001,
            "u_max": PI - 0.001,
            "v_min": 0,
            "v_max": TAU,
        }

        def __init__(self, **kwargs):
            ParametricSurface.__init__(self, self.func, **kwargs)
            self.scale(self.radius)

        def func(self, u, v):
            return np.array([np.cos(v) * np.sin(u), np.sin(v) * np.sin(u), np.cos(u)])

    __all__.extend(["ParametricSurface", "Sphere"])


# CL18-B: every 2018 file predates the 3 Feb 2019 Cairo (manim_3feb), whose TextMobject joined its arguments with " "
# (sep19 changed it to ""). Extends the CL19 path regex so OldTexText("Let", "$\pi$", "be") renders with the spaces as in 2018.
_CL19_SPACED_TEXT_PATH = _re.compile(_CL19_SPACED_TEXT_PATH.pattern + r"|/_?2018/")


# CL18-B: custom/opening_quote.py (read-only) calls OldTexText but only imports TexText, so every OpeningQuote scene died with
# "NameError: name 'OldTexText' is not defined" (2018: eop bayes/independence/chapter1, cramer). Inject the name into that module.
import custom.opening_quote as _clb_opening_quote_module
_clb_opening_quote_module.OldTexText = OldTexText


# CL18-C: Mobject.surround(mobject, buffer_factor=1.2) of Cairo (3feb/sep19: replace, then scale by buffer_factor). GL's takes buff (an additive length).
# Only used when the Cairo keyword is passed; 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.mobject.mobject import Mobject as _ClCSurroundMobject
    _cl18c_old_surround = _ClCSurroundMobject.surround

    @_wraps(_cl18c_old_surround)
    def _cl18c_surround(self, mobject, dim_to_match=0, stretch=False, *args, buffer_factor=None, **kwargs):
        if buffer_factor is None:
            return _cl18c_old_surround(self, mobject, dim_to_match, stretch, *args, **kwargs)
        self.replace(mobject, dim_to_match, stretch)
        self.scale(buffer_factor)
        return self

    _ClCSurroundMobject.surround = _cl18c_surround


# CL18-D: Cairo `Arc(angle, start_angle=..., radius=...)`: the first positional argument is the angle; GL's is start_angle
# (so `Arc(-TAU/2, radius=r, start_angle=-TAU/4)` raised "multiple values for argument 'start_angle'"). Only the
# one-positional-argument call is reinterpreted (GL itself, e.g. Circle, passes two). 2018 only.
if _CL18_2018:
    _cl18d_arc_init = Arc.__init__

    @_wraps(_cl18d_arc_init)
    def _cl18d_arc_new_init(self, *args, **kwargs):
        if len(args) == 1 and "angle" not in kwargs:
            kwargs["angle"] = args[0]
            args = ()
        result = _cl18d_arc_init(self, *args, **kwargs)
        # remembered for Cairo's set_bound_angles() + init_points() regeneration below
        names = ("start_angle", "angle", "radius", "n_components", "arc_center")
        params = dict(start_angle=0, angle=TAU / 4, radius=1.0, arc_center=ORIGIN)
        params.update({k: v for k, v in zip(names, args)})
        params.update({k: kwargs[k] for k in names if k in kwargs})
        self.__dict__["_cl18d_arc_params"] = params
        return result

    Arc.__init__ = _cl18d_arc_new_init

    # Cairo: arc.set_bound_angles(start, stop) changed start_angle/angle and arc.init_points() rebuilt the points from
    # (start_angle, angle, radius, arc_center) around the ORIGINAL arc_center
    def _cl18d_set_bound_angles(self, start=0, stop=np.pi):
        params = self.__dict__["_cl18d_arc_params"]
        params["start_angle"] = start
        params["angle"] = stop - start
        return self

    def _cl18d_arc_init_points(self):
        params = self.__dict__.get("_cl18d_arc_params")
        if params is None:  # called by Mobject.__init__ before the arc was built: GL builds the points in Arc.__init__
            return
        from manimlib.utils.bezier import quadratic_bezier_points_for_arc
        fresh = VMobject()
        fresh.set_points(quadratic_bezier_points_for_arc(params["angle"], int(15 * (abs(params["angle"]) / TAU)) + 1))
        fresh.rotate(params["start_angle"], about_point=ORIGIN)
        fresh.scale(params["radius"], about_point=ORIGIN)
        fresh.shift(params["arc_center"])
        self.set_points(fresh.get_points())

    Arc.set_bound_angles = _cl18d_set_bound_angles
    Arc.init_points = _cl18d_arc_init_points


# CL18-A: Transform/MoveToTarget(..., replace_mobject_with_target_in_scene=True) of Cairo (WindingNumber_G, cramer). In GL it is a class
# attribute of Transform, not a constructor argument, so the kwarg reached Animation.__init__ and raised TypeError. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.animation.transform import Transform as _Cl18aTransform
    _cl18a_old_transform_init = _Cl18aTransform.__init__

    @_wraps(_cl18a_old_transform_init)
    def _cl18a_transform_init(self, *args, replace_mobject_with_target_in_scene=None, **kwargs):
        _cl18a_old_transform_init(self, *args, **kwargs)
        if replace_mobject_with_target_in_scene is not None:
            self.replace_mobject_with_target_in_scene = replace_mobject_with_target_in_scene

    _Cl18aTransform.__init__ = _cl18a_transform_init


# CL18-C: Arrow.tip of Cairo (the arrow head as a separate triangle: arrow.tip.set_fill(...), arrow.tip.scale(2)). GL's Arrow is one filled shape without a
# head submobject. 2018 only: `tip` answers the arrow itself, so recoloring the head recolors the arrow (scenes that do it recolor the stroke the same
# color right before, so it is equivalent); scenes that rescale the head only must be changed by hand.
if _CAIRO_ERA and _CL18_2018 and not hasattr(Arrow, "tip"):
    Arrow.tip = property(lambda self: self)


# CL18-C: in 2018 SpecialThreeDScene.get_sphere() answers the faces-based Sphere above (the 2019 CairoSphere has a different constructor/structure and
# the 2018 StereoProjected* subclasses and sphere-slicing code (south_hemisphere.remove(...), u_index/v_index) assume the Cairo Sphere).
if _CAIRO_ERA and _CL18_2018:
    def _cl18c_get_sphere(self, **kwargs):
        return Sphere(**merge_dicts_recursively(self.sphere_config, kwargs))

    SpecialThreeDScene.get_sphere = _cl18c_get_sphere


# CL18-D: 3feb ChangingDecimal also took num_decimal_places / show_ellipsis / include_sign / tracked_mobject as Animation
# CONFIG; the first three were never read by update_number (ignored), tracked_mobject keeps the decimal at a fixed offset
# from another mobject. GL's ChangingDecimal rejects them. Wraps CL18-B's wrapper above. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    _cl18d_cd_init = _ClBChangingDecimal.__init__
    _cl18d_cd_interp = _ClBChangingDecimal.interpolate_mobject

    @_wraps(_cl18d_cd_init)
    def _cl18d_changing_decimal_init(self, *args, **kwargs):
        for key in ("num_decimal_places", "show_ellipsis", "include_sign"):
            kwargs.pop(key, None)
        tracked = kwargs.pop("tracked_mobject", None)
        _cl18d_cd_init(self, *args, **kwargs)
        self.tracked_mobject = tracked
        if tracked is not None:
            self.diff_from_tracked_mobject = self.mobject.get_center() - tracked.get_center()

    @_wraps(_cl18d_cd_interp)
    def _cl18d_changing_decimal_interp(self, alpha):
        _cl18d_cd_interp(self, alpha)
        tracked = getattr(self, "tracked_mobject", None)
        if tracked is not None and getattr(self, "position_update_func", None) is None:
            self.mobject.move_to(tracked.get_center() + self.diff_from_tracked_mobject)

    _ClBChangingDecimal.__init__ = _cl18d_changing_decimal_init
    _ClBChangingDecimal.interpolate_mobject = _cl18d_changing_decimal_interp


# CL18-B: Cairo PiCreatureScene bubble API: pi_creature_says/thinks/introduce_bubble(*args) took an optional leading pi creature
# (default: the primary one), several content strings/mobjects (joined by " " as TextMobject did) and the kwargs
# bubble_class/bubble_kwargs. GL wants (pi_creature, content) with bubble_type/bubble_config. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from custom.characters.pi_creature import PiCreature as _ClBPiCreature
    from custom.characters.pi_creature_scene import PiCreatureScene as _ClBPiCreatureScene

    def _clb_bubble_args(scene, args, kwargs):
        kwargs = dict(kwargs)
        if args and isinstance(args[0], _ClBPiCreature):
            pi_creature, content = args[0], args[1:]
        else:
            pi_creature, content = scene.get_primary_pi_creature(), args
        if "content" in kwargs:
            content = (kwargs.pop("content"),) + tuple(content)
        if "bubble_class" in kwargs:
            kwargs["bubble_type"] = kwargs.pop("bubble_class")
        if "bubble_kwargs" in kwargs:
            kwargs["bubble_config"] = kwargs.pop("bubble_kwargs")
        # think(..., direction=LEFT) reached PiCreatureBubbleIntroduction's digest_config in Cairo and was ignored
        kwargs.pop("direction", None)
        if len(content) == 1:
            content = content[0]
        elif all(isinstance(c, str) for c in content):
            content = " ".join(content)
        else:
            content = OldTexText(*content)
        return pi_creature, content, kwargs

    _clb_pcs_introduce_bubble = _ClBPiCreatureScene.introduce_bubble
    _clb_pcs_says = _ClBPiCreatureScene.pi_creature_says
    _clb_pcs_thinks = _ClBPiCreatureScene.pi_creature_thinks

    @_wraps(_clb_pcs_introduce_bubble)
    def _clb_introduce_bubble(self, *args, **kwargs):
        pi_creature, content, kwargs = _clb_bubble_args(self, args, kwargs)
        return _clb_pcs_introduce_bubble(self, pi_creature, content, **kwargs)

    @_wraps(_clb_pcs_says)
    def _clb_pi_creature_says(self, *args, **kwargs):
        pi_creature, content, kwargs = _clb_bubble_args(self, args, kwargs)
        return _clb_pcs_says(self, pi_creature, content, **kwargs)

    @_wraps(_clb_pcs_thinks)
    def _clb_pi_creature_thinks(self, *args, **kwargs):
        pi_creature, content, kwargs = _clb_bubble_args(self, args, kwargs)
        return _clb_pcs_thinks(self, pi_creature, content, **kwargs)

    _ClBPiCreatureScene.introduce_bubble = _clb_introduce_bubble
    _ClBPiCreatureScene.pi_creature_says = _clb_pi_creature_says
    _ClBPiCreatureScene.pi_creature_thinks = _clb_pi_creature_thinks


# CL18-A: a function stored in a CONFIG dict (`CONFIG = {"func": lambda p: ...}`) was an INSTANCE attribute in Cairo (digest_config used
# setattr on the instance), so `self.func(x)` called it without `self`. manim_imports_ext turns CONFIG keys into CLASS attributes, which
# makes such a function a bound method and `self.func(x)` fails with "takes 1 positional argument but 2 were given". The CONFIG
# functions are re-set as staticmethod. 2018 only (WindingNumber VectorField / Initial2dFuncSceneMorphing).
if _CAIRO_ERA and _CL18_2018:
    def _cl18a_wrap_init_subclass(base):
        previous = base.__dict__["__init_subclass__"].__func__

        def init_subclass(cls, **kwargs):
            previous(cls, **kwargs)
            config = cls.__dict__.get("CONFIG")
            if isinstance(config, dict):
                for key, value in config.items():
                    if isinstance(value, _types.FunctionType) and isinstance(cls.__dict__.get(key), _types.FunctionType):
                        setattr(cls, key, staticmethod(value))
        base.__init_subclass__ = classmethod(init_subclass)

    for _cl18a_base in (Scene, Mobject, Animation):
        _cl18a_wrap_init_subclass(_cl18a_base)


# CL18-D: Cairo's TexMobject/TextMobject.split() indexed across the glyphs when it had a single submobject ("Many old
# scenes assume that when you pass in a single string to TexMobject, it indexes across the characters", manim_3feb
# tex_mobject.py). GL's OldTex keeps that one extra level, so `OldTex("cR")[1]` raised IndexError and `OldTexText("abc")[0]`
# was the whole string. __getitem__/__iter__/__len__ go through split(). 2018 only.
if _CAIRO_ERA and _CL18_2018:
    def _cl18d_oldtex_split(self):
        if len(self.submobjects) == 1:
            return self.submobjects[0].submobjects
        return self.submobjects

    OldTex.split = _cl18d_oldtex_split


# CL18-D: Cairo PiCreature.pupils (VGroup of both pupils, used as `submobject_to_align=randy.pupils[1]` and in
# ReplacementTransform(pi.pupils, ...)); GL's PiCreature keeps each pupil on its eye (`eyes[i].pupil`). New attribute, no flag.
try:
    from custom.characters.pi_creature import PiCreature as _ClDPiCreature
    if not hasattr(_ClDPiCreature, "pupils"):
        _ClDPiCreature.pupils = property(lambda self: VGroup(*[eye.pupil for eye in self.eyes]))
except ImportError:
    pass


# CL18-D: Cairo ThreeDCamera.transform_points_pre_display(mobject, points) / project_points: points as seen by the camera
# (rotation by the camera orientation + perspective, relative to the frame center). Used to put a flat 2D overlay where a
# 3D object appears (sphere_area::AskAboutShadowRelation). New methods, no era flag.
def _cl18d_project_points(self, points):
    frame = self.frame
    points = np.array(points, dtype=float).reshape(-1, 3)
    center = frame.get_center()
    rotated = np.dot(points - center, frame.get_inverse_camera_rotation_matrix().T)
    focal = frame.get_focal_distance()
    denom = np.maximum(focal - rotated[:, 2], 1e-3)
    rotated[:, :2] *= (focal / denom)[:, None]
    return rotated + center


if not hasattr(_Camera, "project_points"):
    _Camera.project_points = _cl18d_project_points
if not hasattr(_Camera, "transform_points_pre_display"):
    _Camera.transform_points_pre_display = lambda self, mobject, points: _cl18d_project_points(self, points)


# CL18-E: FadeIn(mob, direction=v) in Cairo: FadeIn had no `direction` (that is FadeInFrom's) and the Animation base
# absorbed unknown kwargs, so the call was a plain fade-in. GL raises TypeError. Drop the kwarg (same picture). 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.animation.fading import FadeIn as _ClEFadeIn
    _cl18e_fadein_init = _ClEFadeIn.__init__

    @_wraps(_cl18e_fadein_init)
    def _cl18e_fadein_init_nodir(self, *args, direction=None, **kwargs):
        _cl18e_fadein_init(self, *args, **kwargs)

    _ClEFadeIn.__init__ = _cl18e_fadein_init_nodir


# CL18-B: random.sample(VGroup, k): Cairo ran on Python 3.6, where any object with __len__/__getitem__ was accepted; since Python 3.11
# random.sample requires a collections.abc.Sequence ("Population must be a sequence"). Convert such mobject groups to a list. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    import random as _clb_random
    from collections.abc import Sequence as _ClBSequence

    _clb_random_sample = _clb_random.sample

    @_wraps(_clb_random_sample)
    def _clb_sample(population, k, *args, **kwargs):
        if not isinstance(population, (_ClBSequence, set, frozenset, dict)) and hasattr(population, "__len__") \
                and hasattr(population, "__getitem__"):
            population = list(population)
        return _clb_random_sample(population, k, *args, **kwargs)

    _clb_random.sample = _clb_sample


# CL18-E: VMobject().pointwise_become_partial(...) ends with set_points(..., refresh=False), which leaves the (fresh)
# `subpath_range` stale; a later reverse_points() then fails with "IndexError: index 33 is out of bounds" (wallis Lemma1*).
# Recompute the subpath ranges after the partial copy. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.mobject.types.vectorized_mobject import VMobject as _ClEVM2
    _cl18e_become_partial = _ClEVM2.pointwise_become_partial

    @_wraps(_cl18e_become_partial)
    def _cl18e_become_partial_fixed(self, *args, **kwargs):
        result = _cl18e_become_partial(self, *args, **kwargs)
        if self.has_points():
            self.set_subpath_range()
        return result

    _ClEVM2.pointwise_become_partial = _cl18e_become_partial_fixed


# CL18-E: a zero-length DashedLine (observer standing on a lighthouse) got 0 dashes in GL, i.e. no points, and
# get_start/get_length raised "Cannot call Mobject.get_start for a Mobject with no points" (wallis KeeperAndSailor).
# Cairo always made at least 2 dashes. Ask for at least one. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    _cl18e_num_dashes = DashedLine.calculate_num_dashes

    @_wraps(_cl18e_num_dashes)
    def _cl18e_num_dashes_min1(self, *args, **kwargs):
        return max(1, _cl18e_num_dashes(self, *args, **kwargs))

    DashedLine.calculate_num_dashes = _cl18e_num_dashes_min1


# CL18-C: AnimatedStreamLines(...).mobject of 3feb (it was a ContinualAnimation; scenes call VFadeOut(stream_line_animation.mobject)). The CL19 shim above is a
# VGroup itself, so `.mobject` answers the group. 2018 only.
if _CAIRO_ERA and _CL18_2018 and not hasattr(AnimatedStreamLines, "mobject"):
    AnimatedStreamLines.mobject = property(lambda self: self)


# CL18-D: early-2018 manim camera API used by basel (PondScene, InscribedAngleScene, ScreenShapingScene, basel2 PondScene):
# `camera.rotation_mobject` was a point holding the camera position (moving it moved the camera, e.g.
# `ApplyMethod(self.camera.rotation_mobject.move_to, camera.get_spherical_coords(phi, theta, 2 * distance))`) and
# camera.get_phi/get_theta/get_distance/get_spherical_coords. Model: camera distance r from the origin, default 5 (old
# default_distance); GL frame height = FRAME_HEIGHT * r / 5 and orientation (theta_GL = theta + 90 deg, phi). A frame
# updater copies the point into the frame only when the point moved, so frame changes made by the scene are not undone.
_CL18D_DEFAULT_DISTANCE = 5.0


def _cl18d_spherical(phi, theta, distance):
    return distance * np.array([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])


def _cl18d_get_rotation_mobject(self):
    point = self.__dict__.get("_cl18d_rotation_mobject")
    if point is None:
        frame = self.frame
        point = VectorizedPoint(_cl18d_spherical(
            frame.get_phi(), frame.get_theta() - 90 * DEGREES,
            _CL18D_DEFAULT_DISTANCE * frame.get_height() / FRAME_HEIGHT))
        point._cl18d_last = point.get_center().copy()
        self.__dict__["_cl18d_rotation_mobject"] = point

        def sync(frame_mob, dt=0, *args):
            pos = point.get_center()
            if np.linalg.norm(pos - point._cl18d_last) < 1e-9:
                return frame_mob
            point._cl18d_last = pos.copy()
            r = max(np.linalg.norm(pos), 1e-6)
            # looking straight down (phi ~ 0) the azimuth is undefined: keep the frame's theta
            theta = np.arctan2(pos[1], pos[0]) + 90 * DEGREES if np.linalg.norm(pos[:2]) > 1e-6 else None
            frame_mob.set_euler_angles(theta=theta, phi=np.arccos(np.clip(pos[2] / r, -1, 1)))
            frame_mob.set_height(FRAME_HEIGHT * r / _CL18D_DEFAULT_DISTANCE)
            return frame_mob

        frame.add_updater(sync, call=False)
    return point


def _cl18d_cam_position(self):
    return self.rotation_mobject.get_center()


def _cl18d_get_distance(self):
    return float(np.linalg.norm(_cl18d_cam_position(self)))


def _cl18d_cam_get_phi(self):
    pos = _cl18d_cam_position(self)
    return float(np.arccos(np.clip(pos[2] / max(np.linalg.norm(pos), 1e-6), -1, 1)))


def _cl18d_cam_get_theta(self):
    pos = _cl18d_cam_position(self)
    return float(np.arctan2(pos[1], pos[0]))


def _cl18d_get_spherical_coords(self, phi=None, theta=None, distance=None):
    phi = self.get_phi() if phi is None else phi
    theta = self.get_theta() if theta is None else theta
    distance = self.get_distance() if distance is None else distance
    return _cl18d_spherical(phi, theta, distance)


if not hasattr(_Camera, "rotation_mobject"):
    _Camera.rotation_mobject = property(_cl18d_get_rotation_mobject)
for _name, _fn in (("get_phi", _cl18d_cam_get_phi), ("get_theta", _cl18d_cam_get_theta), ("get_distance", _cl18d_get_distance),
                   ("get_spherical_coords", _cl18d_get_spherical_coords)):
    if not hasattr(_Camera, _name):
        setattr(_Camera, _name, _fn)


# CL18-D: CL18-C's read-only `Arrow.tip` (returns the arrow itself) breaks GL's `add_tip()` which assigns `self.tip = tip`
# (basel::InfiniteCircleScene: Arrow(...).add_tip(); get_tip()). Same getter, plus a setter that remembers the added tip. 2018 only.
if _CAIRO_ERA and _CL18_2018 and isinstance(getattr(Arrow, "tip", None), property):
    Arrow.tip = property(lambda self: self.__dict__.get("_cl18d_tip", self),
                         lambda self, value: self.__dict__.__setitem__("_cl18d_tip", value))


# CL18-D: Cairo Arc.radius (also Circle/LabeledArc subclasses reading `arc.radius`): GL's Arc does not keep it. Derived from
# the geometry (distance from the start point to the arc center) unless the scene assigned one. 2018 only.
if _CAIRO_ERA and _CL18_2018 and not hasattr(Arc, "radius"):
    Arc.radius = property(
        lambda self: self.__dict__.get("_cl18d_radius", float(np.linalg.norm(self.get_start() - self.get_arc_center()))),
        lambda self, value: self.__dict__.__setitem__("_cl18d_radius", value))


# CL18-B: Cairo EmptyAnimation (3feb composition.py): an animation of an empty Group that lasts run_time (default 0); used as a pause
# inside Succession (eop BrickRowScene family, JustFlipping, WindingNumber_G). New name, no era flag.
class EmptyAnimation(Animation):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("run_time", 0)
        Animation.__init__(self, Group(), *args, **kwargs)


__all__.append("EmptyAnimation")


# CL18-B: VMobject.rotate() ends with `for mob in self.get_family(): mob.get_unit_normal(refresh=True)`, which assumes every
# family member is a VMobject. With CL18-E's VGroup(non-VMobject) (e.g. a Cube/Surface group inside a VGroup, quat3d RandyPrism)
# it raised AttributeError 'get_unit_normal'. Give plain Mobjects a no-op get_unit_normal. 2018 only.
if _CAIRO_ERA and _CL18_2018 and not hasattr(Mobject, "get_unit_normal"):
    def _clb_mobject_get_unit_normal(self, refresh=False):
        return np.array(OUT, dtype=float)

    Mobject.get_unit_normal = _clb_mobject_get_unit_normal


# CL18-A: CL18-D's OldTex.split() flattens a single submobject (3feb behaviour: `OldTex("abc")[1]` is a glyph). The sep19 files
# (cramer) were written for sep19, where
# `OldTex("...")[0]` is the whole formula and `OldTex(...)[0][i]` its glyphs ("frac = OldTex(...)[0]; frac[16]" in cramer):
# flattening breaks them with IndexError. For callers in those folders the original (non-flattening) split is used.
if _CAIRO_ERA and _CL18_2018:
    # CL18 closing: div_curl's population labels also index `OldTexText("\\# Foxes: ")[0][1]` the sep19 way (IndexError with the flat split)
    _CL18A_SEP19_PATH = _re.compile(r"/_work/_2018/(cramer/|div_curl/(ShowTwoPopulations|PhaseSpaceOfPopulationModel)\.py)")   # scenes that index `OldTex(...)[0][i]`; the rest index the flat glyphs
    _cl18a_flat_split = OldTex.split

    def _cl18a_oldtex_split(self):
        if _CL18A_SEP19_PATH.search(_cl19_caller_path(2)):
            return super(OldTex, self).split()
        return _cl18a_flat_split(self)

    OldTex.split = _cl18a_oldtex_split


# CL18-A: Cairo's MobjectMatrix(array_of_mobjects) took the mobjects as a matrix (a flat array = one column) and kept their size. GL's
# MobjectMatrix(group, n_rows, n_cols, height=4.0) lays a flat group out as a row-major grid and scales it to height 4, so
# `MobjectMatrix(matrix.mob_matrix[:, i])` came out as a giant row. When given a list/array, build the Cairo matrix. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.mobject.matrix import MobjectMatrix as _Cl18aMobjectMatrix
    _cl18a_old_mobject_matrix_init = _Cl18aMobjectMatrix.__init__

    @_wraps(_cl18a_old_mobject_matrix_init)
    def _cl18a_mobject_matrix_init(self, group, *args, **kwargs):
        if isinstance(group, (list, tuple, np.ndarray)) and len(group) > 0:
            if isinstance(group[0], (list, tuple, np.ndarray)):
                rows = [list(row) for row in group]
            else:
                rows = [[mob] for mob in group]
            kwargs.setdefault("height", None)
            kwargs.setdefault("element_alignment_corner", ORIGIN)
            _ClMatrix.__init__(self, rows, **kwargs)
        else:
            _cl18a_old_mobject_matrix_init(self, group, *args, **kwargs)

    _Cl18aMobjectMatrix.__init__ = _cl18a_mobject_matrix_init


# CL18-A: Matrix.copy() of GL rebuilds `elements` as a plain list; Cairo scenes keep calling VGroup methods on the copy
# (`equation.target[2].elements.get_color()`). Same 2018-only treatment as the constructor above.
if _CAIRO_ERA and _CL18_2018:
    _cl18a_old_matrix_copy = _ClMatrix.copy

    @_wraps(_cl18a_old_matrix_copy)
    def _cl18a_matrix_copy(self, *args, **kwargs):
        result = _cl18a_old_matrix_copy(self, *args, **kwargs)
        if isinstance(result.elements, list):
            result.elements = VGroup(*result.elements)
        return result

    _ClMatrix.copy = _cl18a_matrix_copy


# CL18-A: consecutive methods of the SAME mobject in one play call (`self.play(m.next_to, b, UP, m.shift, v)`) were ONE MoveToTarget in
# Cairo (compile_method: the later methods are applied to the same `mobject.target`, so their effects add up). manim_imports_ext builds
# one ApplyMethod per method instead, each aiming at its own target computed from the original state, so only the last one shows
# (for_flammy IntegralSymbols: the "circumference" label never moved above its brace). A single method also becomes a MoveToTarget, as in
# Cairo, which leaves `mobject.target` behind (gauss ShowRowReduction: `row1.set_color` in play(), then `row1.target.next_to(...)`). The groups are merged before the old
# play() runs. A dict after a method's arguments is that method's kwargs (Cairo did the same). 2018 only.
if _CAIRO_ERA and _CL18_2018:
    _cl18a_old_play = Scene.play

    def _cl18a_is_method(arg):
        return _inspect.ismethod(arg) and isinstance(arg.__self__, Mobject)

    def _cl18a_group_methods(args):
        """[(method, [args], kwargs)] for consecutive methods, or None if args[0] is not a method."""
        groups, i = [], 0
        while i < len(args) and _cl18a_is_method(args[i]):
            method, rest = args[i], []
            i += 1
            while i < len(args) and not (isinstance(args[i], Animation) or _cl18a_is_method(args[i])
                                         or type(args[i]).__name__ == "_AnimationBuilder"):
                rest.append(args[i])
                i += 1
            kwargs = {}
            if rest and isinstance(rest[-1], dict):
                kwargs = rest.pop()
            groups.append((method, rest, kwargs, i))
        return groups

    @_wraps(_cl18a_old_play)
    def _cl18a_play(self, *args, **kwargs):
        new_args, i = [], 0
        args = list(args)
        while i < len(args):
            if not _cl18a_is_method(args[i]):
                new_args.append(args[i])
                i += 1
                continue
            groups = _cl18a_group_methods(args[i:])
            consumed = groups[-1][3]
            # split into runs of the same mobject
            run_start = 0
            while run_start < len(groups):
                mobject = groups[run_start][0].__self__
                run_end = run_start
                while run_end + 1 < len(groups) and groups[run_end + 1][0].__self__ is mobject:
                    run_end += 1
                run = groups[run_start:run_end + 1]
                restore = any(g[0].__func__ is Mobject.restore for g in run)
                if restore:
                    for method, rest, mkwargs, _ in run:
                        new_args.append(method)
                        new_args.extend(rest + ([mkwargs] if mkwargs else []))
                else:
                    mobject.generate_target()
                    for method, rest, mkwargs, _ in run:
                        method.__func__(mobject.target, *rest, **mkwargs)
                    new_args.append(MoveToTarget(mobject))
                run_start = run_end + 1
            i += consumed
        return _cl18a_old_play(self, *new_args, **kwargs)

    Scene.play = _cl18a_play


# CL18-D: GL's ThreeDScene.add iterates the mobjects before calling Scene.add, so ContinualAnimation objects (CL18-D) never
# reached the patched Scene.add. Convert them here, then register them once the scene has added their mobjects. 2018 only.
if _CL18_2018:
    _cl18d_3d_add = ThreeDScene.add

    @_wraps(_cl18d_3d_add)
    def _cl18d_threed_add(self, *items, **kwargs):
        cas = [item for item in items if isinstance(item, ContinualAnimation)]
        if not cas:
            return _cl18d_3d_add(self, *items, **kwargs)
        plain = [ca.mobject if isinstance(ca, ContinualAnimation) else ca for ca in items]
        self.__dict__["_cl18_adding"] = True
        try:
            _cl18d_3d_add(self, *plain, **kwargs)
        finally:
            self.__dict__["_cl18_adding"] = False
        for ca in cas:
            ca._cl18_attach()
            if ca not in _cl18_scene_cas(self):
                _cl18_scene_cas(self).append(ca)
        return self

    ThreeDScene.add = _cl18d_threed_add


# CL18-B: Cairo's Mobject.copy() (copy.copy based) kept the saved_state attribute, so ApplyMethod(mob.custom_method) ->
# custom_method calls self.restore() on the *copy* worked (eop SicklyPiCreature.get_better). GL's copy() resets
# saved_state to None ("Trying to restore without having saved"). Keep the reference on copies. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    _clb_mobject_copy = Mobject.copy

    @_wraps(_clb_mobject_copy)
    def _clb_copy_keep_saved_state(self, deep=False):
        result = _clb_mobject_copy(self, deep)
        saved = self.__dict__.get("saved_state")
        if saved is not None and result.__dict__.get("saved_state") is None:
            result.saved_state = saved
        return result

    Mobject.copy = _clb_copy_keep_saved_state


# CL18-C: NumberLine.get_tick_numbers() of Cairo (the tick values from leftmost_tick to x_max); GL names it get_tick_range(). New method, no era flag.
if not hasattr(NumberLine, "get_tick_numbers"):
    NumberLine.get_tick_numbers = lambda self: self.get_tick_range()


# CL18-B: Cairo digest_config applied CONFIG values (color, fill_color, fill_opacity, stroke_color, stroke_width, radius, width,
# height, ...) as constructor defaults of the manim base class: `class UprightCoin(Circle): CONFIG = {"radius": 0.18, "stroke_color": WHITE,
# "fill_opacity": 1}` made a small white-edged filled coin. manim_imports_ext turns CONFIG keys into class attributes only
# ("does not reach the __init__ parameters of the manimgl classes"), so GL built the default Circle (radius 1, red edge, no fill).
# Wrap the __init__ of the GL VMobject/geometry classes: a parameter that is named in the CONFIG of the instance's class and
# was not passed explicitly takes the CONFIG value. 2018 only.
if _CAIRO_ERA and _CL18_GEOM:
    import manimlib.mobject.geometry as _clb_geometry
    from manimlib.mobject.types.vectorized_mobject import VMobject as _ClBVMobject

    def _clb_wrap_config_init(cls):
        original = cls.__dict__.get("__init__")
        if original is None or getattr(original, "_clb_config_wrapped", False):
            return
        try:
            signature = _inspect.signature(original)
        except (TypeError, ValueError):
            return
        names = [n for n, p in signature.parameters.items()
                 if n != "self" and p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
        positional = [n for n, p in signature.parameters.items()
                      if n != "self" and p.kind == p.POSITIONAL_OR_KEYWORD]

        @_wraps(original)
        def init(self, *args, **kwargs):
            keys = getattr(type(self), "_config_keys", ())
            if keys:
                given = set(kwargs) | set(positional[:len(args)])
                for name in names:
                    if name in keys and name not in given:
                        kwargs[name] = getattr(type(self), name)
                        _cl18_geom_probe("config", type(self).__name__, name, kwargs[name])
            return original(self, *args, **kwargs)

        init._clb_config_wrapped = True
        cls.__init__ = init

    _clb_wrap_config_init(_ClBVMobject)
    for _clb_obj in list(vars(_clb_geometry).values()):
        if isinstance(_clb_obj, type) and issubclass(_clb_obj, _ClBVMobject) and _clb_obj.__module__ == _clb_geometry.__name__:
            _clb_wrap_config_init(_clb_obj)


# CL18-B: Cairo's Color() accepted color names ("red", "PURPLE", "blue_d") wherever a color goes (set_stroke("red", 5)); GL's
# hex_to_rgb only parses hex strings and raises "Invalid value 'red' provided for rgb color". Fall back to the manim color
# constants (RED, PURPLE, BLUE_D...) by name. color_to_rgb looks hex_to_rgb up as a module global, so patching it here reaches
# every caller. Only strings that used to raise are affected.
if _CAIRO_ERA:
    import manimlib.utils.color as _clb_color_module
    import manimlib.constants as _clb_constants_module

    _clb_orig_hex_to_rgb = _clb_color_module.hex_to_rgb

    def _clb_hex_to_rgb(hex_code):
        try:
            return _clb_orig_hex_to_rgb(hex_code)
        except ValueError:
            value = getattr(_clb_constants_module, str(hex_code).strip().upper().replace(" ", "_"), None)
            if isinstance(value, str):
                return _clb_orig_hex_to_rgb(value)
            raise

    _clb_color_module.hex_to_rgb = _clb_hex_to_rgb


# CL18-C: NumberLine.add_numbers() without arguments (2018 only). 3feb showed `numbers_to_show` or, by default, the integers from int(leftmost_tick) to int(x_max)
# (default_numbers_to_display); GL labels every tick, so a 0.25 tick step gave rows of "0 0 0 0 1 1 1 1" labels (fourier time axes).
if _CAIRO_ERA and _CL18_2018:
    _cl18c_old_add_numbers = NumberLine.add_numbers

    @_wraps(_cl18c_old_add_numbers)
    def _cl18c_add_numbers(self, *args, **kwargs):
        if not args and "x_values" not in kwargs and getattr(self, "_legacy_numbers_to_show", None) is None:
            step = self.x_step or 1
            first = step * np.ceil(round(self.x_min / step, 9))
            args = ([int(v) for v in np.arange(int(first), int(self.x_max) + 1)],)
        return _cl18c_old_add_numbers(self, *args, **kwargs)

    NumberLine.add_numbers = _cl18c_add_numbers


# CL18-C: NumberLine.pieces of Cairo 3feb (the axes of SpecialThreeDScene were cut in several line pieces; scenes do axis.pieces.set_stroke(width=1/0)).
# GL's NumberLine is a single line (+ ticks as submobjects), so `pieces` answers a proxy that applies set_stroke to the line itself only (recurse=False). 2018 only.
if _CAIRO_ERA and _CL18_2018 and not hasattr(NumberLine, "pieces"):
    class _Cl18cLinePieces:
        def __init__(self, line):
            self._line = line

        def set_stroke(self, *args, **kwargs):
            self._line.set_stroke(*args, recurse=False, **kwargs)
            return self

        def __getattr__(self, name):
            return getattr(self._line, name)

    NumberLine.pieces = property(lambda self: _Cl18cLinePieces(self))


# CL18-E: Cairo's Arc kept its `angle` and `start_angle` as attributes (wallis: `path_arc=O_to_N_arc.angle - arc.angle`);
# GL's Arc does not store them (AttributeError). Record them after construction (same defaults as GL: 0 and TAU/4). 2018 only.
if _CL18_2018:
    _cl18e_arc_init = Arc.__init__

    @_wraps(_cl18e_arc_init)
    def _cl18e_arc_init_attrs(self, *args, **kwargs):
        # Circle(radius=-6) / Arc(radius=-r): a negative radius is a mirrored circle in Cairo (same picture); in GL it collapses to a point
        if kwargs.get("radius") is not None and kwargs["radius"] < 0:
            kwargs["radius"] = abs(kwargs["radius"])
        _cl18e_arc_init(self, *args, **kwargs)
        if len(args) == 1 and "angle" not in kwargs:
            start_angle, angle = kwargs.get("start_angle", 0), args[0]
        else:
            start_angle = args[0] if len(args) > 0 else kwargs.get("start_angle", 0)
            angle = args[1] if len(args) > 1 else kwargs.get("angle", TAU / 4)
        self.__dict__.setdefault("start_angle", start_angle)
        self.__dict__.setdefault("angle", angle)

    Arc.__init__ = _cl18e_arc_init_attrs


# CL18-E: Cairo's Scene.frame_duration (seconds per frame, 1 / frame_rate); used by `self.wait(self.frame_duration)` and
# per-frame shifts. New attribute, nothing wrapped.
if not hasattr(Scene, "frame_duration"):
    Scene.frame_duration = property(lambda self: 1.0 / self.camera.fps)


# CL18-E: Cairo's Animation.update_config(**kwargs) (sets attributes such as rate_func/run_time on an animation reused
# across several play() calls; uncertainty ShowMomentumFormula). New method, nothing wrapped.
if not hasattr(Animation, "update_config"):
    def _cl18e_update_config(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    Animation.update_config = _cl18e_update_config


# CL18-D: Cairo's move_points_along_vector_field(mobject, func) had no coordinate_system (func(point) -> velocity in scene
# coordinates); GL's requires one and calls func with coordinates. Without a coordinate system keep the Cairo behaviour. 2018 only.
if _CL18_2018:
    from manimlib.mobject.vector_field import move_points_along_vector_field as _cl18d_gl_move_points

    def move_points_along_vector_field(mobject, func, coordinate_system=None):
        if coordinate_system is not None:
            return _cl18d_gl_move_points(mobject, func, coordinate_system)

        def apply_nudge(mob, dt):
            mob.apply_function(lambda p: p + func(p) * dt)
        mobject.add_updater(apply_nudge)
        return mobject

    __all__.append("move_points_along_vector_field")


# CL18-C: three Cairo 3feb APIs used by quaternions/div_curl (2018 only).
# 1) VMobject.match_background_image_file(other) / get_background_image_file(): color this mobject with the background image of `other` (shim of color_using_background_image).
# 2) Camera.is_in_frame(mobject): whether the mobject's bounding box overlaps the frame (2D check on the frame rectangle).
# 3) ThreeDScene.begin_ambient_camera_rotation exposes `scene.ambient_camera_rotation` with a mutable `.rate` (scenes do self.ambient_camera_rotation.rate = 0.01).
if _CAIRO_ERA and _CL18_2018:
    if not hasattr(VMobject, "get_background_image_file"):
        VMobject.get_background_image_file = lambda self: getattr(self, "background_image_file", None)

    def _cl18c_match_background_image_file(self, vmobject):
        self.color_using_background_image(vmobject.get_background_image_file())
        return self

    if not hasattr(VMobject, "match_background_image_file"):
        VMobject.match_background_image_file = _cl18c_match_background_image_file

    def _cl18c_is_in_frame(self, mobject):
        frame = self.frame
        center = frame.get_center()
        half_w, half_h = frame.get_width() / 2, frame.get_height() / 2
        return not any([
            mobject.get_right()[0] < center[0] - half_w,
            mobject.get_left()[0] > center[0] + half_w,
            mobject.get_top()[1] < center[1] - half_h,
            mobject.get_bottom()[1] > center[1] + half_h,
        ])

    if not hasattr(_Camera, "is_in_frame"):
        _Camera.is_in_frame = _cl18c_is_in_frame

    def _cl18c_begin_ambient_camera_rotation(self, rate=0.02):
        self.stop_ambient_camera_rotation()
        state = _types.SimpleNamespace(rate=rate)
        self.ambient_camera_rotation = state
        self._cairo_ambient_rotation = lambda frame, dt: frame.increment_theta(state.rate * dt)
        self.frame.add_updater(self._cairo_ambient_rotation)
        return self

    ThreeDScene.begin_ambient_camera_rotation = _cl18c_begin_ambient_camera_rotation


# CL18-D: an SVG path without a fill attribute is black by the SVG standard (svgelements), so SVGMobject("plane2") was black on
# the black background; Cairo's SVGMobject left such paths in the mobject's default colour (white). svg_default only fills what the
# file does not specify, so explicit fills/strokes of the file and scene kwargs (fill_color=, color=) are untouched. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.mobject.svg.svg_mobject import SVGMobject as _ClDSVGMobject

    _cl18d_svg_init = _ClDSVGMobject.__init__

    @_wraps(_cl18d_svg_init)
    def _cl18d_svg_mobject_init(self, *args, **kwargs):
        default = dict(kwargs.pop("svg_default", None) or {})
        if default.get("fill_color") is None and default.get("color") is None:
            default["fill_color"] = "#FFFFFF"
        for key in ("color", "opacity", "fill_color", "fill_opacity", "stroke_width", "stroke_color", "stroke_opacity"):
            default.setdefault(key, None)
        _cl18d_svg_init(self, *args, svg_default=default, **kwargs)

    _ClDSVGMobject.__init__ = _cl18d_svg_mobject_init


# CL18-A: Cairo Camera.extract_mobject_family_members(mobjects, only_those_with_points=False) (used as `word in self.camera.extract_mobject_family_members(self.mobjects)`
# to ask whether a mobject is on screen; WindingNumber_G TransitionFromEquationSolverToZeroFinder). New method, no era flag.
from manimlib.camera.camera import Camera as _Cl18aCamera
from manimlib.utils.family_ops import extract_mobject_family_members as _cl18a_extract_family
if not hasattr(_Cl18aCamera, "extract_mobject_family_members"):
    def _cl18a_camera_extract_family(self, mobjects, only_those_with_points=False):
        family = _cl18a_extract_family(mobjects)
        return [m for m in family if m.has_points()] if only_those_with_points else family
    _Cl18aCamera.extract_mobject_family_members = _cl18a_camera_extract_family


# CL18-D: Cairo merged consecutive method animations of the SAME mobject into one animation
# (`self.play(sphere.scale, 0.75, sphere.shift, 3 * LEFT)` applied both; the shim in manim_imports_ext builds one ApplyMethod per
# method, and the last one on the same mobject wins, so the scale was lost), and a trailing dict after a method's arguments was
# that method's kwargs (`mobs.scale, 2, {"about_point": ORIGIN}`). Merged into one Transform to a copy that received every call
# in order. 2018 only.
if _CL18_2018:
    from manimlib.mobject.mobject import _AnimationBuilder as _ClDAnimationBuilder

    _cl18d_play_prev = Scene.play

    def _cl18d_is_method(arg):
        return _inspect.ismethod(arg) and isinstance(arg.__self__, Mobject) and arg.__func__ is not Mobject.restore

    @_wraps(_cl18d_play_prev)
    def _cl18d_play(self, *proto_animations, **kwargs):
        out = []
        args = list(proto_animations)
        while args:
            arg = args.pop(0)
            if not _cl18d_is_method(arg):
                out.append(arg)
                continue
            calls = []
            while True:
                margs, mkw = [], {}
                # CL18-D: a following `x.restore` also ends this method's arguments (it is not merged, it is left to manim_imports_ext)
                while args and not (isinstance(args[0], (Animation, _ClDAnimationBuilder)) or _cl18d_is_method(args[0])
                                    or (_inspect.ismethod(args[0]) and isinstance(args[0].__self__, Mobject))):
                    item = args.pop(0)
                    if isinstance(item, dict):
                        mkw.update(item)
                    else:
                        margs.append(item)
                calls.append((arg, margs, mkw))
                if args and _cl18d_is_method(args[0]) and args[0].__self__ is arg.__self__:
                    arg = args.pop(0)
                    continue
                break
            if len(calls) == 1 and not calls[0][2]:
                out.append(calls[0][0])
                out.extend(calls[0][1])
                continue
            mob = calls[0][0].__self__
            target = mob.copy()
            for method, margs, mkw in calls:
                method.__func__(target, *margs, **mkw)
            out.append(Transform(mob, target))
        return _cl18d_play_prev(self, *out, **kwargs)

    Scene.play = _cl18d_play


# CL18-D: GL's TeacherStudentsScene paints a GREY_E full-screen background (design of the newest videos); Cairo's was black
# (everything looked washed out and the pi creatures lost contrast). Black background for 2018 scenes.
if _CAIRO_ERA and _CL18_2018:
    from custom.characters.pi_creature_scene import TeacherStudentsScene as _ClDTeacherStudentsScene
    _ClDTeacherStudentsScene.background_color = BLACK

    def _cl18d_no_background(self, color=None):
        # the scene background is already black; the extra full-screen rectangle hides 2D mobjects (depth writes)
        self.background = VectorizedPoint()

    _ClDTeacherStudentsScene.add_background = _cl18d_no_background


# CL18-C: Circle.surround(mobject, buffer_factor=1.2) of 3feb: a circle circumscribing the mobject (diagonal width) scaled by buffer_factor. GL's Circle.surround
# is the Mobject one with an additive `buff` and a stretched ellipse. 2018 only; `buff=` still uses GL's version.
if _CAIRO_ERA and _CL18_2018:
    _cl18c_old_circle_surround = Circle.surround

    @_wraps(_cl18c_old_circle_surround)
    def _cl18c_circle_surround(self, mobject, dim_to_match=0, stretch=False, buffer_factor=None, buff=None):
        if buff is not None and buffer_factor is None:
            return _cl18c_old_circle_surround(self, mobject, dim_to_match, stretch, buff)
        self.replace(mobject, dim_to_match, stretch)
        self.set_width(np.sqrt(mobject.get_width() ** 2 + mobject.get_height() ** 2))
        self.scale(1.2 if buffer_factor is None else buffer_factor)
        return self

    Circle.surround = _cl18c_circle_surround


# CL18-D: Cairo WiggleOutThenIn(mob, scale_value=, angle=, ...): the rotation amplitude was called `angle`; GL calls it
# rotation_angle (an unknown kwarg raised "Animation.__init__() got an unexpected keyword argument 'angle'"). 2018 only.
if _CL18_2018:
    from manimlib.animation.indication import WiggleOutThenIn as _ClDWiggle
    _cl18d_wiggle_init = _ClDWiggle.__init__

    @_wraps(_cl18d_wiggle_init)
    def _cl18d_wiggle_new_init(self, *args, angle=None, **kwargs):
        if angle is not None:
            kwargs.setdefault("rotation_angle", angle)
        _cl18d_wiggle_init(self, *args, **kwargs)

    _ClDWiggle.__init__ = _cl18d_wiggle_new_init


# CL18-C: axes.get_graph(func, num_graph_points=100, ...) of 3feb (2018 only). The kwarg was the number of sampled anchors (Cairo then smoothed them with cubic
# Beziers); GL ignores it and samples every tick/5. Scenes that map the graph through a nonlinear function (fourier: apply_function to polar coordinates, winding
# a 13-cycle wave around a circle) need the anchors dense enough for GL's quadratic curves, otherwise the wound curve is jagged. Samples 4x the Cairo count.
if _CAIRO_ERA and _CL18_2018:
    _cl18c_old_get_graph = CoordinateSystem.get_graph

    @_wraps(_cl18c_old_get_graph)
    def _cl18c_get_graph(self, function, *args, num_graph_points=None, **kwargs):
        if num_graph_points and "step_size" not in kwargs:
            lo = kwargs.get("x_min", self.x_range[0] if len(args) < 1 or args[0] is None else args[0][0])
            hi = kwargs.get("x_max", self.x_range[1] if len(args) < 1 or args[0] is None else args[0][1])
            kwargs["step_size"] = (hi - lo) / (4 * num_graph_points)
            kwargs.setdefault("x_min", lo)
            kwargs.setdefault("x_max", hi)
            args = ()
        return _cl18c_old_get_graph(self, function, *args, **kwargs)

    CoordinateSystem.get_graph = _cl18c_get_graph


# CL18-D: old camera API `camera.spherical_coords_to_point(phi, theta, rho)` (basel::ScreenShapingScene). New method, no flag.
if not hasattr(_Camera, "spherical_coords_to_point"):
    _Camera.spherical_coords_to_point = lambda self, phi, theta, rho: _cl18d_spherical(phi, theta, rho)


# CL18-C: look of 3feb axes and number lines compared with the Cairo frames (2018 only; measured on fourier DrawFrequencyPlot, 3feb vs GL):
# - Axes (plain Axes only; NumberPlane/ThreeDAxes keep their own defaults) had arrow tips by default (number_line_config include_tip=True);
# - NumberLine lines were stroke_width 4 (GL: 2);
# - axis numbers were about 1.8x taller than GL's add_numbers font_size=24 (-> 44) (Cairo: DecimalNumber scaled by number_scale_val 0.75 of the Tex default height).
if _CAIRO_ERA and _CL18_2018:
    _cl18c_old_axes_init = Axes.__init__

    @_wraps(_cl18c_old_axes_init)
    def _cl18c_axes_init(self, *args, **kwargs):
        if type(self) is Axes:
            axis_config = dict(kwargs.get("axis_config") or {})
            axis_config.setdefault("include_tip", True)
            kwargs["axis_config"] = axis_config
        _cl18c_old_axes_init(self, *args, **kwargs)

    Axes.__init__ = _cl18c_axes_init

    _cl18c_old_number_line_init = NumberLine.__init__

    @_wraps(_cl18c_old_number_line_init)
    def _cl18c_number_line_init(self, *args, **kwargs):
        kwargs.setdefault("stroke_width", 4.0)
        _cl18c_old_number_line_init(self, *args, **kwargs)

    NumberLine.__init__ = _cl18c_number_line_init

    _cl18c_old_add_numbers2 = NumberLine.add_numbers

    @_wraps(_cl18c_old_add_numbers2)
    def _cl18c_add_numbers_size(self, *args, **kwargs):
        kwargs.setdefault("font_size", 44)
        return _cl18c_old_add_numbers2(self, *args, **kwargs)

    NumberLine.add_numbers = _cl18c_add_numbers_size


# CL18-E: Cairo's NumberPlane.secondary_lines (the faint grid lines between the main ones). GL names them `faded_lines`.
# Read-only alias, 2018 only (uncertainty CenterOfMassDescription; WindingNumber_G of A also reads it).
if _CL18_2018 and not hasattr(NumberPlane, "secondary_lines"):
    NumberPlane.secondary_lines = property(lambda self: self.faded_lines)


# CL18-E: lights of once_useful_constructs/light.py (AmbientLight, Spotlight, LightSource) build their annuli/sectors in
# init_points(), which Mobject.__init__ calls BEFORE VMobject.__init__ applies its style. In this GL the style is applied
# recursively afterwards (fill_opacity=0, default stroke), so every annulus lost its opacity and got a visible stroke:
# the glow became concentric yellow rings (basel/wallis) or a solid disc. init_points() is written to be re-callable
# (it removes the old submobjects), so call it once more after construction. Also GL's Annulus(color=...) ignores `color`
# (its fill_color defaults to grey): use it as the fill colour like Cairo. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    from manimlib.mobject.geometry import Annulus as _ClEAnnulus
    _cl18e_annulus_init = _ClEAnnulus.__init__

    @_wraps(_cl18e_annulus_init)
    def _cl18e_annulus_init_color(self, *args, **kwargs):
        if "color" in kwargs and "fill_color" not in kwargs:
            kwargs["fill_color"] = kwargs["color"]
        _cl18e_annulus_init(self, *args, **kwargs)

    _ClEAnnulus.__init__ = _cl18e_annulus_init_color

    import once_useful_constructs.light as _cl18e_light
    for _cl18e_name in ("AmbientLight", "Spotlight", "LightSource"):
        _cl18e_cls = getattr(_cl18e_light, _cl18e_name, None)
        if _cl18e_cls is None:
            continue

        def _cl18e_make(cls):
            orig_init = cls.__init__

            @_wraps(orig_init)
            def init_twice(self, *args, **kwargs):
                orig_init(self, *args, **kwargs)
                self.set_submobjects([])   # (the removal loop in init_points skips every other child)
                self.init_points()
            return init_twice

        _cl18e_cls.__init__ = _cl18e_make(_cl18e_cls)


# CL18-D: NumberLine.get_number_mobjects() without arguments in 3feb used default_numbers_to_display(): `numbers_to_show` if the line
# had it, else the integers int(leftmost_tick)..int(x_max). The CL19 shim labelled every tick (0.2 steps: rows of "0 0 1 1 1 1 2 2").
# Same default as CL18-C's add_numbers. 2018 only.
if _CAIRO_ERA and _CL18_2018:
    _cl18d_old_get_number_mobjects = NumberLine.get_number_mobjects

    @_wraps(_cl18d_old_get_number_mobjects)
    def _cl18d_get_number_mobjects(self, *numbers, **kwargs):
        if not numbers:
            legacy = getattr(self, "_legacy_numbers_to_show", None)
            if legacy is not None:
                numbers = [int(v) if float(v).is_integer() else v for v in legacy]
            else:
                step = self.x_step or 1
                first = step * np.ceil(round(self.x_min / step, 9))
                numbers = [int(v) for v in np.arange(int(first), int(self.x_max) + 1)]
        return _cl18d_old_get_number_mobjects(self, *numbers, **kwargs)

    NumberLine.get_number_mobjects = _cl18d_get_number_mobjects


# CL18-E: color= of shapes. In Cairo `Circle(color=BLUE)`, `Dot(p, color=YELLOW)`, `Sector(color=...)`, `Arrow(color=...)` coloured the shape.
# GL's constructors give their own defaults priority over `color` (Circle stroke_color=RED, Dot/AnnularSector/Arrow fill_color=white/grey),
# so every such shape silently kept the default colour (found comparing lost_lecture::ShowEmergingEllipse with Cairo: red circle, white dots).
# Use `color` as that default when the specific colour is not given. 2018 only.
if _CAIRO_ERA and _CL18_GEOM:
    from manimlib.mobject.geometry import Circle as _ClECircle, Dot as _ClEDot, AnnularSector as _ClESector, Arrow as _ClEArrow

    def _cl18e_color_default(cls, key):
        orig = cls.__init__

        @_wraps(orig)
        def init(self, *args, **kwargs):
            if kwargs.get("color") is not None and key not in kwargs:
                kwargs[key] = kwargs["color"]
                try:
                    _default = _inspect.signature(orig).parameters[key].default
                except (KeyError, TypeError, ValueError):
                    _default = None
                _cl18_geom_probe("color", type(self).__name__, key, kwargs[key], _default)
            orig(self, *args, **kwargs)
        cls.__init__ = init

    _cl18e_color_default(_ClECircle, "stroke_color")
    _cl18e_color_default(_ClEDot, "fill_color")
    _cl18e_color_default(_ClESector, "fill_color")
    _cl18e_color_default(_ClEArrow, "fill_color")


# ======================================================================================================================
# CL17-A (2017: eoc, tattoo, qa_round_two, gradient, putnam). All of this only applies to scenes under /_2017/.
# ======================================================================================================================
if _CAIRO_ERA and _CL17_2017:
    import fractions as _cl17a_fractions
    import math as _cl17a_math
    import random as _cl17a_random

    # CL17-A: `fractions.gcd` was removed in Python 3.9 (eoc/chapter9 TryToAddInfinitelyManyPoints).
    if not hasattr(_cl17a_fractions, "gcd"):
        _cl17a_fractions.gcd = _cl17a_math.gcd

    # CL17-A: custom/drawings.py (read-only) uses DISTANCE_COLOR in Car.get_front_line() but never defines it (the eoc chapters did,
    # as BLUE): NameError for every Car scene (eoc/chapter2 IntroduceCar...). Inject the name into that module.
    import custom.drawings as _cl17a_drawings
    if not hasattr(_cl17a_drawings, "DISTANCE_COLOR"):
        _cl17a_drawings.DISTANCE_COLOR = BLUE

    # CL17-A: Cairo's `Mobject(*mobjects)` was a plain container (eoc: `Brace(Mobject(*men[:3]), UP)`); GL's Mobject.__init__ takes
    # (color, opacity, ...), so the mobjects were taken as colours ("setting an array element with a sequence").
    _cl17a_mobject_init = Mobject.__init__

    @_wraps(_cl17a_mobject_init)
    def _cl17a_mobject_init_wrapper(self, *args, **kwargs):
        if args and all(isinstance(a, Mobject) for a in args):
            _cl17a_mobject_init(self, **kwargs)
            self.add(*args)
            return
        _cl17a_mobject_init(self, *args, **kwargs)

    Mobject.__init__ = _cl17a_mobject_init_wrapper

    # CL17-A: `mob.next_to(..., align_using_submobjects=True)` (27 eoc scene copies): not a parameter of next_to in sep19/GL; the
    # flag only chose which sub-box to align. Accepted and ignored.
    _cl17a_next_to = Mobject.next_to

    @_wraps(_cl17a_next_to)
    def _cl17a_next_to_wrapper(self, *args, align_using_submobjects=None, **kwargs):
        return _cl17a_next_to(self, *args, **kwargs)

    Mobject.next_to = _cl17a_next_to_wrapper

    # CL17-A: `random_blink(num_times=1)` of the 2016-17 PiCreatureScene (removed before sep19; tattoo, eoc): one random pi creature blinks per call.
    from custom.characters.pi_creature_scene import PiCreatureScene as _Cl17aPiCreatureScene
    if not hasattr(_Cl17aPiCreatureScene, "random_blink"):
        def _cl17a_random_blink(self, num_times=1):
            for _ in range(int(num_times)):
                self.blink()
        _Cl17aPiCreatureScene.random_blink = _cl17a_random_blink

    # CL17-A: 2017 code is from the 3feb era, where TextMobject joined several arguments with " " ("From day", "5" -> "From day 5"); teacher_says("a", "b", target_mode=..)
    # / student_says / pi_creature_says(..., "a", "b") take any number of content arguments. GL's teacher_says/student_says take exactly one
    # (TypeError: takes 2 positional arguments but 3 were given). Pre-join them here with " " (the same as CL18-B).
    from custom.characters.pi_creature import PiCreature as _Cl17aPiCreature

    def _cl17a_join_content(content):
        if len(content) <= 1:
            return content
        if all(isinstance(c, str) for c in content):
            return (" ".join(content),)
        return (OldTexText(*content),)

    def _cl17a_prejoin_wrapper(orig, leading_creature):
        @_wraps(orig)
        def wrapper(self, *args, **kwargs):
            # teacher_says(..., width=5, height=5): Cairo passed them on to the bubble
            if "width" in kwargs or "height" in kwargs:
                bubble_config = dict(kwargs.get("bubble_config") or {})
                for key in ("width", "height"):
                    if key in kwargs:
                        bubble_config[key] = kwargs.pop(key)
                kwargs["bubble_config"] = bubble_config
            if leading_creature and args and isinstance(args[0], _Cl17aPiCreature):
                return orig(self, args[0], *_cl17a_join_content(args[1:]), **kwargs)
            if leading_creature:
                return orig(self, *_cl17a_join_content(args), **kwargs)
            return orig(self, *_cl17a_join_content(args), **kwargs)
        return wrapper

    from custom.characters.pi_creature_scene import TeacherStudentsScene as _Cl17aTSS
    for _cl17a_name in ("pi_creature_says", "pi_creature_thinks", "introduce_bubble"):
        setattr(_Cl17aPiCreatureScene, _cl17a_name, _cl17a_prejoin_wrapper(getattr(_Cl17aPiCreatureScene, _cl17a_name), True))
    for _cl17a_name in ("teacher_says", "student_says", "teacher_thinks", "student_thinks"):
        if hasattr(_Cl17aTSS, _cl17a_name):
            setattr(_Cl17aTSS, _cl17a_name, _cl17a_prejoin_wrapper(getattr(_Cl17aTSS, _cl17a_name), False))

    # CL17-A: eoc OpeningQuote subclasses give `highlighted_quote_terms` as a dict ({"almost obvious": BLUE}); custom/opening_quote.py
    # (read-only) iterates it as (term, colour) pairs -> "too many values to unpack" (every eoc chapterNOpeningQuote).
    from custom.opening_quote import OpeningQuote as _Cl17aOpeningQuote
    _cl17a_get_quote = _Cl17aOpeningQuote.get_quote

    @_wraps(_cl17a_get_quote)
    def _cl17a_get_quote_wrapper(self, *args, **kwargs):
        terms = getattr(self, "highlighted_quote_terms", None)
        if isinstance(terms, dict):
            self.highlighted_quote_terms = list(terms.items())
        return _cl17a_get_quote(self, *args, **kwargs)

    _Cl17aOpeningQuote.get_quote = _cl17a_get_quote_wrapper


# CL17-B: `shade_in_3d(mobject)` was a free function of the 2017-era Cairo manim (bell, waves, mug use it); neither 3feb nor sep19 nor GL has it.
# New name, no era flag: marks the whole family as depth-tested (what Cairo's flag meant).
def shade_in_3d(mobject, value=True):
    mobject.set_shade_in_3d(value)
    return mobject


__all__.append("shade_in_3d")


# CL17-A: OldTexText(*strings) joins with " " for 2017 as well: the 2017 scripts were written for the 3feb-era TextMobject (arg_separator " ";
# eoc/chapter5 `OldTexText("From day", str(n), "to", str(n+1), ":")` came out as "From day5to6:"). sep19 changed TextMobject to "".
# Same mechanism as CL18-B (the regex only matches /2017/ paths here).
_CL19_SPACED_TEXT_PATH = _re.compile(_CL19_SPACED_TEXT_PATH.pattern + r"|/_?2017/")

# CL17-A: VMobject.set_style_data(stroke_color, stroke_width, fill_color, fill_opacity, family=True) of Cairo (GL has set_style): eoc
# CircleScene.get_unwrapped / get_ring and many circle-area scenes. New method, only when missing.
if _CAIRO_ERA and _CL17_2017 and not hasattr(VMobject, "set_style_data"):
    def _cl17a_set_style_data(self, stroke_color=None, stroke_width=None, fill_color=None, fill_opacity=None, family=True):
        if stroke_color is not None or stroke_width is not None:
            self.set_stroke(color=stroke_color, width=stroke_width, recurse=family)
        if fill_color is not None or fill_opacity is not None:
            self.set_fill(color=fill_color, opacity=fill_opacity, recurse=family)
        return self

    VMobject.set_style_data = _cl17a_set_style_data

# CL17-A: 2017 `Car()` (eoc chapters 1-3, 8): sep19/3feb Car builds its own Randolph driver (`car.randy`, `car.pi_creature`, added to the back, so
# self[0] is the driver and self[1] holds the body parts). custom/drawings.py (read-only) dropped the driver (add_driver is broken: it ignores
# its argument and assigns self.pi_creature to itself) and indexes the body parts with self[0]. Rebuild the sep19 Car: driver at the back, body
# parts indexed with self[1].
if _CAIRO_ERA and _CL17_2017:
    import custom.drawings as _cl17a_drawings_mod
    from custom.characters.pi_creature import Randolph as _Cl17aRandolph

    _cl17a_car_init = _cl17a_drawings_mod.Car.__init__

    @_wraps(_cl17a_car_init)
    def _cl17a_car_init_wrapper(self, *args, **kwargs):
        _cl17a_car_init(self, *args, **kwargs)
        randy = _Cl17aRandolph(mode="happy")
        randy.set_height(0.6 * self.get_height())
        randy.stretch(0.8, 0)
        randy.look(RIGHT)
        randy.move_to(self)
        randy.shift(0.07 * self.height * (RIGHT + UP))
        self.randy = self.pi_creature = randy
        self.add_to_back(randy)

    _cl17a_drawings_mod.Car.__init__ = _cl17a_car_init_wrapper
    # (the body parts are self[0] while Car.__init__ runs, before the driver is added at the back, and self[1] afterwards)
    _cl17a_car_body = lambda self: self[1] if getattr(self, "randy", None) is not None else self[0]
    _cl17a_drawings_mod.Car.get_tires = lambda self: VGroup(_cl17a_car_body(self)[0], _cl17a_car_body(self)[1])
    _cl17a_drawings_mod.Car.get_front_light = lambda self: _cl17a_car_body(self)[3]
    _cl17a_drawings_mod.Car.get_rear_light = lambda self: _cl17a_car_body(self)[4]


# CL17-B: nn (neural network videos) builds ImageMobject from numpy arrays (`ImageMobject(layer_to_image_array(v))`, 0..255 ints, 2-D grey or
# RGBA) and reads `image.pixel_array`; Cairo's default height was 2 (GL 4). GL's ImageMobject only takes a file name. Limited to _2017/nn and
# _2017/bell so other 2017 files that already settled their ImageMobject sizes do not move.
_CL17_B_NN = any(_re.search(r"[/\\]_?2017[/\\](nn|bell)[/\\]", str(arg)) for arg in _ARGV_PATHS)
if _CAIRO_ERA and _CL17_2017 and _CL17_B_NN:
    _cl17b_image_init = ImageMobject.__init__

    @_wraps(_cl17b_image_init)
    def _cl17b_image_init_wrapper(self, filename, height=2.0, **kwargs):
        if isinstance(filename, np.ndarray):
            from hashlib import sha256 as _sha256
            from pathlib import Path as _Path
            from PIL import Image as _PILImage
            from manimlib.utils.directories import get_cache_dir as _get_cache_dir

            pixels = np.asarray(filename)
            if pixels.ndim == 3 and pixels.shape[2] == 1:
                pixels = pixels[:, :, 0]
            if np.issubdtype(pixels.dtype, np.floating) and pixels.size and pixels.max() <= 1:
                pixels = pixels * 255
            pixels = np.clip(pixels, 0, 255).astype(np.uint8)
            folder = _Path(_get_cache_dir()) / "cairo_arrays"
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / (_sha256(str(pixels.shape).encode() + pixels.tobytes()).hexdigest() + ".png")
            if not path.exists():
                _PILImage.fromarray(pixels).save(path)
            filename = str(path)
        self._cl17b_ready = False
        _cl17b_image_init(self, filename, height=height, **kwargs)
        self._cl17b_ready = True   # GL's Mobject.__init__ calls set_color(WHITE): must not tint the pixels

    ImageMobject.__init__ = _cl17b_image_init_wrapper

    # Cairo's `pixel_array` was a live, writable RGBA array that the renderer read each frame (`image.pixel_array[:, :, 3] = alpha`,
    # `image.set_color(WHITE)`). Here the array is created on first access and a per-frame updater (a plain function, so copies keep
    # working) writes it back to a PNG and swaps the texture when its content changed.
    def _cl17b_pixel_sync(mob):
        pa = mob.__dict__.get("_cl17b_pa")
        if pa is None:
            return
        sig = hash(pa.tobytes())
        if sig == mob.__dict__.get("_cl17b_pa_sig"):
            return
        from hashlib import sha256 as _sha256
        from pathlib import Path as _Path
        from PIL import Image as _PILImage
        from manimlib.utils.directories import get_cache_dir as _get_cache_dir
        from manimlib.renderer.texture import ImageFile as _ImageFile
        folder = _Path(_get_cache_dir()) / "cairo_arrays"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / (_sha256(str(pa.shape).encode() + pa.tobytes()).hexdigest() + ".png")
        if not path.exists():
            _PILImage.fromarray(pa).save(path)
        mob.textures["Texture"] = _ImageFile(str(path))
        mob._cl17b_pa_sig = sig

    def _cl17b_get_pixel_array(self):
        pa = self.__dict__.get("_cl17b_pa")
        if pa is None:
            pa = np.array(self.image.convert("RGBA"))
            self._cl17b_pa = pa
            self._cl17b_pa_sig = hash(pa.tobytes())
            self.add_updater(_cl17b_pixel_sync)
        return pa

    def _cl17b_set_color(self, color, alpha=None, *args, **kwargs):
        if not self.__dict__.get("_cl17b_ready", False):
            return self
        pa = self.pixel_array
        pa[:, :, :3] = (np.array(color_to_rgb(color)) * 255).astype(np.uint8)
        if alpha is not None:
            pa[:, :, 3] = int(255 * alpha)
        _cl17b_pixel_sync(self)
        return self

    # Transform(image_a, image_b) in Cairo interpolated the pixel arrays; GL only interpolates the quad. Blend the pixels as well.
    _cl17b_image_interpolate = ImageMobject.interpolate

    def _cl17b_interpolate(self, mobject1, mobject2, alpha, *args, **kwargs):
        result = _cl17b_image_interpolate(self, mobject1, mobject2, alpha, *args, **kwargs)
        if isinstance(mobject1, ImageMobject) and isinstance(mobject2, ImageMobject) and mobject1 is not mobject2:
            a, b = mobject1.pixel_array, mobject2.pixel_array
            if a.shape != b.shape:
                from PIL import Image as _PILImage
                b = np.array(_PILImage.fromarray(b).resize((a.shape[1], a.shape[0])))
            self.pixel_array[...] = ((1 - alpha) * a + alpha * b).astype(np.uint8)
            _cl17b_pixel_sync(self)
        return result

    ImageMobject.interpolate = _cl17b_interpolate
    ImageMobject.pixel_array = property(_cl17b_get_pixel_array)
    ImageMobject.get_pixel_array = lambda self: self.pixel_array
    ImageMobject.set_color = _cl17b_set_color

# CL17-A: Scene.get_mobjects_from_last_animation() of Cairo (sep19 scene.py: finish_animations stores `anim.mobject` of each animation; 12 eoc scene
# copies call it, e.g. tattoo ExplainTrigFunctionDistances). New method + hook on finish_animations, 2017 only.
if _CAIRO_ERA and _CL17_2017:
    _cl17a_finish_animations = Scene.finish_animations

    @_wraps(_cl17a_finish_animations)
    def _cl17a_finish_animations_wrapper(self, animations, *args, **kwargs):
        animations = list(animations)
        result = _cl17a_finish_animations(self, animations, *args, **kwargs)
        self.mobjects_from_last_animation = [anim.mobject for anim in animations]
        return result

    Scene.finish_animations = _cl17a_finish_animations_wrapper
    if not hasattr(Scene, "get_mobjects_from_last_animation"):
        Scene.get_mobjects_from_last_animation = lambda self: getattr(self, "mobjects_from_last_animation", [])


# CL17-B: bell calls `self.update_mobjects()` with no argument (Cairo's dt defaulted); GL's Scene.update_mobjects(dt) requires it.
if _CAIRO_ERA and _CL17_2017 and _CL17_B_NN:
    from manimlib.scene.scene import Scene as _Cl17bScene
    _cl17b_update_mobjects = _Cl17bScene.update_mobjects

    @_wraps(_cl17b_update_mobjects)
    def _cl17b_update_mobjects_wrapper(self, dt=0, *args, **kwargs):
        return _cl17b_update_mobjects(self, dt, *args, **kwargs)

    _Cl17bScene.update_mobjects = _cl17b_update_mobjects_wrapper


# CL17-C: once_useful_constructs/fractals.py (Sierpinski, KochCurve, HilbertCurve, fractalify, ...) needs the Cairo `digest_config` and the CONFIG-kwargs rule,
# which GL no longer has. The ported version lives in `once_useful_constructs/fractals_cl17.py` (see `_CairoConfigKwargs` there) and its public names are
# exported here ONLY for 2017 (coordinator, 2026-10-28: the first version edited fractals.py itself and exported the names for every year, which changed the
# already rendered outside_videos/merch_designs/ShowSierpinski; `fractals.py` is back to the original, which outside_videos still imports with its own digest_config).
if _CAIRO_ERA and _CL17_2017:
    import once_useful_constructs.fractals_cl17 as _cl17c_fractals
    _cl17c_fractal_names = [
        "fractalify", "fractalification_iteration", "SelfSimilarFractal", "Sierpinski", "DiamondFractal", "PentagonalFractal",
        "WonkyHexagonFractal", "CircularFractal", "JaggedCurvePiece", "FractalCurve", "LindenmayerCurve",
        "SelfSimilarSpaceFillingCurve", "HilbertCurve", "HilbertCurve3D", "PeanoCurve", "TriangleFillingCurve",
        "HexagonFillingCurve", "UtahFillingCurve", "FlowSnake", "SierpinskiCurve", "KochSnowFlake", "KochCurve",
        "QuadraticKoch", "QuadraticKochIsland", "StellarCurve", "SnakeCurve",
    ]
    for _cl17c_name in _cl17c_fractal_names:
        globals()[_cl17c_name] = getattr(_cl17c_fractals, _cl17c_name)
    __all__.extend(_cl17c_fractal_names)


# CL17-B: Cairo VMobject.fill_rgb (np array, the fill colour) read by nn (`pixel.fill_rgb[0]` to turn squares back into pixel values).
if _CAIRO_ERA and _CL17_2017 and not hasattr(VMobject, "fill_rgb"):
    VMobject.fill_rgb = property(
        lambda self: np.array(color_to_rgb(self.get_fill_color())),
        lambda self, value: self.set_fill(rgb_to_color(value)),
    )


# CL17-C: Cairo-era `mob.scale(factor, point)` -- 2017 code passes the scaling centre as a 2nd positional argument
# (`self.play(koch.scale, 3, koch.get_left())`, `britain.scale, 2.5, britain.get_corner(...)`); GL's 2nd positional is min_scale_factor.
if _CAIRO_ERA and _CL17_2017:
    _cl17c_scale = Mobject.scale

    @_wraps(_cl17c_scale)
    def _cl17c_scale_wrapper(self, scale_factor, *args, **kwargs):
        if args and np.ndim(args[0]) == 1 and np.size(args[0]) == 3 and "about_point" not in kwargs:
            kwargs["about_point"] = np.asarray(args[0], dtype=float)
            args = args[1:]
        return _cl17c_scale(self, scale_factor, *args, **kwargs)

    Mobject.scale = _cl17c_scale_wrapper


# CL17-C: waves calls `self.update_mobjects()` with no argument (Cairo's dt defaulted); same fix as CL17-B for the rest of 2017.
if _CAIRO_ERA and _CL17_2017 and not _CL17_B_NN:
    from manimlib.scene.scene import Scene as _Cl17cScene
    _cl17c_update_mobjects = _Cl17cScene.update_mobjects

    @_wraps(_cl17c_update_mobjects)
    def _cl17c_update_mobjects_wrapper(self, dt=0, *args, **kwargs):
        return _cl17c_update_mobjects(self, dt, *args, **kwargs)

    _Cl17cScene.update_mobjects = _cl17c_update_mobjects_wrapper

# CL17-A: Rotate/Rotating(..., in_place=True) (the older Cairo flag: rotate about the mobject's own centre, which is also GL's default). GL passes
# unknown kwargs to Animation.__init__ -> TypeError (36 eoc scene copies: ch10 tangent_line wiggle, ch9 solar panels, ch1 rings). Dropped.
if _CAIRO_ERA and _CL17_2017:
    from manimlib.animation.rotation import Rotating as _Cl17aRotating
    _cl17a_rotating_init = _Cl17aRotating.__init__

    @_wraps(_cl17a_rotating_init)
    def _cl17a_rotating_init_wrapper(self, *args, in_place=None, **kwargs):
        _cl17a_rotating_init(self, *args, **kwargs)

    _Cl17aRotating.__init__ = _cl17a_rotating_init_wrapper

    # CL17-A: ThreeDMobject(*mobjects) of Cairo's 3D camera (a plain container whose faces get shaded): a Group here.
    class ThreeDMobject(VGroup):
        pass

    __all__.append("ThreeDMobject")


# CL17-B: small Cairo-era names used by bell / nn that GL no longer has.
#  - Mobject.reset_normal_vector(): Cairo 3D arrows froze their normal vector; GL arrows orient per camera -> no-op (new method).
#  - turn_off_3d_shading(mobject): Cairo free function -> no shading on the whole family (new name).
#  - Eyes.blink_anim(): used by nn (never existed in sep19 either, the original scenes relied on an older pi creature API) -> Blink(eyes).
if not hasattr(Mobject, "reset_normal_vector"):
    Mobject.reset_normal_vector = lambda self: self


def turn_off_3d_shading(mobject):
    for submob in mobject.get_family():
        if hasattr(submob, "set_shading"):
            submob.set_shading(0, 0, 0)
    return mobject


__all__.append("turn_off_3d_shading")

if _CAIRO_ERA and _CL17_2017:
    from custom.characters.pi_creature import Eyes as _Cl17bEyes
    from custom.characters.pi_creature_animations import Blink as _Cl17bBlink
    if not hasattr(_Cl17bEyes, "blink_anim"):
        _Cl17bEyes.blink_anim = lambda self, **kwargs: _Cl17bBlink(self, **kwargs)
    if not hasattr(_Cl17bEyes, "look_at_anim"):
        _Cl17bEyes.look_at_anim = lambda self, target, **kwargs: ApplyMethod(self.look_at, target, **kwargs)
    if not hasattr(_Cl17bEyes, "change_mode_anim"):
        _Cl17bEyes.change_mode_anim = lambda self, mode, **kwargs: ApplyMethod(self.change_mode, mode, **kwargs)
    # Cairo VMobject.is_subpath (False for ordinary mobjects; True only for the pieces Cairo split a path into) is read by nn filters
    if not hasattr(Mobject, "is_subpath"):
        Mobject.is_subpath = False


# ======================================================================================================================
# CL17-D (2017: crypto, leibniz, borsuk, mug, triples, dominos, 256, cba). All of this only applies to scenes under /_2017/.
# ======================================================================================================================
if _CAIRO_ERA and _CL17_2017:
    # CL17-D: 3feb NumberPlane/ComplexPlane silently absorbed unknown kwargs through digest_config: leibniz passes `radius = BLUE_E` (a typo for
    # `color`) and triples `stroke_color = BLUE_E` (unused config). GL raises TypeError in CoordinateSystem.__init__. Drop them (same picture as Cairo).
    _cl17d_plane_init = NumberPlane.__init__

    @_wraps(_cl17d_plane_init)
    def _cl17d_plane_init_wrapper(self, *args, radius=None, stroke_color=None, plane_center=None, **kwargs):
        _cl17d_plane_init(self, *args, **kwargs)

    NumberPlane.__init__ = _cl17d_plane_init_wrapper

    # CL17-D: NumberPlane.get_center_point() of 3feb = the point of coordinates (0, 0) (triples OneMoreExample, ReframeOnLattice).
    if not hasattr(NumberPlane, "get_center_point"):
        NumberPlane.get_center_point = lambda self: self.coords_to_point(0, 0)

    # CL17-D: 3feb NumberPlane.get_space_unit_to_x_unit/y_unit(): scene units per coordinate unit on each axis (leibniz LatticePointScene.get_circle).
    if not hasattr(NumberPlane, "get_space_unit_to_y_unit"):
        NumberPlane.get_space_unit_to_x_unit = lambda self: self.x_axis.get_unit_size()
        NumberPlane.get_space_unit_to_y_unit = lambda self: self.y_axis.get_unit_size()

    # CL17-D: Mobject.scale_about_point / pose_at_angle of 3feb (triples RationalPointsOnUnitCircle, mug AboutToyPuzzles); missing in GL.
    if not hasattr(Mobject, "scale_about_point"):
        Mobject.scale_about_point = lambda self, scale_factor, point: self.scale(scale_factor, about_point=point)
    if not hasattr(Mobject, "pose_at_angle"):
        def _cl17d_pose_at_angle(self, **kwargs):
            self.rotate(TAU / 14, RIGHT + UP, **kwargs)
            return self
        Mobject.pose_at_angle = _cl17d_pose_at_angle

    # CL17-D: VMobject.is_subpath of Cairo SVG glyphs (inner contours were separate family members flagged True); here every glyph is one path.
    if not hasattr(VMobject, "is_subpath"):
        VMobject.is_subpath = False

    # CL17-D: TexMobject.expression_parts (3feb/2017 manim: the list of strings it was built from; borsuk ChoicesForSpherePoint reads it).
    _cl17d_oldtex_init = OldTex.__init__

    @_wraps(_cl17d_oldtex_init)
    def _cl17d_oldtex_init_wrapper(self, *tex_strings, **kwargs):
        _cl17d_oldtex_init(self, *tex_strings, **kwargs)
        self.expression_parts = list(tex_strings)
        self.args = tuple(tex_strings)  # CL17-D: 2017 TexMobject/TextMobject kept the constructor arguments (borsuk brace.label.args[0][1])

    OldTex.__init__ = _cl17d_oldtex_init_wrapper

    # CL17-D: an SVG path made of a single `M x,y` (house.svg ends with `<path d="M14.3,6.5"/>`) leaves 1 point and GL's handle_commands then
    # resizes to -1 points ("all elements of new_shape must be non-negative"; mug house/utilities scenes). Leave such a path empty.
    from manimlib.mobject.svg.svg_mobject import VMobjectFromSVGPath as _Cl17dSVGPath
    _cl17d_handle_commands = _Cl17dSVGPath.handle_commands

    @_wraps(_cl17d_handle_commands)
    def _cl17d_handle_commands_wrapper(self):
        try:
            _cl17d_handle_commands(self)
        except ValueError:
            self.set_points(np.zeros((0, 3)))

    _Cl17dSVGPath.handle_commands = _cl17d_handle_commands_wrapper

    # CL17-D: Cairo's BackgroundRectangle ignored colour changes (set_style_data kept BLACK; only fill_opacity changed), so `words.add_background_rectangle();
    # words.set_color(YELLOW)` left a black box behind yellow text. GL's BackgroundRectangle.set_style does the same for direct calls, but
    # Mobject.set_color of a PARENT group writes the rgba arrays of the whole family, painting the box yellow (leibniz "Multiply by 1" boxes, triples/crypto
    # labels). Keep the rectangle's colour when a colour is set through its parents.
    from manimlib.mobject.shape_matchers import BackgroundRectangle as _Cl17dBackgroundRectangle
    # (this fork keeps the fill colour in `uniforms["fill_rgba"]`, written by VMobject.set_fill, so that is what gets wrapped)
    _cl17d_set_fill = VMobject.set_fill

    @_wraps(_cl17d_set_fill)
    def _cl17d_set_fill_wrapper(self, color=None, opacity=None, *args, recurse=True, **kwargs):
        if color is not None and recurse and not isinstance(self, _Cl17dBackgroundRectangle):
            rects = [m for m in self.get_family() if isinstance(m, _Cl17dBackgroundRectangle)]
            if rects:
                saved = [(m, np.array(m.uniforms["fill_rgba"]), np.array(m.uniforms["fill_rgba_end"])) for m in rects]
                result = _cl17d_set_fill(self, color, opacity, *args, recurse=recurse, **kwargs)
                for m, rgba, rgba_end in saved:
                    m.uniforms["fill_rgba"][:3] = rgba[:3]
                    m.uniforms["fill_rgba_end"][:3] = rgba_end[:3]
                return result
        return _cl17d_set_fill(self, color, opacity, *args, recurse=recurse, **kwargs)

    VMobject.set_fill = _cl17d_set_fill_wrapper

    # CL17-D: Cairo's ThreeDScene started with the camera at phi=0, theta=-90 deg (looking straight down: a flat 2D scene looks flat); GL starts at
    # (-30, 70) and a 2D scene that never calls set_camera_orientation (borsuk jewels/thieves, ThreeDScene used as a plain Scene) comes out tilted and
    # cut off. Same fix as CL19-CL1 (2019), now for 2017.
    ThreeDScene.default_frame_orientation = (0, 0)

    # CL17-D: Cairo's VMobject.init_colors styled only the object itself (family=False). GL's VMobject.init_colors runs AFTER init_points and
    # styles the whole family, so a scene class whose init_points builds children with their own colours/opacity (borsuk `Necklace` of `Jewel`s,
    # `Jewel` of polygons) ends with every child in the container's default style (grey, fill 0). For VMobject subclasses defined in a 2017
    # scene file that already have submobjects when the style is applied, style only the object (fork bug #6, see BUGS_FORK_2018.md).
    _cl17d_init_colors = VMobject.init_colors
    _cl17d_scene_class_cache = {}

    def _cl17d_is_scene_class(cls):
        if cls not in _cl17d_scene_class_cache:
            # (the scene module is not registered in sys.modules by ModuleLoader: read the file from the code of the init_points that runs)
            path = ""
            for _base in cls.__mro__:
                _fn = _base.__dict__.get("init_points")
                if _fn is not None and hasattr(_fn, "__code__"):
                    path = str(_fn.__code__.co_filename)
                    break
            _cl17d_scene_class_cache[cls] = bool(_re.search(r"[/\\]_work[/\\]_?2017[/\\]", path))
        return _cl17d_scene_class_cache[cls]

    @_wraps(_cl17d_init_colors)
    def _cl17d_init_colors_wrapper(self):
        if self.submobjects and _cl17d_is_scene_class(type(self)):
            self.set_stroke(color=self.stroke_color, width=self.stroke_width, opacity=self.stroke_opacity,
                            behind=self.stroke_behind, recurse=False)
            self.set_fill(color=self.fill_color, opacity=self.fill_opacity, border_width=self.fill_border_width, recurse=False)
            self.set_shading(*self.shading, recurse=False)
            self.set_flat_stroke(self.flat_stroke, recurse=False)
            return
        _cl17d_init_colors(self)

    VMobject.init_colors = _cl17d_init_colors_wrapper

    # CL17-D: custom/characters/pi_creature_scene.py (read-only) calls ApplyPointwiseFunction in zoom_in_on_thought_bubble without importing it
    # (crypto NoCommentOnSpeculation): inject the name into that module.
    import custom.characters.pi_creature_scene as _cl17d_pcs_mod
    if not hasattr(_cl17d_pcs_mod, "ApplyPointwiseFunction"):
        from manimlib.animation.transform import ApplyPointwiseFunction as _Cl17dAPF
        _cl17d_pcs_mod.ApplyPointwiseFunction = _Cl17dAPF


# CL17-B: nn scenes mix NetworkScene (whose setup never calls super()) with PiCreatureScene (an InteractiveScene): InteractiveScene.setup
# is then skipped and the first Scene.remove fails with "no attribute 'unselectables'". Class-level default (only read by the selection UI).
if _CAIRO_ERA and _CL17_2017:
    from manimlib.scene.interactive_scene import InteractiveScene as _Cl17bInteractiveScene
    if not hasattr(_Cl17bInteractiveScene, "unselectables"):
        _Cl17bInteractiveScene.unselectables = ()



# CL17-C: flag for the files owned by agent C (fractal_dimension, waves, highD, efvgt).
_CL17_C = any(_re.search(r"[/\\]_?2017[/\\](fractal_dimension|waves|highD|efvgt)[/\\]", str(arg)) for arg in _ARGV_PATHS)

# CL17-C: Cairo's Mobject.split() was `[self] (if it has points) + submobjects`, and __getitem__/__iter__/__len__ go through it:
# `square[0]` is the square itself, `Britain(...)[0]` the outline, `VectorizedPoint()[0]` the point. GL's split() is only the submobjects.
if _CAIRO_ERA and _CL17_C:
    def _cl17c_split(self):
        if self.has_points():
            return [self] + list(self.submobjects)
        return self.submobjects

    Mobject.split = _cl17c_split


# CL17-C: `mob.apply_function(f, maintain_smoothness=False)` -- Cairo kwarg; GL's apply_points_function does not accept it.
if _CAIRO_ERA and _CL17_C:
    _cl17c_apf = Mobject.apply_points_function

    @_wraps(_cl17c_apf)
    def _cl17c_apf_wrapper(self, func, *args, **kwargs):
        kwargs.pop("maintain_smoothness", None)
        return _cl17c_apf(self, func, *args, **kwargs)

    Mobject.apply_points_function = _cl17c_apf_wrapper


# CL17-C: Cairo scenes call `self.add(...)` inside `setup()` before the GL InteractiveScene.setup (PiCreatureScene is one) has run;
# InteractiveScene.remove then reads unselectables / select_top_level_mobs, which do not exist yet. Class-level defaults; the
# real setup overwrites them per instance. highD (Skeptic, TwoDOuterBox, ...).
if _CAIRO_ERA and _CL17_C:
    from manimlib.scene.interactive_scene import InteractiveScene as _Cl17cInteractiveScene
    if not hasattr(_Cl17cInteractiveScene, "unselectables"):
        _Cl17cInteractiveScene.unselectables = []
    if not hasattr(_Cl17cInteractiveScene, "select_top_level_mobs"):
        _Cl17cInteractiveScene.select_top_level_mobs = True

    # Cairo `Mobject.add_updater(mob, f)` returned a ContinualUpdate whose `.mobject` is mob and `.update(0)` applies f.
    # Non-data descriptor, so instances that assign `self.mobject = ...` (BackgroundRectangle, ...) still win.
    class _Cl17cSelfAsMobject:
        def __get__(self, obj, objtype=None):
            return self if obj is None else obj

    if not hasattr(Mobject, "mobject"):
        Mobject.mobject = _Cl17cSelfAsMobject()


# CL17-B: Cairo's Mobject.copy() kept `.target` too (nn: `ReplacementTransform(row.copy(), row.target)` and `LaggedStartMap(ReplacementTransform,
# rows.copy(), lambda m: (m, m.target))`); GL's copy() sets target=None -> "create_target not properly implemented". Only _2017/nn and bell.
if _CAIRO_ERA and _CL17_2017 and _CL17_B_NN:
    _cl17b_copy_prev = Mobject.copy

    @_wraps(_cl17b_copy_prev)
    def _cl17b_copy_keep_target(self, deep=False):
        result = _cl17b_copy_prev(self, deep)
        target = self.__dict__.get("target")
        if target is not None and result.__dict__.get("target") is None:
            result.target = target
        return result

    Mobject.copy = _cl17b_copy_keep_target


# CL17-B: Cairo ApplyMethod accepted `method_kwargs={...}` (kwargs of the animated method); GL takes them as a trailing dict argument.
if _CAIRO_ERA and _CL17_2017:
    _cl17b_apply_method_init = ApplyMethod.__init__

    @_wraps(_cl17b_apply_method_init)
    def _cl17b_apply_method_init_wrapper(self, method, *args, **kwargs):
        method_kwargs = kwargs.pop("method_kwargs", None)
        if method_kwargs:
            args = (*args, method_kwargs)
        _cl17b_apply_method_init(self, method, *args, **kwargs)

    ApplyMethod.__init__ = _cl17b_apply_method_init_wrapper


# CL17-B: DecimalNumber(np.array([x])) (nn: activations are (n, 1) arrays, iterating gives 1-element arrays): Cairo formatted them with "%.2f".
if _CAIRO_ERA and _CL17_2017:
    from manimlib.mobject.numbers import DecimalNumber as _Cl17bDecimalNumber
    _cl17b_get_num_string = _Cl17bDecimalNumber.get_num_string

    @_wraps(_cl17b_get_num_string)
    def _cl17b_get_num_string_wrapper(self, number):
        if isinstance(number, np.ndarray) and number.size == 1:
            number = number.item()
        return _cl17b_get_num_string(self, number)

    _Cl17bDecimalNumber.get_num_string = _cl17b_get_num_string_wrapper


# CL17-C: replacement for Cairo "draw the mobject into a low-res pixel array and read pixels" (fractal_dimension box counting:
# `camera.capture_mobject(m)`; `camera.pixel_array[y, x]`). Rasterises the filled shapes of `vmobject` with PIL at a fixed scale
# and answers which of `points` (N x 3, scene coordinates) fall on a painted pixel. New name, no era flag.
def cairo_filled_mask(vmobject, points, pixels_per_unit=120, samples_per_curve=8, include_stroke=False):
    from PIL import Image, ImageDraw
    points = np.atleast_2d(np.asarray(points, dtype=float))
    frame_w, frame_h = 8.0 * 16 / 9, 8.0
    w, h = int(frame_w * pixels_per_unit), int(frame_h * pixels_per_unit)
    image = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(image)
    ts = np.linspace(0, 1, samples_per_curve + 1)[:, None]

    def to_px(p):
        return ((p[0] + frame_w / 2) * pixels_per_unit, (frame_h / 2 - p[1]) * pixels_per_unit)

    for sub in vmobject.get_family():
        if not sub.has_points() or not hasattr(sub, "get_bezier_tuples"):
            continue
        filled = sub.get_fill_opacity() > 0
        stroked = include_stroke and sub.get_stroke_width() > 0
        if not (filled or stroked):
            continue
        outline = []
        for a, hh, b in sub.get_bezier_tuples():
            outline.extend((1 - ts) ** 2 * a + 2 * (1 - ts) * ts * hh + ts ** 2 * b)
        pixels = [to_px(p) for p in outline]
        if len(pixels) >= 3:
            draw.polygon(pixels, fill=255)
    pixel_array = np.asarray(image)
    xs = np.floor((points[:, 0] + frame_w / 2) * pixels_per_unit).astype(int)
    ys = np.floor((frame_h / 2 - points[:, 1]) * pixels_per_unit).astype(int)
    inside = (xs >= 0) & (xs < w) & (ys >= 0) & (ys < h)
    result = np.zeros(len(points), dtype=bool)
    result[inside] = pixel_array[ys[inside], xs[inside]] > 0
    return result


__all__.append("cairo_filled_mask")


# CL17-C: the 2017 GraphScene API that sep19 dropped: graph_function(func) (sets self.graph / self.func and adds the graph),
# label_graph(graph, label, x_val, direction, buff) and input_to_graph_point(x) with the graph defaulting to self.graph.
# Methods are added only when absent / wrapped for the optional argument; 2017 only. (fractal_dimension plots.)
if _CAIRO_ERA and _CL17_2017:
    if not hasattr(GraphScene, "graph_function"):
        def _cl17c_graph_function(self, func, color=None, animate=False, is_main_graph=True, **kwargs):
            graph = self.get_graph(func, color=color if color is not None else BLUE, **kwargs)
            if is_main_graph:
                self.graph = graph
                self.func = func
            if animate:
                self.play(ShowCreation(graph))
            else:
                self.add(graph)
            return graph
        GraphScene.graph_function = _cl17c_graph_function

    if not hasattr(GraphScene, "label_graph"):
        def _cl17c_label_graph(self, graph, label="f(x)", x_val=None, direction=RIGHT, buff=MED_SMALL_BUFF, color=None):
            label = OldTex(label) if isinstance(label, str) else label
            label.set_color(color if color is not None else graph.get_color())
            if x_val is None:
                # Search from right to left for the last point that is still on screen
                for x_val in np.linspace(self.x_max, self.x_min, 100):
                    if self.input_to_graph_point(x_val, graph)[1] < FRAME_Y_RADIUS:
                        break
                x_val = x_val - 0.2
            label.next_to(self.input_to_graph_point(x_val, graph), direction, buff=buff)
            label.shift_onto_screen()
            self.add(label)
            self.graph_label = label
            return label
        GraphScene.label_graph = _cl17c_label_graph

    _cl17c_input_to_graph_point = GraphScene.input_to_graph_point

    def _cl17c_input_to_graph_point_wrapper(self, x, graph=None):
        return _cl17c_input_to_graph_point(self, x, graph if graph is not None else self.graph)

    GraphScene.input_to_graph_point = _cl17c_input_to_graph_point_wrapper

# CL17-A: the 2017 GraphScene API (the eoc chapters 1-2 and 8 were written against it; sep19 already dropped it, so these scenes also fail in sep19):
#   graph_function(func, color, is_main_graph, animate=True) -> graph (also stored in self.graph / self.func),
#   label_graph(graph, label, proportion, direction, buff, animate=True),
#   get_derivative_graph(graph=None) and input_to_graph_point(x, graph=None) default to self.graph.
if _CAIRO_ERA and _CL17_2017:
    _CL17A_PATH = _re.compile(r"/_work/_2017/(eoc|tattoo|putnam|qa_round_two|gradient)/")

    def _cl17a_graph_function(self, func, color=None, is_main_graph=True, animate=None, **kwargs):
        # eoc/tattoo/putnam/qa/gradient: animate=True by default (the scenes pass animate=False when they do not want it); C's
        # fractal_dimension (CL17-C) wants the graph added silently, as its own definition above.
        if animate is None:
            animate = bool(_CL17A_PATH.search(_cl19_caller_path(2)))
        graph = self.get_graph(func, color=color if color is not None else BLUE, **kwargs)
        if is_main_graph:
            self.graph = graph
            self.func = func
        if animate:
            self.play(ShowCreation(graph))
        self.add(graph)
        return graph

    def _cl17a_label_graph(self, graph, label="f(x)", proportion=None, direction=RIGHT, buff=MED_SMALL_BUFF, animate=None, x_val=None, color=None):
        label = OldTex(label) if isinstance(label, str) else label
        label.set_color(color if color is not None else graph.get_color())
        if proportion is not None:
            label.next_to(graph.point_from_proportion(proportion), direction, buff=buff)
        else:
            if x_val is None:
                for x_val in np.linspace(self.x_max, self.x_min, 100):
                    if self.input_to_graph_point(x_val, graph)[1] < FRAME_Y_RADIUS:
                        break
                x_val = x_val - 0.2
            label.next_to(self.input_to_graph_point(x_val, graph), direction, buff=buff)
            label.shift_onto_screen()
        if animate is None:
            animate = bool(_CL17A_PATH.search(_cl19_caller_path(2)))
        if animate:
            self.play(ShowCreation(label))
        self.add(label)
        self.graph_label = label
        return label

    _cl17a_input_to_graph_point = GraphScene.input_to_graph_point
    _cl17a_get_derivative_graph = GraphScene.get_derivative_graph

    @_wraps(_cl17a_input_to_graph_point)
    def _cl17a_input_to_graph_point_wrapper(self, x, graph=None):
        return _cl17a_input_to_graph_point(self, x, self.graph if graph is None else graph)

    @_wraps(_cl17a_get_derivative_graph)
    def _cl17a_get_derivative_graph_wrapper(self, graph=None, *args, **kwargs):
        return _cl17a_get_derivative_graph(self, self.graph if graph is None else graph, *args, **kwargs)

    # the same default (graph=None -> self.graph) for the other old-API methods that take (x, graph, ...)
    for _cl17a_gname in ("get_vertical_line_to_graph", "angle_of_tangent", "slope_of_tangent"):
        def _cl17a_make_graph_default(orig):
            @_wraps(orig)
            def method(self, x, graph=None, *args, **kwargs):
                return orig(self, x, self.graph if graph is None else graph, *args, **kwargs)
            return method
        setattr(GraphScene, _cl17a_gname, _cl17a_make_graph_default(getattr(GraphScene, _cl17a_gname)))

    GraphScene.graph_function = _cl17a_graph_function
    GraphScene.label_graph = _cl17a_label_graph
    GraphScene.input_to_graph_point = _cl17a_input_to_graph_point_wrapper
    GraphScene.get_derivative_graph = _cl17a_get_derivative_graph_wrapper


# CL17-C: Cairo-era constructor kwargs of the 2017 planes/axes.
#  - NumberPlane/ComplexPlane(space_unit_to_x_unit=, space_unit_to_y_unit=): scene length of one x / y unit (= x_unit_size / y_unit_size).
#  - ThreeDAxes(x_axis_radius=, y_axis_radius=, z_axis_radius=): half length of each axis (= range (-r, r, 1)).
if _CAIRO_ERA and _CL17_C:
    _cl17c_plane_init = NumberPlane.__init__

    @_wraps(_cl17c_plane_init)
    def _cl17c_plane_init_wrapper(self, *args, space_unit_to_x_unit=None, space_unit_to_y_unit=None, **kwargs):
        if space_unit_to_x_unit is not None:
            kwargs.setdefault("x_unit_size", space_unit_to_x_unit)
        if space_unit_to_y_unit is not None:
            kwargs.setdefault("y_unit_size", space_unit_to_y_unit)
        _cl17c_plane_init(self, *args, **kwargs)

    NumberPlane.__init__ = _cl17c_plane_init_wrapper

    _cl17c_axes3d_init = ThreeDAxes.__init__

    @_wraps(_cl17c_axes3d_init)
    def _cl17c_axes3d_init_wrapper(self, *args, x_axis_radius=None, y_axis_radius=None, z_axis_radius=None, **kwargs):
        for key, radius in (("x_range", x_axis_radius), ("y_range", y_axis_radius), ("z_range", z_axis_radius)):
            if radius is not None and key not in kwargs:
                kwargs[key] = (-radius, radius, 1)
        _cl17c_axes3d_init(self, *args, **kwargs)

    ThreeDAxes.__init__ = _cl17c_axes3d_init_wrapper

    # Old ComplexTransformationScene exposed real_labels / imag_labels (the coordinate labels of the background plane).
    import once_useful_constructs.complex_transformation_scene as _cl17c_cts
    _cl17c_add_coordinate_labels = _cl17c_cts.ComplexTransformationScene.add_coordinate_labels

    def _cl17c_cts_add_coordinate_labels(self):
        _cl17c_add_coordinate_labels(self)
        labels = list(getattr(self.background, "coordinate_labels", []))
        self.imag_labels = [lab for lab in labels if "i" in lab.get_tex()]
        self.real_labels = [lab for lab in labels if "i" not in lab.get_tex()]

    _cl17c_cts.ComplexTransformationScene.add_coordinate_labels = _cl17c_cts_add_coordinate_labels

# CL17-A: `class X(CircleScene, ReconfigurableScene)` / `(GraphScene, ReconfigurableScene)`: the MRO reaches GL's InteractiveScene.get_state (undo
# SceneState, no .copy()) before ReconfigurableScene.get_state (the Cairo one: a Group of the top-level mobjects), so
# transition_to_alt_config failed with "'SceneState' object has no attribute 'copy'". GL's get_state/save_state is only used by the editor's undo keys.
if _CAIRO_ERA and _CL17_2017:
    from manimlib.scene.interactive_scene import InteractiveScene as _Cl17aInteractiveScene
    for _cl17a_cls in (Scene, _Cl17aInteractiveScene):
        if "get_state" in _cl17a_cls.__dict__:
            def _cl17a_make_get_state(orig):
                @_wraps(orig)
                def get_state(self, *args, **kwargs):
                    if isinstance(self, ReconfigurableScene):
                        return ReconfigurableScene.get_state(self)
                    return orig(self, *args, **kwargs)
                return get_state
            _cl17a_cls.get_state = _cl17a_make_get_state(_cl17a_cls.__dict__["get_state"])

# CL17-A: more Cairo behaviours the 2017 scenes rely on (all 2017 only):
if _CAIRO_ERA and _CL17_2017:
    # (1) old_chapter1 scenes call self.add() in setup() before GL's InteractiveScene.setup ran: it reads select_top_level_mobs (B added unselectables).
    from manimlib.scene.interactive_scene import InteractiveScene as _Cl17aIS2
    if not hasattr(_Cl17aIS2, "select_top_level_mobs"):
        _Cl17aIS2.select_top_level_mobs = True
    if not hasattr(_Cl17aIS2, "unselectables"):
        _Cl17aIS2.unselectables = []

    # (2) `Mobject.apply_function(f, maintain_smoothness=False)`: GL's apply_points_function has no such kwarg (C added the same wrapper for its files).
    _cl17a_apf = Mobject.apply_points_function

    @_wraps(_cl17a_apf)
    def _cl17a_apf_wrapper(self, func, *args, **kwargs):
        kwargs.pop("maintain_smoothness", None)
        return _cl17a_apf(self, func, *args, **kwargs)

    Mobject.apply_points_function = _cl17a_apf_wrapper

    # (3) `Transform(a, b).update(1)` without a play (Cairo built the start/target mobjects in __init__): begin() first if it never ran.
    _cl17a_anim_update = Animation.update

    @_wraps(_cl17a_anim_update)
    def _cl17a_anim_update_wrapper(self, alpha, *args, **kwargs):
        if not hasattr(self, "families"):
            self.begin()
        return _cl17a_anim_update(self, alpha, *args, **kwargs)

    Animation.update = _cl17a_anim_update_wrapper

    # (4) Cairo's ApplyMethod built `target_mobject` in __init__ (scenes edit `anim.target_mobject[0]` before playing: eoc PiecewiseConstantCar);
    # GL builds it in begin(). Build it now and let begin() use it.
    from manimlib.animation.transform import ApplyMethod as _Cl17aApplyMethod, Transform as _Cl17aTransform
    _cl17a_am_init = _Cl17aApplyMethod.__init__
    _cl17a_tr_begin = _Cl17aTransform.begin

    @_wraps(_cl17a_am_init)
    def _cl17a_am_init_wrapper(self, *args, **kwargs):
        _cl17a_am_init(self, *args, **kwargs)
        if type(self).create_target is _Cl17aApplyMethod.create_target:
            self._cl17a_eager_target = self.create_target()
            self.target_mobject = self._cl17a_eager_target

    @_wraps(_cl17a_tr_begin)
    def _cl17a_tr_begin_wrapper(self, *args, **kwargs):
        eager = getattr(self, "_cl17a_eager_target", None)
        if eager is None:
            return _cl17a_tr_begin(self, *args, **kwargs)
        self._cl17a_eager_target = None
        self.create_target = lambda: eager
        try:
            return _cl17a_tr_begin(self, *args, **kwargs)
        finally:
            del self.create_target

    _Cl17aApplyMethod.__init__ = _cl17a_am_init_wrapper
    _Cl17aTransform.begin = _cl17a_tr_begin_wrapper

# CL17-A: OldTex.break_up_by_substrings strips each part (`"1 "` is stored as "1"), so `get_part_by_tex("1 ", substring=False)` found nothing and
# returned None (eoc/chapter10 ExampleApproximation: approximation_terms = ["1 ", "-x^2", ...]). Strip the query too. 2017 only.
if _CAIRO_ERA and _CL17_2017:
    _cl17a_get_parts_by_tex = OldTex.get_parts_by_tex

    @_wraps(_cl17a_get_parts_by_tex)
    def _cl17a_get_parts_by_tex_wrapper(self, tex, *args, **kwargs):
        if isinstance(tex, str) and tex.strip():
            tex = tex.strip()
        return _cl17a_get_parts_by_tex(self, tex, *args, **kwargs)

    OldTex.get_parts_by_tex = _cl17a_get_parts_by_tex_wrapper

# CL17-A: PiCreature.look(OUT) (look straight at the viewer): custom/characters/pi_creature.py divides by v_norm = 0 (direction has no x/y part) and
# fills the pupils with NaN, which later breaks the Transform of the creature ("repeats may not contain negative values" in align_data_and_family;
# eoc ch2 TCubedExample, ch7 GraphLimitExpression: `play(randy.look, OUT)`). sep19 pretended there was no offset: pupils centred on the irises. 2017 only.
if _CAIRO_ERA and _CL17_2017:
    from custom.characters.pi_creature import PiCreature as _Cl17aPiCreature2
    _cl17a_look = _Cl17aPiCreature2.look

    @_wraps(_cl17a_look)
    def _cl17a_look_wrapper(self, direction):
        direction = np.array(direction, dtype=float)
        if get_norm(direction) > 0 and abs(direction[0]) < 1e-9 and abs(direction[1]) < 1e-9:
            self.purposeful_looking_direction = direction / get_norm(direction)
            for eye in self.eyes:
                iris, pupil = eye
                pupil.move_to(iris.get_center())
            self.eyes[1].pupil.align_to(self.eyes[0].pupil, DOWN)
            return self
        return _cl17a_look(self, direction)

    _Cl17aPiCreature2.look = _cl17a_look_wrapper


# CL17-C: Cairo's Cube was a VGroup of VMobject faces: Cube(fill_opacity=0.5) and cube.set_fill(color, opacity) / set_stroke(...).
# GL's Cube is a Group of Square3D surfaces that only knows `opacity=`. Map the kwarg and give plain Mobjects set_fill / set_stroke
# (VMobject has its own, so only Groups of surfaces get these). efvgt cube symmetries.
if _CAIRO_ERA and _CL17_C:
    from manimlib.mobject.three_dimensions import Cube as _Cl17cCube
    _cl17c_cube_init = _Cl17cCube.__init__

    @_wraps(_cl17c_cube_init)
    def _cl17c_cube_init_wrapper(self, *args, fill_opacity=None, fill_color=None, stroke_width=None, stroke_color=None, **kwargs):
        if fill_opacity is not None:
            kwargs.setdefault("opacity", fill_opacity)
        if fill_color is not None:
            kwargs.setdefault("color", fill_color)
        _cl17c_cube_init(self, *args, **kwargs)

    _Cl17cCube.__init__ = _cl17c_cube_init_wrapper

    if "set_fill" not in Mobject.__dict__:
        def _cl17c_set_fill(self, color=None, opacity=None, recurse=True, **kwargs):
            if color is not None:
                self.set_color(color)
            if opacity is not None:
                self.set_opacity(opacity)
            return self
        Mobject.set_fill = _cl17c_set_fill
    if "set_stroke" not in Mobject.__dict__:
        Mobject.set_stroke = lambda self, *args, **kwargs: self

# CL17-A: scenes (eoc/old_chapter1 CircleScene, include_pi_creature=False) override setup() without calling PiCreatureScene.setup and only set a
# single `self.pi_creature`; GL's PiCreatureScene reads `self.pi_creatures` (wait() blinks, change_mode, get_primary_pi_creature...) -> AttributeError.
# `pi_creatures` becomes a property that falls back to VGroup(self.pi_creature) (or an empty group). 2017 only.
if _CAIRO_ERA and _CL17_2017:
    from custom.characters.pi_creature_scene import PiCreatureScene as _Cl17aPCS3

    def _cl17a_get_pis_attr(self):
        pis = self.__dict__.get("_cl17a_pi_creatures")
        if pis is not None:
            return pis
        single = self.__dict__.get("pi_creature")
        return VGroup(single) if single is not None else VGroup()

    def _cl17a_set_pis_attr(self, value):
        self.__dict__["_cl17a_pi_creatures"] = value

    _Cl17aPCS3.pi_creatures = property(_cl17a_get_pis_attr, _cl17a_set_pis_attr)

# CL17-A: the 2017 Cairo VMobject.set_fill(color) turned a transparent shape opaque ("probably_meant_to_change_opacity": colour given, opacity None and
# self.fill_opacity == 0 -> opacity = 1; manim_3feb at 2017 dates, vectorized_mobject.py). sep19/GL leave the opacity alone, so every
# `ring.set_fill(GREEN)` of a bare Circle/Square/Rectangle stayed invisible (eoc RecapCircleSolution: all rings had fill opacity 0). Only for calls made
# directly from a 2017 scene file (GL's own set_color / gradients call set_fill internally and must keep their behaviour). 2017 only.
if _CAIRO_ERA and _CL17_2017:
    _cl17a_set_fill_orig = VMobject.set_fill

    @_wraps(_cl17a_set_fill_orig)
    def _cl17a_set_fill(self, color=None, opacity=None, *args, **kwargs):
        if color is not None and opacity is None and "/_work/_2017/" in _sys._getframe(1).f_code.co_filename.replace("\\", "/"):
            try:
                transparent = float(self.get_fill_opacity()) == 0
            except Exception:
                transparent = True
            if transparent:
                opacity = 1
        return _cl17a_set_fill_orig(self, color, opacity, *args, **kwargs)

    VMobject.set_fill = _cl17a_set_fill

# CL17-A: the 2017 GraphScene.get_riemann_rectangles(x_min, x_max, dx, ...) (no graph argument: it used self.graph); GL's port takes (graph, x_min,
# x_max, dx): called as (0, R, dr) it silently built the wrong rectangles (eoc/old_chapter1 GraphIntegral, HeartOfCalculus). A numeric first
# argument means the old form. 2017 only.
if _CAIRO_ERA and _CL17_2017:
    _cl17a_get_riemann_rectangles = GraphScene.get_riemann_rectangles

    @_wraps(_cl17a_get_riemann_rectangles)
    def _cl17a_get_riemann_rectangles_wrapper(self, *args, **kwargs):
        if args and isinstance(args[0], (int, float, np.integer, np.floating)):
            graph = getattr(self, "graph", None)
            if graph is None:
                graph = self.get_graph(self.func)   # the old form worked from self.func when no graph had been drawn yet
            args = (graph,) + args
        return _cl17a_get_riemann_rectangles(self, *args, **kwargs)

    GraphScene.get_riemann_rectangles = _cl17a_get_riemann_rectangles_wrapper

# CL17-A: Cairo's Arrow (a Line) was WHITE by default; GL's filled Arrow defaults to the light-grey DEFAULT_MOBJECT_COLOR, so every `Arrow(a, b)` of the
# eoc scenes came out dimmer than the original (compared with a manim_3feb render of eoc/chapter9 AverageOfSineStart). 2017 only, only when the scene
# gives neither color nor fill_color.
if _CAIRO_ERA and _CL17_2017:
    from manimlib.mobject.geometry import Arrow as _Cl17aArrow
    _cl17a_arrow_init = _Cl17aArrow.__init__

    @_wraps(_cl17a_arrow_init)
    def _cl17a_arrow_init_wrapper(self, *args, **kwargs):
        if "color" not in kwargs and "fill_color" not in kwargs:
            kwargs["fill_color"] = WHITE
        _cl17a_arrow_init(self, *args, **kwargs)

    _Cl17aArrow.__init__ = _cl17a_arrow_init_wrapper
