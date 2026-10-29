# ==============================================================================
# Scene:      MoonOrbitCalculation
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 704-770)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoonOrbitCalculation.py MoonOrbitCalculation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoonOrbitCalculation(InteractiveScene):
    def construct(self):
        # Pure ratio
        ratio_tex = R"{\text{28 days} \over \text{4 hours}}"
        new_ratio_tex = R"{\text{28 days} \over \text{3.5 hours}}"
        eq1, eq2 = (
            Tex(ratio_tex + R"= {2 \pi D_M \over 2 R_\text{E}}"),
            Tex(new_ratio_tex + R"= {2 \pi D_M \over 2 R_\text{E}}"),
        )
        for eq in [eq1, eq2]:
            eq.to_corner(UL)
        eq2.move_to(eq1, RIGHT)

        RMO = eq1[R"D_M"]
        RMO_rect = SurroundingRectangle(RMO, buff=0.05)
        RMO_rect.set_stroke(TEAL, 2)
        RMO_words = Text("Distance to the moon", font_size=48)
        RMO_words.next_to(RMO_rect)
        RMO_words.set_color(TEAL)

        self.add(eq1)
        self.wait()
        self.play(
            RMO.animate.set_color(TEAL),
            ShowCreation(RMO_rect),
            FadeIn(RMO_words, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            Transform(eq1[R"28 days"][0], eq2[R"28 days"][0]),
            Transform(eq1[R"\over"][0], eq2[R"\over"][0]),
            Transform(eq1[R"4"], eq2[R"3.5"]),
        )
        self.wait()

        # Equation 2
        eq3 = Tex(
            R"\frac{1}{\pi} \left( " + new_ratio_tex + R"\right) R_\text{E} = D_M"
        )
        eq3.next_to(eq2, DOWN, LARGE_BUFF, aligned_edge=LEFT)
        RMO2 = eq3[R"D_M"]
        RMO2.set_color(TEAL)

        self.play(LaggedStart(
            TransformFromCopy(eq2[new_ratio_tex], eq3[new_ratio_tex]),
            FadeIn(eq3[R"\left("]),
            FadeIn(eq3[R"\right)"]),
            TransformFromCopy(eq2[R"\pi"], eq3[R"\frac{1}{\pi}"]),
            TransformFromCopy(eq2[R"R_\text{E}"], eq3[R"R_\text{E}"]),
            TransformFromCopy(eq2["="], eq3["="]),
            TransformFromCopy(eq2[R"D_M"], eq3[R"D_M"]),
            lag_ratio=0.3,
            run_time=3
        ))
        self.wait()

        # Note the fraction
        frac = eq3[R"\frac{1}{\pi} \left( " + new_ratio_tex + R"\right)"]
        rect = SurroundingRectangle(frac)
        rect.set_stroke(YELLOW, 2)
        value = Tex(R"\approx 61")
        value.next_to(rect, DOWN)
        value.match_color(rect)

        self.play(ShowCreation(rect))
        self.play(Write(value))
        self.wait()
