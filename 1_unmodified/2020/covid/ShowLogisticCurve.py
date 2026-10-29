# ==============================================================================
# Scene:      ShowLogisticCurve
# Source:     videos/_2020/covid.py (lines 1456-1684)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowLogisticCurve.py ShowLogisticCurve -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowLogisticCurve(Scene):
    def construct(self):
        # Init axes
        axes = self.get_axes()
        self.add(axes)

        # Add ODE
        ode = OldTex(
            "{dN \\over dt} =",
            "c",
            "\\left(1 - {N \\over \\text{pop.}}\\right)",
            "N",
            tex_to_color_map={"N": YELLOW}
        )
        ode.set_height(0.75)
        ode.center()
        ode.to_edge(RIGHT)
        ode.shift(1.5 * UP)
        self.add(ode)

        # Show curve
        curve = axes.get_graph(
            lambda x: 8 * smooth(x / 10) + 0.2,
        )
        curve.set_stroke(YELLOW, 3)

        curve_title = OldTexText("Logistic curve")
        curve_title.set_height(0.75)
        curve_title.next_to(curve.get_end(), UL)

        self.play(ShowCreation(curve, run_time=3))
        self.play(FadeIn(curve_title, lag_ratio=0.1))
        self.wait()

        # Early part
        line = Line(
            curve.point_from_proportion(0),
            curve.point_from_proportion(0.25),
        )
        rect = Rectangle()
        rect.set_stroke(width=0)
        rect.set_fill(TEAL, 0.5)
        rect.replace(line, stretch=True)

        exp_curve = axes.get_graph(
            lambda x: 0.15 * np.exp(0.68 * x)
        )
        exp_curve.set_stroke(RED, 3)

        rect.save_state()
        rect.stretch(0, 0, about_edge=LEFT)
        self.play(Restore(rect))
        self.play(ShowCreation(exp_curve, run_time=4))

        # Show capacity
        line = DashedLine(
            axes.c2p(0, 8.2),
            axes.c2p(axes.x_max, 8.2),
        )
        line.set_stroke(BLUE, 2)

        self.play(ShowCreation(line))
        self.wait()
        self.play(FadeOut(rect), FadeOut(exp_curve))

        # Show inflection point
        infl_point = axes.input_to_graph_point(5, curve)
        infl_dot = Dot(infl_point)
        infl_dot.set_stroke(WHITE, 3)

        curve_up_part = curve.copy()
        curve_up_part.pointwise_become_partial(curve, 0, 0.4)
        curve_up_part.set_stroke(GREEN)
        curve_down_part = curve.copy()
        curve_down_part.pointwise_become_partial(curve, 0.4, 1)
        curve_down_part.set_stroke(RED)
        for part in curve_up_part, curve_down_part:
            part.save_state()
            part.stretch(0, 1)
            part.set_y(axes.c2p(0, 0)[1])

        pre_dot = curve.copy()
        pre_dot.pointwise_become_partial(curve, 0.375, 0.425)

        infl_name = OldTexText("Inflection point")
        infl_name.next_to(infl_dot, LEFT)

        self.play(ReplacementTransform(pre_dot, infl_dot, path_arc=90 * DEGREES))
        self.add(curve_up_part, infl_dot)
        self.play(Restore(curve_up_part))
        self.add(curve_down_part, infl_dot)
        self.play(Restore(curve_down_part))
        self.wait()
        self.play(Write(infl_name, run_time=1))
        self.wait()

        # Show tangent line
        x_tracker = ValueTracker(0)
        tan_line = Line(LEFT, RIGHT)
        tan_line.set_width(5)
        tan_line.set_stroke(YELLOW, 2)

        def update_tan_line(line):
            x1 = x_tracker.get_value()
            x2 = x1 + 0.001
            p1 = axes.input_to_graph_point(x1, curve)
            p2 = axes.input_to_graph_point(x2, curve)
            angle = angle_of_vector(p2 - p1)
            line.rotate(angle - line.get_angle())
            line.move_to(p1)

        tan_line.add_updater(update_tan_line)

        dot = Dot()
        dot.scale(0.75)
        dot.set_fill(BLUE, 0.75)
        dot.add_updater(
            lambda m: m.move_to(axes.input_to_graph_point(
                x_tracker.get_value(), curve
            ))
        )

        self.play(
            ShowCreation(tan_line),
            FadeInFromLarge(dot),
        )
        self.play(
            x_tracker.set_value, 5,
            run_time=6,
        )
        self.wait()
        self.play(
            x_tracker.set_value, 9.9,
            run_time=6,
        )
        self.wait()

        # Define growth factor
        gf_label = OldTex(
            "\\text{Growth factor} =",
            "{\\Delta N_d \\over \\Delta N_{d - 1}}",
            tex_to_color_map={
                "\\Delta": WHITE,
                "N_d": YELLOW,
                "N_{d - 1}": BLUE,
            }
        )
        gf_label.next_to(infl_dot, RIGHT, LARGE_BUFF)

        numer_label = OldTexText("New cases one day")
        denom_label = OldTexText("New cases the\\\\previous day")

        for label, tex, vect in (numer_label, "N_d", UL), (denom_label, "N_{d - 1}", DL):
            part = gf_label.get_part_by_tex(tex)
            label.match_color(part)
            label.next_to(part, vect, LARGE_BUFF)
            label.shift(2 * RIGHT)
            arrow = Arrow(
                label.get_corner(vect[1] * DOWN),
                part.get_corner(vect[1] * UP) + 0.25 * LEFT,
                buff=0.1,
            )
            arrow.match_color(part)
            label.add_to_back(arrow)

        self.play(
            FadeIn(gf_label[0], RIGHT),
            FadeIn(gf_label[1:], LEFT),
            FadeOut(ode)
        )
        self.wait()
        for label in numer_label, denom_label:
            self.play(FadeIn(label, lag_ratio=0.1))
            self.wait()

        # Show example growth factors
        self.play(x_tracker.set_value, 1)

        eq = OldTex("=")
        eq.next_to(gf_label, RIGHT)
        gf = DecimalNumber(1.15)
        gf.set_height(0.4)
        gf.next_to(eq, RIGHT)

        def get_growth_factor():
            x1 = x_tracker.get_value()
            x0 = x1 - 0.2
            x2 = x1 + 0.2
            p0, p1, p2 = [
                axes.input_to_graph_point(x, curve)
                for x in [x0, x1, x2]
            ]
            return (p2[1] - p1[1]) / (p1[1] - p0[1])

        gf.add_updater(lambda m: m.set_value(get_growth_factor()))

        self.add(eq, gf)
        self.play(
            x_tracker.set_value, 5,
            run_time=6,
            rate_func=linear,
        )
        self.wait()
        self.play(
            x_tracker.set_value, 9,
            run_time=6,
            rate_func=linear,
        )

    def get_axes(self):
        axes = Axes(
            x_min=0,
            x_max=13,
            y_min=0,
            y_max=10,
            y_axis_config={
                "unit_size": 0.7,
                "include_tip": False,
            }
        )
        axes.center()
        axes.to_edge(DOWN)

        x_label = OldTexText("Time")
        x_label.next_to(axes.x_axis, UP, aligned_edge=RIGHT)
        y_label = OldTexText("N cases")
        y_label.next_to(axes.y_axis, RIGHT, aligned_edge=UP)
        axes.add(x_label, y_label)
        return axes
