# ==============================================================================
# Scene:      HoldUpLastVideo
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 524-550)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HoldUpLastVideo.py HoldUpLastVideo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject used an absolute path in Grant's Dropbox (Part2Thumbnail4.png); changed to the file name (placeholder image in raster_images)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Part2Thumbnail4.png (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from manim_imports_ext import *

class HoldUpLastVideo(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        # CHANGE: the image lived in Grant's Dropbox (absolute path); now it is looked up by name in raster_images (placeholder)
        image = ImageMobject("Part2Thumbnail4")
        tn = Group(
            SurroundingRectangle(image, buff=0).set_stroke(WHITE, 3),
            image,
        )
        tn.set_height(3)
        tn.move_to(self.hold_up_spot, DOWN)
        tn.shift(0.25 * DOWN)

        label = Text("Last video")
        arrow = Vector(RIGHT)
        arrow.next_to(tn, LEFT)
        label.next_to(arrow, LEFT)

        self.play(
            self.teacher.change("raise_right_hand", tn),
            FadeIn(tn, UP),
            self.change_students("pondering", "erm", "tease", look_at=tn)
        )
        self.play(
            FadeIn(label, lag_ratio=0.1),
            GrowArrow(arrow)
        )
        self.wait(4)
