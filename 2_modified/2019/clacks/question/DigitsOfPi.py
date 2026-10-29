# ==============================================================================
# Scene:      DigitsOfPi
# Source:     videos/_2019/clacks/question.py (lines 852-874)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DigitsOfPi.py DigitsOfPi -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Access the glyph group of OldTex to replace pi with the character and show its digits separately.
# ==============================================================================

from manim_imports_ext import *

class DigitsOfPi(Scene):
    CONFIG = {"n_digits": 9}

    def construct(self):
        nd = self.n_digits
        pow10 = int(10**nd)
        rounded_pi = int(pow10 * PI) / pow10
        # CHANGE: index the glyph group inside GL's single OldTex string part.
        equation = OldTex(
            ("\\pi = {:." + str(nd) + "f}...").format(rounded_pi)
        )[0]
        equation.set_color(YELLOW)
        pi_creature = Randolph(color=YELLOW)
        pi_creature.match_width(equation[0])
        pi_creature.scale(1.4)
        pi_creature.move_to(equation[0], DOWN)
        self.add(pi_creature, equation[1])
        self.play(ShowIncreasingSubsets(
            equation[2:],
            rate_func=linear,
            run_time=1,
        ))
        self.play(Blink(pi_creature))
        self.wait()
