# ==============================================================================
# Scene:      ProTipTweakParameters
# Source:     videos/_2018/sphere_area.py (lines 1936-1940)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProTipTweakParameters.py ProTipTweakParameters -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProTipNameThings(Scene):
    CONFIG = {
        "tip_descriptor": "(Deceptively simple) problem solving tip:",
        "tip": "Start with names",
    }

    def construct(self):
        words = OldTexText(
            self.tip_descriptor,
            self.tip,
        )
        words[1].set_color(YELLOW)
        words.to_edge(UP)

        self.play(FadeIn(words[0]))
        self.wait()
        self.play(FadeInFromDown(words[1]))
        self.wait()


class ProTipTweakParameters(ProTipNameThings):
    CONFIG = {
        "tip_descriptor": "Pro tip:",
        "tip": "Tweak parameters $\\rightarrow$ make",
    }
