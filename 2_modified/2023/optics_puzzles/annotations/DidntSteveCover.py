# ==============================================================================
# Scene:      DidntSteveCover
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 77-97)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DidntSteveCover.py DidntSteveCover -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject used an absolute path in Grant's Dropbox (MouldThumbnail.jpg); changed to the file name (placeholder image in raster_images)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/MouldThumbnail.jpg (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DidntSteveCover(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        # CHANGE: the image lived in Grant's Dropbox (absolute path); now it is looked up by name in raster_images (placeholder)
        image = ImageMobject("MouldThumbnail")
        image.set_height(3)
        thumbnail = Group(
            SurroundingRectangle(image, buff=0).set_stroke(WHITE, 3),
            image
        )
        thumbnail.next_to(stds[2].get_corner(UR), UP, buff=1.0)
        thumbnail.shift(RIGHT)

        # Test
        self.play(
            stds[2].says("Didn't Steve Mould\ncover this?", mode="raise_right_hand"),
            morty.change("tease"),
            self.change_students("pondering", "pondering", look_at=thumbnail),
            FadeIn(thumbnail, UP)
        )
        self.wait(4)
