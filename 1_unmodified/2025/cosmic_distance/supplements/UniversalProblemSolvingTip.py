# ==============================================================================
# Scene:      UniversalProblemSolvingTip
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 1145-1163)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UniversalProblemSolvingTip.py UniversalProblemSolvingTip -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UniversalProblemSolvingTip(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Universal Problem Solving Tip #1", font_size=60)
        title.add(Underline(title, buff=-0.025))
        title.to_edge(UP)
        title.set_color(BLUE)
        self.add(title)

        words = TexText(R"If you can't solve a problem, try \\ to solve a simpler problem instead", font_size=60, isolate="simpler problem ")
        words.next_to(title, DOWN, buff=1.5)

        self.play(FadeIn(words, lag_ratio=0.1, run_time=2))
        self.wait()
        self.play(
            FlashUnder(words["simpler problem"], buff=-0.025),
            words["simpler problem"].animate.set_color(YELLOW)
        )
        self.wait()
