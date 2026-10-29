# ==============================================================================
# Scene:      PreSumRuleDiscussion
# Source:     videos/_2017/eoc/chapter4.py (lines 256-302)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreSumRuleDiscussion.py PreSumRuleDiscussion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SINE_COLOR = BLUE


X_SQUARED_COLOR = GREEN


class PreSumRuleDiscussion(Scene):
    def construct(self):
        title = OldTexText("Sum rule")
        title.to_edge(UP)
        self.add(title)

        specific = OldTex(
            "\\frac{d}{dx}(", "\\sin(x)", "+", "x^2", ")",
            "=", "\\cos(x)", "+", "2x"
        )
        general = OldTex(
            "\\frac{d}{dx}(", "g(x)", "+", "h(x)", ")",
            "=", "\\frac{dg}{dx}", "+", "\\frac{dh}{dx}"
        )
        for formula in specific, general:
            formula[1].set_color(SINE_COLOR)
            formula[6].set_color(SINE_COLOR)
            formula[3].set_color(X_SQUARED_COLOR)
            formula[8].set_color(X_SQUARED_COLOR)
        VGroup(specific, general).arrange(DOWN, buff = LARGE_BUFF)

        #Add on rules
        self.add(specific)
        for i in 0, 4, 5:
            self.add(general[i])
        self.wait(2)
        for indices in [(1, 2, 3), (6,), (7, 8)]:
            self.play(*[
                ReplacementTransform(
                    specific[i].copy(), general[i]
                )
                for i in indices
            ])
            self.wait()

        #Highlight parts
        for i in 1, 3, -1, 6, 8:
            if i < 0:
                self.wait()
            else:
                part = specific[i]
                self.play(
                    part.set_color, YELLOW,
                    part.scale, 1.2,
                    rate_func = there_and_back
                )
        self.wait()
