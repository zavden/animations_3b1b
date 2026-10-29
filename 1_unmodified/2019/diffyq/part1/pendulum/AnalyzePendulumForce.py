# ==============================================================================
# Scene:      AnalyzePendulumForce
# Source:     videos/_2019/diffyq/part1/pendulum.py (lines 989-1548)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl AnalyzePendulumForce.py AnalyzePendulumForce -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

class You(PiCreature):
    CONFIG = {
        "color": BLUE_C,
    }



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


class GravityVector(Vector):
    CONFIG = {
        "color": YELLOW,
        "length_multiple": 1 / 9.8,
        # TODO, continually update the length based
        # on the pendulum's gravity?
    }

    def __init__(self, pendulum, **kwargs):
        super().__init__(DOWN, **kwargs)
        self.pendulum = pendulum
        self.scale(self.length_multiple * pendulum.gravity)
        self.attach_to_pendulum(pendulum)

    def attach_to_pendulum(self, pendulum):
        self.add_updater(lambda m: m.shift(
            pendulum.weight.get_center() - self.get_start(),
        ))

    def add_component_lines(self):
        self.component_lines = always_redraw(self.create_component_lines)
        self.add(self.component_lines)

    def create_component_lines(self):
        theta = self.pendulum.get_theta()
        x_new = rotate(RIGHT, theta)
        base = self.get_start()
        tip = self.get_end()
        vect = tip - base
        corner = base + x_new * np.dot(vect, x_new)
        kw = {"dash_length": 0.025}
        return VGroup(
            DashedLine(base, corner, **kw),
            DashedLine(corner, tip, **kw),
        )


