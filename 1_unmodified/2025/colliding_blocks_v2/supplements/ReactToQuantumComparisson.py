# ==============================================================================
# Scene:      ReactToQuantumComparisson
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 229-245)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReactToQuantumComparisson.py ReactToQuantumComparisson -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReactToQuantumComparisson(InteractiveScene):
    def construct(self):
        randy = Randolph(height=3)
        randy.to_edge(LEFT).shift(DOWN)
        randy.body.insert_n_curves(100)

        self.play(randy.change("sassy"))
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change("awe"))
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change("confused"))
        self.play(Blink(randy))
        self.wait()
        self.play(Blink(randy))
        self.wait()
