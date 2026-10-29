# ==============================================================================
# Scene:      ContrastPDEToODE
# Source:     videos/_2019/diffyq/part2/pi_scenes.py (lines 30-80)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContrastPDEToODE.py ContrastPDEToODE -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ContrastPDEToODE(TeacherStudentsScene):
    CONFIG = {
        "random_seed": 2,
    }

    def construct(self):
        student = self.students[2]
        pde, ode = words = VGroup(*[
            OldTexText(
                text + "\\\\",
                "Differential\\\\",
                "Equation"
            )
            for text in ("Partial", "Ordinary")
        ])
        pde[0].set_color(YELLOW)
        ode[0].set_color(BLUE)
        for word in words:
            word.arrange(DOWN, aligned_edge=LEFT)

        words.arrange(RIGHT, buff=LARGE_BUFF)
        words.next_to(student.get_corner(UR), UP, MED_LARGE_BUFF)
        words.shift(UR)
        lt = OldTex("<")
        lt.scale(1.5)
        lt.move_to(Line(pde.get_right(), ode.get_left()))

        for pi in self.pi_creatures:
            pi.add_updater(lambda p: p.look_at(pde))

        self.play(
            FadeInFromDown(VGroup(words, lt)),
            student.change, "raise_right_hand",
        )
        self.play(
            self.change_students("pondering", "pondering", "hooray"),
            self.teacher.change, "happy"
        )
        self.wait(3)
        self.play(
            Swap(ode, pde),
            self.teacher.change, "raise_right_hand",
            self.change_students(
                "erm", "sassy", "confused"
            )
        )
        self.look_at(words)
        self.play_student_changes(
            "thinking", "thinking", "tease",
        )
        self.wait(3)
