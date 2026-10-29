# ==============================================================================
# Scene:      GleickQuote
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 342-369)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GleickQuote.py GleickQuote -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class GleickQuote(Scene):
    def construct(self):
        quote = OldTexText(
            "``[Phase space is] one of the most\\\\",
            "powerful inventions", "of modern science.''\\\\",
        )
        quote.power_part = quote.get_part_by_tex("power")
        book = ImageMobject("ChaosBookCover")
        book.set_height(5)
        book.next_to(ORIGIN, LEFT)
        book.to_edge(DOWN)
        gleick = ImageMobject("JamesGleick")
        gleick.set_height(5)
        gleick.next_to(ORIGIN, RIGHT)
        gleick.to_edge(DOWN)
        quote.to_edge(UP)

        self.play(
            FadeIn(book, RIGHT),
            FadeIn(gleick, LEFT),
        )
        self.wait()
        self.play(Write(quote))
        self.play(Write(
            quote.power_part.copy().set_color(BLUE),
            run_time=1
        ))
        self.wait()
