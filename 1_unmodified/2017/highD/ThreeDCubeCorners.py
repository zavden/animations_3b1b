# ==============================================================================
# Scene:      ThreeDCubeCorners
# Source:     videos/_2017/highD.py (lines 1722-1737)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeDCubeCorners.py ThreeDCubeCorners -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeDCubeCorners(Scene):
    def construct(self):
        coordinates = VGroup(*[
            OldTex("(%d,\\, %d,\\, %d)"%(x, y, z))
            for x, y, z in it.product(*3*[[1, -1]])
        ])
        coordinates.arrange(DOWN, aligned_edge = LEFT)
        name = OldTexText("Corners: ")
        name.next_to(coordinates[0], LEFT)
        group = VGroup(name, coordinates)
        group.set_height(FRAME_HEIGHT - 1)
        group.to_edge(LEFT)

        self.play(Write(name, run_time = 2))
        self.play(LaggedStartMap(FadeIn, coordinates, run_time = 3))
        self.wait()
