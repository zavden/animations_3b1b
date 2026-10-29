# ==============================================================================
# Scene:      AreaToSignedArea
# Source:     videos/_2022/borwein/supplements.py (lines 70-95)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AreaToSignedArea.py AreaToSignedArea -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AreaToSignedArea(InteractiveScene):
    def construct(self):
        # Words
        equals = OldTex("=")
        equals.to_edge(UP, buff=1.0).shift(2.5 * LEFT)
        area = Text("Area")
        area.next_to(equals, RIGHT)
        arrow = Arrow(area.get_bottom(), UP)

        signed_area = Text("Signed area", t2s={"Signed": ITALIC})
        signed_area.next_to(equals, RIGHT)

        blue_minus_red = OldTexText(
            "= (Blue area) - (Red area)",
            tex_to_color_map={"(Blue area)": BLUE, "(Red area)": RED}
        )
        blue_minus_red.next_to(signed_area, RIGHT)

        self.play(FadeIn(equals), Write(area), ShowCreation(arrow))
        self.wait()
        self.play(TransformMatchingShapes(area, signed_area))
        self.wait()
        self.play(FadeIn(blue_minus_red[:2]))
        self.wait()
        self.play(FadeIn(blue_minus_red[2:]))
        self.wait()
