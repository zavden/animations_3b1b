# ==============================================================================
# Scene:      RotatingExponentials
# Source:     videos/_2025/laplace/shm.py (lines 951-1103)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotatingExponentials.py RotatingExponentials -w -m --fps 15
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


class RotatingExponentials(InteractiveScene):
    def construct(self):
        # Create time tracker
        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        get_t = t_tracker.get_value
        omega = PI / 2

        def get_x():
            return math.cos(omega * get_t())

        self.add(t_tracker)

        # Create two complex planes side by side
        left_plane, right_plane = planes = VGroup(
            ComplexPlane(
                (-2, 2), (-2, 2),
                background_line_style=dict(stroke_color=BLUE, stroke_width=1),
            )
            for _ in range(2)
        )
        for plane in planes:
            plane.axes.set_stroke(width=1)
            plane.set_height(3.5)
            plane.add_coordinate_labels(font_size=16)
        planes.arrange(RIGHT, buff=1.0)
        planes.to_edge(RIGHT)
        planes.to_edge(UP, buff=1.5)

        self.add(planes)

        # Add titles
        t2c = {R"\omega": PINK}
        left_title, right_title = titles = VGroup(
            Tex(tex, t2c=t2c, font_size=48)
            for tex in [
                R"e^{+i \omega t}",
                R"e^{-i \omega t}",
            ]
        )
        for title, plane in zip(titles, planes):
            title.next_to(plane, UP)

        self.add(titles)

        # Create rotating vectors
        left_vector = self.get_rotating_vector(left_plane, 1j * omega, t_tracker, color=TEAL)
        right_vector = self.get_rotating_vector(right_plane, -1j * omega, t_tracker, color=RED)
        vectors = VGroup(left_vector, right_vector)

        left_tail, right_tail = tails = VGroup(
            TracingTail(vect.get_end, stroke_color=vect.get_color(), time_traced=2)
            for vect in vectors
        )

        self.add(Point())
        self.add(vectors, tails)

        # Add time display
        time_display = Tex("t = 0.00", font_size=36).to_corner(UR)
        time_label = time_display.make_number_changeable("0.00")
        time_label.add_updater(lambda m: m.set_value(t_tracker.get_value()))

        # Animate rotation
        self.wait(12)

        # Add spring
        spring = SrpingMassSystem(
            equilibrium_position=planes[0].get_bottom() + DOWN,
            equilibrium_length=3,
            n_spring_curls=8,
            mass_width=0.5,
            spring_radius=0.2,
        )
        spring.pause()
        unit_size = planes[0].x_axis.get_unit_size()
        spring.add_updater(lambda m: m.set_x(unit_size * get_x()))

        v_line = Line()
        v_line.set_stroke(BLUE_A, 2)
        v_line.f_always.put_start_and_end_on(spring.mass.get_top, left_vector.get_end)

        self.play(VFadeIn(spring), VFadeIn(v_line))
        self.wait(20)
        self.play(
            VFadeOut(spring),
            VFadeOut(v_line),
            VFadeOut(tails),
        )

        # Add them up
        new_plane_center = planes.get_center()
        shift_factor = ValueTracker(0)
        right_vector.add_updater(lambda m: m.shift(shift_factor.get_value() * left_vector.get_vector()))

        sum_expr = VGroup(titles[0], Tex(R"+"), titles[1])
        sum_expr.target = sum_expr.generate_target()
        sum_expr.target.arrange(RIGHT, buff=MED_SMALL_BUFF, aligned_edge=DOWN)
        sum_expr.target.next_to(planes, UP, MED_SMALL_BUFF)
        sum_expr[1].set_opacity(0).next_to(planes, UP)

        result_dot = GlowDot()
        result_dot.f_always.move_to(right_vector.get_end)

        self.play(
            planes[0].animate.move_to(new_plane_center),
            planes[1].animate.move_to(new_plane_center).set_opacity(0),
            MoveToTarget(sum_expr),
            run_time=2,
        )
        self.play(shift_factor.animate.set_value(1))
        self.play(FadeIn(result_dot))
        self.wait(4)

        # Add another spring
        spring = SrpingMassSystem(
            equilibrium_position=planes[0].get_bottom() + DOWN,
            equilibrium_length=5,
            n_spring_curls=8,
            mass_width=0.5,
            spring_radius=0.2,
        )
        spring.pause()
        unit_size = planes[0].x_axis.get_unit_size()
        spring.add_updater(lambda m: m.set_x(2 * unit_size * get_x()))

        v_line = Line()
        v_line.set_stroke(BLUE_A, 2)
        v_line.f_always.put_start_and_end_on(spring.mass.get_top, result_dot.get_center)

        self.play(VFadeIn(spring), VFadeIn(v_line))
        self.wait(2)

        # Right hand side
        rhs = Tex(R"= 2 \cos(\omega t)", t2c={R"\omega": PINK})
        rhs.next_to(sum_expr, RIGHT, buff=MED_SMALL_BUFF).shift(SMALL_BUFF * DOWN)

        self.play(Write(rhs))
        self.wait(20)

    def get_rotating_vector(self, plane, s, t_tracker, color=TEAL, thickness=3):
        """Create a rotating vector for e^(st) on the given plane"""
        def update_vector(vector):
            t = t_tracker.get_value()
            c = vector.coef_tracker.get_value()
            z = c * np.exp(s * t)
            vector.put_start_and_end_on(plane.n2p(0), plane.n2p(z))

        vector = Arrow(LEFT, RIGHT, fill_color=color, thickness=thickness)
        vector.coef_tracker = ComplexValueTracker(1)
        vector.add_updater(update_vector)

        return vector
