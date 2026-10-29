# ==============================================================================
# Scene:      AddedPromoWords
# Source:     videos/_2017/putnam.py (lines 1495-1507)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AddedPromoWords.py AddedPromoWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AddedPromoWords(Scene):
    def construct(self):
        words = OldTexText(
            "First", "$2^8$", "vistors get",
            "$(e^\\pi - \\pi)\\%$", "off"
        )
        words.set_width(FRAME_WIDTH - 1)
        words.to_edge(DOWN)
        words.set_color_by_tex("2^8", YELLOW)
        words.set_color_by_tex("pi", PINK)

        self.play(Write(words))
        self.wait()
