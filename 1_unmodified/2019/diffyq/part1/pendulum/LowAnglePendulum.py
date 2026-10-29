# ==============================================================================
# Scene:      LowAnglePendulum
# Source:     videos/_2019/diffyq/part1/pendulum.py (lines 737-812)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LowAnglePendulum.py LowAnglePendulum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Pendulum(VGroup):
    CONFIG = {
        "length": 3,
        "gravity": 9.8,
        "weight_diameter": 0.5,
        "initial_theta": 0.3,
        "omega": 0,
        "damping": 0.1,
        "top_point": 2 * UP,
        "rod_style": {
            "stroke_width": 3,
            "stroke_color": GREY_B,
            "sheen_direction": UP,
            "sheen_factor": 1,
        },
        "weight_style": {
            "stroke_width": 0,
            "fill_opacity": 1,
            "fill_color": GREY_BROWN,
            "sheen_direction": UL,
            "sheen_factor": 0.5,
            "background_stroke_color": BLACK,
            "background_stroke_width": 3,
            "background_stroke_opacity": 0.5,
        },
        "dashed_line_config": {
            "num_dashes": 25,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "angle_arc_config": {
            "radius": 1,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "velocity_vector_config": {
            "color": RED,
        },
        "theta_label_height": 0.25,
        "set_theta_label_height_cap": False,
        "n_steps_per_frame": 100,
        "include_theta_label": True,
        "include_velocity_vector": False,
        "velocity_vector_multiple": 0.5,
        "max_velocity_vector_length_to_length_ratio": 0.5,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_fixed_point()
        self.create_rod()
        self.create_weight()
        self.rotating_group = VGroup(self.rod, self.weight)
        self.create_dashed_line()
        self.create_angle_arc()
        if self.include_theta_label:
            self.add_theta_label()
        if self.include_velocity_vector:
            self.add_velocity_vector()

        self.set_theta(self.initial_theta)
        self.update()

    def create_fixed_point(self):
        self.fixed_point_tracker = VectorizedPoint(self.top_point)
        self.add(self.fixed_point_tracker)
        return self

    def create_rod(self):
        rod = self.rod = Line(UP, DOWN)
        rod.set_height(self.length)
        rod.set_style(**self.rod_style)
        rod.move_to(self.get_fixed_point(), UP)
        self.add(rod)

    def create_weight(self):
        weight = self.weight = Circle()
        weight.set_width(self.weight_diameter)
        weight.set_style(**self.weight_style)
        weight.move_to(self.rod.get_end())
        self.add(weight)

    def create_dashed_line(self):
        line = self.dashed_line = DashedLine(
            self.get_fixed_point(),
            self.get_fixed_point() + self.length * DOWN,
            **self.dashed_line_config
        )
        line.add_updater(
            lambda l: l.move_to(self.get_fixed_point(), UP)
        )
        self.add_to_back(line)

    def create_angle_arc(self):
        self.angle_arc = always_redraw(lambda: Arc(
            arc_center=self.get_fixed_point(),
            start_angle=-90 * DEGREES,
            angle=self.get_arc_angle_theta(),
            **self.angle_arc_config,
        ))
        self.add(self.angle_arc)

    def get_arc_angle_theta(self):
        # Might be changed in certain scenes
        return self.get_theta()

    def add_velocity_vector(self):
        def make_vector():
            omega = self.get_omega()
            theta = self.get_theta()
            mvlr = self.max_velocity_vector_length_to_length_ratio
            max_len = mvlr * self.rod.get_length()
            vvm = self.velocity_vector_multiple
            multiple = np.clip(
                vvm * omega, -max_len, max_len
            )
            vector = Vector(
                multiple * RIGHT,
                **self.velocity_vector_config,
            )
            vector.rotate(theta, about_point=ORIGIN)
            vector.shift(self.rod.get_end())
            return vector

        self.velocity_vector = always_redraw(make_vector)
        self.add(self.velocity_vector)
        return self

    def add_theta_label(self):
        self.theta_label = always_redraw(self.get_label)
        self.add(self.theta_label)

    def get_label(self):
        label = OldTex("\\theta")
        label.set_height(self.theta_label_height)
        if self.set_theta_label_height_cap:
            max_height = self.angle_arc.get_width()
            if label.get_height() > max_height:
                label.set_height(max_height)
        top = self.get_fixed_point()
        arc_center = self.angle_arc.point_from_proportion(0.5)
        vect = arc_center - top
        norm = get_norm(vect)
        vect = normalize(vect) * (norm + self.theta_label_height)
        label.move_to(top + vect)
        return label

    #
    def get_theta(self):
        theta = self.rod.get_angle() - self.dashed_line.get_angle()
        theta = (theta + PI) % TAU - PI
        return theta

    def set_theta(self, theta):
        self.rotating_group.rotate(
            theta - self.get_theta()
        )
        self.rotating_group.shift(
            self.get_fixed_point() - self.rod.get_start(),
        )
        return self

    def get_omega(self):
        return self.omega

    def set_omega(self, omega):
        self.omega = omega
        return self

    def get_fixed_point(self):
        return self.fixed_point_tracker.get_location()

    #
    def start_swinging(self):
        self.add_updater(Pendulum.update_by_gravity)

    def end_swinging(self):
        self.remove_updater(Pendulum.update_by_gravity)

    def update_by_gravity(self, dt):
        theta = self.get_theta()
        omega = self.get_omega()
        nspf = self.n_steps_per_frame
        for x in range(nspf):
            d_theta = omega * dt / nspf
            d_omega = op.add(
                -self.damping * omega,
                -(self.gravity / self.length) * np.sin(theta),
            ) * dt / nspf
            theta += d_theta
            omega += d_omega
        self.set_theta(theta)
        self.set_omega(omega)
        return self


class ThetaVsTAxes(Axes):
    CONFIG = {
        "x_min": 0,
        "x_max": 8,
        "y_min": -PI / 2,
        "y_max": PI / 2,
        "y_axis_config": {
            "tick_frequency": PI / 8,
            "unit_size": 1.5,
        },
        "axis_config": {
            "color": "#EEEEEE",
            "stroke_width": 2,
            "include_tip": False,
        },
        "graph_style": {
            "stroke_color": GREEN,
            "stroke_width": 3,
            "fill_opacity": 0,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_labels()

    def add_axes(self):
        self.axes = Axes(**self.axes_config)
        self.add(self.axes)

    def add_labels(self):
        x_axis = self.get_x_axis()
        y_axis = self.get_y_axis()

        t_label = self.t_label = OldTex("t")
        t_label.next_to(x_axis.get_right(), UP, MED_SMALL_BUFF)
        x_axis.label = t_label
        x_axis.add(t_label)
        theta_label = self.theta_label = OldTex("\\theta(t)")
        theta_label.next_to(y_axis.get_top(), UP, SMALL_BUFF)
        y_axis.label = theta_label
        y_axis.add(theta_label)

        self.y_axis_label = theta_label
        self.x_axis_label = t_label

        x_axis.add_numbers()
        y_axis.add(self.get_y_axis_coordinates(y_axis))

    def get_y_axis_coordinates(self, y_axis):
        texs = [
            # "\\pi \\over 4",
            # "\\pi \\over 2",
            # "3 \\pi \\over 4",
            # "\\pi",
            "\\pi / 4",
            "\\pi / 2",
            "3 \\pi / 4",
            "\\pi",
        ]
        values = np.arange(1, 5) * PI / 4
        labels = VGroup()
        for pos_tex, pos_value in zip(texs, values):
            neg_tex = "-" + pos_tex
            neg_value = -1 * pos_value
            for tex, value in (pos_tex, pos_value), (neg_tex, neg_value):
                if value > self.y_max or value < self.y_min:
                    continue
                symbol = OldTex(tex)
                symbol.scale(0.5)
                point = y_axis.number_to_point(value)
                symbol.next_to(point, LEFT, MED_SMALL_BUFF)
                labels.add(symbol)
        return labels

    def get_live_drawn_graph(self, pendulum,
                             t_max=None,
                             t_step=1.0 / 60,
                             **style):
        style = merge_dicts_recursively(self.graph_style, style)
        if t_max is None:
            t_max = self.x_max

        graph = VMobject()
        graph.set_style(**style)

        graph.all_coords = [(0, pendulum.get_theta())]
        graph.time = 0
        graph.time_of_last_addition = 0

        def update_graph(graph, dt):
            graph.time += dt
            if graph.time > t_max:
                graph.remove_updater(update_graph)
                return
            new_coords = (graph.time, pendulum.get_theta())
            if graph.time - graph.time_of_last_addition >= t_step:
                graph.all_coords.append(new_coords)
                graph.time_of_last_addition = graph.time
            points = [
                self.coords_to_point(*coords)
                for coords in [*graph.all_coords, new_coords]
            ]
            graph.set_points_smoothly(points)

        graph.add_updater(update_graph)
        return graph


class LowAnglePendulum(Scene):
    CONFIG = {
        "pendulum_config": {
            "initial_theta": 20 * DEGREES,
            "length": 2.0,
            "damping": 0,
            "top_point": ORIGIN,
        },
        "axes_config": {
            "y_axis_config": {"unit_size": 0.75},
            "x_axis_config": {
                "unit_size": 0.5,
                "numbers_to_show": range(2, 25, 2),
                "number_scale_val": 0.5,
            },
            "x_max": 25,
            "axis_config": {
                "tip_length": 0.3,
                "stroke_width": 2,
            }
        },
        "axes_corner": UL,
    }

    def construct(self):
        pendulum = Pendulum(**self.pendulum_config)
        axes = ThetaVsTAxes(**self.axes_config)
        axes.center()
        axes.to_corner(self.axes_corner, buff=LARGE_BUFF)
        graph = axes.get_live_drawn_graph(pendulum)

        L = pendulum.length
        g = pendulum.gravity
        theta0 = pendulum.initial_theta
        prediction = axes.get_graph(
            lambda t: theta0 * np.cos(t * np.sqrt(g / L))
        )
        dashed_prediction = DashedVMobject(prediction, num_dashes=300)
        dashed_prediction.set_stroke(WHITE, 1)
        prediction_formula = OldTex(
            "\\theta_0", "\\cos(\\sqrt{g / L} \\cdot t)"
        )
        prediction_formula.scale(0.75)
        prediction_formula.next_to(
            dashed_prediction, UP, SMALL_BUFF,
        )

        theta0 = prediction_formula.get_part_by_tex("\\theta_0")
        theta0_brace = Brace(theta0, UP, buff=SMALL_BUFF)
        theta0_brace.stretch(0.5, 1, about_edge=DOWN)
        theta0_label = Integer(
            pendulum.initial_theta * 180 / PI,
            unit="^\\circ"
        )
        theta0_label.scale(0.75)
        theta0_label.next_to(theta0_brace, UP, SMALL_BUFF)

        group = VGroup(theta0_brace, theta0_label, prediction_formula)
        group.shift_onto_screen(buff=MED_SMALL_BUFF)

        self.add(axes, dashed_prediction, pendulum)
        self.play(
            ShowCreation(dashed_prediction, run_time=2),
            FadeInFromDown(prediction_formula),
            FadeInFromDown(theta0_brace),
            FadeInFromDown(theta0_label),
        )
        self.play(
            ShowCreationThenFadeAround(theta0_label),
            ShowCreationThenFadeAround(pendulum.theta_label),
        )
        self.wait()

        pendulum.start_swinging()
        self.add(graph)
        self.wait(30)
