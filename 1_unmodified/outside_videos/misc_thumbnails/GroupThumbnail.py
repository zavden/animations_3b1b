# ==============================================================================
# Scene:      GroupThumbnail
# Source:     videos/outside_videos/misc_thumbnails.py (lines 75-91)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GroupThumbnail.py GroupThumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GroupThumbnail(ThreeDScene):
    def construct(self):
        cube = Cube()
        cubes = Group(cube)
        for axis in [[1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1]]:
            for angle in [60 * DEGREES]:
                cubes.add(cube.copy().rotate(angle, axis))

        cubes.rotate(95 * DEGREES, RIGHT)
        cubes.rotate(30 * DEGREES, UP)
        cubes.set_height(6)
        cubes.center()
        # cubes.set_y(-0.5)
        cubes.set_color(BLUE_D)
        cubes.set_shadow(0.65)
        cubes.set_gloss(0.5)
        self.add(cubes)
