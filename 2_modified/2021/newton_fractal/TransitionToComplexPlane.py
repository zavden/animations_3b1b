# ==============================================================================
# Scene:      TransitionToComplexPlane
# Source:     videos/_2021/newton_fractal.py (lines 2414-2621)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl TransitionToComplexPlane.py TransitionToComplexPlane -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Text(alignment="\\flushleft") -> alignment="LEFT" (Pango does not know the LaTeX option)
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex no longer accepts OldTex: it has no get_symbol_substrings)
#   - self.play(..., path_arc=...) -> animate(path_arc=...) in each animation (Scene.play no longer accepts path_arc)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2022/quintic/roots_and_coefs.py -----

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


class FasterNewtonExample(RealNewtonsMethod):
    coefs = [0.1440, -1.0, 1.2, 1]
    poly_tex = "x^3 + 1.2x^2 - x + 0.144"
    dpoly_tex = "3x^2 + 2.4x - 1"
    n_search_steps = 6
    graph_x_range = (-2, 2)
    seed = 1.18
    axes_config = {
        "x_range": (-2, 2, 0.2),
        "y_range": (-1, 3, 0.2),
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

    def construct(self):
        self.add_graph()
        self.add_title(self.axes)
        self.draw_graph()
        self.introduce_step()
        self.find_root()

    def find_root(self, cycle_run_time=1.0):
        for n in range(self.n_search_steps):
            self.step_towards_root(
                added_anims=self.cycle_rule_entries_anims(),
                fade_tan_with_vline=True
            )


class RealNewtonsMethodHigherGraph(FasterNewtonExample):
    coefs = [1, -1, 1, 0, 0, 0.99]
    poly_tex = "x^5 + x^2 - x + 1"
    n_search_steps = 20


class TransitionToComplexPlane(RealNewtonsMethodHigherGraph):
    poly_tex = "z^5 + z^2 - z + 1"

    def construct(self):
        self.add_graph()
        self.add_title(self.axes)
        self.poly.save_state()
        self.poly.to_corner(UL)
        self.center_graph()
        self.show_example_point()
        self.separate_input_and_output()
        self.move_input_around_plane()

    def center_graph(self):
        shift_vect = DOWN - self.axes.c2p(0, 0)

        self.play(
            self.axes.animate.shift(shift_vect),
            self.graph.animate.shift(shift_vect),
        )
        self.wait()

    def show_example_point(self):
        axes = self.axes

        input_tracker = ValueTracker(1)
        get_x = input_tracker.get_value

        def get_px():
            return poly(get_x(), self.coefs)

        def get_graph_point():
            return axes.c2p(get_x(), get_px())

        marker = ArrowTip().set_height(0.1)
        input_marker = marker.copy().rotate(PI / 2)
        input_marker.set_color(YELLOW)
        output_marker = marker.copy()
        output_marker.set_color(MAROON_B)
        input_marker.add_updater(lambda m: m.move_to(axes.x_axis.n2p(get_x()), UP))
        output_marker.add_updater(lambda m: m.shift(axes.y_axis.n2p(get_px()) - m.get_start()))

        v_line = always_redraw(
            lambda: axes.get_v_line(get_graph_point(), line_func=Line).set_stroke(YELLOW, 1)
        )
        h_line = always_redraw(
            lambda: axes.get_h_line(get_graph_point(), line_func=Line).set_stroke(MAROON_B, 1)
        )

        self.add(
            input_tracker,
            input_marker,
            output_marker,
            v_line,
            h_line,
        )

        self.play(input_tracker.animate.set_value(-0.5), run_time=3)
        self.play(input_tracker.animate.set_value(1.0), run_time=3)
        self.play(ShowCreationThenFadeOut(
            axes.get_tangent_line(get_x(), self.graph).set_stroke(RED, 3)
        ))

        self.input_tracker = input_tracker
        self.input_marker = input_marker
        self.output_marker = output_marker
        self.v_line = v_line
        self.h_line = h_line

    def separate_input_and_output(self):
        axes = self.axes
        x_axis, y_axis = axes.x_axis, axes.y_axis
        graph = self.graph
        input_marker = self.input_marker
        output_marker = self.output_marker
        v_line = self.v_line
        h_line = self.h_line

        in_plane = ComplexPlane(
            (-2, 2),
            (-2, 2),
            height=5,
            width=5,
        )
        in_plane.add_coordinate_labels(font_size=18)
        in_plane.to_corner(DL)
        out_plane = in_plane.deepcopy()
        out_plane.to_corner(DR)

        input_word = Text("Input")
        output_word = Text("Output")

        input_word.next_to(in_plane.x_axis, UP)
        output_word.rotate(PI / 2)
        output_word.next_to(out_plane.y_axis, RIGHT, buff=0.5)

        cl_copy = axes.coordinate_labels.copy()
        axes.coordinate_labels.set_opacity(0)
        self.play(
            *map(FadeOut, (v_line, h_line, graph, cl_copy)),
        )

        for axis1, axis2 in [(x_axis, in_plane.x_axis), (y_axis, out_plane.y_axis)]:
            axis1.generate_target()
            axis1.target.scale(axis2.get_unit_size() / axis1.get_unit_size())
            axis1.target.shift(axis2.n2p(0) - axis1.target.n2p(0))
        self.play(
            MoveToTarget(x_axis),
            MoveToTarget(y_axis),
            FadeIn(input_word),
            FadeIn(output_word),
        )
        self.wait()
        self.add(in_plane, input_marker)
        self.play(
            input_word.animate.next_to(in_plane, UP),
            x_axis.animate.set_stroke(width=0),
            Write(in_plane, lag_ratio=0.03),
        )
        self.play(
            Rotate(
                VGroup(y_axis, output_word, output_marker),
                -PI / 2,
                about_point=out_plane.n2p(0)
            )
        )
        self.add(out_plane, output_marker)
        self.play(
            output_word.animate.next_to(out_plane, UP),
            y_axis.animate.set_stroke(width=0),
            Write(out_plane, lag_ratio=0.03),
        )
        self.wait()

        self.in_plane = in_plane
        self.out_plane = out_plane
        self.input_word = input_word
        self.output_word = output_word

    def move_input_around_plane(self):
        in_plane = self.in_plane
        out_plane = self.out_plane
        input_marker = self.input_marker
        output_marker = self.output_marker

        in_dot, out_dot = [
            Dot(radius=0.05).set_fill(marker.get_fill_color()).move_to(marker.get_start())
            for marker in (input_marker, output_marker)
        ]
        in_dot.set_fill(YELLOW, 1)

        in_tracer = TracingTail(in_dot, stroke_color=in_dot.get_color())
        out_tracer = TracingTail(out_dot, stroke_color=out_dot.get_color())
        self.add(in_tracer, out_tracer)

        out_dot.add_updater(lambda m: m.move_to(out_plane.n2p(
            poly(in_plane.p2n(in_dot.get_center()), self.coefs)
        )))

        z_label = OldTex("z", font_size=24)
        z_label.set_fill(YELLOW)
        z_label.add_background_rectangle()
        z_label.add_updater(lambda m: m.next_to(in_dot, UP, SMALL_BUFF))
        pz_label = OldTex("P(z)", font_size=24)
        pz_label.set_fill(MAROON_B)
        pz_label.add_background_rectangle()
        pz_label.add_updater(lambda m: m.next_to(out_dot, UP, SMALL_BUFF))

        self.play(
            *map(FadeOut, (input_marker, output_marker)),
            *map(FadeIn, (in_dot, out_dot)),
            FadeIn(z_label),
            FlashAround(z_label),
        )
        self.play(
            FadeTransform(z_label.copy(), pz_label)
        )
        z_values = [
            complex(-0.5, 0.5),
            complex(-0.5, -0.5),
            complex(-0.25, 0.25),
            complex(0.5, -0.5),
            complex(0.5, 0.5),
            complex(1, 0.25),
        ]
        for z in z_values:
            # CHANGE: Scene.play no longer accepts path_arc: it is passed to the animation with animate(path_arc=...)
            self.play(
                in_dot.animate(path_arc=PI / 2).move_to(in_plane.n2p(z)),
                run_time=2,
            )
            self.wait()

        self.remove(in_tracer, out_tracer)
        in_plane.generate_target()
        in_dot.generate_target()
        group = VGroup(in_plane.target, in_dot.target)
        group.set_height(8).center().to_edge(RIGHT, buff=0),
        self.play(
            MoveToTarget(in_plane),
            MoveToTarget(in_dot),
            FadeOut(self.input_word),
            FadeOut(self.output_word),
            FadeOut(out_plane),
            FadeOut(out_dot),
            FadeOut(pz_label),
            self.poly.animate.restore().shift(0.32 * RIGHT),
        )
