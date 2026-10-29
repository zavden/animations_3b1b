# ==============================================================================
# Scene:      LowerBound
# Source:     videos/_2017/eoc/chapter8.py (lines 2023-2255)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl LowerBound.py LowerBound -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
#   - NameError in the original: draw_curve unpacks `label` but writes `graph_label`
#   - a VGroup slice is a VGroup in GL (list + VGroup fails)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

DISTANCE_COLOR = BLUE


VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter8.py -----

def v_rate_func(t):
    return 4*t - 4*(t**2)


def v_func(t):
    return t*(8-t)


def s_func(t):
    return 4*t**2 - (t**3)/3.


class PlotVelocity(GraphScene):
    CONFIG = {
        "x_min" : -1,
        "x_max" : 9,
        "x_axis_width" : 9,
        "x_tick_frequency" : 1,
        "x_labeled_nums" : list(range(1, 9)),
        "x_axis_label" : "$t$",
        "y_min" : 0,
        "y_max" : 25,
        "y_axis_height" : 6,
        "y_tick_frequency" : 5,
        "y_labeled_nums" : list(range(5, 30, 5)),
        "y_axis_label" : "Velocity in $\\frac{\\text{meters}}{\\text{second}}$",
        "num_graph_anchor_points" : 50,
    }
    def construct(self):
        self.setup_axes()
        self.add_speedometer()
        self.plot_points()
        self.draw_curve()

    def add_speedometer(self):
        speedometer = Speedometer()
        speedometer.next_to(self.y_axis_label_mob, RIGHT, LARGE_BUFF)
        speedometer.to_edge(UP)

        self.play(DrawBorderThenFill(
            speedometer, 
            lag_ratio = 0.5,
            rate_func=linear,
        ))

        self.speedometer = speedometer

    def plot_points(self):
        times = list(range(0, 9))
        points = [
            self.coords_to_point(t, v_func(t))
            for t in times
        ]
        dots = VGroup(*[Dot(p, radius = 0.07) for p in points])
        dots.set_color(VELOCITY_COLOR)

        pre_dots = VGroup()
        dot_intro_anims = []

        for time, dot in zip(times, dots):
            pre_dot = dot.copy()
            self.speedometer.move_needle_to_velocity(v_func(time))
            pre_dot.move_to(self.speedometer.get_needle_tip())
            pre_dot.set_fill(opacity = 0)
            pre_dots.add(pre_dot)
            dot_intro_anims += [
                ApplyMethod(
                    pre_dot.set_fill, YELLOW, 1,
                    run_time = 0.1,
                ),
                ReplacementTransform(
                    pre_dot, dot,
                    run_time = 0.9,
                )
            ]
        self.speedometer.move_needle_to_velocity(0)

        self.play(
            Succession(
                *dot_intro_anims, rate_func=linear
            ),
            ApplyMethod(
                self.speedometer.move_needle_to_velocity,
                v_func(4),
                rate_func = squish_rate_func(
                    lambda t : 1-v_rate_func(t),
                    0, 0.95,
                )
            ),
            run_time = 5
        )
        self.wait()

    def draw_curve(self):
        graph, label = self.get_v_graph_and_label()

        self.revert_to_original_skipping_status()
        self.play(ShowCreation(graph, run_time = 3))
        # CHANGE: NameError in the original: draw_curve unpacks `label` but writes `graph_label`
        self.play(Write(label))
        self.wait()

    ##

    def get_v_graph_and_label(self):
        graph = self.get_graph(
            v_func, 
            x_min = 0,
            x_max = 8,
            color = VELOCITY_COLOR
        )
        graph_label = OldTex("v(t)", "=t(8-t)")
        graph_label.set_color_by_tex("v(t)", VELOCITY_COLOR)
        graph_label.next_to(
            graph.point_from_proportion(7./8.),
            UP+RIGHT
        )
        self.v_graph = graph
        self.v_graph_label = graph_label
        return graph, graph_label


