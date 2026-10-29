# ==============================================================================
# Scene:      TenDThumbnail
# Source:     videos/_2017/highD.py (lines 3609-3656)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TenDThumbnail.py TenDThumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TenDThumbnail(Scene):
    def construct(self):
        square = Square()
        square.set_height(3.5)
        square.set_stroke(YELLOW, 5)
        r = square.get_width() / 2
        circles = VGroup(*[
            Circle(radius=r).move_to(corner)
            for corner in square.get_vertices()
        ])
        circles.set_stroke(BLUE, 5)
        circles.set_fill(BLUE, 0.5)
        circles.set_sheen(0.5, UL)
        lil_circle = Circle(
            radius=(np.sqrt(2) - 1) * r
        )
        lil_circle.set_stroke(YELLOW, 3)
        lil_circle.set_fill(YELLOW, 0.5)

        group = VGroup(circles, lil_circle, square)
        group.to_edge(LEFT)
        square.scale(2)

        words = OldTexText(
            "What\\\\"
            "about\\\\"
            "in 10D?\\\\"
            # "dimensions?"
        )
        words.set_height(5)
        words.to_edge(RIGHT)

        arrow = Arrow(
            words[0][0].get_left(),
            lil_circle.get_center(),
            path_arc=90 * DEGREES,
            buff=0.5,
        )
        arrow.set_color(RED)
        arrow.set_stroke(width=12)
        arrow_group = VGroup(
            arrow.copy().set_stroke(BLACK, 16),
            arrow,
        )

        self.add(group)
        self.add(words)
        self.add(arrow_group)
