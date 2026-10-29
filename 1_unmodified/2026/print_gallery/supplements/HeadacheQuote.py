# ==============================================================================
# Scene:      HeadacheQuote
# Source:     videos/_2026/print_gallery/supplements.py (lines 753-776)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HeadacheQuote.py HeadacheQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HeadacheQuote(InteractiveScene):
    def construct(self):
        # Test
        text = Text(
            "The realization of this\nidea caused him “some\nalmighty headaches.”",
            font_size=48,
            alignment="LEFT"
        )
        line = Line(text.get_corner(UL), text.get_corner(DL))
        line.set_stroke(WHITE, 5)
        line.shift(MED_SMALL_BUFF * LEFT)
        line.scale(1.25)

        attribution = Text("From Bruno Ernst in\nThe Magic Mirror of M.C. Escher", font_size=30, alignment="LEFT")
        attribution.set_color(GREY_A)
        attribution.next_to(line, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        self.add(line)
        self.play(
            FadeIn(text, lag_ratio=0.1, run_time=2),
            FadeIn(attribution, 0.25 * DOWN, time_span=(1, 2))
        )
        self.play(text["“some\nalmighty headaches.”"].animate.set_color(YELLOW))
        self.wait()
