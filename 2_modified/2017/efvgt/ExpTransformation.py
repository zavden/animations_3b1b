# ==============================================================================
# Scene:      ExpTransformation
# Source:     videos/_2017/efvgt.py (lines 3322-3352)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExpTransformation.py ExpTransformation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The repo stubbed ComplexTransformationScene out; import the ported once_useful_constructs one
# ==============================================================================

from manim_imports_ext import *

# CHANGE: The repo stubbed ComplexTransformationScene out; import the ported once_useful_constructs one
from once_useful_constructs.complex_transformation_scene import ComplexTransformationScene


class ExpTransformation(ComplexTransformationScene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }
    def construct(self):
        self.camera.camera_distance = 10,
        self.add_transformable_plane()
        self.prepare_for_transformation(self.plane)
        final_plane = self.plane.copy().apply_complex_function(np.exp)
        cylinder = self.plane.copy().apply_function(
            lambda x_y_z : np.array([x_y_z[0], np.sin(x_y_z[1]), -np.cos(x_y_z[1])])
        )
        title = OldTex("x \\to e^x")
        title.add_background_rectangle()
        title.scale(1.5)
        title.next_to(ORIGIN, RIGHT)
        title.to_edge(UP, buff = MED_SMALL_BUFF)
        self.add_foreground_mobjects(title)

        self.play(Transform(
            self.plane, cylinder, 
            run_time = 3,
            path_arc_axis = RIGHT,
            path_arc = np.pi,
        ))
        self.play(Rotate(
            self.plane, -np.pi/3, UP, 
            run_time = 5
        ))
        self.play(Transform(self.plane, final_plane, run_time = 3))
        self.wait(3)
