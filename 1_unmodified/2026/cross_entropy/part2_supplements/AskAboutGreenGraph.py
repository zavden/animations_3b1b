# ==============================================================================
# Scene:      AskAboutGreenGraph
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 51-62)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutGreenGraph.py AskAboutGreenGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutGreenGraph(InteractiveScene):
    def construct(self):
        morty = Mortimer().flip()
        morty.to_edge(LEFT).shift(DOWN)
        morty.body.insert_n_curves(1000)
        self.play(
            morty.says("What is this\nnew curve?", "speaking", look_at=3 * RIGHT),
        )
        self.play(Blink(morty))
        self.play(morty.change("tease"))
        self.play(Blink(morty))
        self.wait(5)