class AreaIsDerivative(PlotVelocity, ReconfigurableScene):
    CONFIG = {
        "y_axis_label" : "",
        "num_rects" : 400,
        "dT" : 0.25,
        "variable_point_label" : "T",
        "area_opacity" : 0.8,
    }
    def setup(self):
        PlotVelocity.setup(self)
        ReconfigurableScene.setup(self)
        self.setup_axes()
        self.add(*self.get_v_graph_and_label())
        self.x_axis_label_mob.shift(MED_LARGE_BUFF*DOWN)
        self.v_graph_label.shift(MED_LARGE_BUFF*DOWN)
        self.foreground_mobjects = []

    def construct(self):
        self.introduce_variable_area()
        self.write_integral()
        self.nudge_input()
        self.show_rectangle_approximation()

    def introduce_variable_area(self):
        area = self.area = self.get_area(0, 6)
        x_nums = self.x_axis.numbers

        self.play(Write(area, run_time = 2))
        self.play(FadeOut(self.x_axis.numbers))
        self.add_T_label(6)
        self.change_area_bounds(
            new_t_max = 4,
            rate_func = there_and_back,
            run_time = 2
        )
        self.wait()

    def write_integral(self):
        integral = OldTex("\\int", "^T", "_0", "v(t)", "\\,dt")
        integral.to_corner(UP+RIGHT)
        integral.shift(2*LEFT)
        top_T = integral.get_part_by_tex("T")
        moving_T = self.T_label_group[0]

        s_T = OldTex("s(T)", "= ")
        s_T.set_color_by_tex("s", DISTANCE_COLOR)
        s_T.next_to(integral, LEFT)

        int_arrow, s_arrow = [
            Arrow(
                mob.get_left(), self.area.get_center(),
                color = WHITE
            )
            for mob in (integral, s_T)
        ]

        distance_word = OldTexText("Distance")
        distance_word.move_to(self.area)

        self.play(Write(integral))
        self.play(ShowCreation(int_arrow))
        self.foreground_mobjects.append(int_arrow)
        self.wait()
        self.change_area_bounds(
            new_t_max = 8,
            rate_func = there_and_back,
            run_time = 3,
        )
        self.play(Indicate(top_T))
        self.play(ReplacementTransform(
            top_T.copy(), moving_T
        ))
        self.change_area_bounds(
            new_t_max = 3,
            rate_func = there_and_back,
            run_time = 3
        )
        self.wait()
        self.play(Write(distance_word, run_time = 2))
        self.play(
            ReplacementTransform(int_arrow, s_arrow),
            FadeIn(s_T)
        )
        self.wait()
        self.play(FadeOut(distance_word))
        self.change_area_bounds(new_t_max = 0, run_time = 2)
        self.change_area_bounds(
            new_t_max = 8, 
            rate_func=linear,
            run_time = 7.9,
        )
        self.wait()
        self.change_area_bounds(new_t_max = 5)
        self.wait()

    def nudge_input(self):
        dark_area = self.area.copy()
        dark_area.set_fill(BLACK, opacity = 0.5)
        curr_T = self.x_axis.point_to_number(self.area.get_right())
        new_T = curr_T + self.dT

        rect = Rectangle(
            stroke_width = 0,
            fill_color = YELLOW,
            fill_opacity = 0.75
        )
        rect.replace(
            VGroup(
                VectorizedPoint(self.coords_to_point(new_T, 0)),
                self.right_v_line,
            ),
            stretch = True
        )

        dT_brace = Brace(rect, DOWN, buff = 0)
        dT_label = dT_brace.get_text("$dT$", buff = SMALL_BUFF)
        dT_label_group = VGroup(dT_label, dT_brace)

        ds_label = OldTex("ds")
        ds_label.next_to(rect, RIGHT, LARGE_BUFF, UP)
        ds_label.set_color(DISTANCE_COLOR)
        ds_arrow = Arrow(ds_label.get_left(), rect.get_left())
        ds_arrow.set_color(WHITE)

        v_brace = Brace(rect, LEFT, buff = SMALL_BUFF)
        v_T_label = v_brace.get_text("$v(T)$", buff = SMALL_BUFF)

        self.change_area_bounds(new_t_max = new_T)
        self.play(
            FadeIn(dark_area),
            *list(map(Animation, self.foreground_mobjects))
        )
        self.play(
            FadeOut(self.T_label_group),
            FadeIn(dT_label_group)
        )
        self.wait()
        self.play(Write(ds_label))
        self.play(ShowCreation(ds_arrow))
        self.wait(2)
        self.play(GrowFromCenter(v_brace))
        self.play(ReplacementTransform(
            self.v_graph_label.get_part_by_tex("v").copy(),
            v_T_label,
            run_time = 2
        ))
        self.wait()
        self.play(Indicate(dT_label))
        self.wait()

        self.rect = rect
        self.dT_label_group = dT_label_group
        self.v_T_label_group = VGroup(v_T_label, v_brace)
        self.dark_area = dark_area
        self.ds_label = ds_label
        self.ds_arrow = ds_arrow

    def show_rectangle_approximation(self):
        formula1 = OldTex("ds", "=", "v(T)", "dT")
        formula2 = OldTex("{ds", "\\over\\,", "dT}", "=", "v(T)")
        for formula in formula1, formula2:
            formula.next_to(self.v_graph_label, UP, LARGE_BUFF)
            formula.set_color_by_tex("ds", DISTANCE_COLOR)

        self.play(
            DrawBorderThenFill(self.rect),
            Animation(self.ds_arrow)
        )
        self.wait()
        self.play(*[
            ReplacementTransform(
                mob, formula1.get_part_by_tex(tex),
                run_time = 2
            )
            for mob, tex in [
                (self.ds_label, "ds"),
                (self.ds_arrow, "="),
                (self.v_T_label_group[0].copy(), "v(T)"),
                (self.dT_label_group[0].copy(), "dT"),
            ]
        ])
        self.wait()
        self.transition_to_alt_config(
            dT = self.dT/5.0,
            transformation_kwargs = {"run_time" : 2},
        )
        self.wait()
        self.play(*[
            ReplacementTransform(
                formula1.get_part_by_tex(tex),
                formula2.get_part_by_tex(tex),
            )
            for tex in ("ds", "=", "v(T)", "dT")
        ] + [
            Write(formula2.get_part_by_tex("over"))
        ])
        self.wait()


    ####

    def add_T_label(self, x_val, **kwargs):
        triangle = RegularPolygon(n=3, start_angle = np.pi/2)
        triangle.set_height(MED_SMALL_BUFF)
        triangle.move_to(self.coords_to_point(x_val, 0), UP)
        triangle.set_fill(WHITE, 1)
        triangle.set_stroke(width = 0)
        T_label = OldTex(self.variable_point_label)
        T_label.next_to(triangle, DOWN)
        v_line = self.get_vertical_line_to_graph(
            x_val, self.v_graph,
            color = YELLOW
        )

        self.play(
            DrawBorderThenFill(triangle),
            ShowCreation(v_line),
            Write(T_label, run_time = 1),
            **kwargs
        )

        self.T_label_group = VGroup(T_label, triangle)
        self.right_v_line = v_line

    def get_area(self, t_min, t_max):
        numerator = max(t_max - t_min, 0.01)
        dx = float(numerator) / self.num_rects
        return self.get_riemann_rectangles(
            self.v_graph,
            x_min = t_min,
            x_max = t_max,
            dx = dx,
            stroke_width = 0,
        ).set_fill(opacity = self.area_opacity)

    def change_area_bounds(self, new_t_min = None, new_t_max = None, **kwargs):
        curr_t_min = self.x_axis.point_to_number(self.area.get_left())
        curr_t_max = self.x_axis.point_to_number(self.area.get_right())
        if new_t_min is None:
            new_t_min = curr_t_min
        if new_t_max is None:
            new_t_max = curr_t_max

        group = VGroup(self.area, self.right_v_line, self.T_label_group)
        def update_group(group, alpha):
            area, v_line, T_label = group
            t_min = interpolate(curr_t_min, new_t_min, alpha)
            t_max = interpolate(curr_t_max, new_t_max, alpha)
            new_area = self.get_area(t_min, t_max)
            new_v_line = self.get_vertical_line_to_graph(
                t_max, self.v_graph
            )
            new_v_line.set_color(v_line.get_color())
            T_label.move_to(new_v_line.get_bottom(), UP)

            #Fade close to 0
            T_label[0].set_fill(opacity = min(1, t_max)) 

            Transform(area, new_area).update(1)
            Transform(v_line, new_v_line).update(1)
            return group

        self.play(
            UpdateFromAlphaFunc(group, update_group),
            *list(map(Animation, self.foreground_mobjects)),
            **kwargs
        )


