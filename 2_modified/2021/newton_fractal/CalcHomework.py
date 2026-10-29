# ==============================================================================
# Scene:      CalcHomework
# Source:     videos/_2021/newton_fractal.py (lines 2260-2360)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl CalcHomework.py CalcHomework -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Text(alignment="\\flushleft") -> alignment="LEFT" (Pango does not know the LaTeX option)
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex no longer accepts OldTex: it has no get_symbol_substrings)
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

def glow_dot(point, r_min=0.05, r_max=0.15, color=YELLOW, n=20, opacity_mult=1.0):
    result = VGroup(*(
        Dot(point, radius=interpolate(r_min, r_max, a))
        for a in np.linspace(0, 1, n)
    ))
    result.set_fill(color, opacity=opacity_mult / n)
    return result


class RealNewtonsMethod(Scene):
    coefs = [-0.2, -1, 1, 0, 0, 1]
    poly_tex = "x^5 + x^2 - x - 0.2"
    dpoly_tex = "5x^4 + 2x - 1"
    seed = 1.3
    graph_x_range = (-1.5, 1.5)
    axes_config = {
        "x_range": (-2, 2, 0.2),
        "y_range": (-2, 6, 0.2),
        "height": 8,
        "width": 8,
        "axis_config": {
            "tick_size": 0.05,
            "longer_tick_multiple": 2.0,
            "tick_offset": 0,
            # Change name
            "big_tick_numbers": list(range(-2, 3)),
            "include_tip": False,
        }
    }
    graph_color = BLUE_C
    guess_color = YELLOW
    rule_font_size = 42
    n_search_steps = 5

    def construct(self):
        self.add_graph()
        self.add_title(self.axes)
        self.draw_graph()
        self.highlight_roots()
        self.preview_iterative_root_finding()
        self.introduce_step()
        self.find_root()

    def add_graph(self):
        axes = self.axes = Axes(**self.axes_config)
        axes.to_edge(RIGHT)
        axes.add_coordinate_labels(
            np.arange(*self.axes.x_range[:2]),
            np.arange(self.axes.y_range[0] + 1, self.axes.y_range[1]),
        )
        self.add(axes)

        graph = self.graph = axes.get_graph(
            lambda x: poly(x, self.coefs),
            x_range=self.graph_x_range,
        )
        graph.set_color(self.graph_color)

        self.add(graph)

    def add_title(self, axes, opacity=0):
        title = OldTexText("Newton's method", font_size=60)
        title.move_to(midpoint(axes.get_left(), LEFT_SIDE))
        title.to_edge(UP)
        title.set_opacity(opacity)

        poly = OldTex(f"P({self.poly_tex[0]}) = ", self.poly_tex, "= 0 ")
        poly.match_width(title)
        poly.next_to(title, DOWN, buff=MED_LARGE_BUFF)
        poly.set_fill(GREY_A)
        title.add(poly)

        self.title = title
        self.poly = poly
        self.add(title)

    def draw_graph(self):
        rect = SurroundingRectangle(self.poly[:-1])
        rect.set_stroke(self.graph_color, 2)

        self.play(
            FlashAround(self.poly[:-1], color=self.graph_color, run_time=2),
            ShowCreation(rect, run_time=2),
            ShowCreation(self.graph, run_time=4),
        )
        self.wait()
        self.play(
            rect.animate.replace(self.poly[-1], stretch=True).scale(1.2)
        )
        self.wait()
        self.play(FadeOut(rect))

    def highlight_roots(self):
        roots = coefficients_to_roots(self.coefs)
        real_roots = [
            root.real for root in roots
            if abs(root.imag) < 1e-6
        ]
        real_roots.sort()

        dots = VGroup(*(
            # Dot(self.axes.c2p(r, 0), radius=0.05)
            glow_dot(self.axes.c2p(r, 0))
            for r in real_roots
        ))
        squares = VGroup(*[
            Square().set_height(0.25).move_to(dot)
            for dot in dots
        ])
        squares.set_stroke(YELLOW, 3)
        squares.set_fill(opacity=0)

        self.play(
            LaggedStart(
                *[
                    FadeIn(dot, scale=0.1)
                    for dot in dots
                ] + [
                    VShowPassingFlash(square, time_width=2.0, run_time=2)
                    for square in squares
                ],
                lag_ratio=0.15
            ),
        )
        self.wait()

        # Show values numerically
        root_strs = ["{0:.4}".format(root) for root in real_roots]
        equations = VGroup(*(
            OldTex(
                "P(", root_str, ")", "=", "0",
                font_size=self.rule_font_size
            ).set_color_by_tex(root_str, YELLOW)
            for root_str in root_strs
        ))
        equations.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        equations.next_to(self.poly, DOWN, LARGE_BUFF, aligned_edge=LEFT)
        question = Text("How do you\ncompute these?")
        question.next_to(equations, RIGHT, buff=LARGE_BUFF)
        question.set_color(YELLOW)

        arrows = VGroup(*(
            Arrow(
                question.get_corner(UL) + 0.2 * DL,
                eq[1].get_corner(UR) + 0.25 * LEFT,
                path_arc=arc, stroke_width=3,
                buff=0.2,
            )
            for eq, arc in zip(equations, [0.7 * PI, 0.5 * PI, 0.0 * PI])
        ))
        arrows.set_color(YELLOW)

        self.play(
            LaggedStartMap(FadeIn, equations, lag_ratio=0.25),
            LaggedStart(*(
                FadeTransform(dot.copy(), eq[1])
                for dot, eq in zip(dots, equations)
            ), lag_ratio=0.25)
        )
        self.wait()
        self.play(
            Write(question),
            Write(arrows)
        )
        self.wait()

        self.play(LaggedStart(
            FadeOut(dots),
            FadeOut(question),
            FadeOut(arrows),
            FadeOut(equations),
            lag_ratio=0.25
        ))
        self.wait()

    def preview_iterative_root_finding(self):
        axes = self.axes
        axis = axes.x_axis
        coefs = self.coefs
        n_steps = 5

        root_seekers = VGroup(*(
            ArrowTip().set_height(0.2).rotate(-PI / 2).move_to(axis.n2p(x), DOWN)
            for x in np.arange(-2, 2.0, 0.2)[:-1]
        ))
        root_seekers.set_stroke(YELLOW, 2, opacity=0.5)
        root_seekers.set_fill(YELLOW, opacity=0.3)

        # CHANGE: Text(alignment=) takes LEFT/CENTER/RIGHT, not "\\flushleft"
        words = Text("Approximate\nSolutions", alignment="LEFT")
        words.move_to(axes.c2p(0, 3))
        words.align_to(axis, LEFT)
        words.set_color(YELLOW)

        self.play(
            FadeIn(root_seekers, lag_ratio=0.1),
            Write(words),
        )

        for n in range(n_steps):
            for rs in root_seekers:
                rs.generate_target()
                x = axis.p2n(rs.get_center())
                if n == 0 and abs(x - 0.4) < 0.1:
                    x = 0.6
                new_x = x - poly(x, coefs) / dpoly(x, coefs)
                rs.target.set_x(axis.n2p(new_x)[0])
            self.play(*map(MoveToTarget, root_seekers), run_time=1.0)
        self.wait()

        values = VGroup(*(
            DecimalNumber(
                axis.p2n(rs.get_center()),
                num_decimal_places=5,
                show_ellipsis=True,
            ).next_to(rs, UP, SMALL_BUFF)
            for rs in root_seekers[0::len(root_seekers) // 2]
        ))
        values.set_fill(YELLOW)
        values.set_stroke(BLACK, 8, background=True)
        last_value = VMobject()
        for value in values:
            self.play(
                FadeIn(value),
                FadeOut(last_value)
            )
            self.wait(0.5)
            last_value = value
        self.play(FadeOut(last_value))
        self.play(
            FadeOut(words),
            FadeOut(root_seekers),
        )

    def introduce_step(self):
        axes = self.axes
        graph = self.graph

        # Add labels
        guess_label = OldTex(
            "\\text{Guess: } x_0 = " + f"{self.seed}",
            tex_to_color_map={"x_0": YELLOW}
        )
        guess_label.next_to(self.poly, DOWN, LARGE_BUFF)
        guess_marker, guess_value, guess_tracker = self.get_guess_group()
        get_guess = guess_tracker.get_value

        self.play(self.title.animate.set_opacity(1))
        self.wait()
        self.play(Write(guess_label))
        self.play(
            FadeTransform(
                guess_label[1].copy(),
                VGroup(guess_marker, guess_value)
            )
        )
        self.wait()

        # Add lines
        v_line = axes.get_v_line(axes.i2gp(get_guess(), graph))
        tan_line = self.get_tan_line(get_guess())

        v_line_label = OldTex("P(x_0)", font_size=30, fill_color=GREY_A)
        v_line_label.next_to(v_line, RIGHT, SMALL_BUFF)

        self.add(v_line, guess_marker, guess_value)
        self.play(ShowCreation(v_line))
        self.play(FadeIn(v_line_label, 0.2 * RIGHT))
        self.wait()
        self.play(
            ShowCreation(tan_line),
            graph.animate.set_stroke(width=2),
        )

        # Mention next guess
        next_guess_label = Text("Next guess", font_size=30)
        next_guess_label.set_color(RED)
        next_guess_label.next_to(axes.c2p(0, 0), RIGHT, MED_LARGE_BUFF)
        next_guess_label.shift(UP)
        next_guess_arrow = Arrow(next_guess_label, tan_line.get_start(), buff=0.1)
        next_guess_arrow.set_stroke(RED, 3)

        coord = axes.coordinate_labels[0][-1]
        coord_copy = coord.copy()
        coord.set_opacity(0)
        self.play(
            coord_copy.animate.scale(0),
            ShowCreation(next_guess_arrow),
            FadeIn(next_guess_label),
        )
        self.wait()

        # Show derivative
        dpoly = OldTex("P'(x) = ", self.dpoly_tex)
        dpoly.match_height(self.poly)
        dpoly.match_style(self.poly)
        dpoly.next_to(self.poly, DOWN, aligned_edge=LEFT)

        self.play(
            FadeIn(dpoly, 0.5 * DOWN),
            guess_label.animate.shift(0.25 * DOWN)
        )
        self.play(FlashAround(dpoly))
        self.wait()

        # Show step
        step_arrow = Arrow(v_line.get_start(), tan_line.get_start(), buff=0)
        step_arrow.set_stroke(GREY_A, 3)
        step_arrow.shift(0.1 * UP)
        step_word = Text("Step", font_size=24)
        step_word.set_stroke(BLACK, 3, background=True)
        step_word.next_to(step_arrow, UP, SMALL_BUFF)

        self.play(
            ShowCreation(step_arrow),
            FadeIn(step_word)
        )
        self.wait()

        # Show slope
        slope_eq_texs = [
            "P'(x_0) = {P(x_0) \\over -\\text{Step}}",
            "\\text{Step} = -{P(x_0) \\over P'(x_0)}",
        ]
        slope_eqs = [
            OldTex(
                tex,
                isolate=[
                    "P'(x_0)",
                    "P(x_0)",
                    "\\text{Step}",
                    "-"
                ],
                font_size=self.rule_font_size,
            )
            for tex in slope_eq_texs
        ]
        for slope_eq in slope_eqs:
            slope_eq.set_fill(GREY_A)
            slope_eq.set_color_by_tex("Step", WHITE)
            slope_eq.next_to(guess_label, DOWN, LARGE_BUFF)

        rule = self.rule = self.get_update_rule()
        rule.next_to(guess_label, DOWN, LARGE_BUFF)

        for line in [v_line, Line(tan_line.get_start(), v_line.get_start())]:
            self.play(
                VShowPassingFlash(
                    Line(line.get_start(), line.get_end()).set_stroke(YELLOW, 10).insert_n_curves(20),
                    time_width=1.0,
                    run_time=1.5
                )
            )
        self.wait()
        self.play(
            FadeTransform(v_line_label.copy(), slope_eqs[0].get_part_by_tex("P(x_0)")),
            FadeTransform(step_word.copy(), slope_eqs[0].get_part_by_tex("\\text{Step}")),
            FadeIn(slope_eqs[0][3:5]),
        )
        self.wait()
        self.play(FadeIn(slope_eqs[0][:2]))
        self.wait()
        # CHANGE: TransformMatchingTex only works with the new Tex (get_symbol_substrings); with OldTex the shapes are matched
        self.play(TransformMatchingShapes(*slope_eqs, path_arc=PI / 2))
        self.wait()
        self.play(
            FadeIn(rule),
            slope_eqs[1].animate.to_edge(DOWN)
        )
        self.wait()

        # Transition to x1
        self.add(tan_line, guess_value)
        self.play(
            FadeOut(next_guess_label),
            FadeOut(next_guess_arrow),
            FadeOut(step_word),
            FadeOut(step_arrow),
            FadeOut(v_line),
            FadeOut(v_line_label),
            guess_tracker.animate.set_value(self.get_next_guess(get_guess())),
        )
        self.play(FadeOut(tan_line))

    def find_root(self, cycle_run_time=1.0):
        for n in range(self.n_search_steps):
            self.play(*self.cycle_rule_entries_anims(), run_time=cycle_run_time)
            self.step_towards_root()

    def step_towards_root(self, fade_tan_with_vline=False, added_anims=None):
        guess = self.guess_tracker.get_value()
        next_guess = self.get_next_guess(guess)

        v_line = self.axes.get_v_line(self.axes.i2gp(guess, self.graph))
        tan_line = self.get_tan_line(guess)

        self.add(v_line, tan_line, self.guess_marker, self.guess_value)
        self.play(
            ShowCreation(v_line),
            GrowFromCenter(tan_line)
        )
        anims = [
            FadeOut(v_line),
            self.guess_tracker.animate.set_value(next_guess)
        ]
        if added_anims is not None:
            anims += added_anims
        tan_fade = FadeOut(tan_line)
        if fade_tan_with_vline:
            self.play(*anims, tan_fade)
        else:
            self.play(*anims)
            self.play(tan_fade)

    #
    def get_guess_group(self):
        axes = self.axes
        guess_tracker = ValueTracker(self.seed)
        get_guess = guess_tracker.get_value

        guess_marker = Triangle(start_angle=PI / 2)
        guess_marker.set_height(0.1)
        guess_marker.set_width(0.1, stretch=True)
        guess_marker.set_fill(self.guess_color, 1)
        guess_marker.set_stroke(width=0)
        guess_marker.add_updater(lambda m: m.move_to(
            axes.c2p(get_guess(), 0), UP
        ))
        guess_value = DecimalNumber(0, num_decimal_places=3, font_size=24)

        def update_guess_value(gv):
            gv.set_value(get_guess())
            gv.next_to(guess_marker, DOWN, SMALL_BUFF)
            gv.set_fill(self.guess_color)
            gv.set_stroke(BLACK, 3, background=True)
            return gv

        guess_value.add_updater(update_guess_value)

        self.guess_tracker = guess_tracker
        self.guess_marker = guess_marker
        self.guess_value = guess_value

        return (guess_marker, guess_value, guess_tracker)

    def get_next_guess(self, curr_guess):
        x = curr_guess
        return x - poly(x, self.coefs) / dpoly(x, self.coefs)

    def get_tan_line(self, curr_guess):
        next_guess = self.get_next_guess(curr_guess)
        start = self.axes.c2p(next_guess, 0)
        end = self.axes.i2gp(curr_guess, self.graph)
        line = Line(start, start + 2 * (end - start))
        line.set_stroke(RED, 3)
        return line

    def get_update_rule(self, char="x"):
        rule = OldTex(
            """
                z_1 =
                z_0 - {P(z_0) \\over P'(z_0)}
            """.replace("z", char),
            tex_to_color_map={
                f"{char}_1": self.guess_color,
                f"{char}_0": self.guess_color
            },
            font_size=self.rule_font_size,
        )

        rule.n = 0
        rule.zns = rule.get_parts_by_tex(f"{char}_0")
        rule.znp1 = rule.get_parts_by_tex(f"{char}_1")
        return rule

    def cycle_rule_entries_anims(self):
        rule = self.rule
        rule.n += 1
        char = rule.get_tex().strip()[0]
        zns = VGroup()
        for old_zn in rule.zns:
            zn = OldTex(f"{char}_{{{rule.n}}}", font_size=self.rule_font_size)
            zn[0][1:].set_max_width(0.2, about_edge=DL)
            zn.move_to(old_zn)
            zn.match_color(old_zn)
            zns.add(zn)
        znp1 = OldTex(f"{char}_{{{rule.n + 1}}}", font_size=self.rule_font_size)
        znp1.move_to(rule.znp1)
        znp1.match_color(rule.znp1[0])

        result = (
            FadeOut(rule.zns),
            FadeTransformPieces(rule.znp1, zns),
            FadeIn(znp1, 0.5 * RIGHT)
        )
        rule.zns = zns
        rule.znp1 = znp1
        return result


class GutCheckFormula(RealNewtonsMethod):
    seed = 5.0

    def construct(self):
        self.add_axes_and_graph()
        self.add_rule()
        self.add_guess()
        self.sample_values()

    def add_axes_and_graph(self):
        axes = NumberPlane(
            (-2, 15), (-2, 8),
            faded_line_ratio=1,
            background_line_style={
                "stroke_opacity": 0.5,
                "stroke_color": GREY,
            }
        )
        axes.to_corner(DL, buff=0)
        axes.add_coordinate_labels(font_size=16, fill_opacity=0.5)
        axes.x_axis.numbers.next_to(axes.x_axis, UP, buff=0.05)
        self.add(axes)

        roots = [-1, 3, 4.5]
        coefs = 0.1 * np.array(roots_to_coefficients(roots))
        graph = axes.get_graph(lambda x: poly(x, coefs))
        graph.set_stroke(BLUE, 3)
        self.add(graph)

        self.root_point = axes.c2p(roots[-1], 0)

        self.axes = axes
        self.graph = graph

    def add_rule(self):
        rule = OldTex(
            "x_{n + 1}", "=",
            "x_{n}", " - ", "{P(x) ", "\\over ", "P'(x)}"
        )
        rule.set_stroke(BLACK, 5, background=True)
        rule.to_corner(UR)

        step_box = SurroundingRectangle(rule[3:], buff=0.1)
        step_box.set_stroke(YELLOW, 1.0)
        step_word = Text("Step size", font_size=36)
        step_word.set_color(YELLOW)
        step_word.next_to(step_box, DOWN)

        self.add(rule)
        self.add(step_box)
        self.add(step_word)

        self.rule = rule
        self.step_box = step_box
        self.step_word = step_word

    def add_guess(self, include_px=True):
        guess_group = self.get_guess_group()
        marker, value, tracker = guess_group
        self.guess_tracker = tracker

        def update_v_line(v_line):
            x = tracker.get_value()
            graph_point = self.graph.pfp(
                inverse_interpolate(*self.graph.x_range[:2], x)
            )
            v_line.put_start_and_end_on(
                self.axes.c2p(x, 0),
                graph_point,
            )

        v_line = Line()
        v_line.set_stroke(WHITE, 2)
        v_line.add_updater(update_v_line)

        self.add(*guess_group)
        self.add(v_line)

        if include_px:
            px_label = OldTex("P(x)", font_size=36)
            px_label.add_updater(lambda m: m.next_to(v_line, RIGHT, buff=0.05))
            self.add(px_label)

    def sample_values(self):
        box = self.step_box
        rule = self.rule
        tracker = self.guess_tracker
        graph = self.graph

        words = Text("Gut check!")
        words.next_to(self.step_word, DOWN, LARGE_BUFF)
        words.shift(2 * LEFT)
        arrow = Arrow(words, self.rule)

        self.play(
            Write(words, run_time=1),
            ShowCreation(arrow),
        )
        self.wait()
        self.play(
            FadeOut(words),
            FadeOut(arrow),
            FadeOut(self.step_word),
            box.animate.replace(rule[4], stretch=True).scale(1.2).set_stroke(width=2.0),
        )
        self.play(
            tracker.animate.set_value(6.666),
            run_time=3,
        )

        arrow = Arrow(
            self.axes.c2p(tracker.get_value(), 0),
            self.root_point,
            buff=0,
            stroke_color=RED,
        )
        self.play(ShowCreation(arrow))
        self.wait()

        # Large p_prime
        self.play(
            FadeOut(arrow),
            tracker.animate.set_value(5.0),
        )
        self.play(
            graph.animate.stretch(8, 1, about_point=self.axes.c2p(0, 0)),
            box.animate.replace(self.rule[-1]).scale(1.2),
            run_time=3
        )
        self.wait()

        tan_line = self.get_tan_line(graph, tracker.get_value(), 15)
        self.play(ShowCreation(tan_line))
        self.wait()

    def get_tan_line(self, graph, x, length=5, epsilon=1e-3):
        alpha = inverse_interpolate(*graph.x_range[:2], x)
        tan_line = Line(
            graph.pfp(alpha - epsilon),
            graph.pfp(alpha + epsilon),
        )
        tan_line.set_length(length)
        tan_line.set_stroke(RED, 5)
        return tan_line


class CalcHomework(GutCheckFormula):
    seed = 3.0

    def construct(self):
        # Title
        old_title = Text("Newton-Raphson method", font_size=60)
        old_title.to_edge(UP)
        title = Text("Calc 1", font_size=72)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        line = Underline(title)
        line.scale(2)
        line.set_stroke(WHITE, 2)
        self.add(old_title)

        # Axes
        axes = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-8, 10, 2),
            height=6.5,
            width=FRAME_WIDTH,
            faded_line_ratio=4,
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 1,
            }
        )
        axes.to_edge(DOWN, buff=0)
        axes.add_coordinate_labels(font_size=18)

        self.add(axes)

        # Homework
        hw = OldTexText(
            "Homework:\\\\",
            "\\quad Approximate $\\sqrt{7}$ by hand using\\\\",
            "\\quad the ", "Newton-Raphson method.",
            alignment="",
            font_size=36,
            color=GREY_A,
        )
        hw[1:].shift(MED_SMALL_BUFF * RIGHT + SMALL_BUFF * DOWN)
        hw.add_to_back(
            BackgroundRectangle(hw, fill_opacity=0.8, buff=0.25)
        )
        hw.move_to(axes, UL)
        hw.to_edge(LEFT, buff=0)

        self.wait()
        self.play(
            FadeIn(hw, lag_ratio=0.1, run_time=2),
            FadeTransform(
                old_title,
                hw[-1]
            ),
            FadeIn(title),
            ShowCreation(line),
        )
        self.wait()

        # Graph
        graph = axes.get_graph(
            lambda x: x**2 - 7,
            x_range=(-math.sqrt(17), math.sqrt(17))
        )
        graph.set_stroke(BLUE, 2)
        graph_label = OldTex("x^2 - 7", font_size=36)
        graph_label.set_color(BLUE)
        graph_label.next_to(graph.pfp(0.99), LEFT)

        self.add(graph, hw)
        self.play(ShowCreation(graph, run_time=3))
        self.play(FadeIn(graph_label))
        self.wait()

        # Marker
        axes.x_axis.numbers.remove(axes.x_axis.numbers[-3])
        self.axes = axes
        self.graph = graph
        self.add_guess(include_px=False)
        self.wait()

        # Update
        tan_line = self.get_tan_line(graph, 3)
        tan_line.set_stroke(width=3)
        update_tex = OldTex(
            "3 \\rightarrow 3 - {3^2 - 7 \\over 2 \\cdot 3}",
            tex_to_color_map={"3": YELLOW},
            font_size=28
        )
        update_tex.next_to(axes.c2p(1.2, 0), UR, buff=SMALL_BUFF)

        self.add(tan_line, self.guess_marker, self.guess_value)
        self.play(
            GrowFromCenter(tan_line),
            FadeIn(update_tex),
        )
        self.wait()
        self.play(
            self.guess_tracker.animate.set_value(8 / 3),
            run_time=2
        )
