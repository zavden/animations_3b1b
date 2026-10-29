# ==============================================================================
# Scene:      WeighingIndependenceAssumption
# Source:     videos/_2018/eop/independence.py (lines 2180-2217)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WeighingIndependenceAssumption.py WeighingIndependenceAssumption -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WeighingIndependenceAssumption(PiCreatureScene):
    def construct(self):
        randy = self.randy

        title = OldTexText("Independence")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)
        formula = OldTex(
            "P(", "A", "B", ")", "="
            "P(", "A", ")", "P(", "B", ")"
        )
        formula.set_color_by_tex("A", BLUE)
        formula.set_color_by_tex("B", GREEN)

        clean = OldTexText("Clean")
        clean.next_to(formula, UP)
        VGroup(clean, formula).next_to(randy, UP+LEFT)
        clean.save_state()
        clean.shift(2*(DOWN+RIGHT))
        clean.set_fill(opacity = 0)

        self.play(
            randy.change, "raise_left_hand", clean,
            clean.restore
        )
        self.play(Write(formula))
        self.play(
            randy.change, "raise_right_hand",
            randy.look, UP+RIGHT,
        )
        self.wait(2)

    ####

    def create_pi_creature(self):
        self.randy = Randolph().to_edge(DOWN)
        return self.randy
