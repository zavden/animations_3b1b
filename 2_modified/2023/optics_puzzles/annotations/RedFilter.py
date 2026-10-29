# ==============================================================================
# Scene:      RedFilter
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 832-873)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RedFilter.py RedFilter -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject used an absolute path in Grant's Dropbox (RedFilter.jpg); changed to the file name (placeholder image in raster_images)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/RedFilter.jpg (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RedFilter(InteractiveScene):
    def construct(self):
        # CHANGE: the image lived in Grant's Dropbox (absolute path); now it is looked up by name in raster_images (placeholder)
        image = ImageMobject("RedFilter")
        image.set_height(FRAME_HEIGHT)

        # self.add(image)

        plane = NumberPlane()
        plane.fade(0.75)

        # Pixel indicator
        indicator = self.get_pixel_indicator(image)
        indicator.move_to(plane.c2p(5.25, -0.25), DOWN)

        self.add(indicator)

        # Move around
        self.wait()
        self.play(
            indicator.animate.move_to(plane.c2p(1.5, -0.125), DOWN),
            run_time=6,
        )
        self.wait()
        self.play(
            indicator.animate.move_to(plane.c2p(-3.5, 0), DOWN),
            run_time=6,
        )
        self.wait()

    def get_pixel_indicator(self, image, vect_len=2.0, direction=DOWN, square_size=1.0):
        vect = Vector(vect_len * direction, stroke_color=WHITE)
        square = Square(side_length=square_size)
        square.set_stroke(WHITE, 1)
        square.next_to(vect, -direction)

        def get_color():
            points = vect.get_end() + 0.05 * compass_directions(12)
            rgbs = np.array([image.point_to_rgb(point) for point in points])
            return rgb_to_color(rgbs.mean(0))

        square.add_updater(lambda s: s.set_fill(get_color(), 1))
        return VGroup(square, vect)
