# ==============================================================================
# Scene:      SimpleProjectileEquation
# Source:     videos/_2019/diffyq/part1/staging.py (lines 570-1050)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl SimpleProjectileEquation.py SimpleProjectileEquation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Keep ball.randy and recover its reference in show_trajectory; before, it was a local variable of another method.
#   - Use the Cairo vector field as a group of arrows, with delta_x/delta_y and get_vector, instead of the current GL API.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import CairoVectorField as VectorField


# ----- From _2019/diffyq/part1/shared_constructs.py -----

Lg_formula_config = {
    "tex_to_color_map": {
        "\\theta_0": WHITE,
        "{L}": BLUE,
        "{g}": YELLOW,
    },
}



# ----- From _2019/diffyq/part1/staging.py -----

class ShowGravityAcceleration(Scene):
    CONFIG = {
        "flash": True,
        "add_ball_copies": True,
    }

    def construct(self):
        self.add_gravity_field()
        self.add_title()
        self.pulse_gravity_down()
        self.show_g_value()
        self.show_trajectory()
        self.combine_v_vects()
        self.show_g_symbol()

    def add_gravity_field(self):
        gravity_field = self.gravity_field = VectorField(
            lambda p: DOWN,
            # delta_x=2,
            # delta_y=2,
        )
        gravity_field.set_opacity(0.5)
        gravity_field.sort(
            lambda p: -p[1],
        )
        self.add(gravity_field)

    def add_title(self):
        title = self.title = OldTexText("Gravitational acceleration")
        title.scale(1.5)
        title.to_edge(UP)
        title.add_background_rectangle(
            buff=0.05,
            opacity=1,
        )
        self.play(FadeInFromDown(title))

    def pulse_gravity_down(self):
        field = self.gravity_field
        self.play(LaggedStart(*[
            ApplyFunction(
                lambda v: v.set_opacity(1).scale(1.2),
                vector,
                rate_func=there_and_back,
            )
            for vector in field
        ]), run_time=2, lag_ratio=0.001)
        self.add(self.title)

    def show_g_value(self):
        title = self.title
        g_eq = self.g_eq = OldTex(
            "-9.8", "{\\text{m/s}", "\\over", "\\text{s}}",
            **Lg_formula_config
        )
        g_eq.add_background_rectangle_to_submobjects()
        g_eq.scale(2)
        g_eq.center()
        num, ms, per, s = g_eq

        self.add(num)
        self.wait(0.75)
        self.play(
            FadeIn(ms, 0.25 * DOWN, run_time=0.5)
        )
        self.wait(0.25)
        self.play(LaggedStart(
            GrowFromPoint(per, per.get_left()),
            FadeIn(s, 0.5 * UP),
            lag_ratio=0.7,
            run_time=0.75
        ))
        self.wait()
        self.play(
            g_eq.scale, 0.5,
            g_eq.next_to, title, DOWN,
        )

    def show_trajectory(self):
        total_time = 6

        ball = self.get_ball()
        # CHANGE: recover the character created inside get_ball.
        randy = ball.randy

        p0 = 3 * DOWN + 5 * LEFT
        v0 = 2.8 * UP + 1.5 * RIGHT
        g = 0.9 * DOWN
        graph = ParametricCurve(
            lambda t: p0 + v0 * t + 0.5 * g * t**2,
            t_min=0,
            t_max=total_time,
        )
        # graph.center().to_edge(DOWN)
        dashed_graph = DashedVMobject(graph, num_dashes=60)
        dashed_graph.set_stroke(WHITE, 1)

        ball.move_to(graph.get_start())
        randy.add_updater(
            lambda m, dt: m.rotate(dt).move_to(ball)
        )
        times = np.arange(0, total_time + 1)

        velocity_graph = ParametricCurve(
            lambda t: v0 + g * t,
            t_min=0, t_max=total_time,
        )
        v_point = VectorizedPoint()
        v_point.move_to(velocity_graph.get_start())

        def get_v_vect():
            result = Vector(
                v_point.get_location(),
                color=RED,
                tip_length=0.2,
            )
            result.scale(0.5, about_point=result.get_start())
            result.shift(ball.get_center())
            result.set_stroke(width=2, family=False)
            return result
        v_vect = always_redraw(get_v_vect)
        self.add(v_vect)

        flash_rect = FullScreenRectangle(
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.2,
        )
        flash = FadeOut(
            flash_rect,
            rate_func=squish_rate_func(smooth, 0, 0.1)
        )

        time_label = OldTexText("Time = ")
        time_label.shift(MED_SMALL_BUFF * LEFT)
        time_tracker = ValueTracker(0)
        time = DecimalNumber(0)
        time.next_to(time_label, RIGHT)
        time.add_updater(lambda d, dt: d.set_value(
            time_tracker.get_value()
        ))
        time_group = VGroup(time_label, time)
        time_group.center().to_edge(DOWN)
        self.add(time_group)

        ball_copies = VGroup()
        v_vect_copies = VGroup()
        self.add(dashed_graph, ball)
        for t1, t2 in zip(times, times[1:]):
            v_vect_copy = v_vect.copy()
            v_vect_copies.add(v_vect_copy)
            ball_copy = ball.copy()
            ball_copy.clear_updaters()
            ball_copies.add(ball_copy)

            if self.add_ball_copies:
                self.add(v_vect_copy)
                self.add(ball_copy, ball)

            dashed_graph.save_state()
            kw = {
                "rate_func": lambda alpha: interpolate(
                    t1 / total_time,
                    t2 / total_time,
                    alpha
                )
            }
            anims = [
                ShowCreation(dashed_graph, **kw),
                MoveAlongPath(ball, graph, **kw),
                MoveAlongPath(v_point, velocity_graph, **kw),
                ApplyMethod(
                    time_tracker.increment_value, 1,
                    rate_func=linear
                ),
            ]
            if self.flash:
                anims.append(flash)
            self.play(*anims, run_time=1)
            dashed_graph.restore()
        randy.clear_updaters()
        self.play(FadeOut(time_group))
        self.wait()

        self.v_vects = v_vect_copies

    def combine_v_vects(self):
        v_vects = self.v_vects.copy()
        v_vects.generate_target()
        new_center = 2 * DOWN + 2 * LEFT
        for vect in v_vects.target:
            vect.scale(1.5)
            vect.set_stroke(width=2)
            vect.shift(new_center - vect.get_start())

        self.play(MoveToTarget(v_vects))

        delta_vects = VGroup(*[
            Arrow(
                v1.get_end(),
                v2.get_end(),
                buff=0.01,
                color=YELLOW,
            ).set_opacity(0.5)
            for v1, v2 in zip(v_vects, v_vects[1:])
        ])
        brace = Brace(Line(ORIGIN, UP), RIGHT)
        braces = VGroup(*[
            brace.copy().match_height(arrow).next_to(
                arrow, RIGHT, buff=0.2 * SMALL_BUFF
            )
            for arrow in delta_vects
        ])
        amounts = VGroup(*[
            OldTexText("9.8 m/s").scale(0.5).next_to(
                brace, RIGHT, SMALL_BUFF
            )
            for brace in braces
        ])

        self.play(
            FadeOut(self.gravity_field),
            FadeIn(delta_vects, lag_ratio=0.1),
        )
        self.play(
            LaggedStartMap(GrowFromCenter, braces),
            LaggedStartMap(FadeInFrom, amounts, lambda m: (m, LEFT)),
        )
        self.wait()

    def show_g_symbol(self):
        g = OldTex("g")
        brace = Brace(self.g_eq[0][2:], UP, buff=SMALL_BUFF)
        g.scale(1.5)
        g.next_to(brace, UP)
        g.set_color(YELLOW)
        self.play(
            FadeOut(self.title),
            GrowFromCenter(brace),
            FadeIn(g, UP),
        )
        self.wait()

    #
    def get_ball(self):
        ball = Circle(
            stroke_width=1,
            stroke_color=WHITE,
            fill_color=GREY,
            fill_opacity=1,
            sheen_factor=1,
            sheen_direction=UL,
            radius=0.25,
        )
        randy = Randolph(mode="pondering")
        randy.eyes.set_stroke(BLACK, 0.5)
        randy.match_height(ball)
        randy.scale(0.75)
        randy.move_to(ball)
        ball.add(randy)
        # CHANGE: keep the reference that show_trajectory uses.
        ball.randy = randy
        return ball


