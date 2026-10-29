# ==============================================================================
# Scene:      AskWhyForSinusoidalGratingFact
# Source:     videos/_2024/holograms/supplements.py (lines 1068-1098)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhyForSinusoidalGratingFact.py AskWhyForSinusoidalGratingFact -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskWhyForSinusoidalGratingFact(TeacherStudentsScene):
    def construct(self):
        # Test
        stds = self.students
        morty = self.teacher

        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)

        self.play(LaggedStart(
            stds[1].says("Wait, why?", mode="confused", look_at=self.screen),
            stds[0].change("pondering", self.screen),
            stds[2].change("maybe", self.screen),
        ))
        self.wait()

        implication = VGroup(
            Tex(R"\Leftarrow").scale(2),
            Text("More formal\nholography explanation")
        )
        implication.arrange(RIGHT, buff=0.25)
        implication.move_to(2.5 * UP + 2.5 * RIGHT)

        self.play(
            morty.change("raise_right_hand"),
            GrowFromPoint(implication, morty.get_corner(UL))
        )
        self.play(self.change_students("thinking", "sassy", "erm"))
        self.look_at(self.screen)
        self.play(stds[1].change("pondering", self.screen))
        self.wait(4)
