# ==============================================================================
# Scene:      MentionQuiz
# Source:     videos/_2025/grover/qc_supplements.py (lines 168-196)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionQuiz.py MentionQuiz -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MentionQuiz(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher

        to_confusion = VGroup(
            Vector(1.5 * RIGHT, thickness=6),
            Text("???", font_size=90).space_out_submobjects(1.5)
        )
        to_confusion.arrange(RIGHT)
        to_confusion.next_to(self.screen, RIGHT)
        to_confusion.shift(0.5 * UP + LEFT)

        for pi in self.pi_creatures:
            pi.body.insert_n_curves(1000)

        self.play(
            morty.change("angry", self.screen),
            self.change_students("thinking", "tease", "confused", look_at=self.screen),
        )
        self.wait(2)
        self.play(
            morty.change("raise_right_hand", to_confusion),
            self.change_students("erm", "guilty", "hesitant"),
            FadeInFromPoint(to_confusion, morty.get_corner(UL), lag_ratio=0.1),
        )
        self.wait()
        self.play(morty.says("Quiz time!"))
        self.wait(3)
