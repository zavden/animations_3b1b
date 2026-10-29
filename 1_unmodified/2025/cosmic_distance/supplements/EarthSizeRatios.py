# ==============================================================================
# Scene:      EarthSizeRatios
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 668-693)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EarthSizeRatios.py EarthSizeRatios -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EarthSizeRatios(InteractiveScene):
    def construct(self):
        # Test
        equation = Tex(R"""
            {7^\circ \over 360^\circ} = 
            {\text{dist}(\text{Alexandria}, \text{Syene}) \over \text{Circumference of Earth}}
        """, font_size=42)
        equation.to_corner(UL)
        dist_term = equation[R"\text{dist}(\text{Alexandria}, \text{Syene})"][0]

        self.play(FadeIn(equation[R"7^\circ"], UL))
        self.play(Write(equation[R"\over 360^\circ}"]))
        self.wait()
        self.play(LaggedStart(
            Write(equation[R"="][0]),
            FadeTransformPieces(equation[R"7^\circ"][0].copy(), dist_term),
            FadeTransformPieces(equation[R"\over"][0].copy(), equation[R"\over"][1]),
            FadeTransformPieces(equation[R"360^\circ"][0].copy(), equation[R"\text{Circumference of Earth}"][0]),
            lag_ratio=0.1,
        ))
        self.wait()

        # Highlight dist
        rect = SurroundingRectangle(dist_term)
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
