# ==============================================================================
# Scene:      ShowFamilyOfRealSolutions
# Source:     videos/_2025/laplace/shm.py (lines 1460-1560)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowFamilyOfRealSolutions.py ShowFamilyOfRealSolutions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SrpingMassSystem(VGroup):
    def __init__(
        self,
        x0=0,
        v0=0,
        k=3,
        mu=0.1,
        equilibrium_length=7,
        equilibrium_position=ORIGIN,
        direction=RIGHT,
        spring_stroke_color=GREY_B,
        spring_stroke_width=2,
        spring_radius=0.25,
        n_spring_curls=8,
        mass_width=1.0,
        mass_color=BLUE_E,
        mass_label="m",
        external_force=None,
    ):
        super().__init__()
        self.equilibrium_position = equilibrium_position
        self.fixed_spring_point = equilibrium_position - (equilibrium_length - 0.5 * mass_width) * direction
        self.direction = direction
        self.rot_off_horizontal = angle_between_vectors(RIGHT, direction)
        self.mass = self.get_mass(mass_width, mass_color, mass_label)
        self.spring = self.get_spring(spring_stroke_color, spring_stroke_width, n_spring_curls, spring_radius)
        self.add(self.spring, self.mass)

        self.k = k
        self.mu = mu
        self.set_x(x0)
        self.velocity = v0

        self.external_force = external_force

        self._is_running = True
        self.add_updater(lambda m, dt: m.time_step(dt))

    def get_spring(self, stroke_color, stroke_width, n_curls, radius):
        spring = ParametricCurve(
            lambda t: [t, -radius * math.sin(TAU * t), radius * math.cos(TAU * t)],
            t_range=(0, n_curls, 1e-2),
            stroke_color=stroke_color,
            stroke_width=stroke_width,
        )
        spring.rotate(self.rot_off_horizontal)
        return spring

    def get_mass(self, mass_width, mass_color, mass_label):
        mass = Square(mass_width)
        mass.set_fill(mass_color, 1)
        mass.set_stroke(WHITE, 1)
        mass.set_shading(0.1, 0.1, 0.1)
        label = Tex(mass_label)
        label.set_max_width(0.5 * mass.get_width())
        label.move_to(mass)
        mass.add(label)
        mass.label = label
        return mass

    def set_x(self, x):
        self.mass.move_to(self.equilibrium_position + x * self.direction)
        spring_width = SMALL_BUFF + get_norm(self.mass.get_left() - self.fixed_spring_point)
        self.spring.rotate(-self.rot_off_horizontal)
        self.spring.set_width(spring_width, stretch=True)
        self.spring.rotate(self.rot_off_horizontal)
        self.spring.move_to(self.fixed_spring_point, -self.direction)

    def get_x(self):
        return (self.mass.get_center() - self.equilibrium_position)[0]

    def time_step(self, delta_t, dt_size=1e-3):
        if not self._is_running:
            return
        if delta_t == 0:
            return

        state = [self.get_x(), self.velocity]
        sub_steps = max(int(delta_t / dt_size), 1)
        true_dt = delta_t / sub_steps
        for _ in range(sub_steps):
            # ODE
            x, v = state
            state += np.array([v, self.get_force(x, v)]) * true_dt

        self.set_x(state[0])
        self.velocity = state[1]

    def pause(self):
        self._is_running = False

    def unpause(self):
        self._is_running = True

    def set_k(self, k):
        self.k = k
        return self

    def set_mu(self, mu):
        self.mu = mu
        return self

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity
        return self

    def get_velocity_vector(self, scale_factor=0.5, thickness=3.0, v_offset=-0.25, color=GREEN):
        """Get a vector showing the mass's velocity"""
        vector = Vector(RIGHT, fill_color=color)
        v_shift = v_offset * UP
        vector.add_updater(lambda m: m.put_start_and_end_on(
            self.mass.get_center() + v_shift,
            self.mass.get_center() + v_shift + scale_factor * self.velocity * RIGHT
        ))
        return vector

    def get_force_vector(self, scale_factor=0.5, thickness=3.0, v_offset=-0.25, color=RED):
        """Get a vector showing the mass's velocity"""
        vector = Vector(RIGHT, fill_color=color)
        v_shift = v_offset * UP
        vector.add_updater(lambda m: m.put_start_and_end_on(
            self.mass.get_center() + v_shift,
            self.mass.get_center() + v_shift + scale_factor * self.get_force(self.get_x(), self.velocity) * RIGHT
        ))
        return vector

    def add_external_force(self, func):
        self.external_force = func

    def get_force(self, x, v):
        force = -self.k * x - self.mu * v
        if self.external_force is not None:
            force += self.external_force()
        return force


