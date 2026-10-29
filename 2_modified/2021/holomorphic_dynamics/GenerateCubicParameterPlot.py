# ==============================================================================
# Scene:      GenerateCubicParameterPlot
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2426-2598)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl GenerateCubicParameterPlot.py GenerateCubicParameterPlot -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal, MetaNewtonFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - The fractal orders the roots with the scene's coefficients_to_roots (like Grant), not with np.roots, so that each root keeps its color
#   - manimgl bug: with n_steps=0 the Newton shader gives NaN (log(0)); NewtonFractal is wrapped to start `step_size` at 1.0 with replace_shader_code (so n_steps=0 colors by the nearest root, as in the original)
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

ROOT_COLORS_DEEP = ["#440154", "#3b528b", "#21908c", "#5dc963", "#29abca"]


# CHANGE: manimgl's NewtonFractal, MetaNewtonFractal are used (manimlib/mobject/fractals.py, WGSL shaders). Grant's
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


# ----- From _2021/holomorphic_dynamics.py -----

class GenerateCubicParameterPlot(Scene):
    colors = ROOT_COLORS_DEEP[0::2]

    def construct(self):
        # Title
        colors = self.colors
        kw = {
            "tex_to_color_map": {
                "\\lambda": colors[2],
            }
        }
        title = OldTex(
            "z_{n+1} = z_n - {P(z_n) \\over P'(z_n)} \\qquad\\qquad ",
            "P(z) = (z - 1)(z + 1)(z - \\lambda)",
            font_size=30,
            **kw
        )
        title.to_edge(UP)
        self.add(title)

        # Planes
        planes = VGroup(*(
            ComplexPlane(
                (-2, 2), (-2, 2),
                background_line_style={
                    "stroke_color": GREY_B,
                    "stroke_opacity": 0.5,
                },
            )
            for x in range(2)
        ))
        for plane, vect in zip(planes, [DL, DR]):
            plane.add_coordinate_labels(font_size=18)
            plane.set_height(5)
            plane.to_corner(vect, buff=MED_SMALL_BUFF)

        root_dots = VGroup(*(
            Dot(planes[0].n2p(z), color=color)
            for color, z in zip(colors, [-1, 1, 1j])
        ))
        root_dots.set_stroke(BLACK, 2)

        lambda_label = OldTex("\\lambda", font_size=36)
        lambda_label.set_color(interpolate_color(colors[2], WHITE, 0.75))
        lambda_label.set_stroke(BLACK, 3, background=True)
        lambda_label.add_updater(lambda m: m.next_to(
            root_dots[2], UR, buff=SMALL_BUFF,
        ))

        # Fractals
        left_fractal = NewtonFractal(
            planes[0], coefs=[-1, 0, 0, 1],
            colors=colors,
            black_for_cycles=True,
        )
        left_fractal.add_updater(lambda m: m.set_roots([
            planes[0].p2n(rd.get_center())
            for rd in root_dots
        ]))

        right_fractal = MetaNewtonFractal(
            planes[1],
            colors=colors,
            fixed_roots=[-1, 1],
        )
        row_meta_fractal = right_fractal.deepcopy()
        col_meta_fractal = right_fractal.deepcopy()

        self.add(left_fractal, planes[0], planes, root_dots, lambda_label)

        # Plane titles
        plane_titles = VGroup(
            OldTexText("Pixel $\\leftrightarrow z_0$"),
            OldTexText("Pixel $\\leftrightarrow$ ", "$\\lambda$"),
        )
        plane_titles[1][-1].set_color(colors[2])
        for plane_title, plane in zip(plane_titles, planes):
            plane_title.next_to(plane, UP, MED_SMALL_BUFF)
        plane_titles[0].align_to(plane_titles[1], UP)

        self.add(plane_titles[0])

        # Show left plane
        pins = VGroup()
        for rd in root_dots[:2]:
            pin = SVGMobject("push_pin")
            pin.set_fill(GREY_C)
            pin.set_stroke(width=0)
            pin.set_gloss(0.5)
            pin.set_height(0.3)
            pin.rotate(10 * DEGREES)
            pin.move_to(rd.get_center(), DR)
            pins.add(pin)
            self.play(
                FadeIn(pin, 0.25 * DR),
                FlashAround(rd),
            )

        self.wait()
        circle = Circle()
        circle.scale(0.5)
        circle.rotate(PI / 2)
        circle.move_to(root_dots[2].get_center(), UP)

        self.play(MoveAlongPath(root_dots[2], circle, run_time=5))
        self.play(
            root_dots[2].animate.move_to(planes[0].get_corner(UL)),
            run_time=2
        )
        self.wait()

        # Center of mass dot
        com_dot = Dot()
        com_dot.set_fill(opacity=0)
        com_dot.set_stroke(YELLOW, 3)
        com_dot.add_updater(lambda m: m.move_to(
            np.array([rd.get_center() for rd in root_dots]).mean(0)
        ))
        self.play(FadeIn(com_dot, scale=0.5), FadeOut(pins))
        self.wait()

        # Right plane
        self.play(Write(plane_titles[1]))
        self.wait()

        # Show filling process
        step = 0.1
        square = Square()
        square.set_stroke(WHITE, 2)
        arrow = Arrow(LEFT, RIGHT, stroke_width=3)
        self.add(row_meta_fractal, col_meta_fractal, planes[1])
        self.add(square, arrow)

        x_range = np.arange(-2, 2 + step, step)
        y_range = np.arange(2, -2, -step)

        thin_height = plane.get_y_unit_size() * step
        col_meta_fractal.set_height(thin_height)
        square.set_height(thin_height)

        epsilon = 1e-6
        for y, back in zip(y_range, it.cycle([False, True])):
            height = max(epsilon, plane.get_y_unit_size() * abs(2 - y))
            row_meta_fractal.set_height(height, stretch=True)
            row_meta_fractal.move_to(planes[1], UP)
            x0 = (2 if back else -2)
            for x in (x_range[::-1] if back else x_range):
                width = max(epsilon, planes[1].get_x_unit_size() * abs(x - x0))
                col_meta_fractal.set_width(width, stretch=True)
                col_meta_fractal.next_to(row_meta_fractal, DOWN, buff=0)
                col_meta_fractal.align_to(row_meta_fractal, RIGHT if back else LEFT)

                root_dots[2].move_to(planes[0].c2p(x, y))
                square.move_to(
                    col_meta_fractal, DOWN + (LEFT if back else RIGHT)
                )
                self.update_mobjects(0)
                arrow.put_start_and_end_on(
                    com_dot.get_center(),
                    square.get_center(),
                )
                self.wait(1 / 15)

        self.play(FadeOut(arrow), FadeOut(square))
        self.wait()

        # Zoom in to meta fractal
        frame = self.camera.frame
        self.play(
            frame.animate.replace(planes[1], 1),
            run_time=3,
        )
        self.wait()
