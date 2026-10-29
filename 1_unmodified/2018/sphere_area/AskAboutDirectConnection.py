# ==============================================================================
# Scene:      AskAboutDirectConnection
# Source:     videos/_2018/sphere_area.py (lines 2605-2677)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutDirectConnection.py AskAboutDirectConnection -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Cylinder(Sphere):
    """
    Inherits from sphere so as to be as aligned as possible
    for transformations
    """

    def func(self, u, v):
        return np.array([
            np.cos(v),
            np.sin(v),
            np.cos(u)
        ])


class AskAboutDirectConnection(TeacherStudentsScene, SpecialThreeDScene):
    CONFIG = {
        "camera_config": {
            "light_source_start_point": [-4, 5, 7],
        }
    }

    def construct(self):
        sphere = Sphere()
        cylinder = Cylinder()
        for mob in sphere, cylinder:
            mob.rotate(70 * DEGREES, LEFT)
        formula = OldTex("4\\pi R^2")
        formula.set_color(BLUE)
        circle = Circle()
        circle.set_stroke(width=0)
        circle.set_fill(GREY_BROWN, 1)
        area_label = OldTex("\\pi R^2", background_stroke_width=0)
        area_label.scale(1.5)
        circle.add(area_label)
        group = VGroup(
            sphere, cylinder, formula, circle
        )
        for mob in group:
            mob.set_height(1.5)
        formula.scale(0.5)
        group.arrange(RIGHT, buff=1.5)
        group.to_edge(UP, buff=2)
        group[1:3].to_edge(UP)

        arrows = VGroup()
        for m1, m2 in zip(group, group[1:]):
            arrow = Arrow(
                m1.get_center(), m2.get_center(),
                buff=1,
                color=WHITE
            )
            arrows.add(arrow)
        direct_arrow = Arrow(
            sphere, circle, color=WHITE
        )
        q_marks = OldTex(*"???")
        q_marks.space_out_submobjects(1.5)
        q_marks.scale(1.5)
        q_marks.next_to(direct_arrow, DOWN)

        self.play(
            self.teacher.change, "raise_right_hand",
            self.change_students(
                *3 * ["pondering"],
                look_at=group,
            ),
            LaggedStartMap(FadeInFromDown, group),
            LaggedStartMap(GrowArrow, arrows)
        )
        self.wait()
        self.play(
            self.teacher.change, "pondering",
            self.students[2].change, "raise_right_hand",
            GrowArrow(direct_arrow),
            LaggedStartMap(
                FadeInFrom, q_marks,
                lambda m: (m, UP),
                lag_ratio=0.8,
                run_time=1.5,
            )
        )
        self.play_student_changes(
            "erm", "sassy", "raise_right_hand",
        )
        self.wait(2)
        self.look_at(group)
        self.wait(2)
