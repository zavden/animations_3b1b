# ==============================================================================
# Scene:      WaitWhat
# Source:     videos/_2026/hairy_ball/supplements.py (lines 373-383)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WaitWhat.py WaitWhat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WaitWhat(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph(height=4)
        randy.to_edge(LEFT, buff=2.5)
        randy.shift(DOWN)
        randy.body.insert_n_curves(1000)

        self.play(randy.says("Wait...what?", mode="confused", bubble_direction=RIGHT, look_at=RIGHT))
        self.play(Blink(randy))
        self.wait(3)
