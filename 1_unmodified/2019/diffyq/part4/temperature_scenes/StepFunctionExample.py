# ==============================================================================
# Scene:      StepFunctionExample
# Source:     videos/_2019/diffyq/part4/temperature_scenes.py (lines 6-238)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part2/heat_equation.py, _2019/diffyq/part2/shared_constructs.py, _2019/diffyq/part3/staging.py
#
# Run from this folder:
#     manimgl StepFunctionExample.py StepFunctionExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


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



# ----- From _2019/diffyq/part3/staging.py -----

class FourierSeriesIllustraiton(Scene):
    CONFIG = {
        "n_range": range(1, 31, 2),
        "axes_config": {
            "axis_config": {
                "include_tip": False,
            },
            "x_axis_config": {
                "tick_frequency": 1 / 4,
                "unit_size": 4,
            },
            "x_min": 0,
            "x_max": 1,
            "y_min": -1,
            "y_max": 1,
        },
        "colors": [BLUE, GREEN, RED, YELLOW, PINK],
    }

    def construct(self):
        aaa_group = self.get_axes_arrow_axes()
        aaa_group.shift(2 * UP)
        aaa_group.shift_onto_screen()
        axes1, arrow, axes2 = aaa_group

        axes2.add(self.get_target_func_graph(axes2))

        sine_graphs = self.get_sine_graphs(axes1)
        partial_sums = self.get_partial_sums(axes1, sine_graphs)

        sum_tex = self.get_sum_tex()
        sum_tex.next_to(axes1, DOWN, LARGE_BUFF)
        sum_tex.shift(RIGHT)
        eq = OldTex("=")
        target_func_tex = self.get_target_func_tex()
        target_func_tex.next_to(axes2, DOWN)
        target_func_tex.match_y(sum_tex)
        eq.move_to(midpoint(
            target_func_tex.get_left(),
            sum_tex.get_right()
        ))

        range_words = OldTexText(
            "For $0 \\le x \\le 1$"
        )
        range_words.next_to(
            VGroup(sum_tex, target_func_tex),
            DOWN,
        )

        rects = it.chain(
            [
                SurroundingRectangle(piece)
                for piece in self.get_sum_tex_pieces(sum_tex)
            ],
            it.cycle([None])
        )

        self.add(axes1, arrow, axes2)
        self.add(sum_tex, eq, target_func_tex)
        self.add(range_words)

        curr_partial_sum = axes1.get_graph(lambda x: 0)
        curr_partial_sum.set_stroke(width=1)
        for sine_graph, partial_sum, rect in zip(sine_graphs, partial_sums, rects):
            anims1 = [
                ShowCreation(sine_graph)
            ]
            partial_sum.set_stroke(BLACK, 4, background=True)
            anims2 = [
                curr_partial_sum.set_stroke,
                {"width": 1, "opacity": 0.5},
                curr_partial_sum.set_stroke,
                {"width": 0, "background": True},
                ReplacementTransform(
                    sine_graph, partial_sum,
                    remover=True
                ),
            ]
            if rect:
                rect.match_style(sine_graph)
                anims1.append(ShowCreation(rect))
                anims2.append(FadeOut(rect))
            self.play(*anims1)
            self.play(*anims2)
            curr_partial_sum = partial_sum

    def get_axes_arrow_axes(self):
        axes1 = Axes(**self.axes_config)
        axes1.x_axis.add_numbers(
            0.5, 1,
            num_decimal_places=1
        )
        axes1.y_axis.add_numbers(
            -1, 1,
            direction=LEFT,
            num_decimal_places=1,
        )
        axes2 = axes1.deepcopy()

        arrow = Arrow(LEFT, RIGHT, color=WHITE)
        group = VGroup(axes1, arrow, axes2)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        return group

    def get_sine_graphs(self, axes):
        sine_graphs = VGroup(*[
            axes.get_graph(self.generate_nth_func(n))
            for n in self.n_range
        ])
        sine_graphs.set_stroke(width=3)
        for graph, color in zip(sine_graphs, it.cycle(self.colors)):
            graph.set_color(color)
        return sine_graphs

    def get_partial_sums(self, axes, sine_graphs):
        partial_sums = VGroup(*[
            axes.get_graph(self.generate_kth_partial_sum_func(k + 1))
            for k in range(len(self.n_range))
        ])
        partial_sums.match_style(sine_graphs)
        return partial_sums

    def get_sum_tex(self):
        return OldTex(
            "\\frac{4}{\\pi} \\left(",
            "\\frac{\\cos(\\pi x)}{1}",
            "-\\frac{\\cos(3\\pi x)}{3}",
            "+\\frac{\\cos(5\\pi x)}{5}",
            "- \\cdots \\right)"
        ).scale(0.75)

    def get_sum_tex_pieces(self, sum_tex):
        return sum_tex[1:4]

    def get_target_func_tex(self):
        step_tex = OldTex(
            """
            1 \\quad \\text{if $x < 0.5$} \\\\
            0 \\quad \\text{if $x = 0.5$} \\\\
            -1 \\quad \\text{if $x > 0.5$} \\\\
            """
        )
        lb = Brace(step_tex, LEFT, buff=SMALL_BUFF)
        step_tex.add(lb)
        return step_tex

    def get_target_func_graph(self, axes):
        step_func = axes.get_graph(
            lambda x: (1 if x < 0.5 else -1),
            discontinuities=[0.5],
            color=YELLOW,
            stroke_width=3,
        )
        dot = Dot(axes.c2p(0.5, 0), color=step_func.get_color())
        dot.scale(0.5)
        step_func.add(dot)
        return step_func

    # def generate_nth_func(self, n):
    #     return lambda x: (4 / n / PI) * np.sin(TAU * n * x)

    def generate_nth_func(self, n):
        return lambda x: np.prod([
            (4 / PI),
            (1 / n) * (-1)**((n - 1) / 2),
            np.cos(PI * n * x)
        ])

    def generate_kth_partial_sum_func(self, k):
        return lambda x: np.sum([
            self.generate_nth_func(n)(x)
            for n in self.n_range[:k]
        ])



