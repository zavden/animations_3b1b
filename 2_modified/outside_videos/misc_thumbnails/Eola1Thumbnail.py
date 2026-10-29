# ==============================================================================
# Scene:      Eola1Thumbnail
# Source:     videos/outside_videos/misc_thumbnails.py (lines 162-205)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Eola1Thumbnail.py Eola1Thumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
# ==============================================================================

from manim_imports_ext import *

class Eola1Thumbnail(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=(-2, 2),
            y_range=(-5, 5),
        )
        plane.set_width(FRAME_WIDTH / 3)
        plane.to_edge(LEFT, buff=0)
        plane.shift(1.5 * DOWN)
        # CHANGE: Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
        vect = FillArrow(
            plane.get_origin(), plane.c2p(1, 2),
            buff=0,
            thickness=0.1,
        )
        vect.set_color(YELLOW)
        self.add(plane, vect)

        coords = IntegerMatrix([[1], [2]])
        coords.set_height(3)
        coords.set_color(TEAL)
        coords.center()
        coords.match_y(vect)
        self.add(coords)

        symbol = OldTex("\\vec{\\textbf{v} } \\in V")
        symbol.set_color(BLUE)
        symbol.set_width(FRAME_WIDTH / 3 - 1)
        symbol.set_x(FRAME_WIDTH / 3)
        symbol.match_y(vect)
        self.add(symbol)

        lines = VGroup(*(Line(DOWN, UP) for x in range(2)))
        lines.set_height(FRAME_HEIGHT)
        lines.arrange(RIGHT, buff=FRAME_WIDTH / 3)
        lines.set_stroke(GREY_A, 5)
        self.add(lines)

        title = Text("Vectors", font_size=120)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        shadow = VGroup()
        for w in np.linspace(50, 0, 100):
            shadow.add(title.copy().set_fill(opacity=0).set_stroke(BLACK, width=w, opacity=0.01))
        self.add(shadow)
        self.add(title)
