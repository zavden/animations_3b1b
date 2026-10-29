# ==============================================================================
# Scene:      DescribeBit
# Source:     videos/_2022/wordle/scenes.py (lines 1835-1865)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DescribeBit.py DescribeBit -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DescribeBit(TeacherStudentsScene):
    def construct(self):
        words = OldTexText(
            "Standard unit of\\\\information: The bit",
            tex_to_color_map={"The bit": YELLOW}
        )
        words.next_to(self.teacher.get_corner(UL), UP, MED_LARGE_BUFF)
        words.to_edge(RIGHT)

        self.play(
            self.teacher.change("raise_left_hand"),
            FadeIn(words, UP)
        )
        self.play_student_changes(
            "happy", "pondering", "thinking",
            look_at=words
        )
        self.wait(4)

        formula = OldTex("I = -\\log_2(p)", tex_to_color_map={"I": YELLOW})
        formula.next_to(self.teacher.get_corner(UL), UP)

        self.play(
            words.animate.to_edge(UP),
            FadeIn(formula, UP),
            self.teacher.change("raise_right_hand", formula),
            self.students[0].change("erm", formula),
            self.students[1].change("confused", formula),
            self.students[2].change("pondering", formula),
        )
        self.wait(5)
