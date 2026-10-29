# ==============================================================================
# Scene:      PeculiarBoundaryProperty
# Source:     videos/_2021/newton_fractal.py (lines 3761-3895)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl PeculiarBoundaryProperty.py PeculiarBoundaryProperty -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - The fractal orders the roots with the scene's coefficients_to_roots (like Grant), not with np.roots, so that each root keeps its color
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


CUBIC_COLORS = [RED_E, TEAL_E, BLUE_E]


# CHANGE: manimgl's NewtonFractal is used (manimlib/mobject/fractals.py, WGSL shaders). Grant's
# copy, with GLSL shaders (`shader_folder`), which this manimgl cannot use, was here.

# CHANGE: manimgl orders the roots of some coefficients with np.roots; Grant ordered them with the
# coefficients_to_roots above (the one from roots_and_coefs), and which root gets which color
# depends on that order. The scene's own is used so that the basins match the root points.
import manimlib.mobject.fractals as _manimgl_fractals
_manimgl_fractals.coefficients_to_roots = coefficients_to_roots


class PeculiarBoundaryProperty(Scene):
    coefs = [-1, 0, 0, 1]
    colors = [RED_E, TEAL_E, BLUE_E]

    def construct(self):
        # Title
        title = Text("Peculiar property", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.set_stroke(BLACK, 5, background=True)
        underline = Underline(title, buff=-0.05)
        underline.set_width(title.get_width() + 1)
        underline.insert_n_curves(20)
        underline.set_stroke(BLUE, [1, *5 * [3], 1])

        subtitle = OldTexText(
            "Boundary of one color",
            " = "
            "Boundary of any other",
            tex_to_color_map={
                "one color": BLUE_D,
                "any other": RED_D,
            }
        )
        subtitle.next_to(underline, DOWN, MED_LARGE_BUFF)

        # Setup for planes
        grid = VGroup(*(
            ComplexPlane(
                x_range=(-3, 3),
                y_range=(-2, 2),
            )
            for n in range(6)
        ))

        grid.arrange_in_grid(2, 3, v_buff=2, h_buff=3)
        grid.set_width(FRAME_WIDTH - 2)
        grid.to_edge(DOWN, buff=MED_LARGE_BUFF)

        arrows = VGroup()
        bound_words = VGroup()
        for p1, p2 in zip(grid[:3], grid[3:]):
            arrow = Arrow(p1, p2, stroke_width=4, buff=0.1)
            arrows.add(arrow)
            bound_word = Text("Boundary", font_size=24)
            bound_word.next_to(arrow, RIGHT, buff=SMALL_BUFF)
            bound_words.add(bound_word)

        low_equals = VGroup(
            OldTex("=").move_to(grid[3:5]),
            OldTex("=").move_to(grid[4:6]),
        )

        # Fractals
        fractals = Group(*(
            NewtonFractal(plane, coefs=self.coefs, colors=self.colors)
            for plane in grid
        ))
        alpha = 0.2
        for k in 0, 3:
            fractals[0 + k].set_opacities(alpha, 1, alpha)
            fractals[1 + k].set_opacities(alpha, alpha, 1)
            fractals[2 + k].set_opacities(1, alpha, alpha)

        boxes = VGroup(*(
            SurroundingRectangle(fractal, buff=0)
            for fractal in fractals
        ))
        boxes.set_stroke(GREY_B, 1)

        # Initial fractal
        big_plane = grid[0].deepcopy()
        big_plane.set_height(6.5)
        big_plane.center().to_edge(DOWN)
        big_fractal = NewtonFractal(big_plane, coefs=self.coefs, colors=self.colors)
        big_julia = big_fractal.copy()
        big_julia.set_julia_highlight(1e-3)
        big_julia.set_colors(3 * [WHITE])

        self.add(big_fractal)

        # Animations
        def get_show_border_anims(fractal):
            f_copy = fractal.copy()
            fractal.set_julia_highlight(5e-3)
            fractal.set_colors(3 * [WHITE])
            return (FadeOut(f_copy), GrowFromCenter(fractal))

        def high_to_low_anims(index):
            return (
                ShowCreation(arrows[index]),
                FadeIn(bound_words[index]),
                TransformFromCopy(fractals[index], fractals[index + 3]),
                TransformFromCopy(boxes[index], boxes[index + 3]),
            )

        self.add(underline, title)
        self.play(
            ShowCreation(underline),
            GrowFromCenter(big_julia, run_time=4)
        )
        self.play(
            big_julia.animate.set_julia_highlight(0.02).set_colors(CUBIC_COLORS).set_opacity(0)
        )
        self.wait()

        self.play(
            big_fractal.animate.set_opacities(alpha, alpha, 1)
        )
        self.wait()

        self.play(
            ReplacementTransform(big_fractal, fractals[1]),
            FadeIn(subtitle[:2]),
            ReplacementTransform(
                boxes[1].copy().replace(big_fractal).set_opacity(0),
                boxes[1],
            ),
        )
        self.play(*high_to_low_anims(1))
        self.play(*get_show_border_anims(fractals[4]))
        self.wait(2)

        subtitle[2:].set_opacity(0)
        self.add(subtitle[2:])
        for i in 2, 0:
            self.play(
                FadeIn(fractals[i]),
                FadeIn(boxes[i]),
                subtitle[2:].animate.set_opacity(1),
            )
            self.play(*high_to_low_anims(i))
            self.play(*get_show_border_anims(fractals[i + 3]))
            self.wait()

        self.play(Write(low_equals))