# ----- From _2019/diffyq/part4/temperature_scenes.py -----

class StepFunctionExample(BringTwoRodsTogether, FourierSeriesIllustraiton):
    CONFIG = {
        "axes_config": {
            "y_min": -1.5,
            "y_max": 1.5,
            "y_axis_config": {
                "unit_size": 2.5,
                "tick_frequency": 0.5,
            },
            "x_min": 0,
            "x_max": 1,
            "x_axis_config": {
                "unit_size": 8,
                "tick_frequency": 0.1,
                "include_tip": False,
            },
        },
        "y_labels": [-1, 1],
        "graph_x_min": 0,
        "graph_x_max": 1,
        "midpoint": 0.5,
        "min_temp": -1,
        "max_temp": 1,
        "alpha": 0.25,
        "step_size": 0.01,
        "n_range": range(1, 41, 2),
    }

    def construct(self):
        self.setup_axes()
        self.setup_graph()
        self.setup_clock()

        self.bring_rods_together()
        self.let_evolve_for_a_bit()
        self.add_labels()
        self.compare_to_sine_wave()
        self.sum_of_sine_waves()

    def bring_rods_together(self):
        rods = VGroup(
            self.get_rod(0, 0.5),
            self.get_rod(0.5, 1),
        )
        rods.add_updater(self.update_rods)

        arrows = VGroup(
            Vector(RIGHT).next_to(rods[0], UP),
            Vector(LEFT).next_to(rods[1], UP),
        )

        words = VGroup(
            OldTexText("Hot").next_to(rods[0], DOWN),
            OldTexText("Cold").next_to(rods[1], DOWN),
        )

        for pair in rods, words:
            pair.save_state()
            pair.space_out_submobjects(1.2)

        black_rects = VGroup(*[
            Square(
                side_length=1,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            ).move_to(self.axes.c2p(0, u))
            for u in [1, -1]
        ])
        black_rects[0].add_updater(
            lambda m: m.align_to(rods[0].get_right(), LEFT)
        )
        black_rects[1].add_updater(
            lambda m: m.align_to(rods[1].get_left(), RIGHT)
        )

        self.add(
            self.axes,
            self.graph,
            self.clock,
        )
        self.add(rods, words)
        self.add(black_rects)

        kw = {
            "run_time": 2,
            "rate_func": rush_into,
        }
        self.play(
            Restore(rods, **kw),
            Restore(words, **kw),
            *map(ShowCreation, arrows)
        )
        self.remove(black_rects)

        self.to_fade = VGroup(words, arrows)
        self.rods = rods

    def let_evolve_for_a_bit(self):
        rods = self.rods
        # axes = self.axes
        time_label = self.time_label
        graph = self.graph
        graph.save_state()

        graph.add_updater(self.update_graph)
        time_label.next_to(self.clock, DOWN)
        time_label.add_updater(
            lambda d, dt: d.increment_value(dt)
        )
        rods.add_updater(self.update_rods)

        self.add(time_label)
        self.play(
            FadeOut(self.to_fade),
            self.get_clock_anim(1)
        )
        self.play(self.get_clock_anim(3))

        time_label.clear_updaters()
        graph.clear_updaters()
        self.play(
            self.get_clock_anim(
                -4,
                run_time=1,
                rate_func=smooth,
            ),
            graph.restore,
            time_label.set_value, 0,
        )
        rods.clear_updaters()
        self.wait()

    def add_labels(self):
        axes = self.axes
        y_axis = axes.y_axis
        x_axis = axes.x_axis
        y_numbers = y_axis.get_number_mobjects(
            *np.arange(-1, 1.5, 0.5),
            unit="^\\circ",
            num_decimal_places=1
        )
        x_numbers = x_axis.get_number_mobjects(
            *np.arange(0.2, 1.2, 0.2),
            num_decimal_places=1,
        )

        self.play(FadeIn(y_numbers))
        self.play(ShowCreationThenFadeAround(y_numbers[-1]))
        self.play(ShowCreationThenFadeAround(y_numbers[0]))
        self.play(
            LaggedStartMap(
                FadeInFrom, x_numbers,
                lambda m: (m, UP)
            ),
            self.rods.set_opacity, 0.8,
        )
        self.wait()

    def compare_to_sine_wave(self):
        phi_tracker = ValueTracker(0)
        get_phi = phi_tracker.get_value
        k_tracker = ValueTracker(TAU)
        get_k = k_tracker.get_value
        A_tracker = ValueTracker(1)
        get_A = A_tracker.get_value

        sine_wave = always_redraw(lambda: self.axes.get_graph(
            lambda x: get_A() * np.sin(
                get_k() * x - get_phi()
            ),
            x_min=self.graph_x_min,
            x_max=self.graph_x_max,
        ).color_using_background_image("VerticalTempGradient"))

        self.play(ShowCreation(sine_wave, run_time=3))
        self.wait()
        self.play(A_tracker.set_value, 1.25)
        self.play(A_tracker.set_value, 0.75)
        self.play(phi_tracker.set_value, -PI / 2)
        self.play(k_tracker.set_value, 3 * TAU)
        self.play(k_tracker.set_value, 2 * TAU)
        self.play(
            k_tracker.set_value, PI,
            A_tracker.set_value, 4 / PI,
            run_time=3
        )
        self.wait()

        self.sine_wave = sine_wave

    def sum_of_sine_waves(self):
        curr_sine_wave = self.sine_wave
        axes = self.axes

        sine_graphs = self.get_sine_graphs(axes)
        partial_sums = self.get_partial_sums(axes, sine_graphs)

        curr_partial_sum = partial_sums[0]
        curr_partial_sum.set_color(WHITE)
        self.play(
            FadeOut(curr_sine_wave),
            FadeIn(curr_partial_sum),
            FadeOut(self.rods),
        )
        # Copy-pasting from superclass...in theory,
        # this should be better abstracted, but eh.
        pairs = list(zip(sine_graphs, partial_sums))[1:]
        for sine_graph, partial_sum in pairs:
            anims1 = [
                ShowCreation(sine_graph)
            ]
            partial_sum.set_stroke(BLACK, 4, background=True)
            anims2 = [
                curr_partial_sum.set_stroke,
                {"width": 1, "opacity": 0.25},
                curr_partial_sum.set_stroke,
                {"width": 0, "background": True},
                ReplacementTransform(
                    sine_graph, partial_sum,
                    remover=True
                ),
            ]
            self.play(*anims1)
            self.play(*anims2)
            curr_partial_sum = partial_sum

    #
    def setup_axes(self):
        super().setup_axes()
        self.axes.shift(
            self.axes.c2p(0, 0)[1] * DOWN
        )
