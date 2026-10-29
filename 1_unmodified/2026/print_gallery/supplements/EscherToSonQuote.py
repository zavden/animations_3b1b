# ==============================================================================
# Scene:      EscherToSonQuote
# Source:     videos/_2026/print_gallery/supplements.py (lines 24-63)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EscherToSonQuote.py EscherToSonQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EscherToSonQuote(InteractiveScene):
    def construct(self):
        # Add quote
        quote = Text("""
            “...the most peculiar thing I
            have ever done...a young man
            looking with interest at a print
            on the wall of an exhibition
            that features himself.”
        """, alignment="LEFT")
        quote.to_edge(RIGHT)
        quote.set_color(GREY_B)

        underline = VGroup(
            Underline(quote["the most peculiar thing I"], buff=-0.05, stretch_factor=1),
            Underline(quote["have ever done"], buff=0.05, stretch_factor=1),
        )
        underline.set_stroke(TEAL, 2)

        self.play(FadeIn(quote, lag_ratio=5e-3, run_time=2))
        self.play(
            LaggedStart(
                quote["a young man"].animate.set_fill(YELLOW).set_anim_args(lag_ratio=0.1),
                quote["looking with interest at a print"].animate.set_fill(YELLOW).set_anim_args(lag_ratio=0.1),
                quote["that features himself"].animate.set_fill(YELLOW).set_anim_args(lag_ratio=0.1),
                lag_ratio=0.5
            )
        )
        self.wait()
        self.play(
            quote[20:].animate.set_fill(GREY),
            LaggedStart(
                quote["the most peculiar thing I"].animate.set_fill(TEAL).set_anim_args(lag_ratio=0.1),
                quote["have ever done"].animate.set_fill(TEAL).set_anim_args(lag_ratio=0.1),
                lag_ratio=0.5,
                run_time=2
            ),
            Write(underline, run_time=4, lag_ratio=0.5),
        )
        self.wait()
