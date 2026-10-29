# ==============================================================================
# Scene:      HoldUpThumbnail
# Source:     videos/_2024/transformers/chm.py (lines 10-29)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HoldUpThumbnail.py HoldUpThumbnail -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - raster_images/Chapter5_TN3.png (placeholder; Grant's Dropbox path, which _lib resolves by name)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HoldUpThumbnail(TeacherStudentsScene):
    def construct(self):
        # Test
        im = ImageMobject("/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2024/transformers/Thumbnails/Chapter5_TN3.png")
        im_group = Group(
            SurroundingRectangle(im, buff=0).set_stroke(WHITE, 3),
            im
        )
        im_group.set_height(3)
        im_group.move_to(self.hold_up_spot, DOWN)

        morty = self.teacher
        stds = self.students

        self.play(
            FadeIn(im_group, UP),
            morty.change("raise_right_hand", look_at=im_group),
            self.change_students("tease", "happy", "tease", look_at=im_group),
        )
        self.wait(4)
