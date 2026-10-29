# ==============================================================================
# Scene:      PhotographVsHologram
# Source:     videos/_2024/holograms/supplements.py (lines 4-34)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PhotographVsHologram.py PhotographVsHologram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PhotographVsHologram(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Single piece of film")
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        photo = VGroup(
            Text("Photograph"),
            Text("One point of view"),
        )
        holo = VGroup(
            Text("Our Recording"),
            Text("Many points of view"),
        )
        for part, x in zip([photo, holo], [-1, 1]):
            part[1].scale(0.7)
            part[1].set_color(GREY_A)
            part.arrange(DOWN)
            part.set_x(x * FRAME_WIDTH / 4)
            part.set_y(2)
            part.add_to_back(Arrow(title.get_edge_center(x * RIGHT), part.get_top(), path_arc=-x * 60 * DEGREES))

        self.add(title)

        for part in [photo, holo]:
            self.play(
                GrowArrow(part[0]),
                FadeInFromPoint(part[1], part[0].get_start()),
            )
            self.wait()
            self.play(Write(part[2]))
            self.wait()
