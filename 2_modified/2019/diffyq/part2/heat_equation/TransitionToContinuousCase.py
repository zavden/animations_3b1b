# ==============================================================================
# Scene:      TransitionToContinuousCase
# Source:     videos/_2019/diffyq/part2/heat_equation.py (lines 2339-2687)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part2/shared_constructs.py
#
# Run from this folder:
#     manimgl TransitionToContinuousCase.py TransitionToContinuousCase -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use the Cairo signature of smooth(t, inflection), keeping the one-argument call.
#   - the copy of v_line keeps its updater (become(get_v_line)) and rebuilds its points during TransformFromCopy (different data sizes when interpolating); it starts from a copy without updaters
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import cairo_smooth as smooth


# ----- From _2019/diffyq/part2/shared_constructs.py -----

def temperature_to_color(temp, min_temp=-1, max_temp=1):
    colors = [BLUE, TEAL, GREEN, YELLOW, "#ff0000"]

    alpha = inverse_interpolate(min_temp, max_temp, temp)
    index, sub_alpha = integer_interpolate(
        0, len(colors) - 1, alpha
    )
    return interpolate_color(
        colors[index], colors[index + 1], sub_alpha
    )



# ----- From _2019/diffyq/part2/heat_equation.py -----

class BringTwoRodsTogether(Scene):
    CONFIG = {
        "step_size": 0.05,
        "axes_config": {
            "x_min": -1,
            "x_max": 11,
            "y_min": -10,
            "y_max": 100,
            "y_axis_config": {
                "unit_size": 0.06,
                "tick_frequency": 10,
            },
        },
        "y_labels": range(20, 100, 20),
        "graph_x_min": 0,
        "graph_x_max": 10,
        "midpoint": 5,
        "max_temp": 90,
        "min_temp": 10,
        "wait_time": 30,
        "default_n_rod_pieces": 20,
        "alpha": 1.0,
    }

    def construct(self):
        self.setup_axes()
        self.setup_graph()
        self.setup_clock()

        self.show_rods()
        self.show_equilibration()

    def setup_axes(self):
        axes = Axes(**self.axes_config)
        axes.center().to_edge(UP)

        y_label = axes.get_y_axis_label("\\text{Temperature}")
        y_label.to_edge(UP)
        axes.y_axis.label = y_label
        axes.y_axis.add(y_label)
        axes.y_axis.add_numbers(*self.y_labels)

        self.axes = axes
        self.y_label = y_label

    def setup_graph(self):
        graph = self.axes.get_graph(
            self.initial_function,
            x_min=self.graph_x_min,
            x_max=self.graph_x_max,
            step_size=self.step_size,
            discontinuities=[self.midpoint],
        )
        graph.color_using_background_image("VerticalTempGradient")

        self.graph = graph

    def setup_clock(self):
        clock = Clock()
        clock.set_height(1)
        clock.to_corner(UR)
        clock.shift(MED_LARGE_BUFF * LEFT)

        time_lhs = OldTexText("Time: ")
        time_label = DecimalNumber(
            0, num_decimal_places=2,
        )
        time_rhs = OldTexText("s")
        time_group = VGroup(
            time_lhs,
            time_label,
            # time_rhs
        )
        time_group.arrange(RIGHT, aligned_edge=DOWN)
        time_rhs.shift(SMALL_BUFF * LEFT)
        time_group.next_to(clock, DOWN)

        self.time_group = time_group
        self.time_label = time_label
        self.clock = clock

    def show_rods(self):
        rod1, rod2 = rods = VGroup(
            self.get_rod(0, 5),
            self.get_rod(5, 10),
        )
        rod1.set_color(rod1[0].get_color())
        rod2.set_color(rod2[-1].get_color())

        rods.save_state()
        rods.space_out_submobjects(1.5)
        rods.center()

        labels = VGroup(
            OldTex("90^\\circ"),
            OldTex("10^\\circ"),
        )
        for rod, label in zip(rods, labels):
            label.next_to(rod, DOWN)
            rod.label = label

        self.play(
            FadeIn(rod1, UP),
            Write(rod1.label),
        )
        self.play(
            FadeIn(rod2, DOWN),
            Write(rod2.label)
        )
        self.wait()

        self.rods = rods
        self.rod_labels = labels

    def show_equilibration(self):
        rods = self.rods
        axes = self.axes
        graph = self.graph
        labels = self.rod_labels
        self.play(
            Write(axes),
            rods.restore,
            rods.space_out_submobjects, 1.1,
            FadeIn(self.time_group),
            FadeIn(self.clock),
            *[
                MaintainPositionRelativeTo(
                    rod.label, rod
                )
                for rod in rods
            ],
        )

        br1 = Rectangle(height=0.2, width=1)
        br1.set_stroke(width=0)
        br1.set_fill(BLACK, opacity=1)
        br2 = br1.copy()
        br1.add_updater(lambda b: b.move_to(axes.c2p(0, 90)))
        br1.add_updater(
            lambda b: b.align_to(rods[0].get_right(), LEFT)
        )
        br2.add_updater(lambda b: b.move_to(axes.c2p(0, 10)))
        br2.add_updater(
            lambda b: b.align_to(rods[1].get_left(), RIGHT)
        )

        self.add(graph, br1, br2)
        self.play(
            ShowCreation(graph),
            labels[0].align_to, axes.c2p(0, 87), UP,
            labels[1].align_to, axes.c2p(0, 13), DOWN,
        )
        self.play()
        self.play(
            rods.restore,
            rate_func=rush_into,
        )
        self.remove(br1, br2)

        graph.add_updater(self.update_graph)
        self.time_label.add_updater(
            lambda d, dt: d.increment_value(dt)
        )
        rods.add_updater(self.update_rods)

        self.play(
            self.get_clock_anim(self.wait_time),
            FadeOut(labels)
        )

    #
    def get_clock_anim(self, time, **kwargs):
        config = {
            "run_time": time,
            "hours_passed": time,
        }
        config.update(kwargs)
        return ClockPassesTime(self.clock, **config)

    def initial_function(self, x):
        epsilon = 1e-10
        if x < self.midpoint - epsilon:
            return self.max_temp
        elif x > self.midpoint + epsilon:
            return self.min_temp
        else:
            return (self.min_temp + self.max_temp) / 2

    def update_graph(self, graph, dt, alpha=None, n_mini_steps=500):
        if alpha is None:
            alpha = self.alpha
        points = np.append(
            graph.get_start_anchors(),
            [graph.get_last_point()],
            axis=0,
        )
        for k in range(n_mini_steps):
            y_change = np.zeros(points.shape[0])
            dx = points[1][0] - points[0][0]
            for i in range(len(points)):
                p = points[i]
                lp = points[max(i - 1, 0)]
                rp = points[min(i + 1, len(points) - 1)]
                d2y = (rp[1] - 2 * p[1] + lp[1])

                if (0 < i < len(points) - 1):
                    second_deriv = d2y / (dx**2)
                else:
                    second_deriv = 2 * d2y / (dx**2)
                    # second_deriv = 0

                y_change[i] = alpha * second_deriv * dt / n_mini_steps

            # y_change[0] = y_change[1]
            # y_change[-1] = y_change[-2]
            # y_change[0] = 0
            # y_change[-1] = 0
            # y_change -= np.mean(y_change)
            points[:, 1] += y_change
        graph.set_points_smoothly(points)
        return graph

    def get_second_derivative(self, x, dx=0.001):
        graph = self.graph
        x_min = self.graph_x_min
        x_max = self.graph_x_max

        ly, y, ry = [
            graph.point_from_proportion(
                inverse_interpolate(x_min, x_max, alt_x)
            )[1]
            for alt_x in (x - dx, x, x + dx)
        ]

        # At the boundary, don't return the second deriv,
        # but instead something matching the Neumann
        # boundary condition.
        if x == x_max:
            return (ly - y) / dx
        elif x == x_min:
            return (ry - y) / dx
        else:
            d2y = ry - 2 * y + ly
            return d2y / (dx**2)

    def get_rod(self, x_min, x_max, n_pieces=None):
        if n_pieces is None:
            n_pieces = self.default_n_rod_pieces
        axes = self.axes
        line = Line(axes.c2p(x_min, 0), axes.c2p(x_max, 0))
        rod = VGroup(*[
            Square()
            for n in range(n_pieces)
        ])
        rod.arrange(RIGHT, buff=0)
        rod.match_width(line)
        rod.set_height(0.2, stretch=True)
        rod.move_to(axes.c2p(x_min, 0), LEFT)
        rod.set_fill(opacity=1)
        rod.set_stroke(width=1)
        rod.set_sheen_direction(RIGHT)
        self.color_rod_by_graph(rod)
        return rod

    def update_rods(self, rods):
        for rod in rods:
            self.color_rod_by_graph(rod)

    def color_rod_by_graph(self, rod):
        for piece in rod:
            piece.set_color(color=[
                self.rod_point_to_color(piece.get_left()),
                self.rod_point_to_color(piece.get_right()),
            ])

    def rod_point_to_graph_y(self, point):
        axes = self.axes
        x = axes.x_axis.p2n(point)

        graph = self.graph
        alpha = inverse_interpolate(
            self.graph_x_min,
            self.graph_x_max,
            x,
        )
        return axes.y_axis.p2n(
            graph.point_from_proportion(alpha)
        )

    def y_to_color(self, y):
        y_max = self.max_temp
        y_min = self.min_temp
        alpha = inverse_interpolate(y_min, y_max, y)
        return temperature_to_color(interpolate(-0.8, 0.8, alpha))

    def rod_point_to_color(self, point):
        return self.y_to_color(
            self.rod_point_to_graph_y(point)
        )


