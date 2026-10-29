# ==============================================================================
# Scene:      SmallCircleProperty
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2615-2725)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl SmallCircleProperty.py SmallCircleProperty -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - The fractal orders the roots with the scene's coefficients_to_roots (like Grant), not with np.roots, so that each root keeps its color
#   - manimgl bug: with n_steps=0 the Newton shader gives NaN (log(0)); NewtonFractal is wrapped to start `step_size` at 1.0 with replace_shader_code (so n_steps=0 colors by the nearest root, as in the original)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/MulticoloredNewtonsMapCircle.png (disk with the basins of the cubic Newton fractal, numpy; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
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


# ----- From _2021/holomorphic_dynamics.py -----

MANDELBROT_COLORS = [
    "#00065c",
    "#061e7e",
    "#0c37a0",
    "#205abc",
    "#4287d3",
    "#D9EDE4",
    "#F0F9E4",
    "#BA9F6A",
    "#573706",
]


class SmallCircleProperty(Scene):
    def construct(self):
        # Titles
        rule = OldTexText(
            "For any rational map, color points\\\\based on their limiting behavior...\\\\",
            "(which limit point, which limit cycle, etc.)",
            font_size=36,
        )
        rule.to_corner(UL)
        rule[-1].shift(SMALL_BUFF * DOWN)
        rule[-1].set_color(GREY_B)

        r_map = OldTex("z_{n + 1} = A(z_n) / B(z_n)")
        r_map.to_corner(UR)

        # Fractal
        colors = [
            MANDELBROT_COLORS[0], BLUE_C, BLUE_E, ROOT_COLORS_DEEP[1],
        ]
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.set_height(5)
        plane.to_corner(DR)
        fractal = NewtonFractal(plane, coefs=[5, 4j, 3, 2, 1], colors=colors)

        # Circles
        circles = Circle(radius=0.6).get_grid(3, 1, buff=0.5)
        circles.replace(plane, 1)
        circles.set_x(-1)
        circles.set_stroke(WHITE, 2)

        circles[0].set_fill(colors[2], 1)
        semis = circles[1].copy().pointwise_become_partial(circles[1], 0, 0.5).replicate(2)
        semis[1].rotate(PI, about_point=circles[1].get_center())
        semis[0].set_fill(colors[0], 1)
        semis[1].set_fill(colors[1], 1)
        circles[1].add(semis)

        multi_color_image = ImageMobject("MulticoloredNewtonsMapCircle")
        multi_color_image.add_updater(lambda m: m.replace(circles[2]))

        # Circle label
        circle_labels = VGroup(
            Text("One color"),
            Text("Some colors"),
            Text("All colors"),
        )
        marks = VGroup(Checkmark(), Exmark(), Checkmark())
        for label, mark, circle in zip(circle_labels, marks, circles):
            mark.set_height(0.5 * circle.get_height())
            mark.next_to(circle, LEFT, MED_LARGE_BUFF)
            label.next_to(mark, LEFT, MED_LARGE_BUFF)

        # Little circles
        lil_circles = circles[0].replicate(2)
        lil_circles.set_height(0.2)
        lil_circles[0].move_to(plane.get_corner(UL) + MED_SMALL_BUFF * DR)
        lil_circles[1].move_to(plane).shift([0.22, -0.12, 0])
        lil_circles[1].set_fill(opacity=0)

        lines = VGroup()
        for big, lil in zip(circles[::2], lil_circles):
            vect = normalize(lil.get_center() - big.get_center())
            v1 = rotate_vector(vect, 75 * DEGREES)
            v2 = rotate_vector(vect, -75 * DEGREES)
            big.insert_n_curves(20)
            lines.add(VGroup(
                Line(lil.get_top(), big.get_boundary_point(v1)),
                Line(lil.get_bottom(), big.get_boundary_point(v2)),
            ))
        lines.set_stroke(WHITE, 1)

        # Intro anims
        self.add(rule[0])
        self.play(FadeIn(r_map))
        self.wait()
        fractal.set_opacity(0)
        self.add(fractal)
        for i in range(1, 5):
            opacities = np.zeros(4)
            opacities[:i] = 1
            self.play(fractal.animate.set_opacities(*opacities))
        self.wait()
        self.play(FadeIn(rule[-1], lag_ratio=0.1, run_time=2))
        self.wait()

        # Show circles
        self.add(lil_circles[0])
        self.play(
            TransformFromCopy(lil_circles[0], circles[0]),
            *map(ShowCreation, lines[0]),
            FadeIn(circle_labels[0]),
        )
        self.play(Write(marks[0]))
        self.wait()

        self.add(multi_color_image)
        self.add(lil_circles[1])
        self.play(
            TransformFromCopy(lil_circles[1], circles[2]),
            *map(ShowCreation, lines[1]),
            FadeIn(circle_labels[2]),
        )
        self.play(Write(marks[2]))
        self.wait()

        self.play(
            FadeIn(circle_labels[1]),
            FadeIn(circles[1]),
        )
        self.play(Write(marks[1]))
        self.wait()
