# ==============================================================================
# Scene:      DescribeChaos
# Source:     videos/_2021/holomorphic_dynamics.py (lines 3188-3260)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl DescribeChaos.py DescribeChaos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal, MandelbrotFractal, JuliaFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
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


# CHANGE: manimgl's NewtonFractal, MandelbrotFractal, JuliaFractal are used (manimlib/mobject/fractals.py, WGSL shaders). Grant's
# copy, with GLSL shaders (`shader_folder`), which this manimgl cannot use, was here.


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


class DescribeChaos(Scene):
    def construct(self):
        j_point = 3 * LEFT
        j_value = -0.36554 - 0.29968j

        plane = ComplexPlane((-3, 3), (-2, 2))
        plane.scale(50)
        plane.shift(j_point - plane.n2p(j_value))
        fractal = JuliaFractal(plane)
        fractal.set_c(-0.5 + 0.5j)
        self.add(fractal, plane)

        j_dot = Dot(color=YELLOW, radius=0.05)
        j_dot.move_to(j_point)

        j_label = Text("Julia set point", color=YELLOW)
        j_label.next_to(j_dot, UP, buff=1.0).shift(LEFT)
        j_arrow = Line(j_label.get_bottom(), j_dot.get_center(), buff=0.1)
        j_arrow.set_stroke(width=3)
        j_arrow.set_color(YELLOW)

        surrounding_dots = VGroup(*(
            Dot(radius=0.05).move_to(j_dot.get_center() + buff * vect)
            for n, buff in [(6, 0.2), (12, 0.4)]
            for vect in compass_directions(n)
        ))
        surrounding_dots.set_color(GREY_B)
        # for dot in surrounding_dots:
        #     dot.shift(0.1 * (random.random() - 0.5))
        dots_label = Text("Immediate neighbors")
        dots_label.next_to(surrounding_dots, DOWN)
        dots_label.set_color(GREY_A)
        sublabel = Text("drift far away")
        sublabel.set_color(GREY_A)
        sublabel.next_to(dots_label, DOWN)
        fa = sublabel.get_part_by_text("far away")
        strike = Line(LEFT, RIGHT)
        strike.set_stroke(RED, 10)
        strike.replace(fa, 0)
        new_words = Text("everywhere!")
        new_words.next_to(fa, DOWN)
        new_words.set_color(RED)

        all_words = VGroup(j_label, dots_label, sublabel, new_words)
        all_words.set_stroke(BLACK, 5, background=True)

        arrows = VGroup()
        for dot in surrounding_dots[-12:]:
            point = dot.get_center()
            vect = 0.6 * normalize(point - j_dot.get_center())
            arrows.add(Arrow(point, point + vect, buff=0.1))
        arrows.set_stroke(RED)

        self.add(j_dot)
        self.add(surrounding_dots)
        self.add(j_label, j_arrow)
        self.add(dots_label)

        frame = self.camera.frame
        frame.save_state()
        frame.replace(plane)
        self.play(Restore(frame, run_time=5))
        self.wait()
        self.play(FadeIn(sublabel, lag_ratio=0.1))
        self.wait()
        self.play(
            ShowCreation(strike),
            FadeIn(new_words, shift=0.25 * DOWN)
        )

        self.add(arrows, all_words, strike)
        self.play(LaggedStartMap(ShowCreation, arrows))
        self.wait()
