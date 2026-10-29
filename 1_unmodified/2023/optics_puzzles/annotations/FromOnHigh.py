# ==============================================================================
# Scene:      FromOnHigh
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 319-344)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FromOnHigh.py FromOnHigh -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FromOnHigh(InteractiveScene):
    def construct(self):
        rects = ScreenRectangle().replicate(3)
        rects.set_height(0.3 * FRAME_HEIGHT)
        rects.arrange(RIGHT)
        # self.add(rects)

        top_words = Text("Authoritative explainer")
        top_words.to_edge(UP)
        low_words = Text("Fundamental understanding")
        low_words.to_edge(DOWN)
        cross = Cross(top_words)

        top_arrows = VGroup(*(Arrow(top_words.get_bottom(), rect.get_top()) for rect in rects))
        low_arrows = VGroup(*(Arrow(low_words.get_top(), rect.get_bottom()) for rect in rects))

        # Test
        self.add(top_words)
        self.play(LaggedStartMap(GrowArrow, top_arrows))
        self.play(ShowCreation(cross))
        self.wait()
        self.play(
            Transform(top_arrows, low_arrows),
            FadeTransform(VGroup(top_words, cross), low_words),
        )
        self.wait()
