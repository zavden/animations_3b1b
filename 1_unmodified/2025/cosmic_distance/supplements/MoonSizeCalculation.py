# ==============================================================================
# Scene:      MoonSizeCalculation
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 866-909)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoonSizeCalculation.py MoonSizeCalculation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoonSizeCalculation(InteractiveScene):
    def construct(self):
        # Test
        eq = Tex(
            R"{2 \text{ minutes} \over 24 \text{ hours}} = {2 R_M\over 2 \pi D_M}",
            t2c={"R_M": GREY_B, "D_M": GREY_B}
        )
        eq.to_corner(UL)
        eq.set_backstroke(BLACK, 2)

        self.play(FadeIn(eq[R"{2 \text{ minutes} \over 24 \text{ hours}}"]))
        self.wait()
        self.play(LaggedStart(
            FadeIn(eq["="][0]),
            TransformFromCopy(eq[R"2 \text{ minutes}"][0], eq["2 R_M"][0]),
            TransformFromCopy(eq[R"\over"][0], eq[R"\over"][1]),
            TransformFromCopy(eq[R"24 \text{ hours}"][0], eq[R"2 \pi D_M"][0]),
            lag_ratio=0.35
        ))
        self.wait()

        # Annotations
        top_rect = SurroundingRectangle(SurroundingRectangle(eq["R_M"], buff=0.01).set_stroke(width=1))
        low_rect = SurroundingRectangle(SurroundingRectangle(eq["D_M"], buff=0.01).set_stroke(width=1))
        top_label = TexText("Radius of the moon")
        top_label.next_to(top_rect, RIGHT)
        low_label = TexText("Distance to the moon")
        low_label.next_to(low_rect, RIGHT)

        VGroup(top_rect, low_rect, top_label, low_label).set_color(TEAL)

        self.play(
            ShowCreation(top_rect),
            FadeIn(top_label, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            ReplacementTransform(top_rect, low_rect),
            FadeOut(top_label),
            FadeIn(low_label, lag_ratio=0.1),
        )
        self.wait()
        self.play(FadeOut(low_rect), FadeOut(low_label))
        self.wait()
