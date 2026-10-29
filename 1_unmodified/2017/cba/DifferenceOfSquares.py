# ==============================================================================
# Scene:      DifferenceOfSquares
# Source:     videos/_2017/cba.py (lines 224-290)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DifferenceOfSquares.py DifferenceOfSquares -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DifferenceOfSquares(Scene):
    def construct(self):
        squares = VGroup(*[
            VGroup(*[
                Square()
                for x in range(8)
            ]).arrange(RIGHT, buff=0)
            for y in range(8)
        ]).arrange(DOWN, buff=0)
        squares.set_height(4)
        squares.set_stroke(BLUE, 3)
        squares.set_fill(BLUE, 0.5)

        last_row_parts = VGroup()
        for row in squares[-3:]:
            row[-3:].set_color(RED)
            row[:-3].set_color(BLUE_B)
            last_row_parts.add(row[:-3])
        squares.to_edge(LEFT)

        arrow = Vector(RIGHT, color=WHITE)
        arrow.shift(1.5 * LEFT)
        squares.next_to(arrow, LEFT)

        new_squares = squares[:-3].copy()
        new_squares.next_to(arrow, RIGHT)
        new_squares.align_to(squares, UP)

        x1 = OldTex("x").set_color(BLUE)
        x2 = x1.copy()
        x1.next_to(squares, UP)
        x2.next_to(squares, LEFT)
        y1 = OldTex("y").set_color(RED)
        y2 = y1.copy()
        y1.next_to(squares[-2], RIGHT)
        y2.next_to(squares[-1][-2], DOWN)

        xpy = OldTex("x", "+", "y")
        xmy = OldTex("x", "-", "y")
        for mob in xpy, xmy:
            mob[0].set_color(BLUE)
            mob[2].set_color(RED)
        xpy.next_to(new_squares, UP)
        # xmy.rotate(90 * DEGREES)
        xmy.next_to(new_squares, RIGHT)
        xmy.to_edge(RIGHT)

        self.add(squares, x1, x2, y1, y2)
        self.play(
            ReplacementTransform(
                squares[:-3].copy().set_fill(opacity=0),
                new_squares
            ),
            ShowCreation(arrow),
            lag_ratio=0,
        )
        last_row_parts = last_row_parts.copy()
        last_row_parts.save_state()
        last_row_parts.set_fill(opacity=0)
        self.play(
            last_row_parts.restore,
            last_row_parts.rotate, -90 * DEGREES,
            last_row_parts.next_to, new_squares, RIGHT, {"buff": 0},
            lag_ratio=0,
        )
        self.play(Write(xmy), Write(xpy))
        self.wait()
