# ==============================================================================
# Scene:      MultiplicationFromTheRight
# Source:     videos/_2018/quaternions.py (lines 6010-6046)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MultiplicationFromTheRight.py MultiplicationFromTheRight -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MultiplicationFromTheRight(Scene):
    def construct(self):
        i, dot, j = product = OldTex("i", "\\cdot", "j")
        product.set_height(1.5)
        product.to_edge(UP, buff=LARGE_BUFF)
        i.set_color(GREEN)
        j.set_color(RED)
        i_rect = SurroundingRectangle(i)
        j_rect = SurroundingRectangle(j)
        i_rect.match_height(j_rect, about_edge=UP, stretch=True)
        VGroup(i_rect, j_rect).set_color(WHITE)
        action_words = OldTexText("Think of as \\\\ an action")
        point_words = OldTexText("Think of as \\\\ a point")
        action_words.next_to(i_rect, LEFT)
        point_words.next_to(j_rect, RIGHT)

        arrow = Arrow(
            i.get_top(),
            j.get_top(),
            path_arc=-PI,
        )
        arrow.set_stroke(width=2)

        self.add(product)
        self.play(ShowCreation(arrow))
        self.play(
            FadeIn(i_rect),
            Write(action_words)
        )
        self.wait()
        self.play(
            FadeIn(j_rect),
            Write(point_words)
        )
        self.wait(2)
        self.play(arrow.flip)
        self.play(Swap(point_words, action_words))
