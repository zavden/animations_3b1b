# ==============================================================================
# Scene:      HighlightRect
# Source:     videos/_2025/laplace/supplements.py (lines 438-453)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HighlightRect.py HighlightRect -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The image DynamicExpIntuitionStill.png is read next to the file instead of from Grant's Dropbox
#   - DynamicExpIntuitionStill.png is a frame regenerated from the SPlane scene (exponentials.py)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2025/laplace/DynamicExpIntuitionStill.png
#
# Notes:
#   DynamicExpIntuitionStill.png is the frame of the s plane + dynamic graph of e^{st} (SPlane scene of exponentials.py) with s = -1.3-1.3i and t = 3, generated with _lib/assets/generated/2025/laplace/make_DynamicExpIntuitionStill.py (static scene rendered with render.py). The rectangles in the code point exactly at the Re[e^{st}] graph and at the point s of the plane; it is not Grant's exact frame.
# ==============================================================================

from manim_imports_ext import *

class HighlightRect(InteractiveScene):
    def construct(self):
        # CHANGE: the image lived in Grant's Dropbox; now it is next to this file (frame regenerated from the SPlane scene).
        img = ImageMobject(str(Path(__file__).parent / 'DynamicExpIntuitionStill.png'))
        img.set_height(FRAME_HEIGHT)
        self.add(img)

        # Rects
        rects = VGroup(
            Rectangle(2.25, 1).move_to((2.18, 2.74, 0)),
            Rectangle(2, 0.85).move_to((-5.88, -2.2, 0.0)),
        )
        rects.set_stroke(YELLOW, 2)

        self.play(ShowCreation(rects[0]))
        self.play(TransformFromCopy(*rects))
        self.play(FadeOut(rects))
