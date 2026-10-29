# ==============================================================================
# Scene:      PrepareComplexAlgebra
# Source:     videos/_2024/holograms/supplements.py (lines 1514-1554)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrepareComplexAlgebra.py PrepareComplexAlgebra -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PrepareComplexAlgebra(InteractiveScene):
    def construct(self):
        # Test
        lines = VGroup(
            Tex(R"R \cdot (1 - \text{Opacity})"),
            Tex(R"R \cdot (1 - c|R + O|^2)"),
            Tex(R"R - c R \cdot |R + O|^2"),
        )
        lines.arrange(DOWN, buff=0.75)
        lines.to_edge(UP)

        label = Text("Wave beyond\nthe film")
        arrow = Vector(LEFT)
        arrow.next_to(lines[0], RIGHT)
        label.next_to(arrow, RIGHT)

        rect = SurroundingRectangle(lines[2][R"R \cdot |R + O|^2"], buff=0.05)
        rect.set_stroke(TEAL, 2)

        self.play(
            FadeIn(label, lag_ratio=0.1),
            GrowArrow(arrow),
            FadeIn(lines[0], LEFT),
        )
        self.wait()
        self.play(
            TransformMatchingStrings(lines[0].copy(), lines[1]),
            run_time=2
        )
        self.wait()
        self.play(
            TransformMatchingStrings(lines[1].copy(), lines[2]),
            run_time=2
        )
        self.wait()
        self.play(
            ShowCreation(rect),
            lines[:2].animate.set_opacity(0.5),
            lines[2][R"R - c"].animate.set_opacity(0.5),
        )
        self.wait()
