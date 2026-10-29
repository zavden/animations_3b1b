# ==============================================================================
# Scene:      WhatsGoingOn
# Source:     videos/_2022/borwein/supplements.py (lines 109-119)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatsGoingOn.py WhatsGoingOn -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatsGoingOn(InteractiveScene):
    def construct(self):
        randy = Randolph(height=2)
        randy.to_corner(DL).look(RIGHT)
        self.play(randy.says("What on earth\nis going on?", mode="angry"))
        self.play(randy.animate.look(DR))
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change("confused"))
        self.play(Blink(randy))
        self.wait(2)
