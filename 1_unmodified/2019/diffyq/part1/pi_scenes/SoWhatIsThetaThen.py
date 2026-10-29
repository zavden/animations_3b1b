# ==============================================================================
# Scene:      SoWhatIsThetaThen
# Source:     videos/_2019/diffyq/part1/pi_scenes.py (lines 111-131)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl SoWhatIsThetaThen.py SoWhatIsThetaThen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_ode():
    tex_config = {
        "tex_to_color_map": {
            "{\\theta}": BLUE,
            "{\\dot\\theta}": RED,
            "{\\ddot\\theta}": YELLOW,
            "{t}": WHITE,
            "{\\mu}": WHITE,
        }
    }
    ode = OldTex(
        "{\\ddot\\theta}({t})", "=",
        "-{\\mu} {\\dot\\theta}({t})",
        "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        **tex_config,
    )
    return ode



# ----- From _2019/diffyq/part1/pi_scenes.py -----

class SoWhatIsThetaThen(TeacherStudentsScene):
    def construct(self):
        ode = get_ode()
        ode.to_corner(UL)
        self.add(ode)

        self.student_says(
            "Okay, but then\\\\"
            "what \\emph{is} $\\theta(t)$?"
        )
        self.wait()
        self.play(self.teacher.change, "happy")
        self.wait(2)
        self.teacher_says(
            "First, you must appreciate\\\\"
            "a deep truth...",
            added_anims=[self.change_students(
                *3 * ["confused"]
            )]
        )
        self.wait(4)
