# ==============================================================================
# Scene:      AskWhyThatsTrue
# Source:     videos/_2025/grover/clarification.py (lines 648-685)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhyThatsTrue.py AskWhyThatsTrue -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskWhyThatsTrue(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.play(
            stds[1].says("How does that work?", mode="maybe"),
            stds[0].change('erm', look_at=self.screen),
            stds[2].change("confused", look_at=self.screen),
            morty.change('hesitant'),
        )
        self.look_at(self.screen)
        self.wait(5)

        # Mapping
        mapping = VGroup(
            VGroup(Text("True").set_color(GREEN), Vector(DOWN), Tex(R"\times -1")).arrange(DOWN),
            VGroup(Text("False").set_color(RED), Vector(DOWN), Tex(R"\times +1")).arrange(DOWN),
        )
        for part in mapping:
            tex = part[2]
            tex[1].scale(0.75, about_point=tex[2].get_left())
            tex[0].scale(1.5)
        mapping.arrange(RIGHT, buff=2.0)
        mapping.move_to(self.hold_up_spot, DOWN).shift(LEFT)

        self.play(
            morty.change("raise_right_hand"),
            FadeIn(mapping, UP),
            stds[1].debubble(mode="pondering"),
            stds[0].change("sassy", mapping),
            stds[2].change("hesitant", mapping),
        )
        self.wait()
        self.play(morty.change("hesitant"))
        self.wait(3)
        self.play(morty.change("pondering", mapping))
        self.wait(3)
