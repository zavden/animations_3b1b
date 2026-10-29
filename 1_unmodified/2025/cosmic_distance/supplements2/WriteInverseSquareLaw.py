# ==============================================================================
# Scene:      WriteInverseSquareLaw
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 780-797)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteInverseSquareLaw.py WriteInverseSquareLaw -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteInverseSquareLaw(InteractiveScene):
    def construct(self):
        # Test
        eq = Tex(R"\text{Apparent brightness} = \text{const} \cdot {\text{Absolute brightness} \over (\text{distance})^2}")
        eq.to_edge(UP)
        eq.set_color(GREY_B)

        self.add(eq)
        self.wait()
        words = ["Apparent brightness", "Absolute brightness", "distance"]
        colors = [YELLOW, WHITE, BLUE]
        for text, color in zip(words, colors):
            part = eq[text][0]
            self.play(
                FlashAround(part, color=color, buff=0.1),
                part.animate.set_color(color)
            )
            self.wait()
