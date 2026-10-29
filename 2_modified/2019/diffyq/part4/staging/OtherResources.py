# ==============================================================================
# Scene:      OtherResources
# Source:     videos/_2019/diffyq/part4/staging.py (lines 2159-2196)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OtherResources.py OtherResources -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class OtherResources(Scene):
    def construct(self):
        thumbnails = Group(
            ImageMobject("MathologerFourier"),
            ImageMobject("CodingTrainFourier"),
        )
        names = VGroup(
            OldTexText("Mathologer"),
            OldTexText("The Coding Train"),
        )

        for thumbnail, name in zip(thumbnails, names):
            thumbnail.set_height(3)

        thumbnails.arrange(RIGHT, buff=LARGE_BUFF)
        thumbnails.set_width(FRAME_WIDTH - 1)

        for thumbnail, name in zip(thumbnails, names):
            name.scale(1.5)
            name.next_to(thumbnail, UP)
            thumbnail.add(name)
            self.play(
                FadeInFromDown(name),
                GrowFromCenter(thumbnail)
            )
            self.wait()

        url = OldTexText("www.jezzamon.com")
        url.scale(1.5)
        url.move_to(FRAME_WIDTH * RIGHT / 5)
        url.to_edge(UP)
        self.play(
            thumbnails.arrange, DOWN, {"buff": LARGE_BUFF},
            thumbnails.set_height, FRAME_HEIGHT - 2,
            thumbnails.to_edge, LEFT
        )
        self.play(FadeInFromDown(url))
        self.wait()
