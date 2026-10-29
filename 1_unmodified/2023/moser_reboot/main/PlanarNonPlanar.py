# ==============================================================================
# Scene:      PlanarNonPlanar
# Source:     videos/_2023/moser_reboot/main.py (lines 652-665)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PlanarNonPlanar.py PlanarNonPlanar -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PlanarNonPlanar(InteractiveScene):
    def construct(self):
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.set_stroke(GREY_C, 2)
        self.add(v_line)

        titles = VGroup(
            Text("Planar graph"),
            Text("Non-planar graph"),
        )
        for vect, title in zip([LEFT, RIGHT], titles):
            title.shift(vect * FRAME_WIDTH / 4)
        titles.to_edge(UP)
        self.add(titles)
