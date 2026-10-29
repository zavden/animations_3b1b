# ==============================================================================
# Scene:      CombineColors
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 999-1013)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CombineColors.py CombineColors -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject used an absolute path in Grant's Dropbox (RedStill/OrangeStill/GreenStill/BlueStill/RainbowStill.jpg); changed to the file name (placeholder image in raster_images)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/RedStill.jpg (placeholder, make_optics_puzzles_assets.py)
#   - _lib/assets/raster_images/OrangeStill.jpg (placeholder, make_optics_puzzles_assets.py)
#   - _lib/assets/raster_images/GreenStill.jpg (placeholder, make_optics_puzzles_assets.py)
#   - _lib/assets/raster_images/BlueStill.jpg (placeholder, make_optics_puzzles_assets.py)
#   - _lib/assets/raster_images/RainbowStill.jpg (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CombineColors(InteractiveScene):
    def construct(self):
        # Get images
        # CHANGE: the image lived in Grant's Dropbox (absolute path); now it is looked up by name in raster_images (placeholder)
        folder = ""
        images = Group(*(
            ImageMobject(os.path.join(folder, ext + "Still.jpg"))
            for ext in ["Red", "Orange", "Green", "Blue", "Rainbow"]
        ))
        colors = images[:4]
        rainbow = images[4]
        colors.set_height(FRAME_HEIGHT / 2)
        colors.arrange_in_grid(buff=0)
        rainbow.set_height(FRAME_HEIGHT)

        self.add(*colors)
