# ==============================================================================
# Scene:      PreviousVideos
# Source:     videos/_2017/highD.py (lines 570-586)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreviousVideos.py PreviousVideos -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PreviousVideos(Scene):
    def construct(self):
        titles = VGroup(*list(map(TexText, [
            "Pi hiding in prime regularities",
            "Visualizing all possible pythagorean triples",
            "Borsuk-Ulam theorem",
        ])))
        titles.to_edge(UP, buff = MED_SMALL_BUFF)
        screen = ScreenRectangle(height = 6)
        screen.next_to(titles, DOWN)

        title = titles[0]
        self.add(title, screen)
        self.wait(2)
        for new_title in titles[1:]:
            self.play(Transform(title, new_title))
            self.wait(2)
