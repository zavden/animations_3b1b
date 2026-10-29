# ==============================================================================
# Scene:      AskAboutTheProof
# Source:     videos/_2023/clt_proof/main.py (lines 60-99)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutTheProof.py AskAboutTheProof -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutTheProof(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.pi_creatures.scale(0.5, about_edge=DOWN)
        self.pi_creatures.space_out_submobjects(1.5)

        # Ask
        morty = self.teacher
        stds = self.students
        self.play(
            stds[0].change("pondering", 5 * DOWN),
            stds[1].says("Proof?"),
            stds[2].change("sassy"),
            morty.change("tease"),
        )
        self.wait(6)

        words = VGroup(
            Text("Moment generating functions"),
            Text("Culumants"),
            Text("Characteristic functions"),
        )
        words.move_to(morty.get_corner(UL), DOWN)
        words.shift(0.2 * UP)
        words.scale(0.65)
        self.play(
            morty.change("raise_right_hand"),
            FadeIn(words[0], UP),
            stds[1].debubble(mode="well"),
            stds[0].change("confused", morty.eyes),
            stds[2].change("pondering", morty.eyes),
        )
        self.wait()
        for i in [1, 2]:
            self.play(
                words[:i].animate.next_to(words[i], LEFT, buff=0.5),
                FadeIn(words[i], LEFT)
            )
            self.wait()
        self.wait(3)
