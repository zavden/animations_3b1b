# ==============================================================================
# Scene:      MysteryInputLabel
# Source:     videos/_2018/cramer.py (lines 2207-2215)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MysteryInputLabel.py MysteryInputLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MysteryInputLabel(Scene):
    def construct(self):
        brace = Brace(Line(ORIGIN, RIGHT), DOWN)
        text = brace.get_text("Mystery input")
        self.play(
            GrowFromCenter(brace),
            Write(text)
        )
        self.wait()
