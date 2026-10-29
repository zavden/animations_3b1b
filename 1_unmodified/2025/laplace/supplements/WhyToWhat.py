# ==============================================================================
# Scene:      WhyToWhat
# Source:     videos/_2025/laplace/supplements.py (lines 341-369)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyToWhat.py WhyToWhat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyToWhat(InteractiveScene):
    def construct(self):
        # Title text
        why = Text("Why", font_size=90)
        what = Text("Wait, what does this even mean?", font_size=72)
        VGroup(why, what).to_edge(UP)

        what_word = what["what"][0].copy()
        what["what"][0].set_opacity(0)

        arrow = Arrow(
            what["this"].get_bottom(),
            (2.5, 2, 0),
            thickness=5,
            fill_color=YELLOW
        )

        self.play(FadeIn(why, UP))
        self.wait()
        self.play(
            # FadeOut(why, UP),
            ReplacementTransform(why, what_word),
            FadeIn(what, lag_ratio=0.1),
        )
        self.play(
            GrowArrow(arrow),
            what["this"].animate.set_color(YELLOW)
        )
        self.wait()
