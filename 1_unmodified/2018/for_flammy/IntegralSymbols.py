# ==============================================================================
# Scene:      IntegralSymbols
# Source:     videos/_2018/for_flammy.py (lines 231-326)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntegralSymbols.py IntegralSymbols -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntegralSymbols(Scene):
    def construct(self):
        int_sign = OldTex("\\displaystyle \\int")
        int_sign.set_height(1.5)
        int_sign.move_to(5 * LEFT)

        circumference, times, thickness = ctt = OldTexText(
            "circumference", "$\\times$", "thickness"
        )
        circumference.set_color(MAROON_B)
        ctt.next_to(int_sign, RIGHT, SMALL_BUFF)
        area_brace = Brace(ctt, DOWN)
        area_text = area_brace.get_text("Area of a ring")

        all_rings = OldTexText("All rings")
        all_rings.scale(0.5)
        all_rings.next_to(int_sign, DOWN, SMALL_BUFF)
        all_rings.shift(SMALL_BUFF * LEFT)

        circum_formula = OldTex(
            "2\\pi", "R\\cos(\\theta)",
        )
        circum_formula[1].set_color(RED)
        circum_formula.move_to(circumference)
        circum_brace = Brace(circum_formula, UP)

        R_dtheta = OldTex("R \\, d\\theta")
        R_dtheta.move_to(thickness, LEFT)
        R_dtheta_brace = Brace(R_dtheta, UP)

        zero, pi_halves = bounds = OldTex("0", "\\pi / 2")
        bounds.scale(0.5)
        zero.move_to(all_rings)
        pi_halves.next_to(int_sign, UP, SMALL_BUFF)
        pi_halves.shift(SMALL_BUFF * RIGHT)

        self.add(int_sign)
        self.play(
            GrowFromCenter(area_brace),
            FadeIn(area_text, UP),
        )
        self.wait()
        self.play(FadeInFromDown(circumference))
        self.play(
            FadeInFromDown(thickness),
            Write(times)
        )
        self.play(Write(all_rings))
        self.wait()

        self.play(
            circumference.next_to, circum_brace, UP, MED_SMALL_BUFF,
            circumference.shift, SMALL_BUFF * UR,
            GrowFromCenter(circum_brace),
        )
        self.play(FadeIn(circum_formula, UP))
        self.wait()
        self.play(
            thickness.next_to, circumference, RIGHT, MED_SMALL_BUFF,
            GrowFromCenter(R_dtheta_brace),
            area_brace.stretch, 0.84, 0, {"about_edge": LEFT},
            MaintainPositionRelativeTo(area_text, area_brace),
        )
        self.play(FadeIn(R_dtheta, UP))
        self.wait()
        self.play(ReplacementTransform(all_rings, bounds))
        self.wait()

        # RHS
        rhs = OldTex(
            "\\displaystyle =", "2\\pi R^2", "\\int_0^{\\pi / 2}",
            "\\cos(\\theta)", "d\\theta",
        )
        rhs.set_color_by_tex("cos", RED)
        rhs.next_to(R_dtheta, RIGHT)
        int_brace = Brace(rhs[2:], DOWN)
        q_marks = int_brace.get_text("???")
        one = OldTex("1")
        one.move_to(q_marks)

        self.play(FadeIn(rhs, 4 * LEFT))
        self.wait()
        self.play(ShowCreationThenFadeAround(rhs[1]))
        self.wait()
        self.play(ShowCreationThenFadeAround(rhs[2:]))
        self.wait()
        self.play(
            GrowFromCenter(int_brace),
            LaggedStartMap(
                FadeInFrom, q_marks,
                lambda m: (m, UP),
            )
        )
        self.wait()
        self.play(ReplacementTransform(q_marks, one))
        self.wait()
