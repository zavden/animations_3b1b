# ==============================================================================
# Scene:      WarningCalculus
# Source:     videos/_2023/gauss_int/supplements.py (lines 361-404)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WarningCalculus.py WarningCalculus -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WarningCalculus(InteractiveScene):
    def construct(self):
        # Add warning sign
        warning_sign = Triangle().set_height(2)
        warning_sign.set_stroke(RED, 5)
        warning_sign.set_fill(RED, 0.25)
        warning_sign.round_corners(radius=0.1)
        bang = Text("!")
        bang.set_height(warning_sign.get_height() * 0.7)
        bang.next_to(warning_sign.get_bottom(), UP, SMALL_BUFF)
        bang.match_color(warning_sign)
        warning_sign.add(bang)
        signs = warning_sign.replicate(2)
        signs.arrange(RIGHT)

        warning = VGroup(
            Text("Warning", font_size=120),
            Text("Calculus ahead", font_size=90)
        )
        warning.arrange(DOWN, MED_LARGE_BUFF)
        warning.set_color(RED)
        signs.match_height(warning)
        signs[0].next_to(warning, LEFT)
        signs[1].next_to(warning, RIGHT)
        warning.add(*signs)
        warning.to_edge(UP)

        self.add(warning)

        # Explanation
        text = Text("""
            I mean, it's not that bad, but what follows does assume some familiarity
            with integrals. If you haven't yet learned calculus, feel free to give
            it a go and watch anyway, the visuals hopefully help to make the main idea
            clear, but know that in that case you shouldn't feel bad at all if it
            doesn't make sense!

            If that is you, perhaps I could interest you in watching the series about
            calculus on this channel? I mean, you do you, learn calculus from wherever
            you want. I'm just saying, it's right there if you want it.
        """, alignment="LEFT", font_size=36)
        text.next_to(warning, DOWN, LARGE_BUFF)

        self.play(FadeIn(text, lag_ratio=1 / len(text)))
