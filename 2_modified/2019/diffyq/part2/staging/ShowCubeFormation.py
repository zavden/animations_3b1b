# ==============================================================================
# Scene:      ShowCubeFormation
# Source:     videos/_2019/diffyq/part2/staging.py (lines 369-414)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowCubeFormation.py ShowCubeFormation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use Cairo surfaces/spheres/cubes as groups of VMobject faces compatible with DrawBorderThenFill and the original indexing.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's VMobject faces, needed for fill, stroke and indexing.
from cairo_compat import CairoCube as Cube

class ShowCubeFormation(ThreeDScene):
    CONFIG = {
        "camera_config": {
            "shading_factor": 1.0,
        },
        "color": False,
    }

    def construct(self):
        light_source = self.camera.light_source
        light_source.move_to(np.array([-6, -3, 6]))

        cube = Cube(
            side_length=4,
            fill_color=GREY,
            stroke_color=WHITE,
            stroke_width=0.5,
        )
        cube.set_fill(opacity=1)
        if self.color:
            # cube[0].set_color(BLUE)
            # cube[1].set_color(RED)
            # for face in cube[2:]:
            #     face.set_color([BLUE, RED])
            cube.color_using_background_image("VerticalTempGradient")

        # light_source.next_to(cube, np.array([1, -1, 1]), buff=2)

        cube_3d = cube.copy()
        cube_2d = cube_3d.copy().stretch(0, 2)
        cube_1d = cube_2d.copy().stretch(0, 1)
        cube_0d = cube_1d.copy().stretch(0, 0)

        cube.become(cube_0d)

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-145 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.05)

        for target in [cube_1d, cube_2d, cube_3d]:
            self.play(
                Transform(cube, target, run_time=1.5)
            )
        self.wait(8)
