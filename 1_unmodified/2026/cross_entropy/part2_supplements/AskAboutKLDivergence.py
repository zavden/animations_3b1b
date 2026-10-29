# ==============================================================================
# Scene:      AskAboutKLDivergence
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 664-694)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutKLDivergence.py AskAboutKLDivergence -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutKLDivergence(TeacherStudentsScene):
    def construct(self):
        # Test
        self.remove(self.background)
        morty = self.teacher
        morty.body.insert_n_curves(1000)
        stds = self.students

        self.play(
            stds[2].says("What about\nKL Divergence?", bubble_direction=LEFT),
            stds[0].change("erm", look_at=stds[2].eyes),
            stds[1].change("confused", look_at=stds[2].eyes),
            morty.change("tease")
        )
        self.wait(3)
        self.play(
            morty.change('raise_right_hand', self.screen),
            self.change_students("pondering", "thinking", "pondering", look_at=self.screen),
            FadeOut(stds[2].bubble)
        )
        self.wait(3)

        # Transition elsewhere
        frame = self.frame
        self.play(
            self.change_students("bump", "hesitant", "well"),
            frame.animate.align_to(morty, LEFT).shift(MED_LARGE_BUFF * LEFT),
            morty.change("raise_left_hand", 8 * RIGHT),
            run_time=2
        )
        self.wait()
