# ==============================================================================
# Scene:      AskAboutActuallySolving
# Source:     videos/_2019/diffyq/part1/pi_scenes.py (lines 285-312)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl AskAboutActuallySolving.py AskAboutActuallySolving -w -m --fps 15
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

class AskAboutActuallySolving(TeacherStudentsScene):
    def construct(self):
        ode = get_ode()
        ode.to_corner(UL)
        self.add(ode)
        morty = self.teacher

        self.student_says(
            "Yeah yeah, but how do\\\\"
            "you actually \\emph{solve} it?",
            index=1,
            target_mode="sassy",
            added_anims=[morty.change, "thinking"],
        )
        self.play_student_changes(
            "confused", "sassy", "confused",
            look_at=ode,
        )
        self.wait()
        self.teacher_says(
            "What do you mean\\\\ by ``solve''?",
            target_mode="speaking",
            added_anims=[self.change_students(
                *3 * ["erm"]
            )]
        )
        self.play(self.students[1].change, "angry")
        self.wait(3)
