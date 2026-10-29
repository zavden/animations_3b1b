# ==============================================================================
# Scene:      CyclesHaveSolutions
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2147-2160)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CyclesHaveSolutions.py CyclesHaveSolutions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CyclesHaveSolutions(Scene):
    def construct(self):
        text = VGroup(
            OldTex(
                "f^n(z) = z \\text{ has solutions}",
                tex_to_color_map={"z": BLUE},
            ),
            OldTex("\\sim D^n \\text{ of them...}"),
        )
        text.arrange(DOWN)

        for part in text:
            self.play(FadeIn(part))
            self.wait()
