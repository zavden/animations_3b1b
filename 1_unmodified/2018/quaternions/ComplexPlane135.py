# ==============================================================================
# Scene:      ComplexPlane135
# Source:     videos/_2018/quaternions.py (lines 5491-5521)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexPlane135.py ComplexPlane135 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexPlane135(Scene):
    def construct(self):
        plane = ComplexPlane(unit_size=2)
        plane.add_coordinates()
        for mob in plane.coordinate_labels:
            mob.scale(2, about_edge=UR)

        angle = 3 * TAU / 8
        circle = Circle(radius=2, color=YELLOW)
        arc = Arc(angle, radius=0.5)
        angle_label = Integer(0, unit="^\\circ")
        angle_label.next_to(arc.point_from_proportion(0.5), UR, SMALL_BUFF)
        line = Line(ORIGIN, 2 * RIGHT)

        point = circle.point_from_proportion(angle / TAU)
        dot = Dot(point, color=PINK)
        arrow = Vector(DR)
        arrow.next_to(dot, UL, SMALL_BUFF)
        arrow.match_color(dot)
        label = OldTex("-\\frac{\\sqrt{2}}{2} + \\frac{\\sqrt{2}}{2} i")
        label.next_to(arrow.get_start(), UP, SMALL_BUFF)
        label.set_background_stroke(width=0)

        self.add(plane, circle, line, dot, label, arrow)
        self.play(
            Rotate(line, angle, about_point=ORIGIN),
            ShowCreation(arc),
            ChangeDecimalToValue(angle_label, 135),
            run_time=3
        )
        self.wait()
