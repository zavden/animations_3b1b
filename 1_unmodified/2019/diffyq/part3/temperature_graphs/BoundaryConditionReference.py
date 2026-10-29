# ==============================================================================
# Scene:      BoundaryConditionReference
# Source:     videos/_2019/diffyq/part3/temperature_graphs.py (lines 1495-1534)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part2/heat_equation.py, _2019/diffyq/part2/shared_constructs.py
#
# Run from this folder:
#     manimgl BoundaryConditionReference.py BoundaryConditionReference -w -m --fps 15
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



# ----- From _2019/diffyq/part3/temperature_graphs.py -----

class BoundaryConditionReference(ShowEvolvingTempGraphWithArrows):
    def construct(self):
        self.setup_axes()
        self.setup_graph()

        rod = self.get_rod(0, 10)
        self.color_rod_by_graph(rod)

        boundary_points = [
            rod.get_right(),
            rod.get_left(),
        ]
        boundary_dots = VGroup(*[
            Dot(point, radius=0.2)
            for point in boundary_points
        ])
        boundary_arrows = VGroup(*[
            Vector(2 * DOWN).next_to(dot, UP)
            for dot in boundary_dots
        ])
        boundary_arrows.set_stroke(YELLOW, 10)

        words = OldTexText(
            "Different rules\\\\",
            "at the boundary",
        )
        words.scale(1.5)
        words.to_edge(UP)

        # self.add(self.axes)
        # self.add(self.graph)
        self.add(rod)
        self.play(FadeInFromDown(words))
        self.play(
            LaggedStartMap(GrowArrow, boundary_arrows),
            LaggedStartMap(GrowFromCenter, boundary_dots),
            lag_ratio=0.3,
            run_time=1,
        )
        self.wait()
