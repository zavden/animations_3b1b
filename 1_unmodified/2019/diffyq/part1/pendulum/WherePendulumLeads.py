# ==============================================================================
# Scene:      WherePendulumLeads
# Source:     videos/_2019/diffyq/part1/pendulum.py (lines 900-982)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WherePendulumLeads.py WherePendulumLeads -w -m --fps 15
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


class WherePendulumLeads(PiCreatureScene):
    def construct(self):
        pendulum = Pendulum(
            top_point=UP,
            length=3,
            gravity=20,
        )
        pendulum.start_swinging()

        l_title = OldTexText("Linearization")
        l_title.scale(1.5)
        l_title.to_corner(UL)
        c_title = OldTexText("Chaos")
        c_title.scale(1.5)
        c_title.move_to(l_title)
        c_title.move_to(
            c_title.get_center() * np.array([-1, 1, 1])
        )

        get_theta = pendulum.get_theta
        spring = always_redraw(
            lambda: ParametricCurve(
                lambda t: np.array([
                    np.cos(TAU * t) + (1.4 + get_theta()) * t,
                    np.sin(TAU * t) - 0.5,
                    0,
                ]),
                t_min=-0.5,
                t_max=7,
                color=GREY,
                sheen_factor=1,
                sheen_direction=UL,
            ).scale(0.2).to_edge(LEFT, buff=0)
        )
        spring_rect = SurroundingRectangle(
            spring, buff=MED_LARGE_BUFF,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=0,
        )

        weight = Dot(radius=0.25)
        weight.add_updater(lambda m: m.move_to(
            spring.get_points()[-1]
        ))
        weight.set_color(BLUE)
        weight.set_sheen(1, UL)
        spring_system = VGroup(spring, weight)

        linear_formula = OldTex(
            "\\frac{d \\vec{\\textbf{x}}}{dt}="
            "A\\vec{\\textbf{x}}"
        )
        linear_formula.next_to(spring, UP, LARGE_BUFF)
        linear_formula.match_x(l_title)

        randy = self.pi_creature
        randy.set_height(2)
        randy.center()
        randy.to_edge(DOWN)
        randy.shift(3 * LEFT)
        q_marks = OldTex("???")
        q_marks.next_to(randy, UP)

        self.add(pendulum, randy)
        self.play(
            randy.change, "pondering", pendulum,
            FadeInFromDown(q_marks, lag_ratio=0.3)
        )
        self.play(randy.look_at, pendulum)
        self.wait(5)
        self.play(
            Animation(VectorizedPoint(pendulum.get_top())),
            FadeOut(q_marks, UP, lag_ratio=0.3),
        )
        self.add(spring_system)
        self.play(
            FadeOut(spring_rect),
            FadeIn(linear_formula, UP),
            FadeInFromDown(l_title),
        )
        self.play(FadeInFromDown(c_title))
        self.wait(8)
