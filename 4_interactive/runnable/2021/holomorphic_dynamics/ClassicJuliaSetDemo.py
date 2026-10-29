# ==============================================================================
# Scene:      ClassicJuliaSetDemo
# Source:     videos/_2021/holomorphic_dynamics.py (lines 975-1078)
# Category:   4 · Interactive (runnable)
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl ClassicJuliaSetDemo.py ClassicJuliaSetDemo -w -m --fps 15
#     manimgl ClassicJuliaSetDemo.py ClassicJuliaSetDemo        # interactive window
#
# How to interact:
#   Two planes: on the left the Mandelbrot set and on the right the Julia set of the chosen parameter c. After the initial animation, hold down the SPACE key and move the mouse: the yellow point c follows the cursor and the Julia set on the right changes with it (near the Mandelbrot boundary it looks connected, inside it is a closed curve, outside it is dust). The label shows the value of c.
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal, MandelbrotFractal, JuliaFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - background_line_style without "stroke_color" -> BLUE_D is added, the previous default (manimgl bug: NumberPlane.init_background_lines reads background_line_style["stroke_color"] with no fallback, coordinate_systems.py:669)
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


def get_c_dot_label(dot, get_c, font_size=24, direction=UP):
    c_label = VGroup(
        OldTex("c = ", font_size=font_size),
        DecimalNumber(get_c(), font_size=font_size, include_sign=True)
    ).arrange(RIGHT, buff=0.075)
    c_label[0].shift(0.02 * DOWN)
    c_label.set_color(YELLOW)
    c_label.set_stroke(BLACK, 5, background=True)
    c_label.add_updater(lambda m: m.next_to(dot, direction, SMALL_BUFF))
    c_label.add_updater(lambda m: m[1].set_value(get_c()))
    return c_label


class MandelbrotIntro(Scene):
    n_iterations = 30

    def construct(self):
        self.add_process_description()
        self.add_plane()
        self.show_iterations()
        self.add_mandelbrot_image()

    def add_process_description(self):
        kw = {
            "tex_to_color_map": {
                "{c}": YELLOW,
            }
        }
        terms = self.terms = VGroup(
            OldTex("z_{n + 1} = z_n^2 + {c}", **kw),
            OldTex("{c} \\text{ can be changed}", **kw),
            OldTex("z_0 = 0", **kw),
        )
        terms.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        terms.to_corner(UL)

        equation = OldTex("f(z) = z^2 + c")
        equation.to_edge(UP)

        self.process_terms = terms
        self.add(equation)
        self.wait()
        self.play(FadeTransform(equation, terms[0]))

    def add_plane(self):
        plane = self.plane = ComplexPlane((-2, 1), (-2, 2))
        plane.set_height(4)
        plane.set_height(1.5 * FRAME_HEIGHT)
        plane.next_to(2 * LEFT, RIGHT, buff=0)
        plane.add_coordinate_labels(font_size=24)
        self.add(plane)

    def show_iterations(self):
        plane = self.plane

        # c0 = complex(-0.2, 0.95)
        c0 = complex(-0.6, 0.4)

        c_dot = self.c_dot = Dot()
        c_dot.set_fill(YELLOW)
        c_dot.set_stroke(BLACK, 5, background=True)
        c_dot.move_to(plane.n2p(c0))
        c_dot.add_updater(lambda m: m)  # Null

        n_iter_tracker = ValueTracker(1)

        def get_n_iters():
            return int(n_iter_tracker.get_value())

        def get_c():
            return plane.p2n(c_dot.get_center())

        def update_lines(lines):
            z1 = 0
            c = get_c()
            new_lines = []

            for n in range(get_n_iters()):
                try:
                    z2 = z1**2 + c
                    new_lines.append(Line(
                        plane.n2p(z1),
                        plane.n2p(z2),
                        stroke_color=GREY,
                        stroke_width=2,
                    ))
                    new_lines.append(Dot(
                        plane.n2p(z2),
                        fill_color=YELLOW,
                        fill_opacity=0.5,
                        radius=0.05,
                    ))
                    z1 = z2
                except Exception:
                    pass

            lines.set_submobjects(new_lines)

        c_label = get_c_dot_label(c_dot, get_c)

        lines = VGroup()
        lines.set_stroke(background=True)
        lines.add_updater(update_lines)
        self.add(lines, c_dot, c_label)

        def increase_step(run_time=1.0):
            n_iter_tracker.increment_value(1)
            lines.update()
            lines.suspend_updating()
            self.add(*lines, c_dot, c_label)
            self.play(
                ShowCreation(lines[-2]),
                TransformFromCopy(lines[-3], lines[-1]),
                run_time=run_time
            )
            self.add(lines, c_dot, c_label)
            lines.resume_updating()

        kw = {
            "tex_to_color_map": {
                "c": YELLOW,
            }
        }
        new_lines = VGroup(
            OldTex("z_1 = 0^2 + c = c", **kw),
            OldTex("z_2 = c^2 + c", **kw),
            OldTex("z_3 = (c^2 + c)^2 + c", **kw),
            OldTex("z_4 = ((c^2 + c)^2 + c)^2 + c", **kw),
            OldTex("\\vdots", **kw),
        )
        new_lines.arrange(DOWN, aligned_edge=LEFT)
        new_lines[-2].scale(0.8, about_edge=LEFT)
        new_lines.next_to(self.process_terms[2], DOWN, aligned_edge=LEFT)
        new_lines[-1].match_x(new_lines[-2][0][2])

        # Show c
        self.wait()
        self.play(Write(self.process_terms[1]))
        self.wait(10)

        # Show first step
        dot = Dot(plane.n2p(0))
        self.play(FadeIn(self.process_terms[2], 0.5 * DOWN))
        self.play(FadeIn(dot, scale=0.2, run_time=2))
        self.play(FadeOut(dot))

        self.play(FadeIn(new_lines[0], 0.5 * DOWN))
        self.play(ShowCreationThenFadeOut(
            lines[0].copy().set_stroke(BLUE, 5)
        ))
        self.wait(3)

        # Show second step
        self.play(FadeIn(new_lines[1], 0.5 * DOWN))
        increase_step()
        self.wait(10)

        # Show 3rd to nth steps
        self.play(FadeIn(new_lines[2], 0.5 * DOWN))
        increase_step()
        self.play(FadeIn(new_lines[3], 0.5 * DOWN))
        increase_step()
        self.wait(5)
        self.play(FadeIn(new_lines[4]))
        for n in range(self.n_iterations):
            increase_step(run_time=0.25)

        # Play around
        self.wait(15)

    def add_mandelbrot_image(self):
        mandelbrot_set = MandelbrotFractal(self.plane)

        self.add(mandelbrot_set, *self.mobjects)
        self.play(
            FadeIn(mandelbrot_set, run_time=2),
            # self.plane.animate.set_opacity(0.5)
            self.plane.animate.set_stroke(WHITE, opacity=0.25)
        )

    # Listeners
    def on_mouse_motion(self, point, d_point):
        super().on_mouse_motion(point, d_point)
        if self.window.is_key_pressed(ord(" ")):
            self.c_dot.move_to(point)


