# ==============================================================================
# Scene:      CommentOnGeneralFormula
# Source:     videos/_2026/spheres_talk/supplements.py (lines 576-594)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CommentOnGeneralFormula.py CommentOnGeneralFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CommentOnGeneralFormula(InteractiveScene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)
        randy = Randolph()
        randy.next_to(morty, LEFT, buff=1.5)

        self.play(
            morty.says("Beautiful!", mode="hooray"),
            randy.change("hesitant", morty.eyes)
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.debubble(mode="guilty"),
            randy.says("What about\nodd n?", mode="confused", look_at=3 * LEFT + DOWN)
        )
        self.play(Blink(randy))
        self.wait()
