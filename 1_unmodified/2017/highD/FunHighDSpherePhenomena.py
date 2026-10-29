# ==============================================================================
# Scene:      FunHighDSpherePhenomena
# Source:     videos/_2017/highD.py (lines 3265-3289)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FunHighDSpherePhenomena.py FunHighDSpherePhenomena -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FunHighDSpherePhenomena(Scene):
    def construct(self):
        title = OldTexText(
            "Fun high-D sphere phenomena"
        )
        title.to_edge(UP)
        title.set_color(BLUE)
        h_line = Line(LEFT, RIGHT).scale(5)
        h_line.next_to(title, DOWN)
        self.add(title, h_line)

        items = VGroup(*list(map(TexText, [
            "$\\cdot$ Most volume is near the equator",
            "$\\cdot$ Most volume is near the surface",
            "$\\cdot$ Sphere packing in 8 dimensions",
            "$\\cdot$ Sphere packing in 24 dimensions",
        ])))
        items.arrange(
            DOWN, buff = MED_LARGE_BUFF, aligned_edge = LEFT
        )
        items.next_to(h_line, DOWN)

        for item in items:
            self.play(LaggedStartMap(FadeIn, item, run_time = 2))
        self.wait()
