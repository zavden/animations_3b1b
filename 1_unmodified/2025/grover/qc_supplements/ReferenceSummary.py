# ==============================================================================
# Scene:      ReferenceSummary
# Source:     videos/_2025/grover/qc_supplements.py (lines 128-149)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceSummary.py ReferenceSummary -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceSummary(InteractiveScene):
    def construct(self):
        # Laptop
        laptop = Laptop()
        self.frame.reorient(85, 79, 0, (-1.04, -1.42, 0.47), 6.97)
        self.add(laptop)

        # Randy
        randy = Randolph(mode="thinking", height=4)
        randy.body.insert_n_curves(100)
        randy.fix_in_frame()
        randy.next_to(ORIGIN, LEFT)
        randy.look_at(2 * RIGHT)

        self.add(randy)
        self.play(Blink(randy))
        self.wait()
        self.play(Blink(randy))
        self.play(randy.change("confused").fix_in_frame())
        self.wait(2)
        self.play(Blink(randy))
        self.wait(2)
