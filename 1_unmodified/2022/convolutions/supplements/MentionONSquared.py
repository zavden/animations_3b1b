# ==============================================================================
# Scene:      MentionONSquared
# Source:     videos/_2022/convolutions/supplements.py (lines 343-372)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionONSquared.py MentionONSquared -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MentionONSquared(InteractiveScene):
    def construct(self):
        # Blah
        morty = Mortimer(height=2)
        kw = dict(tex_to_color_map={"{N}": YELLOW})
        bigO = Tex(R"\mathcal{O}({N}^2)", **kw)
        explanation = VGroup(
            Text("# Operations"),
            OldTex("=").rotate(PI / 2),
            OldTex(
                R"\text{const}",
                R"\cdot {N}^2 +",
                R"\left(\substack{\text{stuff asymptotically} \\ \text{smaller than $N^2$}}\right)",
                **kw
            ),
        )
        explanation[2][0].set_color(GREY_B)
        explanation[2][-1].scale(0.6, about_edge=LEFT)
        explanation.arrange(DOWN)
        explanation.next_to(morty, UR, SMALL_BUFF)

        self.play(morty.says(bigO))
        self.play(Blink(morty))
        self.play(
            FadeIn(explanation, 0.5 * UP),
            morty.change("raise_left_hand", look_at=explanation)
        )
        for x in range(2):
            self.play(Blink(morty))
            self.wait(2)
