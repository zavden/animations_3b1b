# ==============================================================================
# Scene:      DefineDeterminant
# Source:     videos/_2021/shadows.py (lines 1853-1950)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DefineDeterminant.py DefineDeterminant -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - import of get_det_text from once_useful_constructs.linear_algebra (the original did not import it: NameError)
# ==============================================================================

from manim_imports_ext import *
# CHANGE: get_det_text was not imported (NameError in the original); it lives in once_useful_constructs/linear_algebra.py
from once_useful_constructs.linear_algebra import get_det_text

class DefineDeterminant(Scene):
    def construct(self):
        # Planes
        plane = NumberPlane((-2, 2), (-3, 3))
        plane.set_height(FRAME_HEIGHT)
        planes = VGroup(plane, plane.deepcopy())
        planes[0].to_edge(LEFT, buff=0)
        planes[1].to_edge(RIGHT, buff=0)
        planes[1].set_stroke(GREY_A, 1, 0.5)
        planes[1].faded_lines.set_opacity(0)

        titles = VGroup(
            Text("Input"),
            Text("Output"),
        )
        for title, plane in zip(titles, planes):
            title.next_to(plane.get_top(), DOWN)
            title.add_background_rectangle()

        self.add(planes)

        # Area
        square = Square()
        square.set_stroke(YELLOW, 2)
        square.set_fill(YELLOW, 0.5)
        square.replace(Line(planes[0].c2p(-1, -1), planes[0].c2p(1, 1)))
        area_label = OldTexText("Area", "=", "$A$")
        area_label.set_color_by_tex("$A$", YELLOW)
        area_label.next_to(square, UP)
        area_label.add_background_rectangle()
        self.play(
            DrawBorderThenFill(square),
            FadeIn(area_label, 0.25 * UP, rate_func=squish_rate_func(smooth, 0.5, 1))
        )
        self.wait()

        # Arrow
        arrow = Arrow(*planes)
        arrow_label = Text("Linear transformation", font_size=30)
        arrow_label.next_to(arrow, UP)
        mat_mob = Matrix([["a", "b"], ["c", "d"]], h_buff=0.7, v_buff=0.7)
        mat_mob.set_height(0.7)
        mat_mob.next_to(arrow, DOWN)

        # Apply matrix
        matrix = [
            [0.5, 0.4],
            [0.25, 0.75],
        ]

        for mob in planes[0], square:
            mob.output = mob.deepcopy()
            mob.output.apply_matrix(matrix, about_point=planes[0].c2p(0, 0))
            mob.output.move_to(planes[1].get_center())

        planes[0].output.set_stroke(width=1, opacity=1)
        planes[0].output.faded_lines.set_opacity(0)

        self.play(
            ReplacementTransform(planes[0].copy().fade(1), planes[0].output, run_time=2),
            ReplacementTransform(square.copy().fade(1), square.output, run_time=2),
            ShowCreation(arrow),
            FadeIn(arrow_label, 0.25 * RIGHT),
            FadeIn(mat_mob, 0.25 * RIGHT),
        )
        self.wait()

        # New area
        new_area_label = OldTex(
            "\\text{Area} = ", "{c}", "\\cdot", "{A}",
            tex_to_color_map={
                "{c}": RED,
                "{A}": YELLOW,
            }
        )
        new_area_label.add_background_rectangle()
        new_area_label.next_to(square.output, UP)
        new_area_label.shift(0.5 * RIGHT)

        mmc = mat_mob.copy()
        mmc.scale(1.5)
        det = VGroup(get_det_text(mmc), mmc)
        det.set_height(new_area_label.get_height() * 1.2)
        det.move_to(new_area_label.get_part_by_tex("c"), RIGHT)
        det.match_y(new_area_label[-1])
        det_name = OldTexText("``Determinant''", font_size=36)
        det_name.next_to(det, UP, MED_LARGE_BUFF)
        det_name.set_color(RED)
        det_name.add_background_rectangle()

        self.play(FadeTransform(area_label.copy(), new_area_label))
        self.wait()
        self.play(
            FadeTransform(mat_mob.copy(), det),
            FadeTransform(new_area_label.get_part_by_tex("c"), det_name),
            new_area_label[1].animate.next_to(det, LEFT, SMALL_BUFF).match_y(new_area_label[1]),
        )
        self.wait()
