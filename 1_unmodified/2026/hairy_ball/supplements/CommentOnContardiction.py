# ==============================================================================
# Scene:      CommentOnContardiction
# Source:     videos/_2026/hairy_ball/supplements.py (lines 677-694)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CommentOnContardiction.py CommentOnContardiction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CommentOnContardiction(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer(height=3)
        morty.body.insert_n_curves(1000)
        morty.to_corner(DR)
        morty.shift(2 * LEFT)

        qed = Text("Q.E.D.")
        qed.next_to(morty.get_corner(UR), UP, MED_SMALL_BUFF)

        self.play(morty.says("Contradiction!", mode="hooray"))
        self.play(Blink(morty))
        self.wait()
        self.play(morty.change('raise_left_hand', look_at=qed), FadeIn(qed, 0.25 * UP))
        self.play(Blink(morty))
        self.play(morty.change('tease'))
        self.wait()