class ShowEvolvingTempGraphWithArrows(BringTwoRodsTogether):
    CONFIG = {
        "alpha": 0.1,
        "arrow_xs": np.linspace(0, 10, 22)[1:-1],
        "arrow_scale_factor": 0.5,
        "max_magnitude": 1.5,
        "wait_time": 30,
        "freq_amplitude_pairs": [
            (1, 0.5),
            (2, 1),
            (3, 0.5),
            (4, 0.3),
            (5, 0.3),
            (7, 0.2),
            (21, 0.1),
            (41, 0.05),
        ],
    }

    def construct(self):
        self.add_axes()
        self.add_graph()
        self.add_clock()
        self.add_rod()
        self.add_arrows()
        self.initialize_updaters()
        self.let_play()

    def add_axes(self):
        self.setup_axes()
        self.add(self.axes)

    def add_graph(self):
        self.setup_graph()
        self.add(self.graph)

    def add_clock(self):
        self.setup_clock()
        self.add(self.clock)
        self.add(self.time_label)
        self.time_label.next_to(self.clock, DOWN)

    def add_rod(self):
        rod = self.rod = self.get_rod(
            self.graph_x_min,
            self.graph_x_max,
        )
        self.add(rod)

    def add_arrows(self):
        graph = self.graph
        x_min = self.graph_x_min
        x_max = self.graph_x_max

        xs = self.arrow_xs
        arrows = VGroup(*[Vector(DOWN) for x in xs])
        asf = self.arrow_scale_factor

        def update_arrows(arrows):
            for x, arrow in zip(xs, arrows):
                d2y_dx2 = self.get_second_derivative(x)
                mag = asf * np.sign(d2y_dx2) * abs(d2y_dx2)
                mag = np.clip(
                    mag,
                    -self.max_magnitude,
                    self.max_magnitude,
                )
                arrow.put_start_and_end_on(
                    ORIGIN, mag * UP
                )
                point = graph.point_from_proportion(
                    inverse_interpolate(x_min, x_max, x)
                )
                arrow.shift(point - arrow.get_start())
                arrow.set_color(
                    self.rod_point_to_color(point)
                )

        arrows.add_updater(update_arrows)

        self.add(arrows)
        self.arrows = arrows

    def initialize_updaters(self):
        if hasattr(self, "graph"):
            self.graph.add_updater(self.update_graph)
        if hasattr(self, "rod"):
            self.rod.add_updater(self.color_rod_by_graph)
        if hasattr(self, "time_label"):
            self.time_label.add_updater(
                lambda d, dt: d.increment_value(dt)
            )

    def let_play(self):
        self.run_clock(self.wait_time)

    def run_clock(self, time):
        self.play(
            ClockPassesTime(
                self.clock,
                run_time=time,
                hours_passed=time,
            ),
        )

    #
    def temp_func(self, x, t):
        new_x = TAU * x / 10
        return 50 + 20 * np.sum([
            amp * np.sin(freq * new_x) *
            np.exp(-(self.alpha * freq**2) * t)
            for freq, amp in self.freq_amplitude_pairs
        ])

    def initial_function(self, x, time=0):
        return self.temp_func(x, 0)


