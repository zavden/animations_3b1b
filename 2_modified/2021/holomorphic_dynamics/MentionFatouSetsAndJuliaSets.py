# ==============================================================================
# Scene:      MentionFatouSetsAndJuliaSets
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2728-2916)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl MentionFatouSetsAndJuliaSets.py MentionFatouSetsAndJuliaSets -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - The fractal orders the roots with the scene's coefficients_to_roots (like Grant), not with np.roots, so that each root keeps its color
#   - `set_scale` -> `set_scale_factor` (name in manimgl)
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

class MentionFatouSetsAndJuliaSets(Scene):
    colors = [RED_E, BLUE_E, TEAL_E, MAROON_E]

    def construct(self):
        # Introduce terms
        f_group, j_group = self.get_fractals()
        f_name, j_name = VGroup(
            Text("Fatou set"),
            Text("Julia set"),
        )
        f_name.next_to(f_group, UP, MED_LARGE_BUFF)
        j_name.next_to(j_group, UP, MED_LARGE_BUFF)

        self.play(
            Write(j_name),
            GrowFromCenter(j_group)
        )
        self.wait()
        self.play(
            Write(f_name),
            *map(GrowFromCenter, f_group)
        )
        self.wait()

        # Define Fatou set
        fatou_condition = self.get_fatou_condition()
        fatou_condition.set_width(FRAME_WIDTH - 1)
        fatou_condition.center().to_edge(UP, buff=1.0)
        lhs, arrow, rhs = fatou_condition
        f_line = Line(LEFT, RIGHT)
        f_line.match_width(fatou_condition)
        f_line.next_to(fatou_condition, DOWN)
        f_line.set_stroke(WHITE, 1)

        self.play(
            FadeOut(j_name, RIGHT),
            FadeOut(j_group, RIGHT),
            Write(lhs)
        )
        self.wait()
        for words in lhs[-1]:
            self.play(FlashUnder(
                words,
                buff=0,
                time_width=1.5
            ))
        self.play(Write(arrow))
        self.play(LaggedStart(
            FadeTransform(f_name.copy(), rhs[1][:8]),
            FadeIn(rhs),
            lag_ratio=0.5
        ))
        self.wait()

        # Show Julia set
        otherwise = Text("Otherwise...")
        otherwise.next_to(rhs, DOWN, LARGE_BUFF)
        j_condition = OldTexText("$z_0 \\in$", " Julia set", " of $f$")
        j_condition.match_height(rhs)
        j_condition.next_to(otherwise, DOWN, LARGE_BUFF)

        j_group.set_height(4.0)
        j_group.to_edge(DOWN)
        j_group.set_x(-1.0)
        j_name = j_condition.get_part_by_tex("Julia set")
        j_underline = Underline(j_name, buff=0.05)
        j_underline.set_color(YELLOW)
        arrow = Arrow(
            j_name.get_bottom(),
            j_group.get_right(),
            path_arc=-45 * DEGREES,
        )
        arrow.set_stroke(YELLOW, 5)

        julia_set = j_group[0]
        julia_set.update()
        julia_set.suspend_updating()
        julia_copy = julia_set.copy()
        julia_copy.clear_updaters()
        julia_copy.set_colors(self.colors)
        julia_copy.set_julia_highlight(0)

        mover = f_group[:-4]
        mover.generate_target()
        mover.target.match_width(rhs)
        mover.target.next_to(rhs, UP, MED_LARGE_BUFF)
        mover.target.shift_onto_screen(buff=SMALL_BUFF)

        self.play(
            ShowCreation(f_line),
            FadeOut(f_name),
            MoveToTarget(mover),
        )
        self.play(
            Write(otherwise),
            FadeIn(j_condition, 0.5 * DOWN)
        )
        self.wait()
        self.play(
            ShowCreation(j_underline),
            ShowCreation(arrow),
            FadeIn(j_group[1]),
            FadeIn(julia_copy)
        )
        self.play(
            GrowFromPoint(julia_set, julia_set.get_corner(UL), run_time=2),
            julia_copy.animate.set_opacity(0.2)
        )
        self.wait()

    def get_fractals(self, jy=1.5, fy=-2.5):
        coefs = roots_to_coefficients([-1.5, 1.5, 1j, -1j])
        n = len(coefs) - 1
        colors = self.colors
        f_planes = VGroup(*(self.get_plane() for x in range(n)))
        f_planes.arrange(RIGHT, buff=LARGE_BUFF)
        plusses = OldTex("+").replicate(n - 1)
        f_group = Group(*it.chain(*zip(f_planes, plusses)))
        f_group.add(f_planes[-1])
        f_group.arrange(RIGHT)
        fatou = Group(*(
            NewtonFractal(f_plane, coefs=coefs, colors=colors)
            for f_plane in f_planes
        ))
        for i, fractal in enumerate(fatou):
            opacities = n * [0.2]
            opacities[i] = 1
            fractal.set_opacities(*opacities)
        f_group.add(*fatou)
        f_group.set_y(fy)

        j_plane = self.get_plane()
        j_plane.set_y(jy)
        julia = NewtonFractal(j_plane, coefs=coefs, colors=5 * [GREY_A])
        julia.set_julia_highlight(1e-3)
        j_group = Group(julia, j_plane)

        for fractal, plane in zip((*fatou, julia), (*f_planes, j_plane)):
            fractal.plane = plane
            fractal.add_updater(
                lambda m: m.set_offset(
                    m.plane.get_center()
                # CHANGE: set_scale -> set_scale_factor (name in manimgl)
                ).set_scale_factor(
                    m.plane.get_x_unit_size()
                ).replace(m.plane)
            )

        fractals = Group(f_group, j_group)
        return fractals

    def get_plane(self):
        plane = ComplexPlane(
            (-2, 2), (-2, 2),
            background_line_style={"stroke_width": 1, "stroke_color": GREY}
        )
        plane.set_height(2)
        plane.set_opacity(0)
        box = SurroundingRectangle(plane, buff=0)
        box.set_stroke(WHITE, 1)
        plane.add(box)
        return plane

    def get_fatou_condition(self):
        zn = OldTex(
            "z_0", "\\overset{f}{\\longrightarrow}",
            "z_1", "\\overset{f}{\\longrightarrow}",
            "z_2", "\\overset{f}{\\longrightarrow}",
            "\\dots",
            "\\longrightarrow"
        )
        words = VGroup(
            OldTexText("Stable fixed point"),
            OldTexText("Stable cycle"),
            OldTexText("$\\infty$"),
        )
        words.arrange(DOWN, aligned_edge=LEFT)
        brace = Brace(words, LEFT)
        zn.next_to(brace, LEFT)
        lhs = VGroup(zn, brace, words)

        arrow = OldTex("\\Rightarrow")
        arrow.scale(2)
        arrow.next_to(lhs, RIGHT, MED_LARGE_BUFF)
        rhs = OldTex("z_0 \\in", " \\text{Fatou set of $f$}")
        rhs.next_to(arrow, RIGHT, buff=MED_LARGE_BUFF)

        result = VGroup(lhs, arrow, rhs)

        return result
