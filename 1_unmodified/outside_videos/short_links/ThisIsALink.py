# ==============================================================================
# Scene:      ThisIsALink
# Source:     videos/outside_videos/short_links.py (lines 92-111)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisIsALink.py ThisIsALink -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThisIsALink(InteractiveScene):
    def construct(self):
        # Test
        rect = Rectangle(3.5, 0.35)
        rect.set_stroke(YELLOW, 3)
        rect.insert_n_curves(100)
        rect.move_to(2 * UP)
        words = Text("This is\na link!", font_size=60)
        words.next_to(rect, DOWN, buff=2)
        arrow = Arrow(words, rect)
        arrow.shift(0.1 * UP)
        VGroup(words, arrow).set_color(YELLOW)

        self.add(words)
        self.play(
            VShowPassingFlash(rect.copy().set_stroke(width=5), time_width=1.5),
            ShowCreation(rect),
            ShowCreation(arrow),
        )
        self.wait()
