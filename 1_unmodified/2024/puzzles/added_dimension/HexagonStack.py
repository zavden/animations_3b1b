# ==============================================================================
# Scene:      HexagonStack
# Source:     videos/_2024/puzzles/added_dimension.py (lines 375-387)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HexagonStack.py HexagonStack -w -m --fps 15
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


class HexagonStack(CubesAsHexagonTiling):
    n = 5
    colors = [BLUE_B, BLUE_D, BLUE_E]

    def construct(self):
        # Add hexagonal stack
        for x in range(self.n):
            for y in range(self.n - x):
                for z in range(self.n - x - y):
                    self.add_cube(self.get_new_cube(x, y))
        self.remove(self.base_cube)
        self.cubes.set_fill(BLUE_D)
        self.wait()
