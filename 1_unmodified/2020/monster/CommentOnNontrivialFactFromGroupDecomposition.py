# ==============================================================================
# Scene:      CommentOnNontrivialFactFromGroupDecomposition
# Source:     videos/_2020/monster.py (lines 3518-3552)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CommentOnNontrivialFactFromGroupDecomposition.py CommentOnNontrivialFactFromGroupDecomposition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CommentOnNontrivialFactFromGroupDecomposition(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "I...don't\\\\get it.",
            target_mode="confused",
            index=2,
            look_at=self.screen,
            added_anims=[self.teacher.change, "guilty"],
        )
        self.play_student_changes("maybe", "tired", look_at=self.screen)
        self.wait(4)

        fp_words = OldTexText("Fact about\\\\polynomials")
        fp_words.scale(1.25)
        as_words = OldTexText("``Atomic structure''\\\\of a group")
        as_words.scale(1.25)
        implies = OldTex("\\Rightarrow").scale(2)

        self.teacher_holds_up(
            fp_words,
            added_anims=[
                RemovePiCreatureBubble(self.students[2]),
            ]
        )
        self.play_student_changes("pondering", "hesitant", "plain", look_at=fp_words)
        self.wait()
        as_words.next_to(fp_words, LEFT, buff=1.5)
        implies.move_to(midpoint(as_words.get_right(), fp_words.get_left()))

        self.play(
            FadeIn(as_words, RIGHT),
            Write(implies),
            self.change_students(*3 * ["pondering"], look_at=as_words)
        )
        self.wait(5)
