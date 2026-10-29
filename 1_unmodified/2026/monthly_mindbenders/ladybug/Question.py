# ==============================================================================
# Scene:      Question
# Source:     videos/_2026/monthly_mindbenders/ladybug.py (lines 91-99)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Question.py Question -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Question(InteractiveScene):
    def construct(self):
        text = Text("""
            What is the probability that
            the last number painted is 6?
        """)
        text.to_edge(UP)
        self.play(Write(text))
        self.wait()
