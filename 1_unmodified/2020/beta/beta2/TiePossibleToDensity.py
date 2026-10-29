# ==============================================================================
# Scene:      TiePossibleToDensity
# Source:     videos/_2020/beta/beta2.py (lines 1991-2023)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TiePossibleToDensity.py TiePossibleToDensity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TiePossibleToDensity(Scene):
    def construct(self):
        poss = OldTexText("Possibility")
        prob = OldTexText("Probability", " $>$ 0")
        dens = OldTexText("Probability \\emph{density}", " $>$ 0")
        dens[0].set_color(BLUE)
        implies = OldTex("\\Rightarrow")
        implies2 = implies.copy()

        poss.next_to(implies, LEFT)
        prob.next_to(implies, RIGHT)
        dens.next_to(implies, RIGHT)
        cross = Cross(implies)

        self.camera.frame.scale(0.7, about_point=dens.get_center())

        self.add(poss)
        self.play(
            FadeIn(prob, LEFT),
            Write(implies, run_time=1)
        )
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()

        self.play(
            VGroup(implies, cross, prob).shift, UP,
            FadeIn(implies2),
            FadeIn(dens),
        )
        self.wait()

        self.embed()
