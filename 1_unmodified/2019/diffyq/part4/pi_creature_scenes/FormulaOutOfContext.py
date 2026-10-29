# ==============================================================================
# Scene:      FormulaOutOfContext
# Source:     videos/_2019/diffyq/part4/pi_creature_scenes.py (lines 217-235)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FormulaOutOfContext.py FormulaOutOfContext -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FormulaOutOfContext(TeacherStudentsScene):
    def construct(self):
        formula = OldTex(
            "c_{n} = \\int_0^1 e^{-2\\pi i {n} {t}}f({t}){dt}",
            tex_to_color_map={
                "{n}": YELLOW,
                "{t}": PINK,
            }
        )
        formula.scale(1.5)
        formula.next_to(self.students, UP, LARGE_BUFF)

        self.add(formula)
        self.play_all_student_changes(
            "horrified",
            look_at=formula,
        )
        self.play(self.teacher.change, "tease")
        self.wait(3)
