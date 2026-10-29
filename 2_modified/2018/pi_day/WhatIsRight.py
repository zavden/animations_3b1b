# ==============================================================================
# Scene:      WhatIsRight
# Source:     videos/_2018/pi_day.py (lines 794-872)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WhatIsRight.py WhatIsRight -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - zip() result wrapped in list() before slicing (Python 3)
# ==============================================================================

from manim_imports_ext import *

class WhatIsRight(PiCreatureScene):
    CONFIG = {
        "default_pi_creature_kwargs" : {
            "color" : BLUE_D,
            "filp_at_start" : False,
        },
        "default_pi_creature_start_corner" : DOWN,
    }
    def construct(self):
        randy = self.pi_creature
        randy.scale(0.75, about_edge = DOWN)
        title = OldTexText("Which is ``right''?")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)

        sum_over_N_converges = OldTex("1+2+3+\\cdots = -\\frac{1}{12}")
        sum_over_N_diverges = OldTex("1+2+3+\\cdots \\text{ Diverges}")

        literal_derivative = OldTex(
            "f'(x) = \\frac{f(x+dx) - f(x)}{dx}"
        )
        limit_derivative = OldTex(
            "f'(x) = \\lim_{h \\to 0}\\frac{f(x+h) - f(x)}{h}"
        )

        divide_by_zero_definable = OldTex(
            "\\frac{1}{0}", "\\text{ has meaning}"
        )
        divide_by_zero_undefinable = OldTex(
            "\\frac{1}{0}", "\\text{ is undefined}"
        )

        left_mobs = VGroup(
            sum_over_N_converges, literal_derivative,
            divide_by_zero_definable
        )
        right_mobs = VGroup(
            sum_over_N_diverges, limit_derivative,
            divide_by_zero_undefinable
        )

        for mob in left_mobs:
            mob.next_to(randy, UP)
            mob.shift(3.5*LEFT)
        for mob in right_mobs:
            mob.next_to(randy, UP)
            mob.shift(3.5*RIGHT)

        left_mobs.set_color_by_gradient(YELLOW_C, YELLOW_D)
        right_mobs.set_color_by_gradient(GREEN_C, GREEN_D)

        self.play(randy.change, "pondering", title)
        self.wait()
        self.play(randy.change, "sassy", title)
        self.wait()

        last_terms = VGroup()
        # CHANGE: zip() is not subscriptable in Python 3; wrap in list
        for left, right in list(zip(left_mobs, right_mobs))[:-1]:
            right.align_to(left)
            self.play(
                randy.change, "raise_right_hand",
                FadeInFromDown(left),
                last_terms.shift, 1.75*UP
            )
            self.wait()
            self.play(
                randy.change, "raise_left_hand",
                FadeInFromDown(right)
            )
            self.play(randy.change, "plain", right)
            last_terms.add(left, right, title)
        self.play(
            randy.change, "shruggie",
            FadeInFromDown(left_mobs[-1]),
            FadeInFromDown(right_mobs[-1]),
            last_terms.shift, 1.75*UP,
        )
        self.wait(4)
