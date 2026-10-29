# ==============================================================================
# Scene:      HowQuaternionsRotate3dPoints
# Source:     videos/_2018/quaternions.py (lines 6096-6126)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowQuaternionsRotate3dPoints.py HowQuaternionsRotate3dPoints -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowQuaternionsRotate3dPoints(Scene):
    def construct(self):
        title = OldTexText(
            "Coming up:\\\\",
            "How quaternions act on 3d points"
        )
        title.to_edge(UP)

        expression = OldTex(
            "q", "\\cdot", "p", "\\cdot", "q^{-1}"
        )
        expression.scale(2)
        expression.set_color_by_tex("q", PINK)
        expression.set_color_by_tex("p", YELLOW)

        right_arrow = Arrow(
            expression[0].get_top(),
            expression[2].get_top(),
            path_arc=-PI,
            color=WHITE,
        )
        right_arrow.set_stroke(width=4)
        left_arrow = right_arrow.copy()
        left_arrow.flip(about_point=expression[2].get_top())
        left_arrow.shift(SMALL_BUFF * RIGHT)

        self.add(title)
        self.play(Write(expression))
        self.play(ShowCreation(right_arrow))
        self.play(ShowCreation(left_arrow))
        self.wait()
