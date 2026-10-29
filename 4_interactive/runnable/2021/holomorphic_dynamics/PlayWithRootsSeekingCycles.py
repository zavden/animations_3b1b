# ==============================================================================
# Scene:      PlayWithRootsSeekingCycles
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2353-2358)
# Category:   4 · Interactive (runnable)
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl PlayWithRootsSeekingCycles.py PlayWithRootsSeekingCycles -w -m --fps 15
#     manimgl PlayWithRootsSeekingCycles.py PlayWithRootsSeekingCycles        # interactive window
#
# How to interact:
#   Click one of the white points (the roots of the polynomial) and drag it: the Newton fractal is recomputed in real time with the new roots. While you drag a root the frame does not move; outside a root, dragging moves the frame and the mouse wheel zooms toward the cursor (key r: back to the initial frame). The polynomial is z^3 - 2z + 2 at the start and the points that fall into an attracting cycle instead of a root are painted black: move the roots until the black regions appear (or disappear). It has no animation: when the window opens it is ready.
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - The fractal orders the roots with the scene's coefficients_to_roots (like Grant), not with np.roots, so that each root keeps its color
#   - `fractal.colors` (manimgl does not store it) -> get_fractal_colors(fractal), which reads the colors from the uniform
#   - `unlock_mobject_data()`/`lock_static_mobject_data()` are removed from on_mouse_press (they no longer exist in manimgl; clicking a point would fail with AttributeError)
#   - manimgl bug: with n_steps=0 the Newton shader gives NaN (log(0)); NewtonFractal is wrapped to start `step_size` at 1.0 with replace_shader_code (so n_steps=0 colors by the nearest root, as in the original)
#   - on_mouse_press/on_mouse_release: `drag_to_pan` is turned off while dragging a root (this manimgl moves the frame when dragging, and the root would go away with it)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2022/quintic/roots_and_coefs.py -----

def roots_to_coefficients(roots):
    n = len(list(roots))
    return [
        ((-1)**(n - k)) * sum(
            np.prod(tup)
            for tup in it.combinations(roots, n - k)
        )
        for k in range(n)
    ] + [1]


def poly(x, coefs):
    return sum(coefs[k] * x**k for k in range(len(coefs)))


def dpoly(x, coefs):
    return sum(k * coefs[k] * x**(k - 1) for k in range(1, len(coefs)))


def find_root(func, dfunc, seed=complex(1, 1), tol=1e-8, max_steps=100):
    # Use newton's method
    last_seed = np.inf
    for n in range(max_steps):
        if abs(seed - last_seed) < tol:
            break
        last_seed = seed
        seed = seed - func(seed) / dfunc(seed)
    return seed


def coefficients_to_roots(coefs):
    if len(coefs) == 0:
        return []
    elif coefs[-1] == 0:
        return coefficients_to_roots(coefs[:-1])
    roots = []
    # Find a root, divide out by (x - root), repeat
    for i in range(len(coefs) - 1):
        root = find_root(
            lambda x: poly(x, coefs),
            lambda x: dpoly(x, coefs),
        )
        roots.append(root)
        new_reversed_coefs, rem = np.polydiv(coefs[::-1], [1, -root])
        coefs = new_reversed_coefs[::-1]
    return roots



# ----- From _2021/newton_fractal.py -----

ROOT_COLORS_BRIGHT = [RED, GREEN, BLUE, YELLOW, MAROON_B]


ROOT_COLORS_DEEP = ["#440154", "#3b528b", "#21908c", "#5dc963", "#29abca"]


# CHANGE: manimgl's NewtonFractal is used (manimlib/mobject/fractals.py, WGSL shaders). Grant's
# copy, with GLSL shaders (`shader_folder`), which this manimgl cannot use, was here.

# CHANGE: manimgl orders the roots of some coefficients with np.roots; Grant ordered them with the
# coefficients_to_roots above (the one from roots_and_coefs), and which root gets which color
# depends on that order. The scene's own is used so that the basins match the root points.
import manimlib.mobject.fractals as _manimgl_fractals
_manimgl_fractals.coefficients_to_roots = coefficients_to_roots

