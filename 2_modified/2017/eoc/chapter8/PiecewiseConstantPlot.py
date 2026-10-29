# ==============================================================================
# Scene:      PiecewiseConstantPlot
# Source:     videos/_2017/eoc/chapter8.py (lines 725-1355)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl PiecewiseConstantPlot.py PiecewiseConstantPlot -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - NameError in the original: draw_curve unpacks `label` but writes `graph_label`
#   - a single-string OldTexText keeps its glyphs one level down (submobjects[0]); replace the glyph through set_submobjects
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter8.py -----

def v_rate_func(t):
    return 4*t - 4*(t**2)


def v_func(t):
    return t*(8-t)


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


class PiecewiseConstantPlot(PlotVelocity):
    CONFIG = {
        "y_axis_label" : "",
        "min_graph_proportion" : 0.1,
        "max_graph_proportion" : 0.8,
        "num_riemann_approximations" : 7,
        "riemann_rect_fill_opacity" : 0.75,
        "tick_size" : 0.2,
    }
    def construct(self):
        self.setup_graph()
        self.always_changing()
        self.show_piecewise_constant_graph()
        self.compute_distance_on_each_interval()
        self.approximate_original_curve()
        self.revert_to_specific_approximation()
        self.show_specific_rectangle()
        self.show_v_dt_for_all_rectangles()
        self.write_integral_symbol()
        self.roles_of_dt()
        self.what_does_sum_approach()
        self.label_integral()

    def setup_graph(self):
        self.setup_axes()
        self.add(*self.get_v_graph_and_label())

    def always_changing(self):
        dot = Dot()
        arrow = Arrow(LEFT, RIGHT)
        words = OldTexText("Always changing")
        group = VGroup(dot, arrow, words)
        def update_group(group, alpha):
            dot, arrow, words = group
            prop = interpolate(
                self.min_graph_proportion,
                self.max_graph_proportion,
                alpha
            )
            graph_point = self.v_graph.point_from_proportion(prop)
            dot.move_to(graph_point)
            x_val = self.x_axis.point_to_number(graph_point)
            angle = self.angle_of_tangent(x_val, self.v_graph)
            angle += np.pi/2
            vect = rotate_vector(RIGHT, angle)
            arrow.rotate(angle - arrow.get_angle() + np.pi)
            arrow.shift(
                graph_point + MED_SMALL_BUFF*vect - arrow.get_end()
            )
            words.next_to(arrow.get_start(), UP)
            return group
        update_group(group, 0)

        self.play(
            Write(words),
            ShowCreation(arrow),
            DrawBorderThenFill(dot),
            run_time = 1
        )
        self.play(UpdateFromAlphaFunc(
            group, update_group,
            rate_func = there_and_back,
            run_time = 5
        ))
        self.wait()
        self.play(FadeOut(group))

    def show_piecewise_constant_graph(self):
        pw_constant_graph = self.get_pw_constant_graph()
        alt_lines = [
            line.copy().set_color(YELLOW)
            for line in pw_constant_graph[:4]
        ]
        for line in alt_lines:
            line.start_dot = Dot(line.get_start())
            line.end_dot = Dot(line.get_end())
            VGroup(line.start_dot, line.end_dot).set_color(line.get_color())
        line = alt_lines[0]

        faders = [self.v_graph, self.v_graph_label]
        for mob in faders:
            mob.save_state()
            mob.generate_target()
            mob.target.fade(0.7)

        self.play(*list(map(MoveToTarget, faders)))
        self.play(ShowCreation(pw_constant_graph, run_time = 2))
        self.wait()
        self.play(ShowCreation(line))
        self.wait()
        for new_line in alt_lines[1:]:
            for mob in line.end_dot, new_line.start_dot, new_line:
                self.play(Transform(
                    line, mob,
                    run_time = 1./3
                ))
            self.remove(line)
            self.add(new_line)
            self.wait(2)
            line = new_line
        self.play(FadeOut(line))

        self.pw_constant_graph = pw_constant_graph

    def compute_distance_on_each_interval(self):
        rect_list = self.get_riemann_rectangles_list(
            self.v_graph, self.num_riemann_approximations, 
            max_dx = 1,
            x_min = 0,
            x_max = 8,
        )
        for rects in rect_list:
            rects.set_fill(opacity = self.riemann_rect_fill_opacity)
        flat_rects = self.get_riemann_rectangles(
            self.get_graph(lambda t : 0),
            x_min = 0, x_max = 8, dx = 1
        )
        rects = rect_list[0]
        rect = rects[1]
        flat_rects.submobjects[1] = rect.copy()

        right_brace = Brace(rect, RIGHT)
        top_brace = Brace(rect, UP)
        right_brace.label = right_brace.get_text("$7\\frac{\\text{m}}{\\text{s}}$")
        top_brace.label = top_brace.get_text("$1$s")

        self.play(FadeIn(rect))
        for brace in right_brace, top_brace:
            self.play(
                GrowFromCenter(brace),
                Write(brace.label, run_time = 1),
            )
            brace.add(brace.label)
            self.wait()
        self.play(
            ReplacementTransform(
                flat_rects, rects,
                run_time = 2,
                lag_ratio = 0.5,
            ),
            Animation(right_brace)
        )
        self.play(*list(map(FadeOut, [top_brace, right_brace])))
        self.wait()

        self.rects = rects
        self.rect_list = rect_list

    def approximate_original_curve(self):
        rects = self.rects
        self.play(
            FadeOut(self.pw_constant_graph),
            *[
                m.restore 
                for m in (self.v_graph, self.v_graph_label)
            ]+[Animation(self.rects)]
        )
        for new_rects in self.rect_list[1:]:
            self.transform_between_riemann_rects(rects, new_rects)
            self.wait()

    def revert_to_specific_approximation(self):
        rects = self.rects
        rects.save_state()
        target_rects = self.rect_list[2]
        target_rects.set_fill(opacity = 1)

        ticks = self.get_ticks(target_rects)
        tick_pair = VGroup(*ticks[4:6])
        brace = Brace(tick_pair, DOWN, buff = 0)
        dt_label = brace.get_text("$dt$", buff = SMALL_BUFF)

        example_text = OldTexText(
            "For example, \\\\",
            "$dt$", "$=0.25$"
        )
        example_text.to_corner(UP+RIGHT)
        example_text.set_color_by_tex("dt", YELLOW)

        self.play(ReplacementTransform(
            rects, target_rects,
            run_time = 2,
            lag_ratio = 0.5
        ))
        rects.restore()
        self.wait()
        self.play(
            ShowCreation(ticks),
            FadeOut(self.x_axis.numbers)
        )
        self.play(
            GrowFromCenter(brace),
            Write(dt_label)
        )
        self.wait()
        self.play(
            FadeIn(
                example_text, 
                run_time = 2,
                lag_ratio = 0.5,
            ),
            ReplacementTransform(
                dt_label.copy(),
                example_text.get_part_by_tex("dt")
            )
        )
        self.wait()

        self.rects = rects = target_rects
        self.ticks = ticks
        self.dt_brace = brace
        self.dt_label = dt_label
        self.dt_example_text = example_text

    def show_specific_rectangle(self):
        rects = self.rects
        rect = rects[4].copy()
        rect_top = Line(
            rect.get_corner(UP+LEFT),
            rect.get_corner(UP+RIGHT),
            color = self.v_graph.get_color()
        )

        t_vals = [1, 1.25]
        t_labels = VGroup(*[
            OldTex("t=%s"%str(t))
            for t in t_vals
        ])
        t_labels.scale(0.7)
        t_labels.next_to(rect, DOWN)
        for vect, label in zip([LEFT, RIGHT], t_labels):
            label.shift(1.5*vect)
            label.add(Arrow(
                label.get_edge_center(-vect),
                rect.get_corner(DOWN+vect),
                buff = SMALL_BUFF,
                tip_length = 0.15,
                color = WHITE
            ))

        v_lines = VGroup()
        h_lines = VGroup()
        height_labels = VGroup()
        for t in t_vals:
            v_line = self.get_vertical_line_to_graph(
                t, self.v_graph,
                color = YELLOW
            )
            y_axis_point = self.graph_origin[0]*RIGHT
            y_axis_point += v_line.get_end()[1]*UP
            h_line = DashedLine(v_line.get_end(), y_axis_point)
            label = OldTex("%.1f"%v_func(t))
            label.scale(0.5)
            label.next_to(h_line, LEFT, SMALL_BUFF)
            v_lines.add(v_line)
            h_lines.add(h_line)
            height_labels.add(label)

        circle = Circle(radius = 0.25, color = WHITE)
        circle.move_to(rect.get_top())

        self.play(
            rects.set_fill, None, 0.25,
            Animation(rect)
        )
        self.wait()
        for label in t_labels:
            self.play(FadeIn(label))
        self.wait()
        for v_line, h_line, label in zip(v_lines, h_lines, height_labels):
            self.play(ShowCreation(v_line))
            self.play(ShowCreation(h_line))
            self.play(Write(label, run_time = 1))
            self.wait()
        self.wait()
        t_label_copy = t_labels[0].copy()
        self.play(
            t_label_copy.scale, 1./0.7,
            t_label_copy.next_to, self.v_graph_label, DOWN+LEFT, 0
        )
        self.wait()
        self.play(FadeOut(t_label_copy))
        self.wait()

        self.play(ShowCreation(circle))
        self.play(ShowCreation(rect_top))
        self.play(FadeOut(circle))
        rect.add(rect_top)
        self.wait()
        for x in range(2):
            self.play(
                rect.stretch_to_fit_height, v_lines[1].get_height(),
                rect.move_to, rect.get_bottom(), DOWN,
                Animation(v_lines),
                run_time = 4,
                rate_func = there_and_back
            )

        self.play(*list(map(FadeOut, [
            group[1]
            for group in (v_lines, h_lines, height_labels)
        ])))
        self.play(
            v_lines[0].set_color, RED,
            rate_func = there_and_back,
        )
        self.wait()

        area = OldTexText(
            "7$\\frac{\\text{m}}{\\text{s}}$",
            "$\\times$",
            "0.25s",
            "=",
            "1.75m"
        )
        area.next_to(rect, RIGHT, LARGE_BUFF)
        arrow = Arrow(
            area.get_left(), rect.get_center(), 
            buff = 0,
            color = WHITE
        )
        area.shift(SMALL_BUFF*RIGHT)

        self.play(
            Write(area),
            ShowCreation(arrow)
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [
            area, arrow, 
            v_lines[0], h_lines[0], height_labels[0],
            rect, t_labels
        ])))

    def show_v_dt_for_all_rectangles(self):
        dt_brace_group = VGroup(self.dt_brace, self.dt_label)
        rects_subset = self.rects[10:20]

        last_rect = None
        for rect in rects_subset:
            brace = Brace(rect, LEFT, buff = 0)
            v_t = OldTex("v(t)")
            v_t.next_to(brace, LEFT, SMALL_BUFF)
            anims = [
                rect.set_fill, None, 1,
                dt_brace_group.next_to, rect, DOWN, SMALL_BUFF
            ]
            if last_rect is not None:
                anims += [
                    last_rect.set_fill, None, 0.25,
                    ReplacementTransform(last_brace, brace),
                    ReplacementTransform(last_v_t, v_t),
                ]
            else:
                anims += [
                    GrowFromCenter(brace),
                    Write(v_t)
                ]
            self.play(*anims)
            self.wait()

            last_rect = rect
            last_brace = brace
            last_v_t = v_t

        self.v_t = last_v_t
        self.v_t_brace = last_brace

    def write_integral_symbol(self):
        integral = OldTex(
            "\\int", "^8", "_0", "v(t)", "\\,dt"
        )
        integral.to_corner(UP+RIGHT)
        int_copy = integral.get_part_by_tex("int").copy()
        bounds = list(map(integral.get_part_by_tex, ["0", "8"]))

        sum_word = OldTexText("``Sum''")
        sum_word.next_to(integral, DOWN, MED_LARGE_BUFF, LEFT)
        alt_sum_word = sum_word.copy()
        int_symbol = OldTex("\\int")
        int_symbol.replace(alt_sum_word[1], dim_to_match = 1)
        # CHANGE: a single-string OldTexText keeps its glyphs one level down (submobjects[0]); replace the glyph through set_submobjects
        glyphs = list(alt_sum_word.submobjects[0].submobjects)
        glyphs[1] = int_symbol
        alt_sum_word.submobjects[0].set_submobjects(glyphs)

        self.play(FadeOut(self.dt_example_text))
        self.play(Write(integral.get_part_by_tex("int")))
        self.wait()
        self.play(Transform(int_copy, int_symbol))
        self.play(Write(alt_sum_word), Animation(int_copy))
        self.remove(int_copy)
        self.play(ReplacementTransform(alt_sum_word, sum_word))
        self.wait()

        for bound in bounds:
            self.play(Write(bound))
        self.wait()
        for bound, num in zip(bounds, [0, 8]):
            bound_copy = bound.copy()
            point = self.coords_to_point(num, 0)
            self.play(
                bound_copy.scale, 1.5,
                bound_copy.next_to, point, DOWN, MED_LARGE_BUFF
            )
        self.play(ApplyWave(self.ticks, direction = UP))
        self.wait()

        for mob, tex in (self.v_t, "v(t)"), (self.dt_label, "dt"):
            self.play(ReplacementTransform(
                mob.copy().set_color(YELLOW), 
                integral.get_part_by_tex(tex),
                run_time = 2
            ))
        self.wait()

        self.integral = integral
        self.sum_word = sum_word

    def roles_of_dt(self):
        rects = self.rects
        next_rects = self.rect_list[3]

        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT)
        int_dt = self.integral.get_part_by_tex("dt")
        dt_copy = int_dt.copy()

        self.play(FadeIn(morty))
        self.play(
            morty.change_mode, "raise_right_hand",
            morty.look, UP+RIGHT,
            dt_copy.next_to, morty.get_corner(UP+RIGHT), UP,
            dt_copy.set_color, YELLOW
        )
        self.play(Blink(morty))
        self.play(
            ReplacementTransform(
                dt_copy.copy(), int_dt,
                run_time = 2
            ),
            morty.look_at, int_dt
        )
        self.wait(2)
        self.play(
            ReplacementTransform(dt_copy.copy(), self.dt_label),
            morty.look_at, self.dt_label
        )
        self.play(*[
            ApplyMethod(
                tick.shift, tick.get_height()*UP/2,
                run_time = 2,
                rate_func = squish_rate_func(
                    there_and_back,
                    alpha, alpha+0.2,
                )
            )
            for tick, alpha in zip(
                self.ticks, 
                np.linspace(0, 0.8, len(self.ticks))
            )
        ])
        self.wait()

        #Shrink dt just a bit
        self.play(
            morty.change_mode, "pondering",
            rects.set_fill, None, 0.75,
            *list(map(FadeOut, [
                dt_copy, self.v_t, self.v_t_brace
            ]))
        )
        rects.align_family(next_rects)
        for every_other_rect in rects[::2]:
            every_other_rect.set_fill(opacity = 0)
        self.play(
            self.dt_brace.stretch, 0.5, 0,
            self.dt_brace.move_to, self.dt_brace, LEFT,
            ReplacementTransform(
                rects, next_rects,
                run_time = 2,
                lag_ratio = 0.5
            ),
            Transform(
                self.ticks, self.get_ticks(next_rects),
                run_time = 2,
                lag_ratio = 0.5,
            ),
        )
        self.rects = rects = next_rects
        self.wait()
        self.play(Blink(morty))
        self.play(*[
            ApplyFunction(
                lambda r : r.shift(0.2*UP).set_fill(None, 1),
                rect,
                run_time = 2,
                rate_func = squish_rate_func(
                    there_and_back,
                    alpha, alpha+0.2,
                )
            )
            for rect, alpha in zip(
                rects, 
                np.linspace(0, 0.8, len(rects))
            )
        ]+[
            morty.change_mode, "thinking",
        ])
        self.wait()

        self.morty = morty

    def what_does_sum_approach(self):
        morty = self.morty
        rects = self.rects

        cross = OldTex("\\times")
        cross.replace(self.sum_word, stretch = True)
        cross.set_color(RED)
        brace = Brace(self.integral, DOWN)
        dt_to_0 = brace.get_text("$dt \\to 0$")

        distance_words = OldTexText(
            "Area", "= Distance traveled"
        )
        distance_words.next_to(rects, UP)
        arrow = Arrow(
            distance_words[0].get_bottom(),
            rects.get_center(),
            color = WHITE
        )

        self.play(PiCreatureSays(
            morty, "Why not $\\Sigma$?",
            target_mode = "sassy"
        ))
        self.play(Blink(morty))
        self.wait()
        self.play(Write(cross))
        self.wait()
        self.play(
            RemovePiCreatureBubble(morty, target_mode = "plain"),
            *list(map(FadeOut, [
                cross, self.sum_word, self.ticks,
                self.dt_brace, self.dt_label,
            ]))
        )
        self.play(FadeIn(brace), FadeIn(dt_to_0))
        for new_rects in self.rect_list[4:]:
            rects.align_family(new_rects)
            for every_other_rect in rects[::2]:
                every_other_rect.set_fill(opacity = 0)
            self.play(
                Transform(
                    rects, new_rects, 
                    run_time = 2,
                    lag_ratio = 0.5
                ),
                morty.look_at, rects,
            )
            self.wait()

        self.play(
            Write(distance_words),
            ShowCreation(arrow),
            morty.change_mode, "pondering",
            morty.look_at, distance_words,
        )
        self.wait()
        self.play(Blink(morty))
        self.wait()

        self.area_arrow = arrow

    def label_integral(self):
        words = OldTexText("``Integral of $v(t)$''")
        words.to_edge(UP)
        arrow = Arrow(
            words.get_right(),
            self.integral.get_left()
        )

        self.play(Indicate(self.integral))
        self.play(Write(words, run_time = 2))
        self.play(ShowCreation(arrow))
        self.wait()
        self.play(*[
            ApplyFunction(
                lambda r : r.shift(0.2*UP).set_fill(None, 1),
                rect,
                run_time = 3,
                rate_func = squish_rate_func(
                    there_and_back,
                    alpha, alpha+0.2,
                )
            )
            for rect, alpha in zip(
                self.rects, 
                np.linspace(0, 0.8, len(self.rects))
            )
        ]+[
            Animation(self.area_arrow),
            self.morty.change_mode, "happy",
            self.morty.look_at, self.rects,
        ])
        self.wait()

    #####

    def get_pw_constant_graph(self):
        result = VGroup()
        for left_x in range(8):
            xs = [left_x, left_x+1]
            y = self.v_graph.underlying_function(left_x)
            line = Line(*[
                self.coords_to_point(x, y)
                for x in xs
            ])
            line.set_color(self.v_graph.get_color())
            result.add(line)
        return result

    def get_ticks(self, rects):
        ticks = VGroup(*[
            Line(
                point+self.tick_size*UP/2, 
                point+self.tick_size*DOWN/2
            )
            for t in np.linspace(0, 8, len(rects)+1)
            for point in [self.coords_to_point(t, 0)]
        ])
        ticks.set_color(YELLOW)
        return ticks
