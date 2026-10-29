# ==============================================================================
# Scene:      StretchLabel
# Source:     videos/_2021/shadows.py (lines 2217-2231)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StretchLabel.py StretchLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StretchLabel(Scene):
    def construct(self):
        label = VGroup(
            Vector(0.5 * LEFT),
            OldTex("1.5 \\times"),
            Vector(0.5 * RIGHT)
        )
        label.set_color(YELLOW)
        label.arrange(RIGHT, buff=SMALL_BUFF)

        self.play(
            *map(ShowCreation, label[::2]),
            Write(label[1]),
        )
        self.wait()