class ClassicJuliaSetDemo(MandelbrotIntro):
    def construct(self):
        # Init planes
        kw = {
            # CHANGE: NumberPlane/ComplexPlane: background_line_style without stroke_color gives KeyError (manimgl no longer merges it with the default value, BLUE_D)
            "background_line_style": {
                "stroke_color": BLUE_D,
                "stroke_width": 0.5,
            }
        }
        planes = VGroup(
            ComplexPlane((-2, 1), (-1.6, 1.6), **kw),
            ComplexPlane((-2, 2), (-2, 2), **kw),
        )
        for plane, corner in zip(planes, [DL, DR]):
            plane.set_stroke(WHITE, opacity=0.5)
            plane.set_height(6)
            plane.to_corner(corner, buff=MED_SMALL_BUFF)
            plane.to_edge(DOWN, SMALL_BUFF)

        planes[1].add_coordinate_labels(font_size=18)
        planes[0].add_coordinate_labels(
            (-1, 0, 1, 1j, -1j),
            font_size=18
        )

        # Init fractals
        mandelbrot = MandelbrotFractal(planes[0])
        julia = JuliaFractal(planes[1])
        fractals = Group(mandelbrot, julia)

        self.add(*fractals, *planes)

        # Add c_dot
        c_dot = self.c_dot = Dot(radius=0.05)
        c_dot.set_fill(YELLOW, 1)
        c_dot.move_to(planes[0].c2p(-0.5, 0.5))
        c_dot.add_updater(lambda m: m)

        def get_c():
            return planes[0].p2n(c_dot.get_center())

        c_label = get_c_dot_label(c_dot, get_c, direction=UR)
        julia.add_updater(lambda m: m.set_c(get_c()))

        self.add(c_dot, c_label)

        # Add labels
        kw = {
            "tex_to_color_map": {
                "{z_0}": GREY_A,
                "{c}": YELLOW,
                "\\text{Pixel}": BLUE_D,
            },
        }

        title = OldTexText("Iterate\\\\$z^2 + c$")
        title.move_to(Line(*planes))
        title[0][-1].set_color(YELLOW)
        self.add(title)

        labels = VGroup(
            VGroup(
                OldTex("{c} \\leftrightarrow \\text{Pixel}", **kw),
                OldTex("z_0 = 0", **kw),
            ),
            VGroup(
                OldTex("{c} = \\text{const.}", **kw),
                OldTex("z_0 \\leftrightarrow \\text{Pixel}", **kw),
            )
        )

        for label, plane in zip(labels, planes):
            label.arrange(DOWN, aligned_edge=LEFT)
            label.next_to(plane, UP)

        space_labels = VGroup(
            OldTex("{c}\\text{-space}", **kw),
            OldTex("{z_0}\\text{-space}", **kw),
        )
        for label, plane in zip(space_labels, planes):
            label.scale(0.5)
            label.move_to(plane, UL).shift(SMALL_BUFF * DR)
        self.add(space_labels)

        # Animations
        self.add(labels[0])
        self.wait(2)
        self.play(
            TransformFromCopy(
                labels[0][0][0],
                labels[1][0][0],
            ),
            FadeIn(labels[1][0][1]),
        )
        self.wait(2)
        self.play(
            TransformFromCopy(
                labels[0][1].get_part_by_tex("z_0"),
                labels[1][1].get_part_by_tex("z_0"),
            ),
            FadeTransform(
                labels[0][0][1:].copy(),
                labels[1][1][1:],
            ),
        )
