# ==============================================================================
# Scene:      LaminarFlowLabel
# Source:     videos/_2018/turbulence.py (lines 818-834)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LaminarFlowLabel.py LaminarFlowLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LaminarFlowLabel(Scene):
    def construct(self):
        words = OldTexText("Laminar flow")
        words.scale(1.5)
        words.to_edge(UP)
        subwords = OldTexText(
            "`Lamina', in Latin, means \\\\"
            "``a thin sheet of material''",
            tex_to_color_map={"Lamina": YELLOW},
            arg_separator="",
        )
        subwords.next_to(words, DOWN, MED_LARGE_BUFF)
        VGroup(words, subwords).set_background_stroke(width=4)
        self.play(Write(words))
        self.wait()
        self.play(FadeInFromDown(subwords))
        self.wait()
