# ==============================================================================
# Scene:      MinimizeSharding
# Source:     videos/_2018/borsuk_addition.py (lines 266-310)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl MinimizeSharding.py MinimizeSharding -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class MinimizeSharding(Scene):
    def construct(self):
        piece_groups = VGroup(*[
            VGroup(*[
                self.get_piece()
                for x in range(3)
            ]).arrange(RIGHT, buff=SMALL_BUFF)
            for y in range(4)
        ]).arrange(RIGHT, buff=SMALL_BUFF)

        self.add(piece_groups)
        self.play(*[
            ApplyMethod(mob.space_out_submobjects, 0.7)
            for mob in piece_groups
        ])
        self.wait()
        group1 = piece_groups[:2]
        group2 = piece_groups[2:]
        self.play(
            group1.arrange, DOWN,
            group1.next_to, ORIGIN, LEFT, LARGE_BUFF,
            group2.arrange, DOWN,
            group2.next_to, ORIGIN, RIGHT, LARGE_BUFF,
        )
        self.wait()

    def get_piece(self):
        jagged_spots = [
            ORIGIN, 2 * UP + RIGHT, 4 * UP + LEFT, 6 * UP,
        ]
        corners = list(it.chain(
            jagged_spots,
            [6 * UP + 10 * RIGHT],
            [
                p + 10 * RIGHT
                for p in reversed(jagged_spots)
            ],
            [ORIGIN]
        ))
        piece = VMobject().set_points_as_corners(corners)
        piece.set_width(1)
        piece.center()
        piece.set_stroke(WHITE, width=0.5)
        piece.set_fill(BLUE, opacity=1)
        return piece
