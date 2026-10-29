# ==============================================================================
# Scene:      Cycles
# Source:     videos/_2021/holomorphic_dynamics.py (lines 1753-2099)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl Cycles.py Cycles -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingShapes has no `fade_transform_mismatches`; the argument is removed
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex no longer accepts OldTex: it has no get_symbol_substrings)
#   - Grant's NewtonFractal, MandelbrotFractal, JuliaFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - background_line_style without "stroke_color" -> BLUE_D is added, the previous default (manimgl bug: NumberPlane.init_background_lines reads background_line_style["stroke_color"] with no fallback, coordinate_systems.py:669)
#   - ParametricCurve(t_range=(0, TAU)) -> t_range=(0, TAU, 0.1) (it now requires the step)
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


def glow_dot(point, r_min=0.05, r_max=0.15, color=YELLOW, n=20, opacity_mult=1.0):
    result = VGroup(*(
        Dot(point, radius=interpolate(r_min, r_max, a))
        for a in np.linspace(0, 1, n)
    ))
    result.set_fill(color, opacity=opacity_mult / n)
    return result


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


def get_iteration_label(font_size=36):
    kw = {
        "tex_to_color_map": {
            "z_0": BLUE_C,
            "z_1": BLUE_D,
            "z_2": GREEN_D,
            "z_3": GREEN_E,
            "z_{n + 1}": GREEN_D,
            "z_n": BLUE,
            "\\longrightarrow": WHITE,
        },
        "font_size": font_size,
    }
    iterations = OldTex(
        """
        z_0 \\longrightarrow
        z_1 \\longrightarrow
        z_2 \\longrightarrow
        z_3 \\longrightarrow
        \\cdots
        """,
        **kw
    )
    for part in iterations.get_parts_by_tex("\\longrightarrow"):
        f = OldTex("f", **kw)
        f.scale(0.5)
        f.next_to(part, UP, buff=0)
        part.add(f)

    rule = OldTex("z_{n + 1} &= f(z_n)", **kw)
    result = VGroup(rule, iterations)
    result.arrange(DOWN, buff=MED_LARGE_BUFF)
    return result


