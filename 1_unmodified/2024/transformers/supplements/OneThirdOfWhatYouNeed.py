# ==============================================================================
# Scene:      OneThirdOfWhatYouNeed
# Source:     videos/_2024/transformers/supplements.py (lines 1282-1314)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneThirdOfWhatYouNeed.py OneThirdOfWhatYouNeed -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OneThirdOfWhatYouNeed(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle().fix_in_frame())
        title = Text("Attention is All You Need", font_size=72)
        all_word = title["All"][0]
        cross = Line(all_word.get_left(), all_word.get_right())
        cross.set_stroke(RED, 8)
        correction = Text("About 1/3 of What", font_size=60)
        correction.set_color(RED)
        correction.next_to(all_word, UP, MED_LARGE_BUFF)
        lines = VGroup(
            CubicBezier(
                all_word.get_corner(UP + v),
                all_word.get_corner(UP + v) + 0.5 * UP,
                correction.get_corner(DOWN + v) + 0.5 * DOWN,
                correction.get_corner(DOWN + v),
            )
            for v in [LEFT, RIGHT]
        )
        lines.set_stroke(RED, 2)

        self.add(title)
        self.wait()
        self.add(all_word, cross)
        self.play(ShowCreation(cross), all_word.animate.set_fill(opacity=0.5))
        self.play(
            FadeTransform(all_word.copy(), correction),
            ShowCreation(lines, lag_ratio=0),
        )
        self.wait()
        self.play(self.frame.animate.set_y(-3.75).set_height(11), run_time=2)
        self.wait()
