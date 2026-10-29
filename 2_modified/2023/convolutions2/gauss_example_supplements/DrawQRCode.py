# ==============================================================================
# Scene:      DrawQRCode
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 1166-1183)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DrawQRCode.py DrawQRCode -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - SubstackQR2.svg: real QR of https://www.3blue1brown.com, with background and frame as the first 2 submobjects, at the root of _lib/assets/svg_images/ (make_convolutions2_assets.py); the scene asks for it by Grant's Dropbox path and manim_imports_ext finds it by name
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DrawQRCode(InteractiveScene):
    def construct(self):
        # Test
        # self.add(FullScreenRectangle(fill_color=GREY_A))
        code = SVGMobject("/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2023/convolutions2/gauss_example_supplements/images/SubstackQR2.svg")
        code.remove(*code[:2])
        code.set_fill(BLACK, 1)
        code.set_height(7)
        back_rect = SurroundingRectangle(code)
        back_rect.set_fill(GREY_A, 1)
        back_rect.set_stroke(WHITE, 1)

        code.shuffle()
        self.play(
            FadeIn(back_rect, time_span=(3, 5)),
            Write(code, stroke_color=RED_E, stroke_width=2, lag_ratio=0.005, run_time=5),
        )
        self.wait()
