# ==============================================================================
# Scene:      ShowSinExpDerivatives
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 362-615)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part2/wordy_scenes.py
#
# Run from this folder:
#     manimgl ShowSinExpDerivatives.py ShowSinExpDerivatives -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part2/wordy_scenes.py -----

class WriteHeatEquationTemplate(Scene):
    CONFIG = {
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{T}": WHITE,
                "{t}": YELLOW,
                "{x}": GREEN,
                "{y}": RED,
                "{z}": BLUE,
                "\\partial": WHITE,
                "2": WHITE,
            },
        },
    }

    def get_d1_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}({x}, {t})", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2} ({x}, {t})",
            **self.tex_mobject_config
        )

    def get_d1_equation_without_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            **self.tex_mobject_config
        )

    def get_d3_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2} + ",
            "{\\partial^2 {T} \\over \\partial {y}^2} + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_general_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha", "\\nabla^2 {T}",
            **self.tex_mobject_config,
        )

    def get_d3_equation_with_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}",
            "({x}, {y}, {z}, {t})", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {y}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "({x}, {y}, {z}, {t})",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_d1_words(self):
        return OldTexText("Heat equation\\\\", "(1 dimension)")

    def get_d3_words(self):
        return OldTexText("Heat equation\\\\", "(3 dimensions)")

    def get_d1_group(self):
        group = VGroup(
            self.get_d1_words(),
            self.get_d1_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group

    def get_d3_group(self):
        group = VGroup(
            self.get_d3_words(),
            self.get_d3_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group



# ----- From _2019/diffyq/part3/wordy_scenes.py -----

class ShowSinExpDerivatives(WriteHeatEquationTemplate):
    CONFIG = {
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{0}": WHITE,
                "\\partial": WHITE,
                "=": WHITE,
            }
        }
    }

    def construct(self):
        pde = self.get_d1_equation_without_inputs()
        pde.to_edge(UP)
        pde.generate_target()

        new_rhs = OldTex(
            "=- \\alpha \\cdot T",
            **self.tex_mobject_config,
        )
        new_rhs.next_to(pde, RIGHT)
        new_rhs.align_to(pde.get_part_by_tex("alpha"), DOWN)

        equation1 = OldTex(
            "T({x}, {0}) = \\sin\\left({x}\\right)",
            **self.tex_mobject_config
        )
        equation2 = OldTex(
            "T({x}, {t}) = \\sin\\left({x}\\right)",
            "e^{-\\alpha{t}}",
            **self.tex_mobject_config
        )
        for eq in equation1, equation2:
            eq.next_to(pde, DOWN, MED_LARGE_BUFF)

        eq2_part1 = equation2[:len(equation1)]
        eq2_part2 = equation2[len(equation1):]

        # Rectangles
        exp_rect = SurroundingRectangle(eq2_part2)
        exp_rect.set_stroke(RED, 3)
        sin_rect = SurroundingRectangle(
            eq2_part1[-3:]
        )
        sin_rect.set_color(BLUE)

        VGroup(pde.target, new_rhs).center().to_edge(UP)

        # Show proposed solution
        self.add(pde)
        self.add(equation1)
        self.wait()
        self.play(
            MoveToTarget(pde),
            FadeIn(new_rhs, LEFT)
        )
        self.wait()
        self.play(
            ReplacementTransform(equation1, eq2_part1),
            FadeIn(eq2_part2),
        )
        self.play(ShowCreation(exp_rect))
        self.wait()
        self.play(FadeOut(exp_rect))

        # Take partial derivatives wrt x
        q_mark = OldTex("?")
        q_mark.next_to(pde.get_part_by_tex("="), UP)
        q_mark.set_color(RED)

        arrow1 = Vector(3 * DOWN + 1 * RIGHT, color=WHITE)
        arrow1.scale(1.2 / arrow1.get_length())
        arrow1.next_to(
            eq2_part2.get_corner(DL),
            DOWN, MED_LARGE_BUFF
        )
        ddx_label1 = OldTex(
            "\\partial \\over \\partial {x}",
            **self.tex_mobject_config,
        )
        ddx_label1.scale(0.7)
        ddx_label1.next_to(
            arrow1.point_from_proportion(0.8),
            UR, SMALL_BUFF
        )

        pde_ddx = VGroup(
            *pde.get_parts_by_tex("\\partial")[2:],
            pde.get_parts_by_tex("\\over")[1],
            pde.get_part_by_tex("{x}"),
        )
        pde_ddx_rect = SurroundingRectangle(pde_ddx)
        pde_ddx_rect.set_color(GREEN)

        eq2_part2_rect = SurroundingRectangle(eq2_part2)

        dx = OldTex(
            "\\cos\\left({x}\\right)", "e^{-\\alpha {t}}",
            **self.tex_mobject_config
        )
        ddx = OldTex(
            "-\\sin\\left({x}\\right)", "e^{-\\alpha {t}}",
            **self.tex_mobject_config
        )
        dx.next_to(arrow1, DOWN)
        dx.align_to(eq2_part2, RIGHT)
        x_shift = arrow1.get_end()[0] - arrow1.get_start()[0]
        x_shift *= 2
        dx.shift(x_shift * RIGHT)
        arrow2 = arrow1.copy()
        arrow2.next_to(dx, DOWN)
        arrow2.shift(MED_SMALL_BUFF * RIGHT)
        dx_arrows = VGroup(arrow1, arrow2)

        ddx_label2 = ddx_label1.copy()
        ddx_label2.shift(
            arrow2.get_center() - arrow1.get_center()
        )
        ddx.next_to(arrow2, DOWN)
        ddx.align_to(eq2_part2, RIGHT)
        ddx.shift(2 * x_shift * RIGHT)

        rhs = equation2[-6:]

        self.play(
            FadeInFromDown(q_mark)
        )
        self.play(
            ShowCreation(pde_ddx_rect)
        )
        self.wait()
        self.play(
            LaggedStart(
                GrowArrow(arrow1),
                GrowArrow(arrow2),
            ),
            TransformFromCopy(
                pde_ddx[0], ddx_label1
            ),
            TransformFromCopy(
                pde_ddx[0], ddx_label2
            ),
        )
        self.wait()
        self.play(
            TransformFromCopy(rhs, dx)
        )
        self.wait()
        self.play(
            FadeIn(eq2_part2_rect)
        )
        self.play(
            Transform(
                eq2_part2_rect,
                SurroundingRectangle(dx[-3:])
            )
        )
        self.play(
            FadeOut(eq2_part2_rect)
        )
        self.wait()
        self.play(
            TransformFromCopy(dx, ddx)
        )
        self.play(
            FadeIn(
                SurroundingRectangle(ddx).match_style(
                    pde_ddx_rect
                )
            )
        )
        self.wait()

        # Take partial derivative wrt t
        pde_ddt = pde[:pde.index_of_part_by_tex("=") - 1]
        pde_ddt_rect = SurroundingRectangle(pde_ddt)

        dt_arrow = Arrow(
            arrow1.get_start(),
            arrow2.get_end() + RIGHT,
            buff=0
        )
        dt_arrow.flip(UP)
        dt_arrow.next_to(dx_arrows, LEFT, MED_LARGE_BUFF)

        dt_label = OldTex(
            "\\partial \\over \\partial {t}",
            **self.tex_mobject_config,
        )
        dt_label.scale(1)
        dt_label.next_to(
            dt_arrow.get_center(), UL,
            SMALL_BUFF,
        )

        rhs_copy = rhs.copy()
        rhs_copy.next_to(dt_arrow.get_end(), DOWN)
        rhs_copy.shift(MED_LARGE_BUFF * LEFT)
        rhs_copy.match_y(ddx)

        minus_alpha_in_exp = rhs_copy[-3][1:].copy()
        minus_alpha_in_exp.set_color(RED)
        minus_alpha = OldTex("-\\alpha")
        minus_alpha.next_to(rhs_copy, LEFT)
        minus_alpha.align_to(rhs_copy[0][0], DOWN)
        dot = OldTex("\\cdot")
        dot.move_to(midpoint(
            minus_alpha.get_right(),
            rhs_copy.get_left(),
        ))

        self.play(
            TransformFromCopy(
                pde_ddx_rect,
                pde_ddt_rect,
            )
        )
        self.play(
            GrowArrow(dt_arrow),
            TransformFromCopy(
                pde_ddt,
                dt_label,
            )
        )
        self.wait()
        self.play(TransformFromCopy(rhs, rhs_copy))
        self.play(FadeIn(minus_alpha_in_exp))
        self.play(
            ApplyMethod(
                minus_alpha_in_exp.replace, minus_alpha,
                path_arc=TAU / 4
            ),
            FadeIn(dot),
        )
        self.play(
            FadeIn(minus_alpha),
            FadeOut(minus_alpha_in_exp),
        )
        self.wait()
        rhs_copy.add(minus_alpha, dot)
        self.play(
            FadeIn(SurroundingRectangle(rhs_copy))
        )
        self.wait()

        #
        checkmark = OldTex("\\checkmark")
        checkmark.set_color(GREEN)
        checkmark.move_to(q_mark, DOWN)
        self.play(
            FadeInFromDown(checkmark),
            FadeOut(q_mark, UP)
        )
        self.wait()