class DiscreteSetup(ShowEvolvingTempGraphWithArrows):
    CONFIG = {
        "step_size": 1,
        "rod_piece_size_ratio": 1 / 3,
        "dashed_line_stroke_opacity": 1.0,
        "dot_radius": DEFAULT_DOT_RADIUS,
        "freq_amplitude_pairs": [
            (1, 0.5),
            (2, 1),
            (3, 0.5),
            (4, 0.3),
            (5, 0.3),
            (7, 0.2),
            (21, 0.1),
            # (41, 0.05),
        ],
    }

    def construct(self):
        self.add_axes()
        self.add_graph()
        self.discretize()
        self.let_time_pass()
        self.show_nieghbor_rule()
        self.focus_on_three_points()
        self.show_difference_formula()
        self.gut_check_new_interpretation()
        self.write_second_difference()
        self.emphasize_final_expression()

    def add_axes(self):
        super().add_axes()
        self.axes.shift(MED_SMALL_BUFF * LEFT)

    def add_graph(self):
        points = self.get_points(time=0)
        graph = VMobject()
        graph.set_points_smoothly(points)
        graph.color_using_background_image("VerticalTempGradient")

        self.add(graph)

        self.graph = graph
        self.points = points

    def discretize(self):
        axes = self.axes
        x_axis = axes.x_axis
        graph = self.graph

        piecewise_graph = CurvesAsSubmobjects(graph)
        dots = self.get_dots()
        v_lines = VGroup(*map(self.get_v_line, dots))

        rod_pieces = VGroup()
        for x in self.get_sample_inputs():
            piece = Line(LEFT, RIGHT)
            piece.set_width(
                self.step_size * self.rod_piece_size_ratio
            )
            piece.move_to(axes.c2p(x, 0))
            piece.set_color(
                self.rod_point_to_color(piece.get_center())
            )
            rod_pieces.add(piece)

        word = OldTexText("Discrete version")
        word.scale(1.5)
        word.next_to(x_axis, UP)
        word.set_stroke(BLACK, 3, background=True)

        self.remove(graph)
        self.play(
            ReplacementTransform(
                piecewise_graph, dots,
            ),
            Write(word, run_time=1)
        )
        self.add(v_lines, word)
        self.play(
            x_axis.fade, 0.8,
            TransformFromCopy(
                x_axis.tick_marks[1:],
                rod_pieces,
            ),
            LaggedStartMap(ShowCreation, v_lines)
        )
        self.play(FadeOut(word))
        self.wait()

        self.rod_pieces = rod_pieces
        self.dots = dots
        self.v_lines = v_lines

    def let_time_pass(self):
        dots = self.dots

        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t_tracker)

        self.add_clock()
        self.time_label.next_to(self.clock, DOWN)
        self.time_label.add_updater(
            lambda m: m.set_value(t_tracker.get_value())
        )
        dots.add_updater(lambda d: d.become(
            self.get_dots(t_tracker.get_value())
        ))
        run_time = 5
        self.play(
            ClockPassesTime(
                self.clock,
                run_time=run_time,
                hours_passed=run_time,
            ),
        )
        t_tracker.clear_updaters()
        t_tracker.set_value(run_time)
        self.wait()
        self.play(
            t_tracker.set_value, 0,
            FadeOut(self.clock),
            FadeOut(self.time_label),
        )
        self.remove(t_tracker)
        dots.clear_updaters()

    def show_nieghbor_rule(self):
        dots = self.dots
        rod_pieces = self.rod_pieces
        index = self.index = 2

        p1, p2, p3 = rod_pieces[index:index + 3]
        d1, d2, d3 = dots[index:index + 3]
        point_label = OldTexText("Point")
        neighbors_label = OldTexText("Neighbors")
        words = VGroup(point_label, neighbors_label)
        for word in words:
            word.scale(0.7)
            word.add_background_rectangle()

        point_label.next_to(p2, DOWN)
        neighbors_label.next_to(p2, UP, buff=1)
        bottom = neighbors_label.get_bottom()
        kw = {
            "buff": 0.1,
            "stroke_width": 2,
            "tip_length": 0.15
        }
        arrows = VGroup(
            Arrow(bottom, p1.get_center(), **kw),
            Arrow(bottom, p3.get_center(), **kw),
        )
        arrows.set_color(WHITE)

        dot = Dot()
        dot.set_fill(GREY, opacity=0.2)
        dot.replace(p2)
        dot.scale(3)

        self.play(
            dot.scale, 0,
            dot.set_opacity, 0,
            FadeIn(point_label, DOWN)
        )
        self.play(
            FadeIn(neighbors_label, DOWN),
            *map(GrowArrow, arrows)
        )
        self.wait()

        # Let d2 change
        self.play(
            d1.set_y, 3,
            d3.set_y, 3,
        )

        def get_v():
            return 0.25 * np.sum([
                d1.get_y(),
                -2 * d2.get_y(),
                + d3.get_y(),
            ])
        v_vect_fader = ValueTracker(0)
        v_vect = always_redraw(
            lambda: Vector(
                get_v() * UP,
                color=temperature_to_color(
                    get_v(), -2, 2,
                ),
            ).shift(d2.get_center()).set_opacity(
                v_vect_fader.get_value(),
            )
        )
        d2.add_updater(
            lambda d, dt: d.shift(
                get_v() * dt * UP,
            )
        )

        self.add(v_vect)
        self.play(v_vect_fader.set_value, 1)
        self.wait(3)
        self.play(
            d1.set_y, 0,
            d3.set_y, 0,
        )
        self.wait(4)
        self.play(FadeOut(VGroup(
            point_label,
            neighbors_label,
            arrows
        )))

        self.v_vect = v_vect
        self.example_pieces = VGroup(p1, p2, p3)
        self.example_dots = VGroup(d1, d2, d3)

    def focus_on_three_points(self):
        dots = self.example_dots
        d1, d2, d3 = dots
        pieces = self.example_pieces
        y_axis = self.axes.y_axis

        x_labels, T_labels = [
            VGroup(*[
                OldTex("{}_{}".format(s, i))
                for i in [1, 2, 3]
            ]).scale(0.8)
            for s in ("x", "T")
        ]
        for xl, piece in zip(x_labels, pieces):
            xl.next_to(piece, DOWN)
            xl.add_background_rectangle()
        for Tl, dot in zip(T_labels, dots):
            Tl.dot = dot
            Tl.add_updater(lambda m: m.next_to(
                m.dot, RIGHT, SMALL_BUFF
            ))
            Tl.add_background_rectangle()
        T1, T2, T3 = T_labels

        d2.movement_updater = d2.get_updaters()[0]
        dots.clear_updaters()
        self.remove(self.v_vect)

        self.play(
            ShowCreationThenFadeAround(pieces),
            FadeOut(self.dots[:self.index]),
            FadeOut(self.v_lines[:self.index]),
            FadeOut(self.rod_pieces[:self.index]),
            FadeOut(self.dots[self.index + 3:]),
            FadeOut(self.v_lines[self.index + 3:]),
            FadeOut(self.rod_pieces[self.index + 3:]),
        )
        self.play(LaggedStartMap(
            FadeInFrom, x_labels,
            lambda m: (m, LEFT),
            lag_ratio=0.3,
            run_time=2,
        ))
        self.play(
            d3.set_y, 1,
            d2.set_y, 0.25,
            d1.set_y, 0,
        )
        self.wait()
        self.play(LaggedStart(*[
            TransformFromCopy(xl, Tl)
            for xl, Tl in zip(x_labels, T_labels)
        ], lag_ratio=0.3, run_time=2))
        self.wait()

        # Show lines
        h_lines = VGroup(*map(self.get_h_line, dots))
        hl1, hl2, hl3 = h_lines

        average_pointer = ArrowTip(
            start_angle=0,
            length=0.2,
        )
        average_pointer.set_color(YELLOW)
        average_pointer.stretch(0.25, 1)
        average_pointer.add_updater(
            lambda m: m.move_to(
                0.5 * (hl1.get_start() + hl3.get_start()),
                RIGHT
            )
        )
        average_arrows = always_redraw(lambda: VGroup(*[
            Arrow(
                hl.get_start(),
                average_pointer.get_right(),
                color=WHITE,
                buff=0.0,
            )
            for hl in [hl1, hl3]
        ]))
        average_label = OldTex(
            "{T_1", "+", "T_3", "\\over", "2}"
        )
        average_label.scale(0.5)
        average_label.add_updater(lambda m: m.next_to(
            average_pointer, LEFT, SMALL_BUFF
        ))

        average_rect = SurroundingRectangle(average_label)
        average_rect.add_updater(
            lambda m: m.move_to(average_label)
        )
        average_words = OldTexText("Neighbor\\\\average")
        average_words.match_width(average_rect)
        average_words.match_color(average_rect)
        average_words.add_updater(
            lambda m: m.next_to(average_rect, UP, SMALL_BUFF)
        )

        mini_T1 = average_label.get_part_by_tex("T_1")
        mini_T3 = average_label.get_part_by_tex("T_3")
        for mini, line in (mini_T1, hl1), (mini_T3, hl3):
            mini.save_state()
            mini.next_to(line, LEFT, SMALL_BUFF)

        self.add(hl1, hl3, T_labels)
        y_axis.remove(y_axis.numbers)
        self.play(
            GrowFromPoint(hl1, hl1.get_end()),
            GrowFromPoint(hl3, hl3.get_end()),
            TransformFromCopy(
                T1, mini_T1,
            ),
            TransformFromCopy(
                T3, mini_T3,
            ),
            FadeOut(y_axis.numbers),
            y_axis.set_stroke, {"width": 1},
        )
        self.play(
            FadeIn(average_pointer),
            Restore(mini_T1),
            Restore(mini_T3),
            FadeIn(average_label[1]),
            FadeIn(average_label[3:]),
            *map(GrowArrow, average_arrows)
        )
        self.add(average_arrows, average_label)
        self.play(
            ShowCreation(average_rect),
            FadeIn(average_words),
        )
        self.play(
            GrowFromPoint(hl2, hl2.get_end())
        )
        self.wait()

        # Show formula
        formula = OldTex(
            "\\left(",
            "{T_1", "+", "T_3", "\\over", "2}",
            "-", "T_2",
            "\\right)"
        )
        formula.to_corner(UR, buff=MED_LARGE_BUFF)
        formula.shift(1.7 * LEFT)
        brace = Brace(formula, DOWN)
        diff_value = DecimalNumber(include_sign=True)
        diff_value.add_updater(lambda m: m.set_value(
            y_axis.p2n(average_pointer.get_right()) -
            y_axis.p2n(d2.get_center())
        ))
        diff_value.next_to(brace, DOWN)

        self.play(
            ReplacementTransform(
                average_label.deepcopy(),
                formula[1:1 + len(average_label)]
            ),
            TransformFromCopy(T2, formula[-2]),
            FadeIn(formula[-3]),
            FadeIn(formula[-1]),
            FadeIn(formula[0]),
            GrowFromCenter(brace),
            FadeIn(diff_value)
        )
        self.wait()

        # Changes
        self.play(FadeIn(self.v_vect))
        d2.add_updater(d2.movement_updater)
        self.wait(5)

        self.play(
            d3.set_y, 3,
            d1.set_y, 2.5,
            d2.set_y, -2,
        )
        self.wait(5)
        self.play(
            d3.set_y, 1,
            d1.set_y, -1,
        )
        self.wait(8)

        # Show derivative
        lhs = OldTex(
            "{dT_2", "\\over", "dt}", "=", "\\alpha"
        )
        dt = lhs.get_part_by_tex("dt")
        alpha = lhs.get_part_by_tex("\\alpha")
        lhs.next_to(formula, LEFT, SMALL_BUFF)

        self.play(Write(lhs))
        self.play(ShowCreationThenFadeAround(dt))
        self.wait()
        self.play(ShowCreationThenFadeAround(alpha))
        self.wait()
        self.play(
            FadeOut(brace),
            FadeOut(diff_value),
        )

        self.lhs = lhs
        self.rhs = formula

    def show_difference_formula(self):
        lhs = self.lhs
        rhs = self.rhs
        d1, d2, d3 = self.example_dots

        new_rhs = OldTex(
            "=",
            "{\\alpha", "\\over", "2}",
            "\\left(",
            "(", "T_3", "-", "T_2", ")",
            "-",
            "(", "T_2", "-", "T_1", ")",
            "\\right)"
        )
        big_parens = VGroup(
            new_rhs.get_part_by_tex("\\left("),
            new_rhs.get_part_by_tex("\\right)"),
        )
        for paren in big_parens:
            paren.scale(2)
        new_rhs.next_to(rhs, DOWN)
        new_rhs.align_to(lhs.get_part_by_tex("="), LEFT)

        def p2p_anim(mob1, mob2, tex, index=0):
            return TransformFromCopy(
                mob1.get_parts_by_tex(tex)[index],
                mob2.get_parts_by_tex(tex)[index],
            )

        self.play(
            p2p_anim(lhs, new_rhs, "="),
            p2p_anim(rhs, new_rhs, "\\left("),
            p2p_anim(rhs, new_rhs, "\\right)"),
            p2p_anim(lhs, new_rhs, "\\alpha"),
            p2p_anim(rhs, new_rhs, "\\over"),
            p2p_anim(rhs, new_rhs, "2"),
        )
        self.play(
            p2p_anim(rhs, new_rhs, "T_3"),
            p2p_anim(rhs, new_rhs, "-"),
            p2p_anim(rhs, new_rhs, "T_2"),
            FadeIn(new_rhs.get_parts_by_tex("(")[1]),
            FadeIn(new_rhs.get_parts_by_tex(")")[0]),
        )
        self.play(
            p2p_anim(rhs, new_rhs, "T_2", -1),
            p2p_anim(rhs, new_rhs, "-", -1),
            p2p_anim(rhs, new_rhs, "T_1"),
            FadeIn(new_rhs.get_parts_by_tex("-")[1]),
            FadeIn(new_rhs.get_parts_by_tex("(")[2]),
            FadeIn(new_rhs.get_parts_by_tex(")")[1]),
        )
        self.wait()

        self.rhs2 = new_rhs

        # Show deltas
        T1_index = new_rhs.index_of_part_by_tex("T_1")
        T3_index = new_rhs.index_of_part_by_tex("T_3")
        diff1 = new_rhs[T1_index - 2:T1_index + 1]
        diff2 = new_rhs[T3_index:T3_index + 3]
        brace1 = Brace(diff1, DOWN, buff=SMALL_BUFF)
        brace2 = Brace(diff2, DOWN, buff=SMALL_BUFF)
        delta_T1 = OldTex("\\Delta T_1")
        delta_T1.next_to(brace1, DOWN, SMALL_BUFF)
        delta_T2 = OldTex("\\Delta T_2")
        delta_T2.next_to(brace2, DOWN, SMALL_BUFF)
        minus = OldTex("-")
        minus.move_to(Line(
            delta_T1.get_right(),
            delta_T2.get_left(),
        ))
        braces = VGroup(brace1, brace2)
        deltas = VGroup(delta_T1, delta_T2)

        kw = {
            "direction": LEFT,
            "buff": SMALL_BUFF,
            "min_num_quads": 2,
        }
        lil_brace1 = always_redraw(lambda: Brace(
            Line(d1.get_left(), d2.get_left()), **kw
        ))
        lil_brace2 = always_redraw(lambda: Brace(
            Line(d2.get_left(), d3.get_left()), **kw
        ))
        lil_braces = VGroup(lil_brace1, lil_brace2)
        lil_delta_T1 = delta_T1.copy()
        lil_delta_T2 = delta_T2.copy()
        lil_deltas = VGroup(lil_delta_T1, lil_delta_T2)
        for brace, delta in zip(lil_braces, lil_deltas):
            delta.brace = brace
            delta.add_updater(lambda d: d.next_to(
                d.brace, LEFT, SMALL_BUFF,
            ))

        delta_T1.set_color(BLUE)
        lil_delta_T1.set_color(BLUE)
        delta_T2.set_color(RED)
        lil_delta_T2.set_color(RED)

        double_difference_brace = Brace(deltas, DOWN)
        double_difference_words = OldTexText(
            "Difference of differences"
        )
        double_difference_words.next_to(
            double_difference_brace, DOWN
        )

        self.play(
            GrowFromCenter(brace1),
            GrowFromCenter(lil_brace1),
            FadeIn(delta_T1),
            FadeIn(lil_delta_T1),
        )
        self.wait()
        self.play(
            GrowFromCenter(brace2),
            GrowFromCenter(lil_brace2),
            FadeIn(delta_T2),
            FadeIn(lil_delta_T2),
        )
        self.wait()
        self.play(
            Write(minus),
            GrowFromCenter(double_difference_brace),
            Write(double_difference_words),
        )
        self.wait()

        self.braces = braces
        self.deltas = deltas
        self.delta_minus = minus
        self.lil_braces = lil_braces
        self.lil_deltas = lil_deltas
        self.double_difference_brace = double_difference_brace
        self.double_difference_words = double_difference_words

    def gut_check_new_interpretation(self):
        lil_deltas = self.lil_deltas
        d1, d2, d3 = self.example_dots

        self.play(ShowCreationThenFadeAround(lil_deltas[0]))
        self.play(ShowCreationThenFadeAround(lil_deltas[1]))
        self.wait()
        self.play(
            d2.shift, MED_SMALL_BUFF * UP,
            rate_func=there_and_back,
        )
        self.wait()
        self.play(
            d3.set_y, 3,
            d1.set_y, -0.5,
        )
        self.wait(5)
        self.play(
            d3.set_y, 1.5,
            d1.set_y, -2,
        )
        self.wait(5)

    def write_second_difference(self):
        dd_word = self.double_difference_words

        delta_delta = OldTex("\\Delta \\Delta T_1")
        delta_delta.set_color(MAROON_B)

        delta_delta.move_to(dd_word, UP)

        second_difference_word = OldTexText(
            "``Second difference''"
        )
        second_difference_word.next_to(delta_delta, DOWN)

        self.play(
            FadeOut(dd_word, UP),
            FadeIn(delta_delta, UP),
        )
        self.wait()
        self.play(
            Write(second_difference_word),
        )
        self.wait()

        # Random play
        d1, d2, d3 = self.example_dots
        self.play(
            d3.set_y, 3,
            d1.set_y, -0.5,
        )
        self.wait(5)
        self.play(
            d3.set_y, 1.5,
            d1.set_y, -2,
        )
        self.wait(5)

        self.delta_delta = delta_delta
        self.second_difference_word = second_difference_word

    def emphasize_final_expression(self):
        lhs = self.lhs
        rhs = self.rhs
        rhs2 = self.rhs2
        old_dd = self.delta_delta
        dd = old_dd.copy()
        old_ao2 = rhs2[1:4]
        ao2 = old_ao2.copy()

        new_lhs = lhs[:-1]
        full_rhs = VGroup(
            lhs[-1],
            lhs[-2].copy(),
            rhs,
            rhs2,
            self.braces,
            self.deltas,
            self.delta_minus,
            self.double_difference_brace,
            old_dd,
            self.second_difference_word,
        )
        new_rhs = VGroup(ao2, dd)
        new_rhs.arrange(RIGHT, buff=SMALL_BUFF)
        new_rhs.next_to(new_lhs, RIGHT)

        self.play(
            full_rhs.to_edge, DOWN, {"buff": LARGE_BUFF},
        )
        self.play(
            TransformFromCopy(old_ao2, ao2),
            TransformFromCopy(old_dd, dd),
        )
        self.play(
            ShowCreationThenFadeAround(
                VGroup(new_lhs, new_rhs)
            )
        )
        self.wait()

    #
    def get_sample_inputs(self):
        return np.arange(
            self.graph_x_min,
            self.graph_x_max + self.step_size,
            self.step_size,
        )

    def get_points(self, time=0):
        return [
            self.axes.c2p(x, self.temp_func(x, t=time))
            for x in self.get_sample_inputs()
        ]

    def get_dots(self, time=0):
        points = self.get_points(time)
        dots = VGroup(*[
            Dot(
                point,
                radius=self.dot_radius
            )
            for point in points
        ])
        dots.color_using_background_image("VerticalTempGradient")
        return dots

    def get_dot_dashed_line(self, dot, index, color=False):
        direction = np.zeros(3)
        direction[index] = -1

        def get_line():
            p1 = dot.get_edge_center(direction)
            p0 = np.array(p1)
            p0[index] = self.axes.c2p(0, 0)[index]
            result = DashedLine(
                p0, p1,
                stroke_width=2,
                color=WHITE,
                stroke_opacity=self.dashed_line_stroke_opacity,
            )
            if color:
                result.color_using_background_image(
                    "VerticalTempGradient"
                )
            return result
        return always_redraw(get_line)

    def get_h_line(self, dot):
        return self.get_dot_dashed_line(dot, 0, True)

    def get_v_line(self, dot):
        return self.get_dot_dashed_line(dot, 1)


