# ==============================================================================
# Scene:      DefineODE
# Source:     videos/_2019/diffyq/part1/staging.py (lines 1274-1683)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/pendulum.py, _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl DefineODE.py DefineODE -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_ode():
    tex_config = {
        "tex_to_color_map": {
            "{\\theta}": BLUE,
            "{\\dot\\theta}": RED,
            "{\\ddot\\theta}": YELLOW,
            "{t}": WHITE,
            "{\\mu}": WHITE,
        }
    }
    ode = OldTex(
        "{\\ddot\\theta}({t})", "=",
        "-{\\mu} {\\dot\\theta}({t})",
        "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        **tex_config,
    )
    return ode



# ----- From _2019/diffyq/part1/pendulum.py -----

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



# ----- From _2019/diffyq/part1/staging.py -----

class DefineODE(Scene):
    CONFIG = {
        "pendulum_config": {
            "length": 2,
            "top_point": 5 * RIGHT + 2 * UP,
            "initial_theta": 150 * DEGREES,
            "mu": 0.3,
        },
        "axes_config": {
            "y_axis_config": {"unit_size": 0.75},
            "y_max": PI,
            "y_min": -PI,
            "x_max": 10,
            "x_axis_config": {
                "numbers_to_show": range(2, 10, 2),
                "unit_size": 1,
            }
        },
    }

    def construct(self):
        self.add_graph()
        self.write_differential_equation()
        self.dont_know_the_value()
        self.show_value_slope_curvature()
        self.write_ode()
        self.show_second_order()
        self.show_higher_order_examples()
        self.show_changing_curvature_group()

    def add_graph(self):
        pendulum = Pendulum(**self.pendulum_config)
        axes = ThetaVsTAxes(**self.axes_config)

        axes.center()
        axes.to_corner(DL)
        graph = axes.get_live_drawn_graph(pendulum)

        pendulum.start_swinging()
        self.add(axes, pendulum, graph)

        self.pendulum = pendulum
        self.axes = axes
        self.graph = graph

    def write_differential_equation(self):
        de_word = OldTexText("Differential", "Equation")
        de_word.to_edge(UP, buff=MED_SMALL_BUFF)

        equation = get_ode()
        equation.next_to(de_word, DOWN)
        thetas = equation.get_parts_by_tex("\\theta")

        lines = VGroup(*[
            Line(v, 1.2 * v)
            for v in compass_directions(25)
        ])
        lines.replace(equation, stretch=True)
        lines.scale(1.5)
        lines.set_stroke(YELLOW)
        lines.shuffle()

        self.add(equation)
        self.wait(5)
        self.play(
            ShowPassingFlashWithThinningStrokeWidth(
                lines,
                lag_ratio=0.002,
                run_time=1.5,
                time_width=0.9,
                n_segments=5,
            )
        )
        self.play(FadeInFromDown(de_word))
        self.wait(2)
        self.play(
            LaggedStartMap(
                ApplyMethod, thetas,
                lambda m: (m.shift, 0.25 * DOWN),
                rate_func=there_and_back,
            )
        )
        self.wait()

        self.de_word = de_word
        self.equation = equation

    def dont_know_the_value(self):
        graph = self.graph
        pendulum = self.pendulum

        q_marks = VGroup(*[
            OldTex("?").move_to(graph.point_from_proportion(a))
            for a in np.linspace(0, 1, 20)
        ])
        q_marks.set_stroke(width=0, background=True)
        self.play(
            VFadeOut(graph),
            FadeOut(pendulum),
            LaggedStart(*[
                UpdateFromAlphaFunc(
                    q_mark,
                    lambda m, a: m.set_height(0.5 * (1 + a)).set_fill(
                        opacity=there_and_back(a)
                    ),
                )
                for q_mark in q_marks
            ], lag_ratio=0.01, run_time=2)
        )
        self.remove(q_marks)

    def show_value_slope_curvature(self):
        axes = self.axes
        p = self.pendulum
        graph = axes.get_graph(
            lambda t: p.initial_theta * np.cos(
                np.sqrt(p.gravity / p.length) * t
            ) * np.exp(-p.mu * t / 2)
        )

        tex_config = {
            "tex_to_color_map": {
                "{\\theta}": BLUE,
                "{\\dot\\theta}": RED,
                "{\\ddot\\theta}": YELLOW,
            },
            "height": 0.5,
        }
        theta, d_theta, dd_theta = [
            OldTex(
                "{" + s + "\\theta}(t)",
                **tex_config
            )
            for s in ("", "\\dot", "\\ddot")
        ]

        t_tracker = ValueTracker(2.5)
        get_t = t_tracker.get_value

        def get_point(t):
            return graph.point_from_proportion(t / axes.x_max)

        def get_dot():
            return Dot(get_point(get_t())).scale(0.5)

        def get_v_line():
            point = get_point(get_t())
            x_point = axes.x_axis.number_to_point(
                axes.x_axis.point_to_number(point)
            )
            return DashedLine(
                x_point, point,
                dash_length=0.025,
                stroke_color=BLUE,
                stroke_width=2,
            )

        def get_tangent_line(curve, alpha):
            line = Line(
                ORIGIN, 1.5 * RIGHT,
                color=RED,
                stroke_width=1.5,
            )
            da = 0.0001
            p0 = curve.point_from_proportion(alpha)
            p1 = curve.point_from_proportion(alpha - da)
            p2 = curve.point_from_proportion(alpha + da)
            angle = angle_of_vector(p2 - p1)
            line.rotate(angle)
            line.move_to(p0)
            return line

        def get_slope_line():
            return get_tangent_line(
                graph, get_t() / axes.x_max
            )

        def get_curve():
            curve = VMobject()
            t = get_t()
            curve.set_points_smoothly([
                get_point(t + a)
                for a in np.linspace(-0.5, 0.5, 11)
            ])
            curve.set_stroke(YELLOW, 1)
            return curve

        v_line = always_redraw(get_v_line)
        dot = always_redraw(get_dot)
        slope_line = always_redraw(get_slope_line)
        curve = always_redraw(get_curve)

        theta.next_to(v_line, RIGHT, SMALL_BUFF)
        d_theta.next_to(slope_line.get_end(), UP, SMALL_BUFF)
        dd_theta.next_to(curve.get_end(), RIGHT, SMALL_BUFF)
        thetas = VGroup(theta, d_theta, dd_theta)

        words = VGroup(
            OldTexText("= Height").set_color(BLUE),
            OldTexText("= Slope").set_color(RED),
            OldTexText("= ``Curvature''").set_color(YELLOW),
        )
        words.scale(0.75)
        for word, sym in zip(words, thetas):
            word.next_to(sym, RIGHT, buff=2 * SMALL_BUFF)
            sym.word = word

        self.play(
            ShowCreation(v_line),
            FadeInFromPoint(dot, v_line.get_start()),
            FadeIn(theta, DOWN),
            FadeIn(theta.word, DOWN),
        )
        self.add(slope_line, dot)
        self.play(
            ShowCreation(slope_line),
            FadeIn(d_theta, LEFT),
            FadeIn(d_theta.word, LEFT),
        )

        a_tracker = ValueTracker(0)
        curve_copy = curve.copy()
        changing_slope = always_redraw(
            lambda: get_tangent_line(
                curve_copy,
                a_tracker.get_value(),
            ).set_stroke(
                opacity=there_and_back(a_tracker.get_value())
            )
        )
        self.add(curve, dot)
        self.play(
            ShowCreation(curve),
            FadeIn(dd_theta, LEFT),
            FadeIn(dd_theta.word, LEFT),
        )
        self.add(changing_slope)
        self.play(
            a_tracker.set_value, 1,
            run_time=3,
        )
        self.remove(changing_slope, a_tracker)

        self.t_tracker = t_tracker
        self.curvature_group = VGroup(
            v_line, slope_line, curve, dot
        )
        self.curvature_group_labels = VGroup(thetas, words)
        self.fake_graph = graph

    def write_ode(self):
        equation = self.equation
        axes = self.axes
        de_word = self.de_word

        ts = equation.get_parts_by_tex("{t}")
        t_rects = VGroup(*map(SurroundingRectangle, ts))  # Rawr
        x_axis = axes.x_axis
        x_axis_line = Line(
            x_axis.get_start(), x_axis.get_end(),
            stroke_color=YELLOW,
            stroke_width=5,
        )

        ordinary = OldTexText("Ordinary")
        de_word.generate_target()
        group = VGroup(ordinary, de_word.target)
        group.arrange(RIGHT)
        group.to_edge(UP)
        ordinary_underline = Line(LEFT, RIGHT)
        ordinary_underline.replace(ordinary, dim_to_match=0)
        ordinary_underline.next_to(ordinary, DOWN, SMALL_BUFF)
        ordinary_underline.set_color(YELLOW)

        self.play(
            ShowCreationThenFadeOut(
                t_rects,
                lag_ratio=0.8
            ),
            ShowCreationThenFadeOut(x_axis_line)
        )
        self.play(
            MoveToTarget(de_word),
            FadeIn(ordinary, RIGHT),
            GrowFromCenter(ordinary_underline)
        )
        self.play(FadeOut(ordinary_underline))
        self.wait()

        self.remove(ordinary, de_word)
        ode_word = self.ode_word = VGroup(*ordinary, *de_word)
        ode_initials = VGroup(*[word[0] for word in ode_word])
        ode_initials.generate_target()
        ode_initials.target.scale(1.2)
        ode_initials.target.set_color(PINK)
        ode_initials.target.arrange(
            RIGHT, buff=0.5 * SMALL_BUFF, aligned_edge=DOWN
        )
        ode_initials.target.to_edge(UP, buff=MED_SMALL_BUFF)

        ode_remaining_letters = VGroup(*it.chain(*[
            word[1:] for word in ode_word
        ]))
        ode_remaining_letters.generate_target()
        for mob in ode_remaining_letters.target:
            mob.shift(0.2 * UP)
            mob.fade(1)

        self.play(
            MoveToTarget(ode_initials),
            MoveToTarget(ode_remaining_letters, lag_ratio=0.05),
        )
        self.wait()

        self.ode_initials = ode_initials

    def show_second_order(self):
        so = OldTexText("Second order")
        so.scale(1.4)
        ode = self.ode_initials
        ode.generate_target()
        group = VGroup(so, ode.target)
        group.arrange(RIGHT, aligned_edge=DOWN)
        group.to_edge(UP, buff=MED_SMALL_BUFF)

        second_deriv = self.equation[:5]

        self.play(
            Write(so),
            MoveToTarget(ode),
        )
        self.wait()
        self.play(FocusOn(second_deriv))
        self.play(
            Indicate(second_deriv, color=YELLOW),
        )
        self.wait()

        self.second_order_word = so

    def show_higher_order_examples(self):
        main_example = self.get_main_example()
        tex_config = {"tex_to_color_map": {"{x}": BLUE}}
        example3 = VGroup(
            OldTexText("Third order ODE"),
            OldTex(
                "\\dddot {x}(t) + \\dot {x}(t)^2 = 0",
                **tex_config,
            )
        )
        example4 = VGroup(
            OldTexText("Fourth order ODE"),
            OldTex(
                "\\ddddot {x}(t) +",
                "a\\dddot {x}(t) \\dot {x}(t) + ",
                "b \\ddot {x}(t) {x}(t)",
                "= 1",
                **tex_config,
            )
        )
        for example in [example3, example4]:
            example[0].scale(1.2)
            example.arrange(DOWN, buff=MED_LARGE_BUFF)
            example.to_edge(UP, buff=MED_SMALL_BUFF)

        self.play(
            FadeOut(main_example),
            FadeIn(example3),
        )
        self.wait(2)
        self.play(
            FadeOut(example3),
            FadeIn(example4),
        )
        self.wait(2)
        self.play(
            FadeOut(example4),
            FadeIn(main_example),
        )
        self.wait(2)

    def get_main_example(self):
        return VGroup(
            self.second_order_word,
            self.ode_initials,
            self.equation
        )

    def show_changing_curvature_group(self):
        t_tracker = self.t_tracker
        curvature_group = self.curvature_group
        labels = self.curvature_group_labels
        graph = VMobject()
        graph.pointwise_become_partial(
            self.fake_graph,
            t_tracker.get_value() / self.axes.x_max,
            1,
        )
        dashed_graph = DashedVMobject(graph, num_dashes=100)
        dashed_graph.set_stroke(GREEN, 1)

        self.play(FadeOut(labels))
        self.add(dashed_graph, curvature_group)
        self.play(
            t_tracker.set_value, 10,
            ShowCreation(dashed_graph),
            run_time=15,
            rate_func=linear,
        )
        self.wait()
