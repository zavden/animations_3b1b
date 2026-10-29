# ==============================================================================
# Scene:      AskAboutMoonrise
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 857-863)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutMoonrise.py AskAboutMoonrise -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutMoonrise(InteractiveScene):
    def construct(self):
        # Test
        question = Text("What does the duration\nof a moonrise tell you?", font_size=60)
        question.set_backstroke(BLACK, 3)
        self.play(Write(question, stroke_color=WHITE, run_time=3))
        self.wait()
