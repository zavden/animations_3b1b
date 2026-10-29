# ==============================================================================
# Scene:      HoldUpDiffractionEquationInAnticipation
# Source:     videos/_2024/holograms/supplements.py (lines 668-699)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldUpDiffractionEquationInAnticipation.py HoldUpDiffractionEquationInAnticipation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HoldUpDiffractionEquationInAnticipation(TeacherStudentsScene):
    def construct(self):
        # Test
        equation = Tex(R"d \cdot \sin(\theta) = n \lambda", font_size=60)
        equation.move_to(self.hold_up_spot, DOWN)
        name = TexText("Diffraction equation")
        name.next_to(equation, UP, buff=1.5)
        arrow = Arrow(name, equation)

        morty = self.teacher
        morty.body.insert_n_curves(100)

        self.play(
            morty.change("raise_right_hand", equation),
            FadeIn(equation, UP),
            self.change_students("confused", "confused", "erm", equation)
        )
        self.play(
            Write(name),
            GrowArrow(arrow),
        )
        self.wait()
        self.play(
            self.change_students("maybe", "confused", "sassy", look_at=self.screen)
        )
        self.wait(3)
        self.play(
            morty.says("You can discover\nthis yourself", mode="hooray"),
            LaggedStartMap(FadeOut, VGroup(equation, arrow, name), shift=UR, lag_ratio=0.2, run_time=2),
            self.change_students("pondering", "pondering", "thinking", look_at=morty.eyes)
        )
        self.wait(3)
