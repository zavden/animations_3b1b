# ==============================================================================
# Scene:      VelocityZero
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 731-736)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VelocityZero.py VelocityZero -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VelocityZero(InteractiveScene):
    def construct(self):
        label = Tex(R"(\text{Velocity} = 0)")
        label.set_color(PINK)
        self.play(FadeIn(label, 0.5 * UP))
        self.wait()
