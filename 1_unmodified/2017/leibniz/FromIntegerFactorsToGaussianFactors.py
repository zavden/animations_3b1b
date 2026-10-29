# ==============================================================================
# Scene:      FromIntegerFactorsToGaussianFactors
# Source:     videos/_2017/leibniz.py (lines 2124-2173)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FromIntegerFactorsToGaussianFactors.py FromIntegerFactorsToGaussianFactors -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FromIntegerFactorsToGaussianFactors(TeacherStudentsScene):
    def construct(self):
        expression = OldTex(
            "30", "=", "2", "\\cdot", "3", "\\cdot", "5"
        )
        expression.shift(2*UP)
        two = expression.get_part_by_tex("2")
        five = expression.get_part_by_tex("5")
        two.set_color(BLUE)
        five.set_color(GREEN)
        two.factors = OldTex("(1+i)", "(1-i)")
        five.factors = OldTex("(2+i)", "(2-i)")
        for mob, vect in (two, DOWN), (five, UP):
            mob.factors.next_to(mob, vect, LARGE_BUFF)
            mob.factors.set_color(mob.get_color())
            mob.arrows = VGroup(*[
                Arrow(
                    mob.get_edge_center(vect),
                    factor.get_edge_center(-vect),
                    color = mob.get_color(),
                    tip_length = 0.15
                )
                for factor in mob.factors
            ])

        self.add(expression)
        for mob in two, five:
            self.play(
                ReplacementTransform(
                    mob.copy(),
                    mob.factors
                ),
                *list(map(ShowCreation, mob.arrows))
            )
            self.wait()
        self.play(*[
            ApplyMethod(pi.change, "pondering", expression)
            for pi in self.get_pi_creatures()
        ])
        self.wait(5)
        group = VGroup(
            expression, 
            two.arrows, two.factors,
            five.arrows, five.factors,
        )
        self.teacher_says(
            "Now for a \\\\ surprising fact...",
            added_anims = [FadeOut(group)]
        )
        self.wait(2)
