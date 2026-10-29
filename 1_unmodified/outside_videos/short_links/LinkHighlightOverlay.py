# ==============================================================================
# Scene:      LinkHighlightOverlay
# Source:     videos/outside_videos/short_links.py (lines 114-129)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LinkHighlightOverlay.py LinkHighlightOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LinkHighlightOverlay(InteractiveScene):
    def construct(self):
        # # Test
        # image = ImageMobject("/Users/grant/Desktop/ShortSample.png")
        # image.set_height(FRAME_HEIGHT)
        # self.add(image)

        # Rect
        rect = VMobject()
        rect.set_points_as_corners([UR, UL, DL, DR])
        rect.set_shape(3.5, 0.5)
        rect.move_to([-2.125, -3.315,  0.], LEFT).shift(0 * UP)
        rect.insert_n_curves(100)
        rect.set_stroke(YELLOW, 4)

        self.play(VShowPassingFlash(rect, time_width=1.5, run_time=3))
