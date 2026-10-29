# ==============================================================================
# Scene:      Show90DegreeRotationColumnByColumn
# Source:     videos/_2021/matrix_exp.py (lines 4689-4729)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Show90DegreeRotationColumnByColumn.py Show90DegreeRotationColumnByColumn -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(..., thickness=X) -> FillArrow(...): the thickness in the 2021 code is in scene units and the current Arrow multiplies it by 0.015 (invisible arrows).
#   - Arc(..., buff=0.1): Arc no longer accepts `buff` (before it was ignored by digest_config); it is removed.
# ==============================================================================

from manim_imports_ext import *

class Show90DegreeRotationColumnByColumn(Scene):
    def construct(self):
        plane = NumberPlane()
        plane.scale(2.5)
        back_plane = plane.deepcopy()
        back_plane.set_stroke(color=GREY, opacity=0.5)
        back_plane.add_coordinate_labels()

        plane2 = plane.copy()
        plane3 = plane.copy()
        plane2.apply_matrix([[0, 0], [1, 1]])
        plane3.apply_matrix([[0, -1], [1, 0]])

        vects = VGroup(
            # CHANGE: Arrow(thickness=...) -> FillArrow: thickness in scene units (the current Arrow multiplies it by 0.015)
            FillArrow(plane.get_origin(), plane.c2p(1, 0), fill_color=GREEN, buff=0, thickness=0.075),
            # CHANGE: Arrow(thickness=...) -> FillArrow: thickness in scene units (the current Arrow multiplies it by 0.015)
            FillArrow(plane.get_origin(), plane.c2p(0, 1), fill_color=RED, buff=0, thickness=0.075),
        )

        self.add(back_plane, plane, *vects)
        self.wait()
        self.play(
            Transform(plane, plane2, path_arc=90 * DEGREES),
            Rotate(vects[0], 90 * DEGREES, about_point=plane.get_origin()),
            run_time=2
        )
        self.wait()
        self.play(
            Transform(plane, plane3, path_arc=90 * DEGREES),
            Rotate(vects[1], 90 * DEGREES, about_point=plane.get_origin()),
            run_time=2
        )
        self.wait()

        # CHANGE: Arc no longer accepts `buff` (before it was ignored); it is removed
        arc = Arc(5 * DEGREES, 80 * DEGREES, radius=1.5)
        arc.set_stroke(width=3)
        arc.add_tip(width=0.15, length=0.15)
        arc2 = arc.copy().rotate(PI, about_point=ORIGIN)
        arcs = VGroup(arc, arc2)
        arcs.set_color(GREY_B)
        self.play(*map(ShowCreation, arcs))
        self.wait()
