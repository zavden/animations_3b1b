# ==============================================================================
# Scene:      GoalsOfMath
# Source:     videos/_2021/shadows.py (lines 6523-6550)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GoalsOfMath.py GoalsOfMath -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GoalsOfMath(TeacherStudentsScene):
    def construct(self):
        words = Text("The goal of math\nis to answer questions")
        words.move_to(self.hold_up_spot, DOWN)
        words.to_edge(RIGHT, buff=2.0)
        aq = words.get_part_by_text("answer questions")
        aq.set_color(BLUE)
        dni = Text(
            "develop new ideas",
            t2c={"new ideas": YELLOW},
            t2s={"new ideas": ITALIC},
        )
        dni.move_to(aq, LEFT)

        self.play(
            self.teacher.change("raise_right_hand", words),
            self.change_students(*3 * ["pondering"], look_at=words),
            Write(words)
        )
        self.wait(2)
        self.add(aq, self.teacher)
        self.play(
            aq.animate.shift(0.5 * DOWN).set_opacity(0.2),
            Write(dni),
            self.teacher.change("well", words),
            self.change_students(*3 * ["thinking"], look_at=words)
        )
        self.wait(3)
