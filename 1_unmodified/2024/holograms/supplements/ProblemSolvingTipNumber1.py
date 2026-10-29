# ==============================================================================
# Scene:      ProblemSolvingTipNumber1
# Source:     videos/_2024/holograms/supplements.py (lines 621-636)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProblemSolvingTipNumber1.py ProblemSolvingTipNumber1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProblemSolvingTipNumber1(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Universal problem-solving tip #1", font_size=72)
        title.to_edge(UP, buff=LARGE_BUFF)
        underline = Underline(title, buff=-SMALL_BUFF)
        parts = VGroup(title[text][0] for text in re.split(" |-", title.text))

        words = Text("Start with the simplest\nversion of your problem", font_size=72)
        words.set_color(YELLOW)

        self.play(LaggedStartMap(FadeIn, parts, shift=0.25 * UP, lag_ratio=0.25, run_time=2))
        self.play(ShowCreation(underline))
        self.wait()
        self.play(Write(words), run_time=3)
        self.wait()