class AnalyzePendulumForce(MovingCameraScene):
    CONFIG = {
        "pendulum_config": {
            "length": 5,
            "top_point": 3.5 * UP,
            "initial_theta": 60 * DEGREES,
            "set_theta_label_height_cap": True,
        },
        "g_vect_config": {
            "length_multiple": 0.25,
        },
        "tan_line_color": BLUE,
        "perp_line_color": PINK,
    }

    def construct(self):
        self.add_pendulum()
        self.show_arc_length()
        self.add_g_vect()
        self.show_constraint()
        self.break_g_vect_into_components()
        self.show_angle_geometry()
        self.show_gsin_formula()
        self.show_sign()
        self.show_acceleration_formula()
        # self.ask_about_what_to_do()

        # self.emphasize_theta()
        # self.show_angular_velocity()
        # self.show_angular_acceleration()
        # self.circle_g_sin_formula()

    def add_pendulum(self):
        pendulum = Pendulum(**self.pendulum_config)
        theta_tracker = ValueTracker(pendulum.get_theta())
        pendulum.add_updater(lambda p: p.set_theta(
            theta_tracker.get_value()
        ))

        self.add(pendulum)
        self.pendulum = pendulum
        self.theta_tracker = theta_tracker

    def show_arc_length(self):
        pendulum = self.pendulum
        angle = pendulum.get_theta()
        height = pendulum.length
        top = pendulum.get_fixed_point()

        line = Line(UP, DOWN)
        line.set_height(height)
        line.move_to(top, UP)
        arc = always_redraw(lambda: Arc(
            start_angle=-90 * DEGREES,
            angle=pendulum.get_theta(),
            arc_center=pendulum.get_fixed_point(),
            radius=pendulum.length,
            stroke_color=GREEN,
        ))

        brace = Brace(Line(ORIGIN, 5 * UP), RIGHT)
        brace.point = VectorizedPoint(brace.get_right())
        brace.add(brace.point)
        brace.set_height(angle)
        brace.move_to(ORIGIN, DL)
        brace.apply_complex_function(np.exp)
        brace.scale(height)
        brace.rotate(-90 * DEGREES)
        brace.move_to(arc)
        brace.shift(MED_SMALL_BUFF * normalize(
            arc.point_from_proportion(0.5) - top
        ))
        x_sym = OldTex("x")
        x_sym.set_color(GREEN)
        x_sym.next_to(brace.point, DR, buff=SMALL_BUFF)

        rhs = OldTex("=", "L", "\\theta")
        rhs.set_color_by_tex("\\theta", BLUE)
        rhs.next_to(x_sym, RIGHT)
        rhs.shift(0.7 * SMALL_BUFF * UP)
        line_L = OldTex("L")
        line_L.next_to(
            pendulum.rod.get_center(), UR, SMALL_BUFF,
        )

        self.play(
            ShowCreation(arc),
            Rotate(line, angle, about_point=top),
            UpdateFromAlphaFunc(
                line, lambda m, a: m.set_stroke(
                    width=2 * there_and_back(a)
                )
            ),
            GrowFromPoint(
                brace, line.get_bottom(),
                path_arc=angle
            ),
        )
        self.play(FadeIn(x_sym, UP))
        self.wait()

        # Show equation
        line.set_stroke(BLUE, 5)
        self.play(
            ShowCreationThenFadeOut(line),
            FadeInFromDown(line_L)
        )
        self.play(
            TransformFromCopy(
                line_L, rhs.get_part_by_tex("L")
            ),
            Write(rhs.get_part_by_tex("="))
        )
        self.play(
            TransformFromCopy(
                pendulum.theta_label,
                rhs.get_parts_by_tex("\\theta"),
            )
        )
        self.add(rhs)

        x_eq = VGroup(x_sym, rhs)

        self.play(
            FadeOut(brace),
            x_eq.rotate, angle / 2,
            x_eq.next_to, arc.point_from_proportion(0.5),
            UL, {"buff": -MED_SMALL_BUFF}
        )

        self.x_eq = x_eq
        self.arc = arc
        self.line_L = line_L

    def add_g_vect(self):
        pendulum = self.pendulum

        g_vect = self.g_vect = GravityVector(
            pendulum, **self.g_vect_config,
        )
        g_word = self.g_word = OldTexText("Gravity")
        g_word.rotate(-90 * DEGREES)
        g_word.scale(0.75)
        g_word.add_updater(lambda m: m.next_to(
            g_vect, RIGHT, buff=-SMALL_BUFF,
        ))

        self.play(
            GrowArrow(g_vect),
            FadeIn(g_word, UP, lag_ratio=0.1),
        )
        self.wait()

    def show_constraint(self):
        pendulum = self.pendulum

        arcs = VGroup()
        for u in [-1, 2, -1]:
            d_theta = 40 * DEGREES * u
            arc = Arc(
                start_angle=pendulum.get_theta() - 90 * DEGREES,
                angle=d_theta,
                radius=pendulum.length,
                arc_center=pendulum.get_fixed_point(),
                stroke_width=2,
                stroke_color=YELLOW,
                stroke_opacity=0.5,
            )
            self.play(
                self.theta_tracker.increment_value, d_theta,
                ShowCreation(arc)
            )
            arcs.add(arc)
        self.play(FadeOut(arcs))

    def break_g_vect_into_components(self):
        g_vect = self.g_vect
        g_vect.component_lines = always_redraw(
            g_vect.create_component_lines
        )
        tan_line, perp_line = g_vect.component_lines
        g_vect.tangent = always_redraw(lambda: Arrow(
            tan_line.get_start(),
            tan_line.get_end(),
            buff=0,
            color=self.tan_line_color,
        ))
        g_vect.perp = always_redraw(lambda: Arrow(
            perp_line.get_start(),
            perp_line.get_end(),
            buff=0,
            color=self.perp_line_color,
        ))

        self.play(ShowCreation(g_vect.component_lines))
        self.play(GrowArrow(g_vect.tangent))
        self.wait()
        self.play(GrowArrow(g_vect.perp))
        self.wait()

    def show_angle_geometry(self):
        g_vect = self.g_vect

        arc = Arc(
            start_angle=90 * DEGREES,
            angle=self.pendulum.get_theta(),
            radius=0.5,
            arc_center=g_vect.get_end(),
        )
        q_mark = OldTex("?")
        q_mark.next_to(arc.get_center(), UL, SMALL_BUFF)
        theta_label = OldTex("\\theta")
        theta_label.move_to(q_mark)

        self.add(g_vect)
        self.play(
            ShowCreation(arc),
            Write(q_mark)
        )
        self.play(ShowCreationThenFadeAround(q_mark))
        self.wait()
        self.play(ShowCreationThenFadeAround(
            self.pendulum.theta_label
        ))
        self.play(
            TransformFromCopy(
                self.pendulum.theta_label,
                theta_label,
            ),
            FadeOut(q_mark)
        )
        self.wait()
        self.play(WiggleOutThenIn(g_vect.tangent))
        self.play(WiggleOutThenIn(
            Line(
                *g_vect.get_start_and_end(),
                buff=0,
            ).add_tip().match_style(g_vect),
            remover=True
        ))
        self.wait()
        self.play(
            FadeOut(arc),
            FadeOut(theta_label),
        )

    def show_gsin_formula(self):
        g_vect = self.g_vect
        g_word = self.g_word
        g_word.clear_updaters()

        g_term = self.g_term = OldTex("-g")
        g_term.add_updater(lambda m: m.next_to(
            g_vect,
            RIGHT if self.pendulum.get_theta() >= 0 else LEFT,
            SMALL_BUFF
        ))

        def create_vect_label(vect, tex, direction):
            label = OldTex(tex)
            label.set_stroke(width=0, background=True)
            label.add_background_rectangle()
            label.scale(0.7)
            max_width = 0.9 * vect.get_length()
            if label.get_width() > max_width:
                label.set_width(max_width)
            angle = vect.get_angle()
            angle = (angle + PI / 2) % PI - PI / 2
            label.next_to(ORIGIN, direction, SMALL_BUFF)
            label.rotate(angle, about_point=ORIGIN)
            label.shift(vect.get_center())
            return label

        g_sin_label = always_redraw(lambda: create_vect_label(
            g_vect.tangent, "-g\\sin(\\theta)", UP,
        ))
        g_cos_label = always_redraw(lambda: create_vect_label(
            g_vect.perp, "-g\\cos(\\theta)", DOWN,
        ))

        self.play(
            ReplacementTransform(g_word[0][0], g_term[0][1]),
            FadeOut(g_word[0][1:]),
            Write(g_term[0][0]),
        )
        self.add(g_term)
        self.wait()
        for label in g_sin_label, g_cos_label:
            self.play(
                GrowFromPoint(label[0], g_term.get_center()),
                TransformFromCopy(g_term, label[1][:2]),
                GrowFromPoint(label[1][2:], g_term.get_center()),
                remover=True
            )
            self.add(label)
            self.wait()

        self.g_sin_label = g_sin_label
        self.g_cos_label = g_cos_label

    def show_sign(self):
        get_theta = self.pendulum.get_theta
        theta_decimal = DecimalNumber(include_sign=True)
        theta_decimal.add_updater(lambda d: d.set_value(
            get_theta()
        ))
        theta_decimal.add_updater(lambda m: m.next_to(
            self.pendulum.theta_label, DOWN
        ))
        theta_decimal.add_updater(lambda m: m.set_color(
            GREEN if get_theta() > 0 else RED
        ))

        self.play(
            FadeIn(theta_decimal, UP),
            FadeOut(self.x_eq),
            FadeOut(self.line_L),
        )
        self.set_theta(-60 * DEGREES, run_time=4)
        self.set_theta(60 * DEGREES, run_time=4)
        self.play(
            FadeOut(theta_decimal),
            FadeIn(self.x_eq),
        )

    def show_acceleration_formula(self):
        x_eq = self.x_eq
        g_sin_theta = self.g_sin_label

        equation = OldTex(
            "a", "=",
            "\\ddot", "x",
            "=",
            "-", "g", "\\sin\\big(", "\\theta", "\\big)",
        )
        equation.to_edge(LEFT)

        second_deriv = equation[2:4]
        x_part = equation.get_part_by_tex("x")
        x_part.set_color(GREEN)
        a_eq = equation[:2]
        eq2 = equation.get_parts_by_tex("=")[1]
        rhs = equation[5:]

        second_deriv_L_form = OldTex(
            "L", "\\ddot", "\\theta"
        )
        second_deriv_L_form.move_to(second_deriv, DOWN)
        eq3 = OldTex("=")
        eq3.rotate(90 * DEGREES)
        eq3.next_to(second_deriv_L_form, UP)

        g_L_frac = OldTex(
            "-", "{g", "\\over", "L}"
        )
        g_L_frac.move_to(rhs[:2], LEFT)
        g_L_frac.shift(SMALL_BUFF * UP / 2)

        mu_term = OldTex(
            "-\\mu", "\\dot", "\\theta",
        )
        mu_term.next_to(g_L_frac, LEFT)
        mu_term.shift(SMALL_BUFF * UP / 2)

        mu_brace = Brace(mu_term, UP)
        mu_word = mu_brace.get_text("Air resistance")

        for mob in equation, second_deriv_L_form, mu_term:
            mob.set_color_by_tex("\\theta", BLUE)

        self.play(
            TransformFromCopy(x_eq[0], x_part),
            Write(equation[:3]),
        )
        self.wait()
        self.play(
            Write(eq2),
            TransformFromCopy(g_sin_theta, rhs)
        )
        self.wait()
        #
        self.show_acceleration_at_different_angles()
        #
        self.play(
            FadeInFromDown(second_deriv_L_form),
            Write(eq3),
            second_deriv.next_to, eq3, UP,
            a_eq.shift, SMALL_BUFF * LEFT,
            eq2.shift, SMALL_BUFF * RIGHT,
            rhs.shift, SMALL_BUFF * RIGHT,
        )
        self.wait()
        self.wait()
        self.play(
            FadeOut(a_eq),
            FadeOut(second_deriv),
            FadeOut(eq3),
            ReplacementTransform(
                second_deriv_L_form.get_part_by_tex("L"),
                g_L_frac.get_part_by_tex("L"),
            ),
            ReplacementTransform(
                equation.get_part_by_tex("-"),
                g_L_frac.get_part_by_tex("-"),
            ),
            ReplacementTransform(
                equation.get_part_by_tex("g"),
                g_L_frac.get_part_by_tex("g"),
            ),
            Write(g_L_frac.get_part_by_tex("\\over")),
            rhs[2:].next_to, g_L_frac, RIGHT, {"buff": SMALL_BUFF},
        )
        self.wait()
        self.play(
            GrowFromCenter(mu_term),
            VGroup(eq2, second_deriv_L_form[1:]).next_to,
            mu_term, LEFT,
        )
        self.play(
            GrowFromCenter(mu_brace),
            FadeInFromDown(mu_word),
        )

    def show_acceleration_at_different_angles(self):
        to_fade = VGroup(
            self.g_cos_label,
            self.g_vect.perp,
        )
        new_comp_line_sytle = {
            "stroke_width": 0.5,
            "stroke_opacity": 0.25,
        }

        self.play(
            FadeOut(self.x_eq),
            to_fade.set_opacity, 0.25,
            self.g_vect.component_lines.set_style,
            new_comp_line_sytle
        )
        self.g_vect.component_lines.add_updater(
            lambda m: m.set_style(**new_comp_line_sytle)
        )
        for mob in to_fade:
            mob.add_updater(lambda m: m.set_opacity(0.25))

        self.set_theta(0)
        self.wait(2)
        self.set_theta(89.9 * DEGREES, run_time=3)
        self.wait(2)
        self.set_theta(
            60 * DEGREES,
            FadeIn(self.x_eq),
            run_time=2,
        )
        self.wait()

    def ask_about_what_to_do(self):
        g_vect = self.g_vect
        g_sin_label = self.g_sin_label
        angle = g_vect.tangent.get_angle()
        angle = (angle - PI) % TAU

        randy = You()
        randy.to_corner(DL)
        bubble = randy.get_bubble(
            height=2,
            width=3.5,
        )
        g_sin_copy = g_sin_label.copy()
        g_sin_copy.remove(g_sin_copy[0])
        g_sin_copy.generate_target()
        g_sin_copy.target.scale(1 / 0.75)
        g_sin_copy.target.rotate(-angle)
        a_eq = OldTex("a=")
        thought_term = VGroup(a_eq, g_sin_copy.target)
        thought_term.arrange(RIGHT, buff=SMALL_BUFF)
        thought_term.move_to(bubble.get_bubble_center())

        rect = SurroundingRectangle(g_sin_copy.target)
        rect.rotate(angle)
        rect.move_to(g_sin_label)

        randy.save_state()
        randy.fade(1)
        self.play(randy.restore, randy.change, "pondering")
        self.play(ShowCreationThenFadeOut(rect))
        self.play(
            ShowCreation(bubble),
            Write(a_eq),
            MoveToTarget(g_sin_copy),
            randy.look_at, bubble,
        )
        thought_term.remove(g_sin_copy.target)
        thought_term.add(g_sin_copy)
        self.play(Blink(randy))
        self.wait()
        self.play(
            ShowCreationThenDestruction(
                thought_term.copy().set_style(
                    stroke_color=YELLOW,
                    stroke_width=2,
                    fill_opacity=0,
                ),
                run_time=2,
                lag_ratio=0.2,
            ),
            randy.change, "confused", thought_term,
        )
        self.play(Blink(randy))
        self.play(
            FadeOut(randy),
            FadeOut(bubble),
            thought_term.next_to, self.pendulum, DOWN, LARGE_BUFF
        )

        self.accleration_equation = thought_term

    def emphasize_theta(self):
        pendulum = self.pendulum

        self.play(FocusOn(pendulum.theta_label))
        self.play(Indicate(pendulum.theta_label))

        pendulum_copy = pendulum.deepcopy()
        pendulum_copy.clear_updaters()
        pendulum_copy.fade(1)
        pendulum_copy.start_swinging()

        def new_updater(p):
            p.set_theta(pendulum_copy.get_theta())
        pendulum.add_updater(new_updater)

        self.add(pendulum_copy)
        self.wait(5)
        pendulum_copy.end_swinging()
        self.remove(pendulum_copy)
        pendulum.remove_updater(new_updater)
        self.update_mobjects(0)

    def show_angular_velocity(self):
        pass

    def show_angular_acceleration(self):
        pass

    def circle_g_sin_formula(self):
        self.play(
            ShowCreationThenFadeAround(
                self.accleration_equation
            )
        )

    #
    def set_theta(self, value, *added_anims, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 2)
        self.play(
            self.theta_tracker.set_value, value,
            *added_anims,
            **kwargs,
        )