class SimpleProjectileEquation(ShowGravityAcceleration):
    CONFIG = {
        "y0": 0,
        "g": 9.8,
        "axes_config": {
            "x_min": 0,
            "x_max": 6,
            "x_axis_config": {
                "unit_size": 1.5,
                "tip_width": 0.15,
            },
            "y_min": -30,
            "y_max": 35,
            "y_axis_config": {
                "unit_size": 0.1,
                "big_tick_numbers": range(
                    -30, 35, 10
                ),
                "tick_size": 0.05,
                "numbers_to_show": range(-30, 31, 10),
                "tip_width": 0.15,
            },
            "center_point": 2 * LEFT,
        }
    }

    def construct(self):
        self.add_axes()
        self.setup_trajectory()

        self.show_trajectory()
        self.show_equation()
        self.solve_for_velocity()
        self.solve_for_position()

    def add_axes(self):
        axes = self.axes = Axes(**self.axes_config)
        axes.set_stroke(width=2)
        axes.add_coordinates()

        t_label = OldTex("t")
        t_label.next_to(axes.x_axis.get_right(), UL)
        axes.add(t_label)

        self.add(axes)

    def setup_trajectory(self):
        axes = self.axes
        total_time = self.total_time = 5

        ball = self.get_ball()
        offset_vector = 3 * LEFT

        g = self.g
        y0 = self.y0
        v0 = 0.5 * g * total_time

        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        # Position
        def y_func(t):
            return -0.5 * g * t**2 + v0 * t + y0

        graph_template = axes.get_graph(y_func, x_max=total_time)
        graph_template.set_stroke(width=2)
        traj_template = graph_template.copy()
        traj_template.stretch(0, 0)
        traj_template.move_to(
            axes.coords_to_point(0, 0), DOWN
        )
        traj_template.shift(offset_vector)
        traj_template.set_stroke(width=0.5)

        graph = VMobject()
        graph.set_stroke(BLUE, 2)
        traj = VMobject()
        traj.set_stroke(WHITE, 0.5)
        graph.add_updater(lambda g: g.pointwise_become_partial(
            graph_template, 0, get_t() / total_time
        ))
        traj.add_updater(lambda t: t.pointwise_become_partial(
            traj_template, 0, get_t() / total_time
        ))

        def get_ball_point():
            return axes.coords_to_point(
                0, y_func(get_t())
            ) + offset_vector

        f_always(ball.move_to, get_ball_point)

        h_line = always_redraw(lambda: DashedLine(
            get_ball_point(),
            axes.input_to_graph_point(get_t(), graph_template),
            stroke_width=1,
        ))

        y_label = OldTex("y", "(t)")
        y_label.set_color_by_tex("y", BLUE)
        y_label.add_updater(
            lambda m: m.next_to(
                graph.get_last_point(),
                UR, SMALL_BUFF,
            )
        )

        # Velocity
        def v_func(t):
            return -g * t + v0

        def get_v_vect():
            return Vector(
                axes.y_axis.unit_size * v_func(get_t()) * UP,
                color=RED,
            )
        v_vect = always_redraw(
            lambda: get_v_vect().shift(get_ball_point())
        )
        v_brace = always_redraw(lambda: Brace(v_vect, LEFT))
        dy_dt_label = OldTex(
            "{d", "y", "\\over dt}", "(t)",
        )
        dy_dt_label.scale(0.8)
        dy_dt_label.set_color_by_tex("y", BLUE)
        y_dot_label = OldTex("\\dot y", "(t)")
        y_dot_label.set_color_by_tex("\\dot y", RED)
        for label in dy_dt_label, y_dot_label:
            label.add_updater(lambda m: m.next_to(
                v_brace, LEFT, SMALL_BUFF,
            ))

        graphed_v_vect = always_redraw(
            lambda: get_v_vect().shift(
                axes.coords_to_point(get_t(), 0)
            )
        )
        v_graph_template = axes.get_graph(
            v_func, x_max=total_time,
        )
        v_graph = VMobject()
        v_graph.set_stroke(RED, 2)
        v_graph.add_updater(lambda m: m.pointwise_become_partial(
            v_graph_template,
            0, get_t() / total_time,
        ))

        # Acceleration
        def get_a_vect():
            return Vector(
                axes.y_axis.unit_size * g * DOWN
            )

        a_vect = get_a_vect()
        a_vect.add_updater(lambda a: a.move_to(
            get_ball_point(), UP,
        ))
        a_brace = Brace(a_vect, RIGHT)
        always(a_brace.next_to, a_vect, RIGHT, SMALL_BUFF)
        d2y_dt2_label = OldTex(
            "d^2", "{y}", "\\over dt}", "(t)"
        )
        d2y_dt2_label.scale(0.8)
        d2y_dt2_label.set_color_by_tex(
            "y", BLUE,
        )
        y_ddot_label = OldTex("\\ddot y", "(t)")
        y_ddot_label.set_color_by_tex("\\ddot y", YELLOW)
        for label in d2y_dt2_label, y_ddot_label:
            label.add_updater(lambda m: m.next_to(
                a_brace, RIGHT, SMALL_BUFF
            ))
        a_graph = axes.get_graph(
            lambda t: -g, x_max=total_time,
        )
        a_graph.set_stroke(YELLOW, 2)

        graphed_a_vect = get_a_vect()
        graphed_a_vect.add_updater(lambda a: a.move_to(
            axes.coords_to_point(get_t(), 0), UP,
        ))

        self.set_variables_as_attrs(
            t_tracker,
            graph,
            y_label,
            traj,
            h_line,
            v_vect,
            v_brace,
            dy_dt_label,
            y_dot_label,
            ball,
            graphed_v_vect,
            v_graph,
            a_vect,
            a_brace,
            d2y_dt2_label,
            y_ddot_label,
            a_graph,
            graphed_a_vect,
        )

    def show_trajectory(self):
        self.add(
            self.h_line,
            self.traj,
            self.ball,
            self.graph,
            self.y_label,
        )
        self.play_trajectory()
        self.wait()

        self.add(
            self.v_vect,
            self.v_brace,
            self.dy_dt_label,
            self.ball,
            self.graphed_v_vect,
            self.v_graph,
        )
        self.play_trajectory()
        self.wait()

        self.add(
            self.a_vect,
            self.ball,
            self.a_brace,
            self.d2y_dt2_label,
            self.a_graph,
            self.graphed_a_vect,
        )
        self.play_trajectory()
        self.wait()

        self.play(
            ReplacementTransform(
                self.dy_dt_label,
                self.y_dot_label,
            ),
            ShowCreationThenFadeAround(
                self.y_dot_label,
            ),
        )
        self.play(
            ReplacementTransform(
                self.d2y_dt2_label,
                self.y_ddot_label,
            ),
            ShowCreationThenFadeAround(
                self.y_ddot_label,
            ),
        )

    def show_equation(self):
        y_ddot = self.y_ddot_label
        new_y_ddot = y_ddot.deepcopy()
        new_y_ddot.clear_updaters()

        equation = VGroup(
            new_y_ddot,
            *Tex(
                "=", "-g",
                tex_to_color_map={"-g": YELLOW},
            ),
        )
        new_y_ddot.next_to(equation[1], LEFT, SMALL_BUFF)
        equation.move_to(self.axes)
        equation.to_edge(UP)

        self.play(
            TransformFromCopy(y_ddot, new_y_ddot),
            Write(equation[1:]),
            FadeOut(self.graph),
            FadeOut(self.y_label),
            FadeOut(self.h_line),
            FadeOut(self.v_graph),
            FadeOut(self.graphed_v_vect),
            FadeOut(self.graphed_a_vect),
        )

        self.equation = equation

    def solve_for_velocity(self):
        axes = self.axes
        equation = self.equation
        v_graph = self.v_graph.deepcopy()
        v_graph.clear_updaters()
        v_start_point = v_graph.get_start()
        origin = axes.coords_to_point(0, 0)
        offset = v_start_point - origin
        v_graph.shift(-offset)

        tex_question, answer1, answer2 = derivs = [
            OldTex(
                "{d", "(", *term, ")", "\\over", "dt}", "(t)",
                "=", "-g",
                tex_to_color_map={
                    "-g": YELLOW,
                    "v_0": RED,
                    "?": RED,
                }
            )
            for term in [
                ("?", "?", "?", "?"),
                ("-g", "t"),
                ("-g", "t", "+", "v_0",),
            ]
        ]
        for x in range(2):
            answer1.submobjects.insert(
                4, VectorizedPoint(answer1[4].get_left())
            )
        for deriv in derivs:
            deriv.next_to(equation, DOWN, MED_LARGE_BUFF)

        question = OldTexText(
            "What function has slope $-g$?",
            tex_to_color_map={"$-g$": YELLOW},
        )
        question.next_to(tex_question, DOWN)
        question.set_stroke(BLACK, 5, background=True)
        question.add_background_rectangle()

        v0_dot = Dot(v_start_point, color=PINK)
        v0_label = OldTex("v_0")
        v0_label.set_color(RED)
        v0_label.next_to(v0_dot, UR, buff=0)

        y_dot_equation = OldTex(
            "{\\dot y}", "(t)", "=",
            "-g", "t", "+", "v_0",
            tex_to_color_map={
                "{\\dot y}": RED,
                "-g": YELLOW,
                "v_0": RED,
            }
        )
        y_dot_equation.to_corner(UR)

        self.play(
            FadeIn(tex_question, DOWN),
            FadeIn(question, UP)
        )
        self.wait()
        self.add(v_graph, question)
        self.play(
            ReplacementTransform(tex_question, answer1),
            ShowCreation(v_graph),
        )
        self.wait()
        self.play(
            ReplacementTransform(answer1, answer2),
            v_graph.shift, offset,
        )
        self.play(
            FadeInFromLarge(v0_dot),
            FadeInFromDown(v0_label),
        )
        self.wait()
        self.play(
            TransformFromCopy(
                answer2[2:6], y_dot_equation[3:],
            ),
            Write(y_dot_equation[:3]),
            equation.shift, LEFT,
        )
        self.play(
            FadeOut(question),
            FadeOut(answer2),
        )

        self.remove(v_graph)
        self.add(self.v_graph)
        self.y_dot_equation = y_dot_equation

    def solve_for_position(self):
        # Largely copied from above...not great
        equation = self.equation
        y_dot_equation = self.y_dot_equation
        graph = self.graph

        all_terms = [
            ("?", "?", "?", "?"),
            ("-", "(1/2)", "g", "t^2", "+", "v_0", "t"),
            ("-", "(1/2)", "g", "t^2", "+", "v_0", "t", "+", "y_0"),
        ]
        tex_question, answer1, answer2 = derivs = [
            OldTex(
                "{d", "(", *term, ")", "\\over", "dt}", "(t)",
                "=",
                "-g", "t", "+", "v_0",
                tex_to_color_map={
                    "g": YELLOW,
                    "v_0": RED,
                    "?": BLUE,
                    "y_0": BLUE,
                }
            )
            for term in all_terms
        ]
        answer1.scale(0.8)
        answer2.scale(0.8)
        for deriv, terms in zip(derivs, all_terms):
            for x in range(len(all_terms[-1]) - len(terms)):
                n = 2 + len(terms)
                deriv.submobjects.insert(
                    n, VectorizedPoint(deriv[n].get_left())
                )
            deriv.next_to(
                VGroup(equation, y_dot_equation),
                DOWN, MED_LARGE_BUFF + SMALL_BUFF
            )
            deriv.shift_onto_screen()
            deriv.add_background_rectangle_to_submobjects()

        y_equation = OldTex(
            "y", "(t)", "=",
            "-", "(1/2)", "g", "t^2",
            "+", "v_0", "t",
            "+", "y_0",
            tex_to_color_map={
                "y": BLUE,
                "g": YELLOW,
                "v_0": RED,
            }
        )
        y_equation.next_to(
            VGroup(equation, y_dot_equation),
            DOWN, MED_LARGE_BUFF,
        )

        self.play(
            FadeIn(tex_question, DOWN),
        )
        self.wait()
        self.add(graph, tex_question)
        self.play(
            ReplacementTransform(tex_question, answer1),
            ShowCreation(graph),
        )
        self.add(graph, answer1)
        self.wait()
        self.play(ReplacementTransform(answer1, answer2))
        self.add(graph, answer2)
        g_updaters = graph.updaters
        graph.clear_updaters()
        self.play(
            graph.shift, 2 * DOWN,
            rate_func=there_and_back,
            run_time=2,
        )
        graph.add_updater(g_updaters[0])
        self.wait()
        br = BackgroundRectangle(y_equation)
        self.play(
            FadeIn(br),
            ReplacementTransform(
                answer2[2:11],
                y_equation[3:]
            ),
            FadeIn(y_equation[:3]),
            FadeOut(answer2[:2]),
            FadeOut(answer2[11:]),
        )
        self.play(ShowCreationThenFadeAround(y_equation))
        self.play_trajectory()

    #
    def play_trajectory(self, *added_anims, **kwargs):
        self.t_tracker.set_value(0)
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, 5,
                rate_func=linear,
                run_time=self.total_time,
            ),
            *added_anims,
        )
        self.wait()