class FixedPoints(Scene):
    def construct(self):
        # Set the stage
        iter_label = self.add_labels()
        rule, iterations = iter_label
        plane = self.add_plane()
        z_dot, z_label = self.add_z_dot()

        # Ask question
        question = OldTexText("When does $z$ stay fixed in place?")
        question.next_to(plane, RIGHT, MED_LARGE_BUFF, aligned_edge=UP)

        arrow = self.get_arrow_loop(z_dot)

        # f(z) = z
        t2c = {"z": BLUE}
        kw = {
            "tex_to_color_map": t2c,
            "isolate": ["=", "\\Rightarrow", "A(", "B(", ")"],
        }
        equation = OldTex("f(z) = z", **kw)
        equation.next_to(question, DOWN, MED_LARGE_BUFF)

        newton_example = OldTex(
            "z - {P(z) \\over P'(z)} = z",
            "\\quad \\Leftrightarrow \\quad ",
            "P(z) = 0",
            **kw,
        )
        newton_example.next_to(equation, DOWN, buff=LARGE_BUFF)
        mandelbrot_example = OldTex(
            "\\text{Exercise 1a: Find the fixed points}\\\\",
            "\\text{of }", "f(z) = z^2 + c",
            alignment="\\centering",
            **kw
        )
        mandelbrot_example[1:].match_x(mandelbrot_example[0])
        mandelbrot_example.move_to(newton_example)

        fixed_point = Text("Fixed point")
        fixed_point.next_to(equation, DOWN, LARGE_BUFF)
        fixed_point.to_edge(RIGHT)
        fp_arrow = Arrow(
            fixed_point.get_left(),
            equation[1].get_bottom(),
            path_arc=-PI / 4,
        )
        fp_group = VGroup(fixed_point, fp_arrow)
        fp_group.set_color(YELLOW)

        self.play(FadeIn(equation, DOWN))
        self.wait(2)
        self.play(
            FadeIn(fixed_point),
            ShowCreation(fp_arrow),
        )
        self.wait()
        self.play(
            FadeIn(newton_example, shift=0.5 * DOWN),
            FadeOut(fp_group),
        )
        self.wait(2)
        self.play(
            FadeOut(newton_example, 0.5 * DOWN),
            FadeIn(mandelbrot_example, 0.5 * DOWN),
        )
        self.wait(2)

        # Rational function
        question_group = VGroup(question, equation)
        question_group.generate_target()
        iterations.generate_target()
        VGroup(question_group.target, iterations.target).to_edge(UP)

        rational_parts = VGroup(
            OldTex("{A(z) \\over B(z)} = z", **kw),
            OldTex("A(z) = z \\cdot B(z)", **kw),
            OldTex("A(z) - z \\cdot B(z) = 0", **kw),
        )
        rational_parts.arrange(DOWN, buff=MED_LARGE_BUFF)
        for part, tex in zip(rational_parts[1:], ("=", "-")):
            curr_x = part.get_part_by_tex(tex).get_x()
            target_x = rational_parts[0].get_part_by_tex("=").get_x()
            part.shift((target_x - curr_x) * RIGHT)
        rational_parts.next_to(question_group.target, DOWN, LARGE_BUFF)

        self.play(
            FadeOut(rule, UP),
            MoveToTarget(question_group),
            MoveToTarget(iterations),
            FadeOut(mandelbrot_example),
            FadeIn(rational_parts[0])
        )
        self.wait()
        for p1, p2 in zip(rational_parts, rational_parts[1:]):
            self.play(
                # CHANGE: TransformMatchingTex only works with the new Tex (get_symbol_substrings); with OldTex the shapes are matched
                TransformMatchingShapes(
                    p1.copy(), p2,
                    path_arc=PI / 2,
                    run_time=2,
                )
            )
            self.wait(2)

        rect = SurroundingRectangle(rational_parts[-1])
        solution_words = Text("Must have\nsolutions!", font_size=36)
        solution_words.set_color(YELLOW)
        solution_words.next_to(rect, RIGHT)
        solution_words.shift_onto_screen()

        self.play(
            ShowCreation(rect),
            Write(solution_words, run_time=1),
        )
        self.wait()

        example_roots = [
            -1.5 + 0.5j, -1.5 - 0.5j,
            -1.0 + 1.2j, -1.0 - 1.2j,
            1.0 + 1.0j, 1.0 - 1.0j,
            0.5, 1.7,
        ]
        glow_dots = VGroup(*(
            glow_dot(plane.n2p(root))
            for root in example_roots
        ))

        self.play(LaggedStartMap(
            FadeIn, glow_dots,
            scale=0.5,
            lag_ratio=0.2,
        ))
        self.wait()

        # Ask about stability
        def get_arrows(point, inward=False):
            arrows = VGroup(*(
                Arrow(ORIGIN, vect, buff=0.3)
                for vect in compass_directions(8)
            ))
            arrows.set_height(1)
            arrows.move_to(point)
            if inward:
                for arrow in arrows:
                    arrow.rotate(PI)
            return arrows

        outward_arrows = get_arrows(glow_dots[2])
        inward_arrows = get_arrows(glow_dots[4], inward=True)
        arrow_groups = VGroup(inward_arrows, outward_arrows)

        stability_words = VGroup(
            Text("Attracting"),
            Text("Repelling"),
        )
        for words, arrows in zip(stability_words, arrow_groups):
            words.scale(0.7)
            words.next_to(arrows, UP, SMALL_BUFF)
            words.set_color(GREY_A)
            words.set_stroke(BLACK, 5, background=True)

        stability_question = Text(
            "When are fixed points stable?"
        )
        stability_question.move_to(question)
        stable_underline = Underline(
            stability_question.get_part_by_text("stable")
        )
        stable_underline.insert_n_curves(20)
        stable_underline.scale(1.2)
        stable_underline.set_stroke(MAROON_B, [1, *4 * [4], 1])

        self.play(
            FadeOut(question, RIGHT),
            FadeIn(stability_question, RIGHT),
            FadeOut(arrow),
            FadeOut(z_dot),
            FadeOut(z_label),
        )
        self.play(ShowCreation(stable_underline))
        self.wait()

        for words, arrows in zip(stability_words, arrow_groups):
            self.play(
                FadeIn(words),
                ShowCreation(arrows, lag_ratio=0.2, run_time=3)
            )
            self.wait()

        # Show derivative condition
        morty = Mortimer(height=2)
        morty.to_corner(DR)

        deriv_ineq = OldTex("|f'(z)| < 1", **kw)
        deriv_ineq.next_to(equation, DOWN, MED_LARGE_BUFF)

        equation.generate_target()
        group = VGroup(equation.target, deriv_ineq)
        group.arrange(RIGHT, buff=LARGE_BUFF)
        group.move_to(equation)

        attracting_condition = deriv_ineq.copy()
        repelling_condition = OldTex("|f'(z)| > 1", **kw)
        conditions = VGroup(attracting_condition, repelling_condition)
        for condition, words in zip(conditions, stability_words):
            condition.scale(0.7)
            condition.set_stroke(BLACK, 5, background=True)
            condition.move_to(words, DOWN)
            if conditions is conditions[0]:
                condition.shift(SMALL_BUFF * UP)
            words.generate_target()
            words.target.next_to(condition, UP, buff=MED_SMALL_BUFF)

        self.play(
            LaggedStartMap(FadeOut, VGroup(
                *rational_parts, rect, solution_words,
            )),
            VFadeIn(morty),
            morty.change("tease"),
        )
        self.play(PiCreatureSays(
            morty, "Use derivatives!",
            target_mode="hooray",
            bubble_config={
                "height": 2,
                "width": 4,
            }
        ))
        self.play(Blink(morty))
        self.wait()
        self.play(RemovePiCreatureBubble(morty, target_mode="happy"))
        for condition, words in zip(conditions, stability_words):
            self.play(
                Write(condition),
                MoveToTarget(words),
            )
            self.wait()
        self.play(
            FadeInFromPoint(deriv_ineq, morty.get_corner(UL)),
            MoveToTarget(equation),
            morty.change("raise_right_hand")
        )
        self.play(Blink(morty))

        # Newton derivative examples
        newton_case = VGroup(
            OldTex("f(z) = z - {P(z) \\over P'(z)}", **kw),
            OldTex("f'(z) = {P(z)P''(z) \\over P'(z)^2}", **kw),
            OldTex("P(z) = 0 \\quad \\Rightarrow \\quad f'(z) = 0", **kw),
        )
        newton_case.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        newton_case.scale(0.8)
        newton_case.next_to(equation, DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)

        alt_line1 = OldTex("f'(z) = 1 - {P'(z)P'(z) - P(z)P''(z) \\over P'(z)^2}", **kw)
        alt_line1.match_height(newton_case[1])
        alt_line1.move_to(newton_case[1], LEFT)

        self.play(
            # CHANGE: TransformMatchingTex only works with the new Tex (get_symbol_substrings); with OldTex the shapes are matched
            TransformMatchingShapes(equation.copy()[:3], newton_case[0]),
            morty.change("pondering", newton_case[0]),
        )
        self.wait()
        self.play(
            # CHANGE: TransformMatchingTex only works with the new Tex (get_symbol_substrings); with OldTex the shapes are matched
            TransformMatchingShapes(
                deriv_ineq[:-1].copy(),
                alt_line1[:4],
            )
        )
        self.wait()
        self.play(
            FadeIn(alt_line1[4:], lag_ratio=0.1, run_time=1.5),
            morty.animate.scale(0.8, about_edge=DR).change("sassy", alt_line1),
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            # CHANGE: TransformMatchingTex only works with the new Tex (get_symbol_substrings); with OldTex the shapes are matched
            TransformMatchingShapes(alt_line1[4:], newton_case[1][4:]),
            morty.change("tease", alt_line1),
        )
        self.remove(alt_line1)
        self.add(newton_case[1])
        self.wait()
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.change("pondering", newton_case[2]),
            FadeIn(newton_case[2])
        )
        self.play(Blink(morty))
        self.wait()

        # Show super-attraction
        super_arrows = VGroup(*(
            get_arrows(dot, inward=True)
            for dot in glow_dots
        ))
        attraction_anims = []
        for cluster in super_arrows:
            for arrow in cluster:
                new_arrow = arrow.copy()
                new_arrow.scale(1.5)
                new_arrow.set_stroke(YELLOW, 8)
                attraction_anims.append(
                    ShowCreationThenFadeOut(new_arrow)
                )

        rect = SurroundingRectangle(newton_case[2][6:])
        super_words = OldTexText("``Superattracting''", font_size=36)
        super_words.set_color(YELLOW)
        super_words.next_to(rect, DOWN, SMALL_BUFF)

        self.play(
            morty.change("thinking"),
            ShowCreation(rect),
            FadeIn(super_words)
        )
        self.play(
            LaggedStartMap(FadeOut, VGroup(
                *conditions, *stability_words,
                outward_arrows, inward_arrows,
            )),
            LaggedStartMap(FadeIn, super_arrows, scale=0.5)
        )
        self.play(
            LaggedStart(*attraction_anims, lag_ratio=0.02),
            run_time=3
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, VGroup(
                *super_arrows, *newton_case,
                rect, super_words, morty,
                glow_dots,
            ))
        )

        # Mandelbrot exercise
        part1 = mandelbrot_example
        part1.set_height(0.9)
        part2 = OldTexText(
            "Exercise 1b: Determine when at least\\\\"
            "one fixed point is attracting.",
        )
        part3 = OldTexText(
            "Exercise 1c$^{**}$: Show that the set of values\\\\",
            "$c$ satisfying this form a cardioid.",
            tex_to_color_map={"$c$": YELLOW}
        )
        parts = VGroup(part1, part2, part3)
        for part in part2, part3:
            part.scale(part1[0][0].get_height() / part[0][0].get_height())
        parts.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        parts.next_to(
            VGroup(equation, deriv_ineq),
            DOWN, buff=LARGE_BUFF,
        )

        mandelbrot = MandelbrotFractal(plane)

        R = 0.25
        cardioid = ParametricCurve(
            lambda t: plane.c2p(
                2 * R * math.cos(t) - R * math.cos(2 * t),
                2 * R * math.sin(t) - R * math.sin(2 * t),
            ),
            # CHANGE: ParametricCurve requires t_range with 3 values (t_min, t_max, step)
            t_range=(0, TAU, 0.1)
        )
        cardioid.set_stroke(YELLOW, 4)

        self.add(mandelbrot, plane)
        plane.generate_target(use_deepcopy=True)
        plane.target.set_stroke(WHITE, opacity=0.5)
        self.play(
            MoveToTarget(plane),
            FadeIn(mandelbrot),
            FadeIn(part1),
        )
        self.wait()
        self.play(Write(part2))
        self.wait()
        print(self.num_plays)
        self.play(Write(part3))
        self.play(ShowCreation(cardioid, run_time=4, rate_func=linear))
        self.play(
            cardioid.animate.set_fill(YELLOW, 0.25),
            run_time=2
        )
        self.wait()

    def add_labels(self):
        iter_label = get_iteration_label(48)
        iter_label.to_edge(UP)
        self.add(iter_label)
        return iter_label

    def add_plane(self):
        plane = self.plane = ComplexPlane(
            (-2, 2), (-2, 2),
            # CHANGE: NumberPlane/ComplexPlane: background_line_style without stroke_color gives KeyError (manimgl no longer merges it with the default value, BLUE_D)
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
            }
        )
        plane.set_height(5)
        plane.to_corner(DL)
        plane.add_coordinate_labels(font_size=16)
        self.add(plane)
        return plane

    def add_z_dot(self, z=1 + 1j, z_tex="z"):
        z_dot = Dot(radius=0.05, color=BLUE)
        z_dot.move_to(self.plane.n2p(z))
        z_label = OldTex(z_tex, font_size=30)
        z_label.next_to(z_dot, UL, buff=0)
        self.add(z_dot, z_label)
        return z_dot, z_label

    def get_arrow_loop(self, dot):
        arrow = Line(
            dot.get_bottom(),
            dot.get_right(),
            path_arc=330 * DEGREES,
            buff=0.05,
        )
        arrow.add_tip(width=0.15, length=0.15)
        arrow.set_color(GREY_A)
        return arrow


