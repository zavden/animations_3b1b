# ==============================================================================
# Scene:      ShowFactorsOf710
# Source:     videos/_2019/spirals.py (lines 3306-3349)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowFactorsOf710.py ShowFactorsOf710 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowFactorsOf710(Scene):
    def construct(self):
        equation = OldTex(
            "710", "=",
            "71", "\\cdot",
            "5", "\\cdot",
            "2",
        )
        equation.scale(1.5)
        equation.to_corner(UL)
        ten = OldTex("10")
        ten.match_height(equation)
        ten.move_to(equation.get_part_by_tex("5"), LEFT)

        self.add(equation[0])
        self.wait()
        self.play(
            TransformFromCopy(
                equation[0][:2],
                equation[2],
            ),
            FadeIn(equation[1]),
            FadeIn(equation[3]),
            TransformFromCopy(
                equation[0][2:],
                ten,
            )
        )
        self.wait()
        self.remove(ten)
        self.play(*[
            TransformFromCopy(ten, mob)
            for mob in equation[4:]
        ])
        self.wait()

        # Circle factors
        colors = [RED, BLUE, PINK]
        for factor, color in zip(equation[:-6:-2], colors):
            rect = SurroundingRectangle(factor)
            rect.set_color(color)
            self.play(ShowCreation(rect))
            self.wait()
            self.play(FadeOut(rect))
