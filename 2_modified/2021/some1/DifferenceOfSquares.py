# ==============================================================================
# Scene:      DifferenceOfSquares
# Source:     videos/_2021/some1.py (lines 871-939)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DifferenceOfSquares.py DifferenceOfSquares -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - old syntax play(mob.restore, mob.rotate, ...): restore does not work inside .animate (the target does not keep saved_state); the final state is built by hand and Transform is used
# ==============================================================================

from manim_imports_ext import *

class DifferenceOfSquares(Scene):
    def construct(self):
        x = 6
        y = 1
        squares = VGroup(*[
            VGroup(*[
                Square()
                for x in range(x)
            ]).arrange(RIGHT, buff=0)
            for y in range(x)
        ]).arrange(DOWN, buff=0)
        squares.set_height(4)
        squares.set_stroke(BLUE_D, 3)
        squares.set_fill(BLUE_D, 0.5)

        last_row_parts = VGroup()
        for row in squares[-y:]:
            row[-y:].set_color(GREY_E)
            row[:-y].set_color(BLUE_B)
            last_row_parts.add(row[:-y])
        squares.to_edge(LEFT)

        arrow = Vector(RIGHT, color=WHITE)
        arrow.shift(1.5 * LEFT)
        squares.next_to(arrow, LEFT)

        new_squares = squares[:-y].copy()
        new_squares.next_to(arrow, RIGHT)
        new_squares.align_to(squares, UP)

        x1 = OldTex(str(x)).set_color(BLUE_D)
        x2 = x1.copy()
        x1.next_to(squares, UP)
        x2.next_to(squares, LEFT)
        y1 = OldTex(str(y)).set_color(BLUE_B)
        y2 = y1.copy()
        y1.next_to(squares[-int(np.ceil(y / 2))], RIGHT)
        y2.next_to(squares[-1][-int(np.ceil(y / 2))], DOWN)

        xpy = OldTex(str(x), "+", str(y))
        xmy = OldTex(str(x), "-", str(y))
        for mob in xpy, xmy:
            mob[0].set_color(BLUE)
            mob[2].set_color(BLUE_B)
        xpy.next_to(new_squares, UP)
        # xmy.rotate(90 * DEGREES)
        xmy.next_to(new_squares, RIGHT)
        xmy.shift(squares[0][0].get_width() * RIGHT)

        self.add(squares, x1, x2, y1, y2)
        self.play(
            ReplacementTransform(
                squares[:-y].copy().set_fill(opacity=0),
                new_squares
            ),
            ShowCreation(arrow),
            lag_ratio=0,
        )
        last_row_parts = last_row_parts.copy()
        last_row_parts.save_state()
        last_row_parts.set_fill(opacity=0)
        # CHANGE: old syntax play(mob.restore, mob.rotate, ...): restore does not work inside .animate (the target does not keep saved_state); the final state is built by hand and Transform is used
        restored = last_row_parts.saved_state.copy()
        restored.rotate(-90 * DEGREES)
        restored.next_to(new_squares, RIGHT, buff=0)
        self.play(Transform(last_row_parts, restored), lag_ratio=0)
        self.play(Write(xmy), Write(xpy))
        self.wait()
