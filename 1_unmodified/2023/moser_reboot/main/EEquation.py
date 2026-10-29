# ==============================================================================
# Scene:      EEquation
# Source:     videos/_2023/moser_reboot/main.py (lines 1023-1032)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EEquation.py EEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EEquation(InteractiveScene):
    def construct(self):
        eq = Tex(R"E = {n \choose 2} + 2 {n \choose 4} + n", font_size=72)
        eq.to_corner(UR)
        self.play(FadeIn(eq[:6], UP))
        self.wait()
        self.play(Write(eq[6:-2]))
        self.wait()
        self.play(Write(eq[-2:]))
        self.wait()