class TransitionToContinuousCase(DiscreteSetup):
    CONFIG = {
        "step_size": 0.1,
        "tangent_line_length": 3,
        "wait_time": 30,
    }

    def construct(self):
        self.add_axes()
        self.add_graph()
        self.show_temperature_difference()
        self.show_second_derivative()
        self.show_curvature_examples()
        self.show_time_changes()

    def add_graph(self):
        self.setup_graph()
        self.play(
            ShowCreation(
                self.graph,
                run_time=3,
            )
        )
        self.wait()

    def show_temperature_difference(self):
        x_tracker = ValueTracker(2)
        dx_tracker = ValueTracker(1)

        line_group = self.get_line_group(
            x_tracker,
            dx_tracker,
        )
        dx_line, dT_line, tan_line, dx_sym, dT_sym = line_group
        tan_line.set_stroke(width=0)

        brace = Brace(dx_line, UP)
        fixed_distance = OldTexText("Fixed\\\\distance")
        fixed_distance.scale(0.7)
        fixed_distance.next_to(brace, UP)
        delta_T = OldTex("\\Delta T")
        delta_T.move_to(dT_sym, LEFT)

        self.play(
            ShowCreation(VGroup(dx_line, dT_line)),
            FadeIn(delta_T, LEFT)
        )
        self.play(
            GrowFromCenter(brace),
            FadeInFromDown(fixed_distance),
        )
        self.wait()
        self.play(
            FadeOut(delta_T, UP),
            FadeIn(dT_sym, DOWN),
            FadeOut(brace, UP),
            FadeOut(fixed_distance, UP),
            FadeIn(dx_sym, DOWN),
        )
        self.add(line_group)
        self.play(
            dx_tracker.set_value, 0.01,
            run_time=5
        )
        self.wait()
        self.play(
            dx_tracker.set_value, 0.3,
        )

        # Show rate of change
        to_zero = OldTex("\\rightarrow 0")
        to_zero.match_height(dT_sym)
        to_zero.next_to(dT_sym, buff=SMALL_BUFF)

        ratio = OldTex(
            "{\\partial T", "\\over", "\\partial x}"
        )
        ratio[0].match_style(dT_sym)
        ratio.to_edge(UP)

        self.play(ShowCreationThenFadeAround(
            dT_sym,
            surrounding_rectangle_config={
                "buff": 0.05,
                "stroke_width": 1,
            }
        ))
        self.play(GrowFromPoint(to_zero, dT_sym.get_right()))
        self.wait()
        self.play(
            TransformFromCopy(
                dT_sym,
                ratio.get_part_by_tex("\\partial T")
            ),
            TransformFromCopy(
                dx_sym,
                ratio.get_part_by_tex("\\partial x")
            ),
            Write(ratio.get_part_by_tex("\\over"))
        )
        self.play(
            ShowCreation(
                tan_line.copy().set_stroke(width=2),
                remover=True
            ),
            FadeOut(to_zero),
        )
        tan_line.set_stroke(width=2)
        self.wait()

        # Look at neighbors
        x0 = x_tracker.get_value()
        dx = dx_tracker.get_value()
        v_line, lv_line, rv_line = v_lines = VGroup(*[
            self.get_v_line(x)
            for x in [x0, x0 - dx, x0 + dx]
        ])
        v_lines[1:].set_color(BLUE)

        self.play(ShowCreation(v_line))
        self.play(
            TransformFromCopy(v_line, lv_line),
            TransformFromCopy(v_line, rv_line),
        )
        self.wait()
        self.play(
            FadeOut(v_lines[1:]),
            ApplyMethod(
                dx_tracker.set_value, 0.01,
                run_time=2
            ),
        )

        self.line_group = line_group
        self.deriv = ratio
        self.x_tracker = x_tracker
        self.dx_tracker = dx_tracker
        self.v_line = v_line

    def show_second_derivative(self):
        x_tracker = self.x_tracker
        deriv = self.deriv
        v_line = self.v_line

        deriv_of_deriv = OldTex(
            "{\\partial",
            "\\left(",
            "{\\partial T", "\\over", "\\partial x}",
            "\\right)",
            "\\over",
            "\\partial x}"
        )
        deriv_of_deriv.set_color_by_tex("\\partial T", RED)

        deriv_of_deriv.to_edge(UP)
        dT_index = deriv_of_deriv.index_of_part_by_tex("\\partial T")
        inner_deriv = deriv_of_deriv[dT_index:dT_index + 3]

        self.play(
            ReplacementTransform(deriv, inner_deriv),
            Write(VGroup(*filter(
                lambda m: m not in inner_deriv,
                deriv_of_deriv,
            )))
        )
        v_line.add_updater(lambda m: m.become(
            self.get_v_line(x_tracker.get_value())
        ))
        for change in [-0.1, 0.1]:
            self.play(
                x_tracker.increment_value, change,
                run_time=3
            )

        # Write second deriv
        second_deriv = OldTex(
            "{\\partial^2 T", "\\over", "\\partial x^2}"
        )
        second_deriv[0].set_color(RED)
        eq = OldTex("=")
        eq.next_to(deriv_of_deriv, RIGHT)
        second_deriv.next_to(eq, RIGHT)
        second_deriv.align_to(deriv_of_deriv, DOWN)
        eq.match_y(second_deriv.get_part_by_tex("\\over"))

        self.play(Write(eq))
        self.play(
            TransformFromCopy(
                deriv_of_deriv.get_parts_by_tex("\\partial")[:2],
                second_deriv.get_parts_by_tex("\\partial^2 T"),
            ),
        )
        self.play(
            Write(second_deriv.get_part_by_tex("\\over")),
            TransformFromCopy(
                deriv_of_deriv.get_parts_by_tex("\\partial x"),
                second_deriv.get_parts_by_tex("\\partial x"),
            ),
        )
        self.wait()

    def show_curvature_examples(self):
        x_tracker = self.x_tracker
        v_line = self.v_line
        line_group = self.line_group

        x_tracker.set_value(3.6)
        self.wait()
        self.play(
            x_tracker.set_value, 3.8,
            run_time=4,
        )
        self.wait()
        x_tracker.set_value(6.2)
        self.wait()
        self.play(
            x_tracker.set_value, 6.4,
            run_time=4,
        )
        self.wait()

        #
        dx = 0.2
        neighbor_lines = always_redraw(lambda: VGroup(*[
            self.get_v_line(
                x_tracker.get_value() + u * dx,
                line_class=Line,
            )
            for u in [-1, 1]
        ]))
        neighbor_lines.set_color(BLUE)

        self.play(FadeOut(line_group))
        self.play(*[
            # CHANGE: the copy of v_line keeps its updater (become(get_v_line)) and rebuilds its points during TransformFromCopy (different data sizes when interpolating); it starts from a copy without updaters
            TransformFromCopy(v_line.copy().clear_updaters(), nl)
            for nl in neighbor_lines
        ])
        self.add(neighbor_lines)
        self.play(
            x_tracker.set_value, 5,
            run_time=5,
            rate_func=lambda t: smooth(t, 3)
        )
        v_line.clear_updaters()
        self.play(
            FadeOut(v_line),
            FadeOut(neighbor_lines),
        )
        self.wait()

    def show_time_changes(self):
        self.setup_clock()
        graph = self.graph

        time_label = self.time_label
        clock = self.clock
        time_label.next_to(clock, DOWN)

        graph.add_updater(self.update_graph)
        time_label.add_updater(
            lambda d, dt: d.increment_value(dt)
        )

        self.add(time_label)
        self.add_arrows()
        self.play(
            ClockPassesTime(
                clock,
                run_time=self.wait_time,
                hours_passed=self.wait_time,
            ),
        )

    #
    def get_v_line(self, x, line_class=DashedLine, stroke_width=2):
        axes = self.axes
        graph = self.graph
        line = line_class(
            axes.c2p(x, 0),
            graph.point_from_proportion(
                inverse_interpolate(
                    self.graph_x_min,
                    self.graph_x_max,
                    x,
                )
            ),
            stroke_width=stroke_width,
        )
        return line

    def get_line_group(self,
                       x_tracker,
                       dx_tracker,
                       dx_tex="\\partial x",
                       dT_tex="\\partial T",
                       max_sym_width=0.5,
                       ):
        graph = self.graph
        get_x = x_tracker.get_value
        get_dx = dx_tracker.get_value

        dx_line = Line(color=WHITE)
        dT_line = Line(color=RED)
        tan_line = Line(color=WHITE)
        lines = VGroup(dx_line, dT_line, tan_line)
        lines.set_stroke(width=2)
        dx_sym = OldTex(dx_tex)
        dT_sym = OldTex(dT_tex)
        dT_sym.match_color(dT_line)
        syms = VGroup(dx_sym, dT_sym)

        group = VGroup(*lines, *syms)

        def update_group(group):
            dxl, dTl, tanl, dxs, dTs = group
            x = get_x()
            dx = get_dx()
            p0, p2 = [
                graph.point_from_proportion(
                    inverse_interpolate(
                        self.graph_x_min,
                        self.graph_x_max,
                        x
                    )
                )
                for x in [x, x + dx]
            ]
            p1 = np.array([p2[0], *p0[1:]])
            dxl.put_start_and_end_on(p0, p1)
            dTl.put_start_and_end_on(p1, p2)
            tanl.put_start_and_end_on(p0, p2)
            tanl.scale(
                self.tangent_line_length /
                tanl.get_length()
            )
            dxs.match_width(dxl)
            dTs.set_height(0.7 * dTl.get_height())
            for sym in dxs, dTs:
                if sym.get_width() > max_sym_width:
                    sym.set_width(max_sym_width)
            dxs.next_to(
                dxl, -dTl.get_vector(), SMALL_BUFF,
            )
            dTs.next_to(
                dTl, dxl.get_vector(), SMALL_BUFF,
            )

        group.add_updater(update_group)
        return group
