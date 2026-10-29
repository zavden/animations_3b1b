# ==============================================================================
# Scene:      ShowDistanceFormula
# Source:     videos/_2017/highD.py (lines 1739-1769)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowDistanceFormula.py ShowDistanceFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowDistanceFormula(TeacherStudentsScene):
    def construct(self):
        rule = OldTex(
            "||(", "x_1", ", ", "x_2", "\\dots, ", "x_n", ")||", 
            "=", 
            "\\sqrt", "{x_1^2", " + ", "x_2^2", " +\\cdots", "x_n^2", "}"
        )
        rule.set_color_by_tex_to_color_map({
            "x_1" : GREEN,
            "x_2" : RED,
            "x_n" : BLUE,
        })
        for part in rule.get_parts_by_tex("x_"):
            if len(part) > 2:
                part[1].set_color(WHITE)
        rule.next_to(self.teacher, UP, LARGE_BUFF)
        rule.to_edge(RIGHT)
        rule.shift(UP)

        rule.save_state()
        rule.shift(2*DOWN)
        rule.set_fill(opacity = 0)

        self.play(
            rule.restore,
            self.teacher.change, "raise_right_hand",
        )
        self.wait(3)
        self.student_says("Why?", index = 0)
        self.play(self.teacher.change, "thinking")
        self.wait(3)
