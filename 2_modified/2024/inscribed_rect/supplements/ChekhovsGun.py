# ==============================================================================
# Scene:      ChekhovsGun
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 319-347)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ChekhovsGun.py ChekhovsGun -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The Chekhov portrait is missing (private): placeholder image AntonChekhovPortrait.png; the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/AntonChekhovPortrait.png (placeholder, _lib/assets/generated/2024/inscribed_rect/make_inscribed_rect_images.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ChekhovsGun(InteractiveScene):
    def construct(self):
        # Add image
        image = ImageMobject("AntonChekhovPortrait")
        image.set_height(5)
        image.to_edge(LEFT, buff=1).to_edge(UP, buff=1)
        border = SurroundingRectangle(image, buff=0)
        border.set_stroke(GREY_B, 2)
        border.set_anti_alias_width(20)
        name = Text("Anton Chekhov")
        name.next_to(image, DOWN)

        self.play(
            Write(name),
            FadeIn(Group(image, border), UP)
        )
        self.wait()

        # Add quote
        quote = TexText(R"""
            ``If in the first act you \\
            have hung a pistol on the \\
            wall, then in the following \\
            one it should be fired.'' \\
        """, alignment="")
        quote.next_to(image, RIGHT, buff=2)

        self.play(Write(quote, run_time=4, lag_ratio=0.2))
        self.wait()
