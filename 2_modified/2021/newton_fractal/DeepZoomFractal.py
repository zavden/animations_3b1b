# ==============================================================================
# Scene:      DeepZoomFractal
# Source:     videos/_2021/newton_fractal.py (lines 3107-3158)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl DeepZoomFractal.py DeepZoomFractal -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - The fractal orders the roots with the scene's coefficients_to_roots (like Grant), not with np.roots, so that each root keeps its color
#   - `fractal.colors` (manimgl does not store it) -> get_fractal_colors(fractal), which reads the colors from the uniform
#   - `unlock_mobject_data()`/`lock_static_mobject_data()` are removed from on_mouse_press (they no longer exist in manimgl; clicking a point would fail with AttributeError)
#   - The frame's `UpdateFromAlphaFunc` with rate_func=lambda t: smooth(min(t, 1)): in this manimgl it does not clip alpha to [0, 1] when another animation in the same play lasts longer (30 s vs 15 s), and the frame moved away from the zoom point (up to 31x) and came out a single color
#   - `drag_to_pan` is turned off while dragging a point (manimgl moves the frame when dragging, and the point did not move) and turned on again on release
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
        self.mouse_drag_point.move_to(point)
        mob.add_updater(lambda m: m.move_to(self.mouse_drag_point))
        # CHANGE: manimgl now moves the frame when dragging (drag_to_pan); while a point is being dragged
        # it is turned off, otherwise the frame shifts with the cursor and the point does not move
        self.drag_to_pan = False
        # CHANGE: `unlock_mobject_data()` removed: this manimgl no longer has it (there is no cached static data to lock)
        # CHANGE: `lock_static_mobject_data()` removed: this manimgl no longer has it (there is no cached static data to lock)

    def on_mouse_release(self, point, button, mods):
        super().on_mouse_release(point, button, mods)
        self.root_dots.clear_updaters()
        # CHANGE: frame panning is turned back on on release
        self.drag_to_pan = True


class DeepZoomFractal(IntroNewtonFractal):
    coefs = [-1.0, 0.0, 0.0, 1.0, 0.0, 1.0]

    plane_config = {
        "x_range": (-4, 4),
        "y_range": (-4, 4),
        "height": 16 * 1,
        "width": 16 * 1,
        "background_line_style": {
            "stroke_color": GREY_A,
            "stroke_width": 1.0,
        },
        "axis_config": {
            "stroke_width": 1.0,
        }
    }

    def construct(self):
        self.init_fractal(root_colors=ROOT_COLORS_DEEP)
        fractal, plane, root_dots = self.group

        he_tracker = ValueTracker(0)
        frame = self.camera.frame
        zoom_point = np.array([
            # -1.91177811, 0.52197285, 0.
            0.72681252, -0.66973296, 0.
        ], dtype=np.float64)

        initial_fh = FRAME_HEIGHT
        frame.add_updater(lambda m: m.set_height(
            initial_fh * 2**(-he_tracker.get_value()),
        ))
        # rd_height = root_dots.get_height()
        # root_dots.add_updater(lambda m: m.set_height(
        #     rd_height * 2**(he_tracker.get_value() / 8),
        #     about_point=zoom_point
        # ))

        self.add(frame)
        self.play(
            UpdateFromAlphaFunc(
                frame,
                lambda m, a: m.move_to(zoom_point * a),
                run_time=15,
                # CHANGE: in this manimgl UpdateFromAlphaFunc does not clip alpha to [0, 1] when another
                # animation in the same play lasts longer (30 s vs 15 s): with an extrapolated `smooth`
                # the frame kept moving away from the zoom point (up to 31x). It is clipped here.
                rate_func=lambda t: smooth(min(t, 1)),
            ),
            ApplyMethod(
                he_tracker.set_value, 14,
                run_time=30,
                rate_func=bezier([0, 0, 1, 1]),
            ),
        )
        self.wait()
