# ==============================================================================
# Scene:      TurbulenceGifLabel
# Source:     videos/_2018/turbulence.py (lines 1531-1544)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TurbulenceGifLabel.py TurbulenceGifLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TurbulenceGifLabel(Scene):
    def construct(self):
        title = OldTexText("Turbulence in 2d")
        title.to_edge(UP)

        attribution = OldTexText(
            "Animation by Gabe Weymouth (@gabrielweymouth)"
        )
        attribution.scale(0.5)
        attribution.to_edge(DOWN)

        self.play(Write(title))
        self.play(FadeIn(attribution, UP))
        self.wait()