class ShowFamilyOfRealSolutions(InteractiveScene):
    t2c = {R"\omega": PINK}
    omega = PI
    x_max = 10

    def construct(self):
        # Add cosine and sine graphs up top
        cos_graph, sin_graph = small_graphs = VGroup(
            self.get_small_graph(math.cos, R"\cos(\omega t)", BLUE),
            self.get_small_graph(math.sin, R"\sin(\omega t)", RED),
        )
        small_graphs.arrange(RIGHT, buff=LARGE_BUFF)
        small_graphs.to_edge(UP, buff=MED_SMALL_BUFF)

        self.add(small_graphs)

        # Add master graph
        coef_trackers = ValueTracker(1).replicate(2)

        def func(t):
            c1 = coef_trackers[0].get_value()
            c2 = coef_trackers[1].get_value()
            return c1 * np.cos(self.omega * t) + c2 * np.sin(self.omega * t)

        axes = Axes((0, self.x_max), (-3, 3), width=self.x_max, height=4)
        axes.to_edge(DOWN)
        graph_label = Tex(R"+1.00 \cos(\omega t) +1.00 \sin(\omega t)", t2c=self.t2c)
        graph_label.next_to(axes.y_axis.get_top(), UR)
        coef_labels = graph_label.make_number_changeable("+1.00", replace_all=True, edge_to_fix=RIGHT, include_sign=True)
        coef_labels.set_color(YELLOW)
        coef_labels[0].add_updater(lambda m: m.set_value(coef_trackers[0].get_value()))
        coef_labels[1].add_updater(lambda m: m.set_value(coef_trackers[1].get_value()))

        graph = axes.get_graph(func)
        graph.set_stroke(TEAL, 5)
        axes.bind_graph_to_func(graph, func)

        self.add(axes)
        self.add(graph_label)
        self.add(graph)

        # Tweak the parameters
        for c1, c2 in [(-0.5, 2), (1.5, 0), (0.25, -2)]:
            self.play(LaggedStart(
                coef_trackers[0].animate.set_value(c1),
                coef_trackers[1].animate.set_value(c2),
                lag_ratio=0.5
            ))
            self.wait()

        # Tweak with spring
        for c1, c2 in [(1.6, 1.8), (-2.7, 0.18), (0.5, -2)]:
            self.play(LaggedStart(
                coef_trackers[0].animate.set_value(c1),
                coef_trackers[1].animate.set_value(c2),
                lag_ratio=0.5
            ))
            self.show_spring(axes, graph, func)

    def get_small_graph(self, func, func_name, color):
        axes = Axes((0, 6), (-2, 2), height=2, width=6)
        graph = axes.get_graph(lambda t: func(self.omega * t))
        graph.set_stroke(color, 3)
        label = Tex(func_name, t2c=self.t2c, font_size=36)
        label.move_to(axes, UP)

        return VGroup(axes, graph, label)

    def show_spring(self, axes, graph, func):
        graph_copy = graph.copy()
        graph_copy.clear_updaters()

        spring = SrpingMassSystem(
            equilibrium_length=4,
            equilibrium_position=axes.get_right() + RIGHT,
            direction=UP,
            mass_width=0.75,
            spring_radius=0.2,
        )
        spring.add_updater(
            lambda m: m.set_x(axes.y_axis.get_unit_size() * axes.y_axis.p2n(graph_copy.get_end()))
        )

        h_line = Line()
        h_line.set_stroke(WHITE, 1)
        h_line.f_always.put_start_and_end_on(
            spring.mass.get_left,
            graph_copy.get_end,
        )

        self.play(
            graph.animate.set_stroke(opacity=0.2),
            ShowCreation(graph_copy, rate_func=linear, run_time=self.x_max),
            VFadeIn(spring, run_time=1),
            VFadeIn(h_line, run_time=1),
        )
        self.play(FadeOut(spring), FadeOut(h_line))
        self.wait()

        self.remove(graph_copy, spring, h_line)
        graph.set_stroke(opacity=1)
