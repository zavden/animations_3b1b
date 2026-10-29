# ==============================================================================
# Scene:      WignerZoom
# Source:     videos/_2023/gauss_int/supplements.py (lines 25-36)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WignerZoom.py WignerZoom -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private image from Grant's Dropbox (absolute path /Users/grant/...) replaced with a placeholder
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/gauss_int/wigner-speech-transition-3.jpg  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WignerZoom(InteractiveScene):
    def construct(self):
        # CHANGE: the private image from Grant's Dropbox was replaced by a placeholder in _lib/assets/raster_images/gauss_int/
        im1 = ImageMobject("gauss_int/wigner-speech-transition-3.jpg")
        im1.set_height(FRAME_HEIGHT)
        self.add(im1)

        # Test
        self.play(
            self.frame.animate.scale(0.4419, about_edge=UL),
            run_time=4,
        )
        self.wait()
