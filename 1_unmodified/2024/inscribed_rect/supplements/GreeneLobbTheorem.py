# ==============================================================================
# Scene:      GreeneLobbTheorem
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 650-674)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GreeneLobbTheorem.py GreeneLobbTheorem -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GreeneLobbTheorem(InteractiveScene):
    def construct(self):
        # Text
        text = Text("""
            Theorem by Greene and Lobb (2020):
            Every smooth closed curve contains
            inscribed rectangles of all possible
            aspect ratios.
        """, t2s={"smooth": ITALIC}, alignment="LEFT")
        text.to_corner(UL)

        title = text["Theorem by Greene and Lobb (2020):"][0]
        underline = Underline(title, stretch_factor=1.1, buff=-0.025)
        underline.set_color(TEAL)
        title.match_color(underline)
        body = text[len(title):]
        body.shift(0.1 * DOWN)

        self.play(
            FadeIn(title),
            ShowCreation(underline)
        )
        self.wait()
        self.play(Write(body, lag_ratio=0.05, run_time=3))
        self.wait()
