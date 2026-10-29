# ==============================================================================
# Scene:      GeneralExpositionIcon
# Source:     videos/outside_videos/for_site.py (lines 39-51)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneralExpositionIcon.py GeneralExpositionIcon -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneralExpositionIcon(Scene):
    def construct(self):
        title = OldTexText("What is \\underline{\\qquad \\qquad}?")
        title.scale(3)
        title.to_edge(UP)
        randy = Randolph()
        randy.change("pondering")
        randy.set_height(4.5)
        randy.to_edge(DOWN)
        randy.look_at(title[0][0])

        self.add(title)
        self.add(randy)
