# ==============================================================================
# Scene:      ConfusedPi
# Source:     videos/_2022/puzzles/subsets.py (lines 4528-4536)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConfusedPi.py ConfusedPi -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConfusedPi(InteractiveScene):
    def construct(self):
        randy = Randolph(mode="erm", height=2)
        self.play(randy.change("maybe").look(UP))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("pondering").look(DL))
        self.play(Blink(randy))
        self.wait(2)
