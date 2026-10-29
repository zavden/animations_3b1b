# ==============================================================================
# Scene:      HintToGeneralChallenge
# Source:     videos/_2019/diffyq/part4/staging.py (lines 2125-2156)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HintToGeneralChallenge.py HintToGeneralChallenge -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HintToGeneralChallenge(Scene):
    def construct(self):
        self.add(FullScreenFadeRectangle(
            fill_color=GREY_E,
            fill_opacity=1,
        ))
        words1 = OldTexText("Hint: Try writing")
        formula1 = OldTex(
            "c_{n} =",
            "{", "a_{n} \\over 2} +",
            "{", "b_{n} \\over 2} i",
            tex_to_color_map={
                "{n}": YELLOW,
            }
        )
        words2 = OldTexText("and")
        formula2 = OldTex(
            "e^{i{x}} =",
            "\\cos\\left({x}\\right) +",
            "i\\sin\\left({x}\\right)",
            tex_to_color_map={
                "{x}": GREEN
            }
        )

        all_words = VGroup(
            words1, formula1,
            words2, formula2
        )
        all_words.arrange(DOWN, buff=LARGE_BUFF)

        self.add(all_words)
