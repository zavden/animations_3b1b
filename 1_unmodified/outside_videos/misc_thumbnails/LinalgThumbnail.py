# ==============================================================================
# Scene:      LinalgThumbnail
# Source:     videos/outside_videos/misc_thumbnails.py (lines 4-48)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LinalgThumbnail.py LinalgThumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LinalgThumbnail(ThreeDScene):
    CONFIG = {
        "camera_config": {
            "anti_alias_width": 0,
        }
    }

    def construct(self):
        grid = NumberPlane((-10, 10), (-10, 10), faded_line_ratio=1)
        grid.set_stroke(width=6)
        grid.faded_lines.set_stroke(width=1)
        grid.apply_matrix([[3, 2], [1, -1]])
        # self.add(grid)

        frame = self.camera.frame
        frame.reorient(0, 75)

        cube = Cube()
        cube.set_color(BLUE)
        cube.set_opacity(0.5)

        edges = VGroup()
        for vect in [OUT, RIGHT, UP, LEFT, DOWN, IN]:
            face = Square()
            face.shift(OUT)
            face.apply_matrix(z_to_vector(vect))
            edges.add(face)
        for sm in edges.family_members_with_points():
            sm.flat_stroke = False
            sm.set_joint_roundness(1)

        edges.set_stroke(WHITE, 4)
        edges.replace(cube)
        edges.apply_depth_test()
        cube = Group(cube, edges)

        cube2 = cube.copy().apply_matrix(
            [[1, 0, 1], [0, 1, 0], [0, 0, 1]]
        )
        # cube2.match_height(cube)
        arrow = Vector(RIGHT)
        arrow.rotate(PI / 2, RIGHT)
        group = Group(cube, arrow, cube2)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        self.add(group)
