# ==============================================================================
# Scene:      TerryTaoQuote
# Source:     videos/_2019/windmill.py (lines 3648-3713)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TerryTaoQuote.py TerryTaoQuote -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class TerryTaoQuote(Scene):
    def construct(self):
        image = ImageMobject("TerryTao")
        image.set_height(4)
        name = OldTexText("Terence Tao")
        name.scale(1.5)
        name.next_to(image, DOWN, buff=0.2)
        tao = Group(image, name)
        tao.to_corner(DL, buff=MED_SMALL_BUFF)

        tiny_tao = ImageMobject("TerryTaoIMO")
        tiny_tao.match_height(image)
        tiny_tao.next_to(image, RIGHT, LARGE_BUFF)

        quote = self.get_quote()

        self.play(
            FadeInFromDown(image),
            Write(name),
        )
        self.wait()
        self.play(
            FadeIn(tiny_tao, LEFT)
        )
        self.wait()
        self.play(FadeOut(tiny_tao))

        #
        self.play(
            FadeIn(
                quote,
                lag_ratio=0.05,
                run_time=5,
                rate_func=bezier([0, 0, 1, 1])
            )
        )
        self.wait()
        story_line = Line()
        story_line.match_width(quote.story_part)
        story_line.next_to(quote.story_part, DOWN, buff=0)
        story_line.set_color(TEAL),
        self.play(
            quote.story_part.set_color, TEAL,
            ShowCreation(story_line),
            lag_ratio=0.2,
        )
        self.wait()

    def get_quote(self):
        story_words = "fables, stories, and anecdotes"
        quote = OldTexText(
            """
            \\Large
            ``Mathematical problems, or puzzles, are important to real mathematics
            (like solving real-life problems), just as fables, stories, and anecdotes
            are important to the young in understanding real life.''\\\\
            """,
            alignment="",
            arg_separator=" ",
            isolate=[story_words]
        )
        quote.story_part = quote.get_part_by_tex(story_words)
        quote.set_width(FRAME_WIDTH - 2.5)
        quote.to_edge(UP)

        return quote
