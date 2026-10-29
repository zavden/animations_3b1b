# ==============================================================================
# Scene:      Show90DegreeRotation
# Source:     videos/_2021/matrix_exp.py (lines 4668-4686)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Show90DegreeRotation.py Show90DegreeRotation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(..., thickness=X) -> FillArrow(...): the thickness in the 2021 code is in scene units and the current Arrow multiplies it by 0.015 (invisible arrows).
# ==============================================================================

from manim_imports_ext import *

class Show90DegreeRotation(Scene):
    def construct(self):
        plane = NumberPlane()
        plane.scale(2.5)
        back_plane = plane.deepcopy()
        back_plane.set_stroke(color=GREY, opacity=0.5)
        back_plane.add_coordinate_labels()

        vects = VGroup(
            # CHANGE: Arrow(thickness=...) -> FillArrow: thickness in scene units (the current Arrow multiplies it by 0.015)
            FillArrow(plane.get_origin(), plane.c2p(1, 0), fill_color=GREEN, buff=0, thickness=0.075),
            # CHANGE: Arrow(thickness=...) -> FillArrow: thickness in scene units (the current Arrow multiplies it by 0.015)
            FillArrow(plane.get_origin(), plane.c2p(0, 1), fill_color=RED, buff=0, thickness=0.075),
        )
        plane.add(*vects)
        plane.set_stroke(background=True)

        self.add(back_plane, plane)
        self.wait()
        self.play(Rotate(plane, 90 * DEGREES, run_time=3))
        self.wait()