# CHANGE: manimgl bug (shaders/newton_fractal.wgsl, fn seek_root): with n_steps = 0 the loop does not
# run, `step_size` stays at 0.0 and log(0) = -inf leaves the color as NaN (the fractal disappears,
# instead of showing the nearest root at each point as in the original). It is initialized to 1.0 by
# replacing the code.
class NewtonFractal(NewtonFractal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.replace_shader_code(r"var step_size = 0\.0;", "var step_size = 1.0;")

# CHANGE: manimgl does not store `fractal.colors`; the colors of each root are read from its uniform
def get_fractal_colors(fractal):
    return [rgb_to_hex(rgba[:3]) for rgba in fractal.uniforms["colors"][:len(fractal.roots)]]


class IntroNewtonFractal(Scene):
    coefs = [1.0, -1.0, 1.0, 0.0, 0.0, 1.0]
    plane_config = {
        "x_range": (-4, 4),
        "y_range": (-4, 4),
        "height": 16,
        "width": 16,
        "background_line_style": {
            "stroke_color": GREY_A,
            "stroke_width": 1.0,
        },
        "axis_config": {
            "stroke_width": 1.0,
        }
    }
    n_steps = 30

    def construct(self):
        self.init_fractal(root_colors=ROOT_COLORS_BRIGHT)
        fractal, plane, root_dots = self.group

        # Transition from last scene
        frame = self.camera.frame
        frame.shift(plane.n2p(2) - RIGHT_SIDE)

        blocker = BackgroundRectangle(plane, fill_opacity=1)
        blocker.move_to(plane.n2p(-2), RIGHT)
        self.add(blocker)

        self.play(
            frame.animate.center(),
            FadeOut(blocker),
            run_time=2,
        )
        self.wait()
        self.play(
            fractal.animate.set_colors(ROOT_COLORS_DEEP),
            *(
                dot.animate.set_fill(interpolate_color(color, WHITE, 0.2))
                for dot, color in zip(root_dots, ROOT_COLORS_DEEP)
            )
        )
        self.wait()

        # Zoom in
        fractal.set_n_steps(40)
        zoom_points = [
            [-3.12334879, 1.61196545, 0.],
            [1.21514006, 0.01415811, 0.],
        ]
        for point in zoom_points:
            self.play(
                frame.animate.set_height(2e-3).move_to(point),
                run_time=25,
                rate_func=bezier(2 * [0] + 6 * [1])
            )
            self.wait()
            self.play(
                frame.animate.center().set_height(8),
                run_time=10,
                rate_func=bezier(6 * [0] + 2 * [1])
            )

        # Allow for play
        self.tie_fractal_to_root_dots(fractal)
        fractal.set_n_steps(12)

    def init_fractal(self, root_colors=ROOT_COLORS_DEEP):
        plane = self.get_plane()
        fractal = self.get_fractal(
            plane,
            colors=root_colors,
            n_steps=self.n_steps,
        )
        root_dots = self.get_root_dots(plane, fractal)
        self.tie_fractal_to_root_dots(fractal)

        self.plane = plane
        self.fractal = fractal
        self.group = Group(fractal, plane, root_dots)
        self.add(*self.group)

    def get_plane(self):
        plane = ComplexPlane(**self.plane_config)
        plane.add_coordinate_labels(font_size=24)
        self.plane = plane
        return plane

    def get_fractal(self, plane, colors=ROOT_COLORS_DEEP, n_steps=30):
        return NewtonFractal(
            plane,
            colors=colors,
            coefs=self.coefs,
            n_steps=n_steps,
        )

    def get_root_dots(self, plane, fractal):
        self.root_dots = VGroup(*(
            Dot(plane.n2p(root), color=color)
            for root, color in zip(
                coefficients_to_roots(fractal.coefs),
                # CHANGE: fractal.colors -> get_fractal_colors(fractal)
                get_fractal_colors(fractal)
            )
        ))
        self.root_dots.set_stroke(BLACK, 5, background=True)
        return self.root_dots

    def tie_fractal_to_root_dots(self, fractal):
        fractal.add_updater(lambda f: f.set_roots([
            self.plane.p2n(dot.get_center())
            for dot in self.root_dots
        ]))

    def on_mouse_press(self, point, button, mods):
        super().on_mouse_press(point, button, mods)
        mob = self.point_to_mobject(point, search_set=self.root_dots)
        if mob is None:
            return
        # CHANGE: this manimgl has drag_to_pan (dragging moves the frame); it is turned off while a root is dragged
        self.drag_to_pan = False
        self.mouse_drag_point.move_to(point)
        mob.add_updater(lambda m: m.move_to(self.mouse_drag_point))
        # CHANGE: `unlock_mobject_data()` removed: this manimgl no longer has it (there is no cached static data to lock)
        # CHANGE: `lock_static_mobject_data()` removed: this manimgl no longer has it (there is no cached static data to lock)

    def on_mouse_release(self, point, button, mods):
        super().on_mouse_release(point, button, mods)
        # CHANGE: dragging the frame is allowed again (see on_mouse_press)
        self.drag_to_pan = True
        self.root_dots.clear_updaters()


class SimpleFractalScene(IntroNewtonFractal):
    colors = ROOT_COLORS_DEEP
    display_polynomial_label = False
    display_root_values = False
    n_steps = 25

    def construct(self):
        self.init_fractal(root_colors=self.colors)
        if self.display_polynomial_label:
            self.add_polynomial_label()
        if self.display_root_values:
            self.add_root_labels()

    def add_polynomial_label(self):
        n = len(self.fractal.roots)
        t2c = {
            f"r_{i + 1}": interpolate_color(self.colors[i], WHITE, 0.5)
            for i in range(n)
        }
        label = OldTex(
            "p(z) = ", *(
                f"(z - r_{i})"
                for i in range(1, n + 1)
            ),
            tex_to_color_map=t2c,
            font_size=36
        )
        label.to_corner(UL)
        label.set_stroke(BLACK, 5, background=True)
        self.add(label)

    def add_root_labels(self):
        for n, root_dot in zip(it.count(1), self.root_dots):
            self.add(self.get_root_label(root_dot, n))

    def get_root_label(self, root_dot, n):
        def get_z():
            return self.plane.p2n(root_dot.get_center())
        label = VGroup(
            OldTex(f"r_{n} = "),
            DecimalNumber(get_z(), include_sign=True),
        )
        label.scale(0.5)
        label.set_stroke(BLACK, 3, background=True)

        def update_label(label):
            label.arrange(RIGHT, buff=0.1)
            label[0].shift(0.1 * label[0].get_height() * DOWN)
            label.next_to(root_dot, UR, SMALL_BUFF)
            label[1].set_value(get_z())

        label.add_updater(update_label)
        return label


class ThreeRootFractal(SimpleFractalScene):
    coefs = [-1.0, 0.0, 0.0, 1.0]
    colors = ROOT_COLORS_DEEP[::2]
    n_steps = 30



# ----- From _2021/holomorphic_dynamics.py -----

class PlayWithRootsSeekingCycles(ThreeRootFractal):
    coefs = [2, -2, 0, 1]

    def construct(self):
        super().construct()
        self.fractal.uniforms["black_for_cycles"] = 1.0
