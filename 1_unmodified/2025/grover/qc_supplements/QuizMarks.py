# ==============================================================================
# Scene:      QuizMarks
# Source:     videos/_2025/grover/qc_supplements.py (lines 199-208)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuizMarks.py QuizMarks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuizMarks(InteractiveScene):
    def construct(self):
        marks = VGroup(
            Exmark().set_color(RED),
            Exmark().set_color(RED),
            Checkmark().set_color(GREEN),
            Exmark().set_color(RED),
        )
        marks.arrange(DOWN).scale(2)
        self.add(marks)
