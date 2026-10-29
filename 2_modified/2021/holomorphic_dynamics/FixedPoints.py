# ==============================================================================
# Scene:      FixedPoints
# Source:     videos/_2021/holomorphic_dynamics.py (lines 1116-1543)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl FixedPoints.py FixedPoints -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingShapes has no `fade_transform_mismatches`; the argument is removed
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex no longer accepts OldTex: it has no get_symbol_substrings)
#   - Grant's NewtonFractal, MandelbrotFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
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


# CHANGE: manimgl's NewtonFractal, MandelbrotFractal are used (manimlib/mobject/fractals.py, WGSL shaders). Grant's
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
