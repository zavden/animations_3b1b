# ==============================================================================
# Scene:      GraphAndHistoryOfExponential
# Source:     videos/_2021/matrix_exp.py (lines 2825-3106)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GraphAndHistoryOfExponential.py GraphAndHistoryOfExponential -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(..., thickness=X) -> FillArrow(...): the thickness in the 2021 code is in scene units and the current Arrow multiplies it by 0.015 (invisible arrows).
#
# Placeholder assets (not Grant's originals):
#   - Placeholder Introductio_in_Analysin_infinitorum.png, Huygens.png and Goldbach.png in _lib/assets/raster_images/ (make_matrix_exp_assets.py)
# ==============================================================================

from manim_imports_ext import *

def get_1d_equation(r="r"):
    return OldTex(
        "{d \\over d{t}} x({t}) = {" + r + "} \\cdot x({t})",
        tex_to_color_map={
            "{t}": GREY_B,
            "{" + r + "}": BLUE,
            "=": WHITE,
        }
    )


class GraphAndHistoryOfExponential(Scene):
    def construct(self):
        # Setup
        axes = Axes(
            x_range=(0, 23, 1),
            y_range=(0, 320, 10),
            height=160,
            width=13,
            axis_config={"include_tip": False}
        )
        axes.y_axis.add(*(axes.y_axis.get_tick(x, size=0.05) for x in range(20)))
        axes.to_corner(DL)
        r = 0.25
        exp_graph = axes.get_graph(lambda t: np.exp(r * t))
        exp_graph.set_stroke([BLUE_E, BLUE, YELLOW])
        graph_template = exp_graph.copy()
        graph_template.set_stroke(width=0)
        axes.add(graph_template)

        equation = self.get_equation()
        solution = OldTex("x({t}) = e^{r{t} }", tex_to_color_map={"{t}": GREY_B, "r": BLUE})
        solution.next_to(equation, DOWN, MED_LARGE_BUFF)

        self.add(axes)
        self.add(axes.get_x_axis_label("t"))
        self.add(axes.get_y_axis_label("x"))
        self.add(equation)

        curr_time = self.time
        exp_graph.add_updater(lambda m: m.pointwise_become_partial(
            graph_template, 0, (self.time - curr_time) / 20,
        ))
        dot = Dot(color=BLUE_B, radius=0.04)
        dot.add_updater(lambda d: d.move_to(exp_graph.get_end()))
        # CHANGE: Arrow(thickness=...) -> FillArrow: thickness in scene units (the current Arrow multiplies it by 0.015)
        vect = FillArrow(DOWN, UP, fill_color=YELLOW, thickness=0.025)
        vect.add_updater(lambda v: v.put_start_and_end_on(
            axes.get_origin(),
            axes.y_axis.get_projection(exp_graph.get_end()),
        ))
        h_line = always_redraw(lambda: DashedLine(
            vect.get_end(), dot.get_left(),
            stroke_width=1,
            stroke_color=GREY_B,
        ))
        v_line = always_redraw(lambda: DashedLine(
            axes.x_axis.get_projection(dot.get_bottom()),
            dot.get_bottom(),
            stroke_width=1,
            stroke_color=GREY_B,
        ))

        def stretch_axes(factor):
            axes.generate_target(use_deepcopy=True)
            axes.target.stretch(factor, 1, about_point=axes.get_origin()),
            axes.target.x_axis.stretch(1 / factor, 1, about_point=axes.get_origin()),
            self.play(MoveToTarget(axes))

        self.add(exp_graph, dot, vect, h_line, v_line)
        # equation.scale(2, about_edge=UP)###
        self.wait(2)

        # Highlight equation parts
        index = equation.index_of_part_by_tex("=")
        lhs = equation[:index]
        rhs = equation[index + 1:]

        for part in (rhs, lhs):
            self.play(FlashAround(part, time_width=3, run_time=2))
            self.wait()
        # self.wait(4)

        stretch_axes(0.2)

        self.wait(6)
        stretch_axes(0.23)
        self.wait(4)

        exp_graph.clear_updaters()
        exp_graph.become(graph_template)
        exp_graph.set_stroke(width=3)
        self.add(exp_graph)
        self.play(FadeOut(vect), FadeOut(dot))
        self.wait()

        # Write exponential growth
        words = Text("Exponential growth")
        words.next_to(axes.c2p(0, 0), UR, buff=0)
        original_words = words.deepcopy()
        original_words.set_opacity(0)

        def func(p):
            t, x = axes.p2c(p)
            angle = axes.angle_of_tangent(t, exp_graph)
            vect = rotate_vector(RIGHT, angle + PI / 2)
            graph_point = axes.input_to_graph_point(t, exp_graph)
            y = (axes.y_axis.get_projection(p) - axes.get_origin())[1]
            return graph_point + y * vect

        fill_tracker = ValueTracker(0)
        words.add_updater(lambda m: m.become(original_words).set_fill(opacity=fill_tracker.get_value()).apply_function(func))

        self.add(words)
        self.play(
            ApplyMethod(original_words.next_to, axes.c2p(14, 0), UP, SMALL_BUFF, run_time=2),
            fill_tracker.animate.set_value(1),
        )
        self.remove(original_words, fill_tracker)
        words.clear_updaters()
        self.wait()

        # Introduce 2.71828
        solution_with_number = OldTex(
            "{d \\over dt}",
            "(2.71828...)^{", "r", "t", "}",
            "=",
            "r", "\\cdot",
            "(2.71828...)^{", "r", "t", "}",
            tex_to_color_map={
                "2.71828...": TEAL,
            }
        )
        solution_with_e = OldTex(
            "{d \\over dt}",
            "{e}^{", "r", "t", "}",
            "=",
            "r", "\\cdot",
            "{e}^{", "r", "t", "}",
            tex_to_color_map={
                "{e}": TEAL,
            }
        )
        for eq in solution_with_number, solution_with_e:
            eq.set_color_by_tex("r", BLUE, substring=False)
            eq.set_color_by_tex("t", GREY_B, substring=False)
            eq.next_to(equation, DOWN, buff=MED_LARGE_BUFF)
        lhs = solution_with_number[:6]
        lhs.save_state()
        lhs.match_x(equation)

        self.play(FadeIn(lhs[1:], DOWN))
        self.wait()
        self.play(Write(lhs[0]))

        dot1 = Dot(radius=0.05, color=RED)
        dot2 = dot1.copy()
        for sec_dot in dot1, dot2:
            sec_dot.x_tracker = ValueTracker(15)
            sec_dot.add_updater(lambda d: d.move_to(axes.input_to_graph_point(
                d.x_tracker.get_value(), exp_graph
            )))
        line = Line(LEFT, RIGHT, stroke_color=GREY_A, stroke_width=2)
        line.add_updater(lambda l: l.put_start_and_end_on(
            dot1.get_center(), dot2.get_center()
        ).set_length(10))

        dot2.x_tracker.set_value(17)
        dot1.x_tracker.set_value(15)
        self.play(
            FadeOut(words),
            FadeIn(dot1),
            FadeIn(dot2),
            FadeIn(line),
        )
        self.play(
            dot2.x_tracker.animate.set_value(15 + 1e-6),
            run_time=3
        )
        self.play(
            dot1.x_tracker.animate.set_value(18),
            dot2.x_tracker.animate.set_value(18 + 1e-6),
            run_time=3
        )
        self.play(
            FadeOut(dot1),
            FadeOut(dot2),
            FadeOut(line),
        )
        self.wait()

        self.play(Restore(lhs))
        self.play(
            FadeIn(solution_with_number[6]),
            TransformFromCopy(lhs[1:], solution_with_number[8:], path_arc=30 * DEGREES),
        )
        self.play(TransformFromCopy(
            solution_with_number[12], solution_with_number[7],
            path_arc=-90 * DEGREES,
        ))
        self.wait()

        # Historical letters
        correspondants = Group()
        for name1, name2, letter, year in [("Leibniz", "Huygens", "b", "1690"), ("Euler", "Goldbach", "e", "1731")]:
            im1 = ImageMobject(name1, height=2.5)
            im2 = ImageMobject(name2, height=2.5)

            lines = VGroup(*(Line(LEFT, RIGHT) for x in range(11)))
            lines.set_width(1.6)
            lines.arrange(DOWN, buff=0.2)
            lines.set_stroke(GREY_A, 2)
            lines[-1].stretch(0.5, 0, about_edge=LEFT)

            eq = OldTex(letter, "= 2.71828\\dots")
            eq[0].scale(1.5, about_edge=RIGHT)
            eq[0].align_to(eq[1], DOWN)
            eq.set_color(TEAL)
            eq.match_width(lines)
            eq.move_to(lines[5])
            lines.remove(*lines[4:7])
            lines.add(eq)
            box = SurroundingRectangle(lines, buff=0.25)
            box.set_stroke(GREY_C, 2)
            note = VGroup(box, lines)
            note.match_height(im1)

            group = Group()
            arrow = Vector(0.5 * RIGHT, fill_color=GREY_A)
            group.add(im1, arrow, note, arrow.copy(), im2)
            group.arrange(RIGHT)
            note.align_to(im1, UP)
            group.next_to(solution_with_number, DOWN, buff=LARGE_BUFF)

            for im, name, index in [(im1, name1, 0), (im2, name2, 4)]:
                name_label = Text(name, font_size=24)
                name_label.set_color(GREY_A)
                name_label.next_to(im, DOWN)
                rect = SurroundingRectangle(im, buff=0, stroke_color=GREY_A, stroke_width=1)
                group.replace_submobject(index, Group(im, rect, name_label))

            date = Text(year, font_size=24)
            date.next_to(box, UP)
            note.add(date)
            group.eq = eq
            group.eq.set_opacity(0)

            correspondants.add(group)

        b_group, e_group = correspondants
        self.play(LaggedStartMap(FadeIn, b_group, shift=0.5 * UP, lag_ratio=0.2, run_time=1))
        b_group.eq.set_fill(opacity=1)
        self.play(Write(b_group.eq, run_time=1))
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, b_group, shift=0.5 * UP),
            LaggedStartMap(FadeIn, e_group, shift=0.5 * UP),
        )
        e_group.eq.set_fill(opacity=1)
        self.play(Write(e_group.eq, run_time=1))
        self.wait()

        # Euler's book
        e_usage = e_group.eq.copy()
        book = ImageMobject("Introductio_in_Analysin_infinitorum")
        book.match_width(e_group[0][0])
        book.move_to(e_group[2][0])
        date = Text("1748", font_size=24)
        date.next_to(book, UP, SMALL_BUFF)

        self.play(
            LaggedStartMap(FadeOut, e_group[2:], shift=0.5 * RIGHT),
            FadeIn(book),
            FadeIn(date),
            e_usage.animate.scale(1.4).next_to(book, RIGHT, aligned_edge=UP).shift(0.25 * DOWN)
        )
        self.wait()

        pi_eq = OldTex("\\pi = 3.1415\\dots", fill_color=GREEN, font_size=36)
        func_eq = OldTex("f(x)", font_size=36)
        pi_eq.next_to(e_usage, DOWN, buff=0.5, aligned_edge=LEFT)
        func_eq.next_to(pi_eq, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(pi_eq, run_time=1))
        self.wait()
        self.play(Write(func_eq, run_time=1))
        self.wait()

        # Final notation
        self.play(FadeTransformPieces(solution_with_number, solution_with_e))
        self.wait()

    def get_equation(self, r="r"):
        return get_1d_equation(r).to_edge(UP)
