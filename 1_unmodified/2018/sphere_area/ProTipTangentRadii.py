# ==============================================================================
# Scene:      ProTipTangentRadii
# Source:     videos/_2018/sphere_area.py (lines 1929-1933)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProTipTangentRadii.py ProTipTangentRadii -w -m --fps 15
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


class ProTipTangentRadii(ProTipNameThings):
    CONFIG = {
        "tip_descriptor": "Pro tip:",
        "tip": "A circle's tangent is perpendicular to its radius",
    }
