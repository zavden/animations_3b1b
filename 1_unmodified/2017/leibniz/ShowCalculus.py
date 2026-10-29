# ==============================================================================
# Scene:      ShowCalculus
# Source:     videos/_2017/leibniz.py (lines 392-439)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowCalculus.py ShowCalculus -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowCalculus(PiCreatureScene):
    def construct(self):
        frac_sum = OldTex(
            "1 - \\frac{1}{3} + \\frac{1}{5} - \\frac{1}{7} + \\cdots",
        )
        int1 = OldTex(
            "= \\int_0^1 (1 - x^2 + x^4 - \\dots )\\,dx"
        )
        int2 = OldTex(
            "= \\int_0^1 \\frac{1}{1+x^2}\\,dx"
        )
        arctan = OldTex("= \\tan^{-1}(1)")
        pi_fourths = OldTex("= \\frac{\\pi}{4}")

        frac_sum.to_corner(UP+LEFT)
        frac_sum.shift(RIGHT)
        rhs_group = VGroup(int1, int2, arctan, pi_fourths)
        rhs_group.arrange(
            DOWN, buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        rhs_group.shift(
            frac_sum.get_right() + MED_SMALL_BUFF*RIGHT \
            -int1[0].get_left()
        )
        
        self.add(frac_sum)
        modes = it.chain(["plain"], it.cycle(["confused"]))
        for rhs, mode in zip(rhs_group, modes):
            self.play(
                FadeIn(rhs),
                self.pi_creature.change, mode
            )
            self.wait()
        self.change_mode("maybe")
        self.wait()
        self.look_at(rhs_group[-1])
        self.wait()
        self.pi_creature_says(
            "Where's the \\\\ circle?",
            bubble_config = {"width" : 4, "height" : 3},
            target_mode = "maybe"
        )
        self.look_at(rhs_group[0])
        self.wait()

    def create_pi_creature(self):
        return Randolph(color = BLUE_C).to_corner(DOWN+LEFT)
