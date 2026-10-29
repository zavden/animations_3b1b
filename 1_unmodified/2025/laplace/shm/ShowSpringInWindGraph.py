# ==============================================================================
# Scene:      ShowSpringInWindGraph
# Source:     videos/_2025/laplace/shm.py (lines 1797-1928)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSpringInWindGraph.py ShowSpringInWindGraph -w -m --fps 15
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


class SpringInTheWind(InteractiveScene):
    F_0 = 1.0
    omega = 2
    k = 3
    mu = 0.1

    def setup(self):
        super().setup()
        # Set up wind

        plane = NumberPlane()
        wind = TimeVaryingVectorField(
            lambda p, t: np.tile(self.external_force(t) * RIGHT, (len(p), 1)),
            plane,
            density=1,
            color=WHITE,
            stroke_width=6,
            stroke_opacity=0.5,
        )

        # Set up spring and ODE
        spring = SrpingMassSystem(
            k=self.k,
            mu=self.mu,
            external_force=lambda: self.external_force(wind.time)
        )
        spring.add_external_force(lambda: self.F_0 * math.cos(self.omega * wind.time))

        self.add(wind)
        self.add(spring)

        self.spring = spring
        self.wind = wind

    def external_force(self, time):
        return self.F_0 * math.cos(self.omega * time)

    def construct(self):
        spring = self.spring
        wind = self.wind
        self.play(VFadeIn(wind))
        self.wait(60)


class ShowSpringInWindGraph(SpringInTheWind):
    mu = 0.25
    k = 3
    omega = 2.5

    def construct(self):
        spring = self.spring
        wind = self.wind

        # Add graph
        t_max = 40
        frame = self.frame
        frame.set_y(1)
        graph_block = Rectangle(width=FRAME_WIDTH, height=2.5)
        graph_block.move_to(frame, UP)
        graph_block.set_stroke(width=0)
        graph_block.set_fill(BLACK, 1)

        axes = Axes((0, t_max), (-0.5, 0.5, 0.25), width=FRAME_WIDTH - 1, height=2.0)
        axes.x_axis.ticks.stretch(0.5, 1)
        axes.move_to(graph_block)
        axis_label = Text("Time", font_size=24)
        axis_label.next_to(axes.x_axis.get_right(), DOWN)
        axes.add(axis_label)

        graph = TracedPath(
            lambda: axes.c2p(self.time, spring.get_x()),
            stroke_color=BLUE,
            stroke_width=3,
        )

        self.add(graph_block)
        self.add(axes)
        self.add(graph)

        # Play it out
        self.wait(t_max)
        graph.clear_updaters()
        self.play(
            VFadeOut(spring),
            VFadeOut(wind),
        )

        # Comment on the graph
        left_highlight = graph_block.copy()
        left_highlight.set_width(6.5, stretch=True, about_edge=LEFT)
        left_highlight.set_fill(YELLOW, 0.2)
        left_highlight.set_height(2, stretch=True)
        right_highlight = left_highlight.copy()
        right_highlight.set_width(10, stretch=True, about_edge=LEFT)
        right_highlight.next_to(left_highlight, RIGHT, buff=0)
        right_highlight.set_fill(GREEN, 0.2)

        self.play(FadeIn(left_highlight))
        self.wait()
        self.play(FadeIn(right_highlight))
        self.wait()

        # Show solution components
        axes1, axes2 = axes_copies = VGroup(axes.deepcopy() for _ in range(2))
        buff = 0.75
        axes_copies.arrange(DOWN, buff=buff)
        axes_copies.next_to(axes, DOWN, buff=buff)

        s_root = (-self.mu + 1j * math.sqrt(-(self.mu**2 - 4 * self.k))) / 2.0
        amp = 0.35
        shm_graph = axes1.get_graph(lambda t: amp * np.exp(s_root * t).real)
        shm_graph.set_stroke(GREEN, 4)
        cos_graph = axes2.get_graph(lambda t: -amp * math.cos(self.omega * t))
        cos_graph.set_stroke(YELLOW, 4)

        equals = Tex(R"=", font_size=72).rotate(90 * DEG)
        equals.move_to(VGroup(axes, axes1)).set_x(-5)
        equals.shift(0.25 * DOWN)
        plus = Tex(R"+", font_size=72)
        plus.move_to(VGroup(axes_copies)).match_x(equals)

        self.play(LaggedStart(
            Write(equals),
            FadeIn(axes1),
            FadeIn(shm_graph),
            Write(plus),
            FadeIn(axes2),
            FadeIn(cos_graph),
            lag_ratio=0.15
        ))
        self.wait()

        # First graph label
        colors = color_gradient([TEAL, RED], 3, interp_by_hsl=True)
        shm_eq = VGroup(
            Text("Solution to", font_size=36),
            Tex(
                R"mx''(t) + \mu x'(t) + k x(t) = 0",
                t2c={
                    "x(t)": colors[0],
                    "x'(t)": colors[1],
                    "x''(t)": colors[2],
                },
                font_size=36,
                alignment="",
            ),
        )
        shm_eq.arrange(DOWN)
        shm_eq.next_to(axes1.x_axis, UP, buff=0.35)
        shm_eq.set_x(-2.5)

        self.add(shm_graph.copy().set_stroke(opacity=0.25))
        self.play(
            FadeIn(shm_eq, lag_ratio=0.1),
            ShowCreation(shm_graph, run_time=3, rate_func=linear),
        )
        self.wait()

        # Grow left highlight
        self.play(
            left_highlight.animate.set_height(8, stretch=True, about_edge=UP).shift(0.15 * UP),
            shm_eq.animate.shift(5 * RIGHT),
            run_time=2,
        )
        self.wait()

        # Draw all graphs
        self.add(graph.copy().set_stroke(opacity=0.25))
        self.add(cos_graph.copy().set_stroke(opacity=0.25))
        self.play(
            left_highlight.animate.set_fill(opacity=0.1),
            *(
                ShowCreation(mob, run_time=15, rate_func=linear)
                for mob in [graph, shm_graph, cos_graph]
            ),
        )
