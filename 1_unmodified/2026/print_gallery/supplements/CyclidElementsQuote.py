# ==============================================================================
# Scene:      CyclidElementsQuote
# Source:     videos/_2026/print_gallery/supplements.py (lines 91-123)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CyclidElementsQuote.py CyclidElementsQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CyclidElementsQuote(InteractiveScene):
    def construct(self):
        # Test
        quote = Text("""
            “I quite intentionally chose serial
            types of objects, such, for instance,
            as a row of prints along the wall and
            blocks of houses in a town. Without the
            cyclic elements, it would be all the
            more difficult to get my meaning over
            to the random viewer.”
        """, alignment="LEFT")
        quote.to_edge(RIGHT)
        quote.shift(UP)
        attribution = Text(
            "From Magic Mirror of M.C. Escher\nby Bruno Ernst.",
            t2s={"Magic Mirror of M.C. Escher": ITALIC},
            font_size=30
        )
        attribution.set_fill(GREY_B)
        attribution.next_to(quote, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        self.play(FadeIn(quote, lag_ratio=0.005, run_time=2))
        self.wait()
        for phrase, color, u in [("row of prints", YELLOW, -1), ("blocks of houses", TEAL, +1)]:
            part = quote[phrase][0]
            underline = Underline(part, stretch_factor=1, buff=u * 0.05)
            underline.set_stroke(color, 3)
            self.play(
                part.animate.set_color(color).set_anim_args(lag_ratio=0.1),
                ShowCreation(underline)
            )
            self.wait()
