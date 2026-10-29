# ==============================================================================
# Scene:      VorticitySynonyms
# Source:     videos/_2018/turbulence.py (lines 883-905)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VorticitySynonyms.py VorticitySynonyms -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VorticitySynonyms(Scene):
    def construct(self):
        words = VGroup(
            OldTexText("High", "vorticity"),
            OldTex(
                "\\text{a.k.a} \\,",
                "|\\nabla \\times \\vec{\\textbf{v}}| > 0"
            ),
            OldTexText("a.k.a", "high", "swirly-swirly", "factor"),
        )
        words[0].set_color_by_tex("vorticity", BLUE)
        words[1].set_color_by_tex("nabla", BLUE)
        words[2].set_color_by_tex("swirly", BLUE)
        words.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=MED_LARGE_BUFF
        )

        for word in words:
            word.add_background_rectangle()
            self.play(FadeInFromDown(word))
            self.wait()
