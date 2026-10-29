# ==============================================================================
# Scene:      BuildUpEquation
# Source:     videos/_2019/diffyq/part1/pendulum.py (lines 1551-1876)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BuildUpEquation.py BuildUpEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BuildUpEquation(Scene):
    CONFIG = {
        "tex_config": {
            "tex_to_color_map": {
                "{a}": YELLOW,
                "{v}": RED,
                "{x}": GREEN,
                "\\theta": BLUE,
                "{L}": WHITE,
            }
        }
    }

    def construct(self):
        # self.add_center_line()
        self.show_derivatives()
        self.show_theta_double_dot_equation()
        self.talk_about_sine_component()
        self.add_air_resistance()

    def add_center_line(self):
        line = Line(UP, DOWN)
        line.set_height(FRAME_HEIGHT)
        line.set_stroke(WHITE, 1)
        self.add(line)

    def show_derivatives(self):
        a_eq = OldTex(
            "{a}", "=", "{d{v} \\over dt}",
            **self.tex_config,
        )
        v_eq = OldTex(
            "{v}", "=", "{d{x} \\over dt}",
            **self.tex_config,
        )
        x_eq = OldTex(
            "{x} = {L} \\theta",
            **self.tex_config,
        )
        eqs = VGroup(a_eq, v_eq, x_eq)
        eqs.arrange(DOWN, buff=LARGE_BUFF)
        eqs.to_corner(UL)

        v_rhs = OldTex(
            "={L}{d\\theta \\over dt}",
            "=", "{L}\\dot{\\theta}",
            **self.tex_config,
        )

        v_rhs.next_to(v_eq, RIGHT, SMALL_BUFF)
        v_rhs.shift(
            UP * (v_eq[1].get_bottom()[1] - v_rhs[0].get_bottom()[1])
        )
        a_rhs = OldTex(
            "={L}{d", "\\dot{\\theta}", "\\over dt}",
            "=", "{L}\\ddot{\\theta}",
            **self.tex_config,
        )
        a_rhs.next_to(a_eq, RIGHT, SMALL_BUFF)
        a_rhs.shift(
            UP * (a_eq[1].get_bottom()[1] - a_rhs[0].get_bottom()[1])
        )

        # a_eq
        self.play(Write(a_eq))
        self.wait()

        # v_eq
        self.play(
            TransformFromCopy(
                a_eq.get_part_by_tex("{v}"),
                v_eq.get_part_by_tex("{v}"),
            )
        )
        self.play(TransformFromCopy(v_eq[:1], v_eq[1:]))
        self.wait()

        # x_eq
        self.play(
            TransformFromCopy(
                v_eq.get_part_by_tex("{x}"),
                x_eq.get_part_by_tex("{x}"),
            )
        )
        self.play(Write(x_eq[1:]))
        self.wait()
        for tex in "L", "\\theta":
            self.play(ShowCreationThenFadeAround(
                x_eq.get_part_by_tex(tex)
            ))
        self.wait()

        # v_rhs
        self.play(*[
            TransformFromCopy(
                x_eq.get_part_by_tex(tex),
                v_rhs.get_part_by_tex(tex),
            )
            for tex in ("=", "{L}", "\\theta")
        ])
        self.play(
            TransformFromCopy(v_eq[-3], v_rhs[2]),
            TransformFromCopy(v_eq[-1], v_rhs[4]),
        )
        self.wait()
        self.play(
            Write(v_rhs[-5]),
            TransformFromCopy(*v_rhs.get_parts_by_tex("{L}")),
            TransformFromCopy(v_rhs[3:4], v_rhs[-3:])
        )
        self.wait()
        self.play(ShowCreationThenFadeAround(v_rhs[2:4]))
        self.play(ShowCreationThenFadeAround(v_rhs[4]))
        self.wait()

        # a_rhs
        self.play(*[
            TransformFromCopy(
                v_rhs.get_parts_by_tex(tex)[-1],
                a_rhs.get_part_by_tex(tex),
            )
            for tex in ("=", "{L}", "\\theta", "\\dot")
        ])
        self.play(
            TransformFromCopy(a_eq[-3], a_rhs[2]),
            TransformFromCopy(a_eq[-1], a_rhs[6]),
        )
        self.wait()
        self.play(
            Write(a_rhs[-5]),
            TransformFromCopy(*a_rhs.get_parts_by_tex("{L}")),
            TransformFromCopy(a_rhs[3:4], a_rhs[-3:]),
        )
        self.wait()

        self.equations = VGroup(
            a_eq, v_eq, x_eq,
            v_rhs, a_rhs,
        )

    def show_theta_double_dot_equation(self):
        equations = self.equations
        a_deriv = equations[0]
        a_rhs = equations[-1][-5:].copy()

        shift_vect = 1.5 * DOWN

        equals = OldTex("=")
        equals.rotate(90 * DEGREES)
        equals.next_to(a_deriv[0], UP, MED_LARGE_BUFF)
        g_sin_eq = OldTex(
            "-", "g", "\\sin", "(", "\\theta", ")",
            **self.tex_config,
        )
        g_sin_eq.next_to(
            equals, UP,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        g_sin_eq.to_edge(LEFT)
        g_sin_eq.shift(shift_vect)

        shift_vect += (
            g_sin_eq[1].get_center() -
            a_deriv[0].get_center()
        )[0] * RIGHT

        equals.shift(shift_vect)
        a_rhs.shift(shift_vect)

        self.play(
            equations.shift, shift_vect,
            Write(equals),
            GrowFromPoint(
                g_sin_eq, 2 * RIGHT + 3 * DOWN
            )
        )
        self.wait()
        self.play(
            a_rhs.next_to, g_sin_eq, RIGHT,
            a_rhs.shift, SMALL_BUFF * UP,
        )
        self.wait()

        # Fade equations
        self.play(
            FadeOut(equals),
            equations.shift, DOWN,
            equations.fade, 0.5,
        )

        # Rotate sides
        equals, L, ddot, theta, junk = a_rhs
        L_dd_theta = VGroup(L, ddot, theta)
        minus, g, sin, lp, theta2, rp = g_sin_eq
        m2, g2, over, L2 = frac = OldTex("-", "{g", "\\over", "L}")
        frac.next_to(equals, RIGHT)

        self.play(
            L_dd_theta.next_to, equals, LEFT,
            L_dd_theta.shift, SMALL_BUFF * UP,
            g_sin_eq.next_to, equals, RIGHT,
            path_arc=PI / 2,
        )
        self.play(
            ReplacementTransform(g, g2),
            ReplacementTransform(minus, m2),
            ReplacementTransform(L, L2),
            Write(over),
            g_sin_eq[2:].next_to, over, RIGHT, SMALL_BUFF,
        )
        self.wait()

        # Surround
        rect = SurroundingRectangle(VGroup(g_sin_eq, frac, ddot))
        rect.stretch(1.1, 0)
        dashed_rect = DashedVMobject(
            rect, num_dashes=50, positive_space_ratio=1,
        )
        dashed_rect.shuffle()
        dashed_rect.save_state()
        dashed_rect.space_out_submobjects(1.1)
        for piece in dashed_rect:
            piece.rotate(90 * DEGREES)
        dashed_rect.fade(1)
        self.play(Restore(dashed_rect, lag_ratio=0.05))
        dashed_rect.generate_target()
        dashed_rect.target.space_out_submobjects(0.9)
        dashed_rect.target.fade(1)
        for piece in dashed_rect.target:
            piece.rotate(90 * DEGREES)
        self.play(MoveToTarget(
            dashed_rect,
            lag_ratio=0.05,
            remover=True
        ))
        self.wait()

        self.main_equation = VGroup(
            ddot, theta, equals,
            m2, L2, over, g2,
            sin, lp, theta2, rp,
        )

    def talk_about_sine_component(self):
        main_equation = self.main_equation
        gL_part = main_equation[4:7]
        sin_part = main_equation[7:]
        sin = sin_part[0]

        morty = Mortimer(height=1.5)
        morty.next_to(sin, DR, buff=LARGE_BUFF)
        morty.add_updater(lambda m: m.look_at(sin))

        self.play(ShowCreationThenFadeAround(gL_part))
        self.wait()
        self.play(ShowCreationThenFadeAround(sin_part))
        self.wait()

        self.play(FadeIn(morty))
        sin.save_state()
        self.play(
            morty.change, "angry",
            sin.next_to, morty, LEFT, {"aligned_edge": UP},
        )
        self.play(Blink(morty))
        morty.clear_updaters()
        self.play(
            morty.change, "concerned_musician",
            morty.look, DR,
        )
        self.play(Restore(sin))
        self.play(FadeOut(morty))
        self.wait()

        # Emphasize theta as input
        theta = sin_part[2]
        arrow = Vector(0.5 * UP, color=WHITE)
        arrow.next_to(theta, DOWN, SMALL_BUFF)
        word = OldTexText("Input")
        word.next_to(arrow, DOWN)

        self.play(
            FadeIn(word, UP),
            GrowArrow(arrow)
        )
        self.play(
            ShowCreationThenDestruction(
                theta.copy().set_style(
                    fill_opacity=0,
                    stroke_width=2,
                    stroke_color=YELLOW,
                ),
                lag_ratio=0.1,
            )
        )
        self.play(FadeOut(arrow), FadeOut(word))

    def add_air_resistance(self):
        main_equation = self.main_equation
        tdd_eq = main_equation[:3]
        rhs = main_equation[3:]

        new_term = OldTex(
            "-", "\\mu", "\\dot{", "\\theta}",
        )
        new_term.set_color_by_tex("\\theta", BLUE)
        new_term.move_to(main_equation)
        new_term.shift(0.5 * SMALL_BUFF * UP)
        new_term[0].align_to(rhs[0], UP)

        brace = Brace(new_term, DOWN)
        words = brace.get_text("Air resistance")

        self.play(
            FadeInFromDown(new_term),
            tdd_eq.next_to, new_term, LEFT,
            tdd_eq.align_to, tdd_eq, UP,
            rhs.next_to, new_term, RIGHT,
            rhs.align_to, rhs, UP,
        )
        self.play(
            GrowFromCenter(brace),
            Write(words)
        )
        self.wait()
