# ==============================================================================
# Scene:      OtherVideos
# Source:     videos/_2023/gauss_int/supplements.py (lines 113-144)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OtherVideos.py OtherVideos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private thumbnails from Grant's Dropbox (absolute folder /Users/grant/...) replaced with placeholders in gauss_int/
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/gauss_int/VCubingxThumbnail.png  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/gauss_int/BrimathThumbnail.png  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/gauss_int/DrAlters.png  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
#   - _lib/assets/raster_images/gauss_int/KeithConrad.png  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OtherVideos(InteractiveScene):
    def construct(self):
        # Test
        # CHANGE: the private image from Grant's Dropbox was replaced by a placeholder in _lib/assets/raster_images/gauss_int/
        folder = "gauss_int/"
        images = Group(*(
            ImageMobject(os.path.join(folder, name))
            for name in ["VCubingxThumbnail", "BrimathThumbnail", "DrAlters", "KeithConrad"]
        ))
        images.set_height(0.35 * FRAME_HEIGHT)
        images.arrange_in_grid(h_buff=2.0, v_buff=1.0)
        images.to_edge(DOWN)
        names = VGroup(
            Text("vcubingx"),
            Text("BriTheMathGuy"),
            Text("idan-alter.github.io"),
            Text("kconrad.math.uconn.edu"),
        )

        rects = VGroup()
        groups = Group()
        for name, image in zip(names, images):
            name.scale(0.75)
            name.move_to(image.get_top())
            name.shift(0.25 * UP)
            rect = SurroundingRectangle(image, buff=0)
            rects.add(rect)
            groups.add(Group(rect, image, name))

        rects.set_stroke(WHITE, 4)

        self.play(LaggedStartMap(FadeIn, groups, lag_ratio=0.5))
        self.wait()
