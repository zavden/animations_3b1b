# ==============================================================================
# Scene:      WignerReverseZoom
# Source:     videos/_2023/gauss_int/supplements.py (lines 39-61)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WignerReverseZoom.py WignerReverseZoom -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private image from Grant's Dropbox (absolute path /Users/grant/...) replaced with a placeholder
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/gauss_int/wigner-speech-transition-4.jpg  (placeholder; script: _lib/assets/generated/2023/gauss_int/make_gauss_int_placeholders.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WignerReverseZoom(InteractiveScene):
    def construct(self):
        # Test
        # CHANGE: the private image from Grant's Dropbox was replaced by a placeholder in _lib/assets/raster_images/gauss_int/
        im1 = ImageMobject("gauss_int/wigner-speech-transition-4.jpg")
        im1.set_height(FRAME_HEIGHT)
        self.add(im1)

        frame = self.frame
        frame.save_state()
        frame.scale(0.4419, about_edge=UL)

        words = TexText(R"Now you're pushing \\ the joke too far...", font_size=20)
        words.set_backstroke(BLACK, 6)
        words.next_to(frame.get_corner(UR), DL, buff=0.2)
        words.shift(0.7 * LEFT)

        self.play(FadeIn(words, lag_ratio=0.1, run_time=2))
        self.play(
            Restore(frame),
            words.animate.set_stroke(width=3),
            run_time=7,
        )
        self.wait()
