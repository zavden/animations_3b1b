# ==============================================================================
# Scene:      BasicSpringScene
# Source:     videos/_2025/laplace/shm.py (lines 150-291)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BasicSpringScene.py BasicSpringScene -w -m --fps 15
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


class BasicSpringScene(InteractiveScene):
    def construct(self):
        # Add spring, give some initial oscillation
        spring = SrpingMassSystem(
            x0=2,
            mu=0.1,
            k=3,
            equilibrium_position=2 * LEFT,
            equilibrium_length=5,
        )
        self.add(spring)

        # Label on a number line
        number_line = NumberLine(x_range=(-4, 4, 1))
        number_line.next_to(spring.equilibrium_position, DOWN, buff=2.0)
        number_line.add_numbers(font_size=24)

        # Dashed line from mass to number line
        dashed_line = DashedLine(
            spring.mass.get_bottom(),
            number_line.n2p(spring.get_x()),
            stroke_color=GREY,
            stroke_width=2
        )
        dashed_line.always.match_x(spring.mass)

        # Arrow tip on number line
        arrow_tip = ArrowTip(length=0.2, width=0.1)
        arrow_tip.rotate(-90 * DEG)  # Point downward
        arrow_tip.set_fill(TEAL)
        arrow_tip.add_updater(lambda m: m.move_to(number_line.n2p(spring.get_x()), DOWN))

        x_label = Tex("x = 0.00", font_size=24)
        x_number = x_label.make_number_changeable("0.00")
        x_number.add_updater(lambda m: m.set_value(spring.get_x()))
        x_label.add_updater(lambda m: m.next_to(arrow_tip, UR, buff=0.1))

        # Ambient playing, fade in labels
        self.wait(2)
        self.play(
            VFadeIn(number_line),
            VFadeIn(dashed_line),
            VFadeIn(arrow_tip),
            VFadeIn(x_label),
        )
        self.wait(7)

        # (For an insertion)
        if False:
            x_label_arrow = Vector(1.5 * DL, thickness=8)
            x_label_arrow.set_fill(YELLOW)
            x_label_arrow.always.move_to(arrow_tip, DL).shift(2 * RIGHT + 0.75 * UP)
            self.play(
                VFadeIn(x_label_arrow, time_span=(1, 2)),
                x_label.animate.scale(2),
                run_time=2
            )
            self.wait(8)

        # Show velocity
        x_color, v_color, a_color = [interpolate_color_by_hsl(TEAL, RED, a) for a in np.linspace(0, 1, 3)]
        v_vect = spring.get_velocity_vector(color=v_color, scale_factor=0.25)
        a_vect = spring.get_force_vector(color=a_color, scale_factor=0.25)
        a_vect.add_updater(lambda m: m.shift(v_vect.get_end() - m.get_start()))

        self.play(VFadeIn(v_vect))
        self.wait(5)
        self.play(VFadeIn(a_vect))
        self.wait(8)
        self.wait_until(lambda: spring.velocity <= 0)

        # Show the force law
        self.remove(v_vect)
        a_vect.remove_updater(a_vect.get_updaters()[-1])
        spring.pause()

        self.wait()
        for x in range(2, 5):
            self.play(spring.animate.set_x(x))
            self.wait()

        # Back and forth
        t_tracker = ValueTracker(0)
        self.play(
            UpdateFromAlphaFunc(
                spring,
                lambda m, a: m.set_x(4 * math.cos(2 * TAU * a)),
                rate_func=linear,
                run_time=8,
            )
        )

        # Ambient springing
        spring.unpause()
        spring.set_mu(0.25)
        self.wait(15)

        # Show the solution graph
        frame = self.frame

        time_tracker = ValueTracker(0)
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        axes = Axes(
            x_range=(0, 20, 1),
            y_range=(-2, 2, 1),
            width=12,
            height=3,
            axis_config={"stroke_color": GREY}
        )
        axes.next_to(spring, UP, LARGE_BUFF)
        axes.align_to(number_line, LEFT)

        x_axis_label = Text("Time", font_size=24).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_axis_label = Tex("x(t)", font_size=24).next_to(axes.y_axis.get_top(), RIGHT, buff=0.1)
        axes.add(x_axis_label)
        axes.add(y_axis_label)

        tracking_point = Point()
        tracking_point.add_updater(lambda p: p.move_to(
            axes.c2p(time_tracker.get_value(), spring.get_x())
        ))

        position_graph = TracedPath(
            tracking_point.get_center,
            stroke_color=BLUE,
            stroke_width=3,
        )

        spring.pause()
        spring.set_velocity(0)
        self.play(
            frame.animate.reorient(0, 0, 0, (2.88, 1.88, 0.0), 12.48),
            FadeIn(axes),
            VFadeOut(a_vect),
            spring.animate.set_x(2),
        )
        self.add(tracking_point, position_graph, time_tracker)
        spring.unpause()
        self.wait(20)
        position_graph.clear_updaters()
        self.wait(20)
