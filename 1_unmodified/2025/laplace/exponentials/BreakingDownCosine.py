# ==============================================================================
# Scene:      BreakingDownCosine
# Source:     videos/_2025/laplace/exponentials.py (lines 1935-1982)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/shm.py
#
# Run from this folder:
#     manimgl BreakingDownCosine.py BreakingDownCosine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/laplace/shm.py -----

def get_coef_colors(n_coefs=3):
    return [
        interpolate_color_by_hsl(TEAL, RED, a)
        for a in np.linspace(0, 1, n_coefs)
    ]


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


class ShowFamilyOfComplexSolutions(RotatingExponentials):
    tex_to_color_map = {R"\omega": PINK}
    plane_config = dict(
        background_line_style=dict(stroke_color=BLUE, stroke_width=1),
        faded_line_style=dict(stroke_color=BLUE, stroke_width=0.5, stroke_opacity=0.25),
    )
    vect_colors = [TEAL, RED]
    rotation_frequency = TAU / 4

    def construct(self):
        # Show the equation
        frame = self.frame
        frame.set_x(-10)

        colors = get_coef_colors()
        t2c = {"x''(t)": colors[2], "x'(t)": colors[1], "x(t)": colors[0]}
        equation = Tex(R"m x''(t) + k x(t) = 0", t2c=t2c, font_size=42)
        equation.next_to(frame.get_left(), RIGHT, buff=1.0)

        arrow = Vector(3.0 * RIGHT, thickness=6, fill_color=GREY_B)
        arrow.next_to(equation, RIGHT, MED_LARGE_BUFF)

        strategy_words = VGroup(
            Text("“Strategy”"),
            TexText(R"Guess $e^{{s}t}$", t2c={R"{s}": YELLOW}, font_size=36, fill_color=GREY_A)
        )
        strategy_words.arrange(DOWN)
        strategy_words.next_to(arrow, UP, MED_SMALL_BUFF)

        self.add(equation)
        self.play(
            GrowArrow(arrow),
            FadeIn(strategy_words, lag_ratio=0.1)
        )
        self.wait()

        # Show two basis solutions on the left
        t2c = self.tex_to_color_map
        left_planes, left_plane_labels = self.get_left_planes(label_texs=[R"e^{+i\omega t}", R"e^{-i\omega t}"])
        rot_vects, tails, t_tracker = self.get_rot_vects(left_planes)
        left_planes_brace = Brace(left_planes, LEFT, MED_SMALL_BUFF)

        self.add(rot_vects, tails)
        self.add(t_tracker)
        self.play(
            GrowFromCenter(left_planes_brace),
            FadeIn(left_planes),
            FadeTransform(strategy_words[1][R"e^{{s}t}"].copy(), left_plane_labels[0]),
            FadeTransform(strategy_words[1][R"e^{{s}t}"].copy(), left_plane_labels[1]),
            VFadeIn(rot_vects),
        )
        self.wait(3)

        self.wait(8)

        # Show combination with tunable parameters
        right_plane = self.get_right_plane()
        right_plane.next_to(left_planes, RIGHT, buff=1.5)

        scaled_solution = Tex(
            R"c_1 e^{+i\omega t} + c_2 e^{-i\omega t}",
            t2c={R"\omega": PINK, "c_1": BLUE, "c_2": BLUE}
        )
        scaled_solution.next_to(right_plane, UP)

        vect1, vect2 = right_rot_vects = self.get_rot_vect_sum(right_plane, t_tracker)
        c1_eq, c2_eq = coef_eqs = VGroup(
            VGroup(Tex(fR"c_{n} = "), DecimalNumber(1))
            for n in [1, 2]
        )
        coef_eqs.scale(0.85)
        for coef_eq in coef_eqs:
            coef_eq.arrange(RIGHT, buff=SMALL_BUFF)
            coef_eq[1].align_to(coef_eq[0][0], DOWN)
            coef_eq[0][:2].set_fill(BLUE)
        coef_eqs.arrange(DOWN, MED_LARGE_BUFF)
        coef_eqs.to_corner(UR)
        coef_eqs.shift(LEFT)

        c1_eq[1].add_updater(lambda m: m.set_value(vect1.coef_tracker.get_value()))
        c2_eq[1].add_updater(lambda m: m.set_value(vect2.coef_tracker.get_value()))

        self.play(
            FadeIn(right_plane),
            FadeOut(left_planes_brace),
            frame.animate.center(),
            run_time=2
        )
        self.play(LaggedStart(
            FadeTransform(left_plane_labels[0].copy(), scaled_solution[R"e^{+i\omega t}"]),
            FadeIn(scaled_solution[R"c_1"]),
            TransformFromCopy(rot_vects[0], right_rot_vects[0], suspend_mobject_updating=True),
            FadeTransform(left_plane_labels[1].copy(), scaled_solution[R"e^{-i\omega t}"]),
            FadeIn(scaled_solution[R"+"][1]),
            FadeIn(scaled_solution[R"c_2"]),
            TransformFromCopy(rot_vects[1], right_rot_vects[1], suspend_mobject_updating=True)
        ))
        self.play(LaggedStart(
            FadeTransformPieces(scaled_solution[R"c_1"].copy(), c1_eq),
            FadeTransformPieces(scaled_solution[R"c_2"].copy(), c2_eq)
        ))
        self.play(LaggedStart(
            vect1.coef_tracker.animate.set_value(2),
            vect2.coef_tracker.animate.set_value(0.5),
            lag_ratio=0.5
        ))

        comb_tail = TracingTail(vect2.get_end, stroke_color=YELLOW, time_traced=2)
        glow_dot = GlowDot()
        glow_dot.f_always.move_to(vect2.get_end)
        self.add(comb_tail)
        self.play(FadeIn(glow_dot))

        self.wait(6)
        self.play(LaggedStart(
            vect1.coef_tracker.animate.set_value(complex(1.5, 1)),
            vect2.coef_tracker.animate.set_value(complex(0.5, -1.25)),
        ))
        self.wait(7)

        # Change the coefficients
        t_tracker.suspend_updating()
        self.play(
            FadeOut(comb_tail, suspend_mobject_updating=True),
            LaggedStart(
                vect1.coef_tracker.animate.set_value(complex(0.31, -0.41)),
                vect2.coef_tracker.animate.set_value(complex(2.71, -0.82)),
            ),
        )
        self.wait()
        self.play(
            LaggedStart(
                vect1.coef_tracker.animate.set_value(complex(-1.03, 0.5)),
                vect2.coef_tracker.animate.set_value(complex(1.5, 0.35)),
            ),
        )
        self.add(comb_tail)
        self.wait(2)
        t_tracker.resume_updating()

        # Zoom out
        self.play(frame.animate.set_height(13.75, about_edge=RIGHT), run_time=2)
        self.wait(4)
        self.play(frame.animate.to_default_state(), run_time=2)

        # Go to real valued
        self.play(
            LaggedStart(
                vect1.coef_tracker.animate.set_value(1),
                vect2.coef_tracker.animate.set_value(1),
            ),
        )
        self.wait(6)

        # Show initial conditions
        initial_conditions = VGroup(
            Tex(R"x_0 = 0.00"),
            Tex(R"v_0 = 0.00"),
        )
        x0_value = initial_conditions[0].make_number_changeable("0.00")
        v0_value = initial_conditions[1].make_number_changeable("0.00")
        x0_value.set_value(2)
        initial_conditions.scale(0.85)
        initial_conditions.arrange(DOWN)
        initial_conditions.move_to(coef_eqs, LEFT)
        initial_conditions.to_edge(UP)
        implies = Tex(R"\Downarrow", font_size=72)
        implies.next_to(initial_conditions, DOWN)

        t_tracker.suspend_updating()
        t_tracker.set_value((t_tracker.get_value() + 2) % 4 - 2)
        self.play(
            FadeIn(initial_conditions),
            Write(implies),
            coef_eqs.animate.next_to(implies, DOWN).align_to(initial_conditions, LEFT),
        )
        self.remove(comb_tail)
        self.play(
            vect1.coef_tracker.animate.set_value(1),
            vect2.coef_tracker.animate.set_value(1),
            t_tracker.animate.set_value(0),
        )
        self.wait()
        self.remove(comb_tail)

        # Highlight values, rise
        t_tracker.resume_updating()

        highlight_rect = SurroundingRectangle(initial_conditions[0])
        highlight_rect.set_stroke(YELLOW, 2)

        self.play(ShowCreation(highlight_rect))
        self.wait()
        self.play(highlight_rect.animate.surround(initial_conditions[1]))
        self.wait(2)
        self.play(highlight_rect.animate.surround(coef_eqs))
        self.wait(4)

        self.play(
            vect1.coef_tracker.animate.set_value(1.5),
            vect2.coef_tracker.animate.set_value(1.5),
            ChangeDecimalToValue(x0_value, 3)
        )
        self.wait(12)

    def get_left_planes(self, label_texs: list[str]):
        planes = VGroup(
            ComplexPlane((-1, 1), (-1, 1), **self.plane_config)
            for _ in range(2)
        )
        planes.arrange(DOWN, buff=1.0)
        planes.set_height(6.5)
        planes.to_corner(DL)
        planes.set_z_index(-1)

        labels = VGroup(Tex(tex, t2c=self.tex_to_color_map) for tex in label_texs)
        for label, plane in zip(labels, planes):
            label.next_to(plane, UP, SMALL_BUFF)

        return planes, labels

    def get_rot_vects(self, planes):
        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        rot_vects = VGroup(
            self.get_rotating_vector(plane, u * 1j * self.rotation_frequency, t_tracker, color)
            for plane, u, color in zip(planes, [+1, -1], self.vect_colors)
        )
        tails = VGroup(
            TracingTail(vect.get_end, stroke_color=vect.get_color(), time_traced=2)
            for vect in rot_vects
        )

        return Group(rot_vects, tails, t_tracker)

    def get_rot_vect_sum(self, plane, t_tracker):
        vect1, vect2 = vect_sum = VGroup(
            self.get_rotating_vector(
                plane,
                u * 1j * self.rotation_frequency,
                t_tracker,
                color,
            )
            for u, color in zip([+1, -1], self.vect_colors)
        )
        vect2.add_updater(lambda m: m.put_start_on(vect1.get_end()))
        return vect_sum

    def get_right_plane(self, x_range=(-3, 3), height=5.5):
        right_plane = ComplexPlane(x_range, x_range, **self.plane_config)
        right_plane.set_height(height)
        return right_plane

    def add_scale_tracker(vector, initial_value=1):
        """
        Assumes the vector has another updater constantly setting a location in the plane
        """
        vector.c_tracker = ComplexValueTracker(initial_value)

        def update_vector(vect):
            c = vect.c_tracker.get_value()
            vect.scale()
            pass



