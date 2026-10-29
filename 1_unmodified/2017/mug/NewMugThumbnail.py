# ==============================================================================
# Scene:      NewMugThumbnail
# Source:     videos/_2017/mug.py (lines 2060-2071)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NewMugThumbnail.py NewMugThumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NewMugThumbnail(Scene):
    def construct(self):
        title = OldTex(
            "V - E + F = 0",
            tex_to_color_map={"0": YELLOW},
        )
        title.scale(3)
        title.to_edge(UP)
        image = ImageMobject("sci_youtubers_thumbnail")
        image.set_height(5.5)
        image.next_to(title, DOWN)
        self.add(title, image)
