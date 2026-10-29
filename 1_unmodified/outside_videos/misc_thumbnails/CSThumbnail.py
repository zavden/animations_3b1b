# ==============================================================================
# Scene:      CSThumbnail
# Source:     videos/outside_videos/misc_thumbnails.py (lines 60-72)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CSThumbnail.py CSThumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CSThumbnail(Scene):
    def construct(self):
        self.add(self.get_background())

    def get_background(self, n=12, k=50, zero_color=GREY_C, one_color=GREY_B):
        choices = (Integer(0, color=zero_color), Integer(1, color=one_color))
        background = VGroup(*(
            random.choice(choices).copy()
            for x in range(n * k)
        ))
        background.arrange_in_grid(n, k)
        background.set_height(FRAME_HEIGHT)
        return background
