# ==============================================================================
# Scene:      NotTheMostComputationallyEfficient
# Source:     videos/_2018/cramer.py (lines 302-318)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotTheMostComputationallyEfficient.py NotTheMostComputationallyEfficient -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NotTheMostComputationallyEfficient(Scene):
    CONFIG = {
        "words": "Not the most \\\\ computationally efficient",
        "word_height": 4,
        "opacity": 0.7,
    }

    def construct(self):
        big_rect = FullScreenFadeRectangle(opacity=self.opacity)
        self.add(big_rect)

        words = OldTexText(self.words)
        words.set_color(RED)
        words.set_stroke(WHITE, 1)
        words.set_width(FRAME_WIDTH - 2 * MED_LARGE_BUFF)
        self.play(Write(words))
        self.wait()
