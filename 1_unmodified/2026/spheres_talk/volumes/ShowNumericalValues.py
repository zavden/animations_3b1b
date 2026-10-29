# ==============================================================================
# Scene:      ShowNumericalValues
# Source:     videos/_2026/spheres_talk/volumes.py (lines 1216-1343)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowNumericalValues.py ShowNumericalValues -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_volume_texs():
    return [
        R"1",
        R"2 r",
        R"\pi r^2",
        R"{4 \over 3} \pi r^3",
        R"{\pi^2 \over 2} r^4",
        R"{8 \over 15} \pi^2 r^5",
        R"{\pi^3 \over 6} r^6",
        R"{16 \pi^3 \over 105} r^7",
        R"{\pi^4 \over 24} r^8",
        R"{32 \pi^4 \over 945} r^9",
        R"{\pi^5 \over 120} r^10",
    ]


class ShowNumericalValues(InteractiveScene):
    def construct(self):
        # Set up
        axes = Axes((0, 25), (0, 5))
        axes.to_edge(DOWN, buff=LARGE_BUFF)
        axes.to_edge(LEFT, buff=MED_LARGE_BUFF)
        axes.x_axis.add_numbers()
        y_label = Text("Volume of a\nunit ball")
        y_label.next_to(axes.y_axis.get_top(), UP)
        y_label.shift_onto_screen(buff=MED_SMALL_BUFF)
        x_label = Text("Dimension")
        x_label.next_to(axes.x_axis.get_end(), UP)
        x_label.shift_onto_screen()
        axes.add(x_label)
        axes.add(y_label)

        def func(n):
            return math.pi**(n / 2) / math.gamma(n/2 + 1)

        graph = axes.get_graph(func)
        graph.set_stroke(BLUE, 2)

        self.add(axes)

        # Add terms
        formulas = VGroup(
            Tex(s.split(" r")[0])
            for s in get_volume_texs()
        )
        v_lines = VGroup(
            axes.get_v_line_to_graph(x, graph, line_func=Line)
            for x in range(len(formulas))
        )
        v_lines.set_stroke(BLUE, 5)
        dots = VGroup(Dot(line.get_end()) for line in v_lines)
        dots.set_fill(BLUE_E)

        expressions = VGroup()
        for n, formula, dot in zip(it.count(), formulas, dots):
            formula.next_to(dot, RIGHT)
            approx = VGroup(
                Tex(R"\approx"),
                DecimalNumber(func(n))
            )
            approx.arrange(RIGHT)
            approx.next_to(formula, RIGHT)
            expressions.add(VGroup(formula, *approx))
            if n < 2:
                approx.set_fill(opacity=0)

        last_expression = VGroup()
        for v_line, dot, expression in zip(v_lines, dots, expressions):
            self.remove(last_expression)
            self.add(v_line, dot, expression)
            self.wait()
            last_expression = expression

        # Show general graph
        gen_formula = Tex(R"\pi^{n/2} \over (n/2)!")
        gen_formula.next_to(axes.i2gp(11, graph), UR)

        self.play(
            ShowCreation(graph),
            v_lines.animate.set_stroke(opacity=0.25),
            dots.animate.set_fill(opacity=0.25),
            FadeOut(last_expression[1:]),
            FadeTransform(last_expression[0], gen_formula),
            run_time=2
        )
        self.wait()

        # Smooth shot of general graph
        if False:
            gen_formula.scale(2).to_corner(UR).fix_in_frame()

            graph_segment = graph.copy().pointwise_become_partial(graph, 0, 0.6)

            self.frame.reorient(0, 0, 0, (-4.4, -2.29, 0.0), 2.91)
            self.remove(graph, y_label)
            self.play(
                self.frame.animate.to_default_state().set_anim_args(run_time=8),
                ShowCreation(graph_segment, time_span=(2, 12), run_time=15),
                LaggedStartMap(ShowCreation, v_lines, lag_ratio=0.75, run_time=12),
                LaggedStartMap(FadeIn, dots, lag_ratio=0.75, run_time=12),
                Write(gen_formula, time_span=(7, 9)),
            )
            self.wait()
            return

        # Add recurrence relationship
        recurrence = Tex(
            R"V_n = {2\pi \over n} V_{n - 2}",
            font_size=72,
            t2c={"V_n": YELLOW, "V_{n - 2}": YELLOW}
        )
        recurrence.to_corner(UR)

        self.add(recurrence)
        self.wait()

        for n in range(1, 9):
            dot1, dot2 = dots = VGroup(Dot(v_lines[k].get_top()) for k in [n, n + 2])
            dots.set_fill(YELLOW)
            arrow = Arrow(
                dot1.get_center(),
                dot2.get_center(),
                path_arc=-75 * DEG,
                thickness=5,
                fill_color=YELLOW,
                buff=0.1
            )
            label = Tex(Rf"2\pi / {n + 2}")
            label.next_to(
                arrow.get_center(),
                rotate_vector(arrow.get_vector(), 90 * DEG),
                buff=0.15,
            )
            group = VGroup(dots, arrow, label)
            self.add(group)
            self.wait()
            self.remove(group)

        # Zoom out
        self.play(
            self.frame.animate.reorient(0, 0, 0, (5.6, 0.15, 0.0), 14.77),
            run_time=3
        )
        self.wait()
