# ==============================================================================
# Scene:      ThisConstant
# Source:     videos/_2022/borwein/supplements.py (lines 246-261)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisConstant.py ThisConstant -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThisConstant(InteractiveScene):
    def construct(self):
        words1 = Text("This constant\nhere")
        words1.to_edge(RIGHT)
        arrow = Arrow(words1.get_bottom() + 0.1 * DOWN, words1.get_bottom() + DOWN + 1.5 * LEFT)
        VGroup(words1, arrow).set_color(YELLOW)

        same = Text("Same").match_style(words1)
        same.move_to(words1.select_part("This"), DR)

        self.play(Write(words1), ShowCreation(arrow), run_time=1)
        self.wait()
        self.play(
            FadeIn(same, 0.5 * UP),
            FadeOut(words1.select_part("This"), 0.5 * UP),
        )