# ----- From _2025/laplace/exponentials.py -----

class BreakingDownCosine(ShowFamilyOfComplexSolutions):
    tex_to_color_map = {"+i": YELLOW, "-i": YELLOW}

    def construct(self):
        # Set up various planes
        left_planes, left_plane_labels = self.get_left_planes(label_texs=[R"e^{+it}", R"e^{-it}"])
        rot_vects, tails, t_tracker = self.get_rot_vects(left_planes)

        right_plane = self.get_right_plane(x_range=(-2, 2))
        right_plane.next_to(left_planes, RIGHT, buff=2.0)
        right_plane.add_coordinate_labels(font_size=16)
        vect_sum = self.get_rot_vect_sum(right_plane, t_tracker)
        for vect in vect_sum:
            vect.coef_tracker.set_value(0.5)

        output_dot = Group(TrueDot(), GlowDot()).set_color(YELLOW)
        output_dot.f_always.move_to(vect_sum[1].get_end)

        self.add(t_tracker)
        self.add(left_planes, left_plane_labels)
        self.add(rot_vects, tails, t_tracker)

        self.add(right_plane)
        self.add(vect_sum)
        self.add(output_dot)
        self.wait(12)

        # Show each part
        for vect in vect_sum:
            vect.coef_tracker.set_value(1)

        inner_arrows = VGroup(Arrow(2 * v, v, buff=0) for v in compass_directions(8))
        inner_arrows.set_fill(YELLOW)
        inner_arrows.move_to(right_plane)

        self.remove(vect_sum, output_dot)
        for i in [0, 1]:
            # self.play(ReplacementTransform(rot_vects[i].copy().clear_updaters(), vect_sum[i]))
            self.play(TransformFromCopy(rot_vects[i], vect_sum[i], suspend_mobject_updating=True))
            self.wait(3)

        self.wait(15)
        self.play(
            *(vs.coef_tracker.animate.set_value(0.5) for vs in vect_sum),
            LaggedStartMap(GrowArrow, inner_arrows, lag_ratio=1e-2, run_time=1)
        )
        self.play(FadeOut(inner_arrows))
        self.wait(12)
