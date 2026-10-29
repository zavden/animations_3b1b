# ==============================================================================
# Scene:      GreeneAndLobb
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 627-647)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GreeneAndLobb.py GreeneAndLobb -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The photos of Joshua Greene and Andrew Lobb are missing (private): placeholder images JoshuaGreene.png and AndrewLobb.png; the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/JoshuaGreene.png (placeholder, _lib/assets/generated/2024/inscribed_rect/make_inscribed_rect_images.py)
#   - _lib/assets/raster_images/AndrewLobb.png (placeholder, _lib/assets/generated/2024/inscribed_rect/make_inscribed_rect_images.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GreeneAndLobb(InteractiveScene):
    def construct(self):
        # Test
        names = VGroup(
            Text("Joshua Greene"),
            Text("Andrew Lobb"),
        )
        images = Group(
            ImageMobject("JoshuaGreene"),
            ImageMobject("AndrewLobb"),
        )
        for image in images:
            image.set_height(5)
        images.arrange(RIGHT, buff=1)
        for image, name in zip(images, names):
            name.next_to(image, DOWN)
            self.play(
                FadeIn(image, 0.5 * UP),
                Write(name)
            )
        self.wait()
