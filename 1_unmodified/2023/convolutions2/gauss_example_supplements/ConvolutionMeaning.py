# ==============================================================================
# Scene:      ConvolutionMeaning
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 389-422)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConvolutionMeaning.py ConvolutionMeaning -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ConvolutionMeaning(InteractiveScene):
    def construct(self):
        # x + y = s
        kw = dict(t2c={"{s}": YELLOW})
        words = VGroup(
            Tex(R"[f * g]({s})", font_size=60, **kw),
            Tex(R"\longrightarrow", **kw),
            Tex(R"\text{How likely is it that } x + y = {s} \, ?", **kw),
        )
        words.arrange(RIGHT, buff=0.5)
        words.to_edge(UP)

        words[0].save_state()
        words[0].set_x(0)
        self.play(FadeIn(words[0], 0.5 * UP))
        self.wait()
        self.play(
            Restore(words[0]),
            Write(words[1]),
            FadeIn(words[2], RIGHT),
        )
        self.wait()

        # Mention sqrt(2)
        new_rhs = Tex(R"(\text{This area}) / \sqrt{2}", font_size=60)
        new_rhs[R"\text{This area}"].set_color(TEAL)
        new_rhs.next_to(words[1], RIGHT)
        new_rhs.set_opacity(0)

        self.play(
            VGroup(*words[:2], new_rhs).animate.set_x(0).set_opacity(1),
            FadeOut(words[2], RIGHT),
        )
        self.wait()
