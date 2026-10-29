# ==============================================================================
# Scene:      MentionImpossibilityOf3dNumbers
# Source:     videos/_2018/quaternions.py (lines 3261-3285)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionImpossibilityOf3dNumbers.py MentionImpossibilityOf3dNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MentionImpossibilityOf3dNumbers(TeacherStudentsScene):
    def construct(self):
        equations = VGroup(
            OldTex("ij = ?"),
            OldTex("ji = ?"),
        )
        equations.arrange(RIGHT, buff=LARGE_BUFF)
        equations.scale(1.5)
        equations.to_edge(UP)
        self.add(equations)

        why = OldTexText("Why not?")
        why.next_to(self.students[1], UP)

        self.teacher_says(
            "Such 3d numbers \\\\ have no good \\\\ multiplication rule",
            bubble_config={"width": 4, "height": 3},
        )
        self.play_all_student_changes("confused")
        self.wait(2)
        self.play(
            self.students[1].change, "maybe",
            FadeInFromLarge(why),
        )
        self.wait(4)
