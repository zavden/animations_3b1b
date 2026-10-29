# ==============================================================================
# Scene:      AskIfItMakesSense
# Source:     videos/_2022/puzzles/subsets.py (lines 5151-5162)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskIfItMakesSense.py AskIfItMakesSense -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskIfItMakesSense(InteractiveScene):
    def construct(self):
        randy = Randolph(height=2)
        randy.to_edge(DOWN)

        self.play(PiCreatureBubbleIntroduction(
            randy, Text("Does this...\nmake sense?", font_size=36),
            bubble_config=dict(width=3.5, height=2),
            target_mode="maybe",
        ))
        self.play(Blink(randy))
        self.wait()
