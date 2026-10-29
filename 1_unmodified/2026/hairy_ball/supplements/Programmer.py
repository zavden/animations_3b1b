# ==============================================================================
# Scene:      Programmer
# Source:     videos/_2026/hairy_ball/supplements.py (lines 176-192)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Programmer.py Programmer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Programmer(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle().fix_in_frame())
        laptop = Laptop()
        self.frame.reorient(60, 66, 0, (0.09, -0.5, 0.13), 4.12)

        randy = Randolph(height=5)
        randy.to_edge(LEFT)
        randy.add_updater(lambda m: m.fix_in_frame().look_at(4 * RIGHT))

        self.add(laptop)
        self.play(randy.change("hesitant"))
        self.play(Blink(randy))
        self.play(randy.change("concentrating"))
        self.play(Blink(randy))
        self.wait()
