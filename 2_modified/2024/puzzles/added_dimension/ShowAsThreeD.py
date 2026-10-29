# ==============================================================================
# Scene:      ShowAsThreeD
# Source:     videos/_2024/puzzles/added_dimension.py (lines 419-485)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowAsThreeD.py ShowAsThreeD -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The original calls `pre_populate()` twice (2 x 32 cubes = a full 4x4x4 stack) and `random_new_cube()` fails with IndexError because there are no gaps; a single call was kept
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CubesAsHexagonTiling(InteractiveScene):
    n = 4
    colors = [GREY, GREY, GREY]

    def setup(self):
        super().setup()
        n = self.n

        # Set up axes and camera angle
        self.frame.set_field_of_view(1 * DEGREES)
        self.frame.reorient(135, 55, 0)
        self.axes = ThreeDAxes((-5, 5), (-5, 5), (-5, 5))

        # Add base
        self.base_cube = self.get_half_cube(
            side_length=n,
            shared_corner=[-1, -1, -1],
            grid=True
        )
        self.add(self.base_cube)
        self.add(Point())

        # Block pattern
        self.block_pattern = np.zeros((n, n, n))
        self.cubes = VGroup()

    def pre_populate(self):
        for x in range(self.n**3 // 2):
            new_cube = self.random_new_cube()
            self.add_cube(new_cube)

    def get_new_cube(self, x, y):
        zero_indices = np.where(self.block_pattern[x, y, :] == 0)
        if len(zero_indices) == 0:
            print("Column full")
            return
        min_z = np.min(zero_indices)
        min_y = np.min(np.where(self.block_pattern[x, :, min_z] == 0))
        min_x = np.min(np.where(self.block_pattern[:, min_y, min_z] == 0))

        return self.get_half_cube((min_x, min_y, min_z))

    def random_new_cube(self):
        empty_spaces = np.transpose(np.where(self.block_pattern[:, :, :] == 0))
        x, y, z = random.choice(empty_spaces)
        return self.get_new_cube(x, y)

    def get_random_cube_from_stack(self):
        filled_spaces = np.transpose(np.where(self.block_pattern[:, :, :] == 1))
        x, y, z = random.choice(filled_spaces)
        max_x = np.max(np.where(self.block_pattern[:, y, z] == 1))
        max_y = np.max(np.where(self.block_pattern[max_x, :, z] == 1))
        max_z = np.max(np.where(self.block_pattern[max_x, max_y, :] == 1))
        for cube in self.cubes:
            if all(cube.get_corner([-1, -1, -1]).astype(int) == (max_x, max_y, max_z)):
                return cube
        return self.cubes[-1]

    def add_cube(self, cube):
        self.cubes.add(cube)
        cube.spacer = Mobject()
        self.add(cube, cube.spacer)
        self.refresh_block_pattern()

    def remove_cube(self, cube):
        self.cubes.remove(cube)
        self.remove(cube, cube.spacer)
        self.refresh_block_pattern()

    def refresh_block_pattern(self):
        self.block_pattern[:, :, :] = 0
        for cube in self.cubes:
            coords = cube.get_corner([-1, -1, -1]).astype(int)
            self.block_pattern[*coords] = 1

    def get_half_cube(self, coords=(0, 0, 0), side_length=1, colors=None, shared_corner=[1, 1, 1], grid=False):
        if colors is None:
            colors = self.colors
        squares = Square(side_length).replicate(3)
        if grid:
            for square in squares:
                grid = Square(side_length=1).get_grid(side_length, side_length, buff=0)
                grid.move_to(square)
                square.add(grid)
        axes = [OUT, DOWN, LEFT]
        for square, color, axis in zip(squares, colors, axes):
            square.set_fill(color, 1)
            square.set_stroke(color, 0)
            square.rotate(90.1 * DEGREES, axis)  # Why 0.1 ?
            square.move_to(ORIGIN, shared_corner)
        squares.move_to(coords, np.array([-1, -1, -1]))
        squares.set_stroke(WHITE, 2)

        return squares

    def animate_in_with_rotation(self, cube, color=TEAL, run_time=2):
        cube.save_state()
        cube.rotate(-60 * DEGREES, axis=[1, 1, 1])
        cube.set_fill(color)
        blackness = cube.copy().set_color(BLACK)
        spacer = Mobject()
        self.play(FadeIn(cube))
        self.add(blackness, spacer, cube)
        self.play(Rotate(cube, 60 * DEGREES, axis=[1, 1, 1], run_time=run_time))
        self.play(Restore(cube))
        self.add_cube(cube)
        self.remove(blackness, spacer)

    def animate_out_with_rotation(self, cube, color=TEAL, run_time=2):
        blackness = cube.copy().set_color(BLACK)
        spacer = Mobject()
        self.play(cube.animate.set_fill(color))
        self.add(blackness, spacer, cube)
        self.play(Rotate(cube, 60 * DEGREES, axis=[1, 1, 1], run_time=run_time))
        self.remove(blackness, spacer)
        self.play(FadeOut(cube))
        self.remove_cube(cube)


class ShowAsThreeD(CubesAsHexagonTiling):
    colors = [BLUE_B, BLUE_D, BLUE_E]

    def construct(self):
        # self.pre_populate()

        # Color
        grey_cubes = self.cubes.copy()
        grey_cubes.set_fill(GREY)
        full_grey = Group()
        for cube in grey_cubes:
            full_grey.add(cube, Point())
        self.add(full_grey)
        self.base_cube.save_state()
        self.base_cube.set_fill(GREY)

        self.wait()
        self.play(
            Restore(self.base_cube),
            FadeOut(full_grey),
        )

        # Change perspective
        # CHANGE: the original calls pre_populate() twice (2 x n**3 // 2 = 64 cubes), which fills the stack and
        # makes random_new_cube() fail further down (IndexError); a single call is kept (32 cubes)
        self.pre_populate()
        self.play(
            # self.frame.animate.reorient(118, 79, 0, (-1.01, 0.75, 1.54), 8.00)
            self.frame.animate.reorient(118, 79, 0, (-1.01, 0.75, 1.54), 12.00).set_field_of_view(40 * DEGREES),
            run_time=3
        )
        self.play(
            # self.frame.animate.reorient(163, 83, 0, (1.82, -0.33, 1.89), 8.00),
            self.frame.animate.reorient(163, 83, 0, (1.82, -0.33, 1.89), 12.00),
            run_time=4
        )
        self.play(self.frame.animate.reorient(135, 55, 0, ORIGIN, 8).set_field_of_view(1 * DEGREES), run_time=3)

        # Rotation is adding
        new_cube = self.random_new_cube()
        self.animate_in_with_rotation(new_cube)
        self.wait()
        self.play(
            new_cube.animate.shift(5 * RIGHT + 3 * OUT),
            run_time=6,
            rate_func=there_and_back_with_pause
        )
        self.wait()

        # Add or remove a few
        for x in range(2):
            new_cube = self.random_new_cube()
            self.animate_in_with_rotation(new_cube, run_time=1)
            old_cube = self.get_random_cube_from_stack()
            if old_cube is not new_cube:
                self.animate_out_with_rotation(old_cube, run_time=1)

        # Remove all
        while len(self.cubes) > 0:
            cube = self.get_random_cube_from_stack()
            self.play(FadeOut(cube, 0.25 * OUT, run_time=0.25))
            self.remove_cube(cube)

        self.wait()
        for x in range(self.n**3):
            cube = self.random_new_cube()
            self.play(FadeIn(cube, shift=0.25 * IN, run_time=0.25))
            self.add_cube(cube)
