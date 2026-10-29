# ==============================================================================
# Scene:      AskAboutHomology
# Source:     videos/_2026/hairy_ball/supplements.py (lines 856-880)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutHomology.py AskAboutHomology -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutHomology(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        chain = Tex(R"\cdots C_{2} \xrightarrow{\partial_2} C_1 \xrightarrow{\partial_1} C_0 \xrightarrow{\partial_0} 0")
        chain.next_to(stds[2], UP, buff=MED_LARGE_BUFF)
        chain.align_to(stds[2].get_center(), RIGHT)

        self.play(
            morty.change("well", stds[2].eyes),
            stds[2].says(
                "What about\nusing homology?",
                mode="tease",
                bubble_direction=LEFT,
                look_at=morty.eyes
            )
        )
        self.play(
            stds[2].change("raise_left_hand", chain),
            self.change_students("confused", "erm"),
            Write(chain),
        )
        self.wait(3)
