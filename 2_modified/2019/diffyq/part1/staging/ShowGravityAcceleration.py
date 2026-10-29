# ==============================================================================
# Scene:      ShowGravityAcceleration
# Source:     videos/_2019/diffyq/part1/staging.py (lines 300-558)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl ShowGravityAcceleration.py ShowGravityAcceleration -w -m --fps 15
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
