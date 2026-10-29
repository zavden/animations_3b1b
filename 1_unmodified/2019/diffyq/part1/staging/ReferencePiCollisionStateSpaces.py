# ==============================================================================
# Scene:      ReferencePiCollisionStateSpaces
# Source:     videos/_2019/diffyq/part1/staging.py (lines 2037-2060)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferencePiCollisionStateSpaces.py ReferencePiCollisionStateSpaces -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferencePiCollisionStateSpaces(Scene):
    CONFIG = {
        "camera_config": {"background_color": GREY_E}
    }

    def construct(self):
        title = OldTexText("The block collision puzzle")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)

        frames = VGroup(*[
            ScreenRectangle(
                height=3.5,
                fill_opacity=1,
                fill_color=BLACK,
                stroke_width=0,
            )
            for x in range(2)
        ])
        frames.arrange(RIGHT, buff=LARGE_BUFF)
        boundary = AnimatedBoundary(frames)
        self.add(frames, boundary)
        self.wait(15)