class Cycles(FixedPoints):
    def construct(self):
        # Set the stage
        iter_label = self.add_labels()
        rule, iterations = iter_label
        self.remove(rule)
        iterations.to_edge(UP)

        plane = self.add_plane()
        z0_dot, z0_label = self.add_z_dot(complex(-1.1, 0.6), "z_0")
        z1_dot, z1_label = self.add_z_dot(complex(0.2, -0.5), "z_1")
        z1_label.next_to(z1_dot, UR, SMALL_BUFF)
        z_dots = VGroup(z0_dot, z1_dot)
        z_labels = VGroup(z0_label, z1_label)

        # Ask question
        question = OldTexText("When does $z$ cycle?")
        question.next_to(plane, UP, MED_SMALL_BUFF)

        kw = {"path_arc": PI / 3, "buff": 0.1}
        arrows = VGroup(
            Arrow(z0_dot, z1_dot, **kw),
            Arrow(z1_dot, z0_dot, **kw),
        )
        arrows.set_stroke(opacity=0.75)
        z_dot = z0_dot.copy()
        z_dot.set_color(YELLOW)

        self.add(question)
        self.play(
            ShowCreation(arrows[0]),
            TransformFromCopy(z0_dot, z1_dot, path_arc=-PI / 3),
            TransformFromCopy(z0_label, z1_label, path_arc=-PI / 3),
        )
        self.wait()
        self.play(
            TransformFromCopy(z1_dot, z_dot, path_arc=-PI / 3),
            ShowCreation(arrows[1]),
        )
        self.wait()
        for n in range(1, 5):
            self.play(z_dot.move_to, z_dots[n % 2], path_arc=PI / 3)
            self.wait()

        # Show formula
        kw = {
            "tex_to_color_map": {"z": BLUE},
            "isolate": ["f"],
        }

        f2_equation = OldTex("f(f(z)) = z", **kw)
        f2_equation.next_to(plane, RIGHT, MED_LARGE_BUFF, aligned_edge=UP)

        julia_fractal = JuliaFractal(plane)
        julia_fractal.set_c(-0.18 + 0.77j)

        z2c = OldTex("f(z) = z^2 + c", **kw)
        z2c.next_to(f2_equation, RIGHT, LARGE_BUFF)

        self.play(FadeIn(f2_equation, 0.25 * DOWN))
        self.wait()
        self.add(julia_fractal, plane, z_dots, z_dot, z_labels, arrows, z_dot)
        julia_fractal.set_opacity(0)
        self.play(
            julia_fractal.animate.set_opacity(0.75),
            Write(z2c),
        )
        self.wait()

        # Example with z^2 + c
        julia_f2_eqs = VGroup(
            OldTex("(z^2 + c)^2 + c = z", **kw),
            OldTex("z^4 + 2cz^2 -z + c^2 + c = 0", **kw),
        )
        julia_f2_eqs.arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        julia_f2_eqs.next_to(f2_equation, DOWN, buff=1.0, aligned_edge=LEFT)

        eq_arrows = VGroup(
            Arrow(f2_equation.get_bottom(), julia_f2_eqs.get_top()),
            Arrow(z2c.get_bottom(), julia_f2_eqs.get_top()),
        )

        self.play(
            *map(ShowCreation, eq_arrows),
            FadeIn(julia_f2_eqs[0], 0.5 * DOWN)
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                julia_f2_eqs[0].copy(),
                julia_f2_eqs[1]
            )
        )
        self.wait()

        # Add fixed_points
        fixed_dots = VGroup(
            Dot(plane.c2p(0.8, -0.5), color=GREY_A),
            Dot(plane.c2p(-0.9, -0.6), color=GREY_A),
        )
        arrow_loops = VGroup(*(
            self.get_arrow_loop(dot)
            for dot in fixed_dots
        ))

        for dot, loop in zip(fixed_dots, arrow_loops):
            loop.set_color(GREY_B)
            self.play(
                FadeIn(dot, scale=0.3),
                ShowCreation(loop),
            )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, VGroup(
                eq_arrows, *julia_f2_eqs,
                *fixed_dots, *arrow_loops,
            ))
        )

        # N cycles
        fn_eq = OldTex(
            "f(f(\\cdots f(z) \\cdots)) = z",
            **kw
        )
        fn_eq.move_to(f2_equation, LEFT)
        fn_eq.shift(SMALL_BUFF * DOWN)
        brace = Brace(
            fn_eq[:fn_eq.index_of_part_by_tex("z")],
            DOWN
        )
        brace_tex = brace.get_tex("n \\text{ times}", buff=SMALL_BUFF)
        brace_tex.scale(0.7, about_edge=UP)

        for z in [-0.2 + 0.6j, 1.1 - 0.6j, 0.4 + 0.2j]:
            dot = z0_dot.copy()
            dot.set_fill(BLUE_D)
            dot.move_to(plane.n2p(z))
            z_dots.add(dot)

        n_arrows = VGroup()
        for d1, d2 in adjacent_pairs(z_dots):
            arrow = Arrow(d1, d2, buff=0.1, path_arc=PI / 8)
            arrow.set_stroke(WHITE, opacity=0.7)
            n_arrows.add(arrow)

        dot_anims = []
        n = len(z_dots)
        for k in range(1, n + 1):
            dot_anims.append(
                ApplyMethod(z_dot.move_to, z_dots[k % n], path_arc=PI / 8)
            )

        self.play(
            TransformMatchingShapes(f2_equation, fn_eq),
            FadeOut(z2c),
            ReplacementTransform(arrows, n_arrows),
            *map(GrowFromCenter, z_dots[2:])
        )
        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_tex, SMALL_BUFF * DOWN),
            Succession(*dot_anims, run_time=3),
        )
        self.wait()

        # Ask about how many solutions
        morty = Mortimer(height=2)
        morty.to_corner(DR)
        z2c.next_to(fn_eq, UP, buff=MED_LARGE_BUFF)

        self.play(
            PiCreatureSays(
                morty, "How many solutions?",
                bubble_config={"height": 2, "width": 4}
            ),
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            FadeIn(z2c),
            RemovePiCreatureBubble(
                morty,
                target_mode="pondering",
                look_at=z2c,
            )
        )
        self.wait()

        # 1,000,000-cycles
        million = Integer(1e6, font_size=36)
        million.next_to(brace, DOWN)
        million.set_value(0)
        mega_poly = OldTex(
            "z^{2^{1{,}000{,}000}} +",
            "\\cdots \\text{(nightmare)} \\cdots",
            "= 0",
            **kw
        )
        mega_poly.next_to(million, DOWN, buff=0.75)
        mega_poly.align_to(fn_eq, LEFT)

        expr = self.show_composition(million, morty, **kw)
        self.play(
            ChangeDecimalToValue(million, 1e6, run_time=2),
            VFadeIn(million),
            FadeOut(brace_tex),
            morty.change("raise_right_hand", fn_eq)
        )
        self.play(Blink(morty))
        self.play(
            FadeOut(expr),
            Write(mega_poly),
            morty.animate.set_height(1.8, about_edge=DR).change("horrified", mega_poly),
        )
        self.play(morty.animate.look_at(mega_poly.get_right()))
        self.wait()

        # Show "million" dots
        N = 5000
        points = np.random.random((N, 3))
        points[:, 2] = 0
        dots = DotCloud(points, radius=0)
        dots.replace(plane)
        dots.set_radius(0.01)
        dots.set_color(GREY_B)
        dots.set_opacity(1)
        dots.add_updater(lambda m: m)

        self.play(
            FadeOut(z_labels),
            FadeOut(z_dots),
            FadeOut(n_arrows),
            morty.change("erm", dots),
            ShowCreation(dots, run_time=5),
        )
        self.wait()
        self.play(
            FadeOut(dots),
            FadeOut(mega_poly),
            FadeOut(morty),
            FadeOut(z2c),
        )

        # Rational map
        rational = OldTex("f(z) = {A(z) \\over B(z)}", **kw)
        rational.next_to(million, DOWN, LARGE_BUFF)
        rational.align_to(fn_eq, LEFT)

        self.play(FadeIn(rational))
        for arrow, dot in zip(n_arrows, [*z_dots[1:], z_dots[0]]):
            self.play(
                ShowCreation(arrow),
                z_dot.animate.move_to(dot),
                path_arc=PI / 6,
            )
            self.add(dot, z_dot)

        # Ask about attracting cycle
        new_question = Text("When is a cycle attracting?")
        new_question.get_part_by_text("attracting").set_color(YELLOW)
        new_question.next_to(question, RIGHT, LARGE_BUFF)

        self.play(
            Write(new_question, run_time=1),
            fn_eq.animate.shift(0.5 * DOWN),
            FadeOut(brace),
            FadeOut(million),
        )

        circle = Circle(radius=0.5)
        circle.set_stroke(YELLOW, 1, 1)
        circle.set_fill(YELLOW, 0.25)
        h_tracker = ValueTracker(1.0)
        circle.add_updater(lambda m: m.set_height(h_tracker.get_value()))
        circle.add_updater(lambda m: m.move_to(z_dot))

        multipliers = [0.9, 0.9, 1.2, 0.5, 1.1]

        self.add(circle, z_dot)
        self.play(GrowFromCenter(circle))

        for n in range(3):
            for mult, dot in zip(multipliers, [*z_dots[1:], z_dots[0]]):
                self.play(
                    ApplyMethod(z_dot.move_to, dot, path_arc=PI / 6),
                    h_tracker.animate.set_value(h_tracker.get_value() * mult),
                )

        # Possibly add on a bit for Fatou's theorem?
        theorem = OldTexText(
            "Theorem (Fatou 1919): If $f(z)$ has an\\\\",
            "attracting cycle, then at least one solution\\\\",
            "to $f'(z) = 0$ will fall into it.",
            font_size=36,
        )
        theorem.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        theorem.next_to(fn_eq, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        self.play(
            rational.animate.set_height(0.8).next_to(fn_eq, RIGHT, LARGE_BUFF),
            FadeIn(theorem),
        )

    def show_composition(self, ref_mob, morty, **kwargs):
        tex = "z^2 + c"
        polys = VGroup(OldTex(tex, **kwargs))
        for n in range(20):
            new_tex_parts = ["\\left(", tex, "\\right)^2 + c"]
            polys.add(OldTex(*new_tex_parts))
            if n < 3:
                tex = "".join(new_tex_parts)

        for poly in polys:
            poly.set_max_width(5)
            poly.next_to(ref_mob, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        degree = VGroup(Text("Degree: "), Integer(2))
        degree.arrange(RIGHT)
        degree.next_to(polys, DOWN, aligned_edge=LEFT)

        curr_poly = polys[0]
        self.play(
            FadeIn(curr_poly),
            FadeIn(degree),
            morty.change("tease", curr_poly),
        )
        for n, poly in enumerate(polys[1:]):
            anims = []
            if n == 4:
                anims.append(morty.change("erm"))
            self.play(
                curr_poly.animate.replace(poly[1]),
                FadeIn(poly[::2]),
                UpdateFromAlphaFunc(
                    degree, lambda m, a: m[1].set_value(
                        (2**(n + 1) if a < 0.5 else 2**(n + 2))
                    )
                ),
                *anims,
                run_time=(1 if n < 5 else 0.25)
            )
            poly.replace_submobject(1, curr_poly)
            self.add(poly)
            curr_poly = poly
        self.wait()
        self.play(FadeOut(degree))
        return poly
