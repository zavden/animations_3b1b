# ==============================================================================
# Scene:      AskHowThisIsHelpful
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 635-643)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskHowThisIsHelpful.py AskHowThisIsHelpful -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskHowThisIsHelpful(InteractiveScene):
    def construct(self):
        randy = Randolph()
        randy.to_corner(DL)
        self.play(randy.says("Why is this\nhelpful?"))
        self.play(Blink(randy))
        self.wait()
        self.play(Blink(randy))
        self.wait()