class LowerBound(AreaIsDerivative):
    CONFIG = {
        "graph_origin" : 2.5*DOWN + 6*LEFT
    }

    def construct(self):
        self.add_integral_and_area()
        self.mention_lower_bound()
        self.drag_right_endpoint_to_zero()
        self.write_antiderivative_difference()
        self.show_alternate_antiderivative_difference()
        self.add_constant_to_antiderivative()

    def add_integral_and_area(self):
        self.area = self.get_area(0, 6)
        self.integral = self.get_integral("0", "T")
        self.remove(self.x_axis.numbers)
        self.add(self.area, self.integral)
        self.add_T_label(6, run_time = 0)

    def mention_lower_bound(self):
        lower_bound = self.integral.get_part_by_tex("0")
        circle = Circle(color = YELLOW)
        circle.replace(lower_bound)
        circle.scale(3)
        zero_label = lower_bound.copy()

        self.play(ShowCreation(circle))
        self.play(Indicate(lower_bound))
        self.play(
            zero_label.scale, 1.5,
            zero_label.next_to, self.graph_origin, DOWN, MED_LARGE_BUFF,
            FadeOut(circle)
        )
        self.wait()

        self.zero_label = zero_label

    def drag_right_endpoint_to_zero(self):
        zero_integral = self.get_integral("0", "0")
        zero_integral[1].set_color(YELLOW)
        zero_int_bounds = list(reversed(
            zero_integral.get_parts_by_tex("0")
        ))
        for bound in zero_int_bounds:
            circle = Circle(color = YELLOW)
            circle.replace(bound)
            circle.scale(3)
            bound.circle = circle
        self.integral.save_state()
        equals_zero = OldTex("=0")
        equals_zero.next_to(zero_integral, RIGHT)
        equals_zero.set_color(GREEN)

        self.change_area_bounds(0, 0, run_time = 3)
        self.play(ReplacementTransform(
            self.zero_label.copy(), equals_zero
        ))
        self.play(Transform(self.integral, zero_integral))
        self.wait(2)
        for bound in zero_int_bounds:
            self.play(ShowCreation(bound.circle))
            self.play(FadeOut(bound.circle))
        self.play(*[
            ReplacementTransform(
                bound.copy(), VGroup(equals_zero[1])
            )
            for bound in zero_int_bounds
        ])
        self.wait(2)
        self.change_area_bounds(0, 5)
        self.play(
            self.integral.restore,
            FadeOut(equals_zero)
        )

        self.zero_integral = zero_integral

    def write_antiderivative_difference(self):
        antideriv_diff = self.get_antiderivative_difference("0", "T")
        equals, at_T, minus, at_zero = antideriv_diff
        antideriv_diff_at_eight = self.get_antiderivative_difference("0", "8")
        at_eight = antideriv_diff_at_eight.left_part
        integral_at_eight = self.get_integral("0", "8")

        for part in at_T, at_zero, at_eight:
            part.brace = Brace(part, DOWN, buff = SMALL_BUFF)
            part.brace.save_state()

        antideriv_text = at_T.brace.get_text("Antiderivative", buff = SMALL_BUFF)
        antideriv_text.set_color(MAROON_B)
        value_at_eight = at_eight.brace.get_text(
            "%.2f"%s_func(8)
        )
        happens_to_be_zero = at_zero.brace.get_text("""
            Happens to
            equal 0
        """)

        big_brace = Brace(VGroup(at_T, at_zero))
        cancel_text = big_brace.get_text("Cancels when $T=0$")

        self.play(*list(map(Write, [equals, at_T])))
        self.play(
            GrowFromCenter(at_T.brace),
            Write(antideriv_text, run_time = 2)
        )
        self.change_area_bounds(0, 5.5, rate_func = there_and_back)
        self.wait()
        self.play(
            ReplacementTransform(at_T.copy(), at_zero),
            Write(minus)
        )
        self.wait()
        self.play(
            ReplacementTransform(at_T.brace, big_brace),
            ReplacementTransform(antideriv_text, cancel_text)
        )
        self.change_area_bounds(0, 0, run_time = 4)
        self.wait()
        self.play(
            ReplacementTransform(big_brace, at_zero.brace),
            ReplacementTransform(cancel_text, happens_to_be_zero),
        )
        self.wait(2)
        self.change_area_bounds(0, 8, run_time = 2)
        self.play(
            Transform(self.integral, integral_at_eight),
            Transform(antideriv_diff, antideriv_diff_at_eight),
            MaintainPositionRelativeTo(at_zero.brace, at_zero),
            MaintainPositionRelativeTo(happens_to_be_zero, at_zero.brace),
        )
        self.play(
            GrowFromCenter(at_eight.brace),
            Write(value_at_eight)
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [
            at_eight.brace, value_at_eight,
            at_zero.brace, happens_to_be_zero,
        ])))

        self.antideriv_diff = antideriv_diff

    def show_alternate_antiderivative_difference(self):
        new_integral = self.get_integral("1", "7")
        new_antideriv_diff = self.get_antiderivative_difference("1", "7")
        numbers = [
            OldTex("%d"%d).next_to(
                self.coords_to_point(d, 0), 
                DOWN, MED_LARGE_BUFF
            )
            for d in (1, 7)
        ]
        # CHANGE: a VGroup slice is a VGroup in GL (list + VGroup fails)
        tex_mobs = [new_integral, *new_antideriv_diff[1::2], *numbers]
        for tex_mob in tex_mobs:
            tex_mob.set_color_by_tex("1", RED)
            tex_mob.set_color_by_tex("7", GREEN)
            tex_mob.set_color_by_tex("\\frac{1}{3}", WHITE)

        self.change_area_bounds(1, 7, run_time = 2)
        self.play(
            self.T_label_group[0].set_fill, None, 0,
            *list(map(FadeIn, numbers))
        )
        self.play(
            Transform(self.integral, new_integral),
            Transform(self.antideriv_diff, new_antideriv_diff),
        )
        self.wait(3)
        for part in self.antideriv_diff[1::2]:
            self.play(Indicate(part, scale_factor = 1.1))
            self.wait()

    def add_constant_to_antiderivative(self):
        antideriv_diff = self.antideriv_diff
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        plus_fives = VGroup(*[OldTex("+5") for i in range(2)])
        plus_fives.set_color(YELLOW)
        for five, part in zip(plus_fives, antideriv_diff[1::2]):
            five.next_to(part, DOWN)
        group = VGroup(
            plus_fives[0],
            antideriv_diff[2].copy(),
            plus_fives[1]
        )

        self.play(Write(plus_fives, run_time = 2))
        self.wait(2)
        self.play(
            group.arrange,
            group.next_to, antideriv_diff, DOWN, MED_LARGE_BUFF
        )
        self.wait()
        self.play(FadeOut(group, run_time = 2))
        self.wait()

    #####

    def get_integral(self, lower_bound, upper_bound):
        result = OldTex(
            "\\int", "^"+upper_bound, "_"+lower_bound, 
            "t(8-t)", "\\,dt"
        )
        result.next_to(self.graph_origin, RIGHT, MED_LARGE_BUFF)
        result.to_edge(UP)
        return result

    def get_antiderivative_difference(self, lower_bound, upper_bound):
        strings = []
        for bound in upper_bound, lower_bound:
            try:
                d = int(bound)
                strings.append("(%d)"%d)
            except:
                strings.append(bound)
        parts = []
        for s in strings:
            part = OldTex(
                "\\left(",
                "4", s, "^2", "-", "\\frac{1}{3}", s, "^3"
                "\\right))"
            )
            part.set_color_by_tex(s, YELLOW, substring = False)
            parts.append(part)
        result = VGroup(
            OldTex("="), parts[0], 
            OldTex("-"), parts[1],
        )
        result.left_part, result.right_part = parts
        result.arrange(RIGHT)
        result.scale(0.9)
        result.next_to(self.integral, RIGHT)
        return result
