# ==============================================================================
# Scene:      RandomGrids
# Source:     videos/_2026/2025_P6/p6.py (lines 1046-1059)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomGrids.py RandomGrids -w -m --fps 15
# ==============================================================================

import tempfile
import os
import random
from manim_imports_ext import *

class Tile(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fill_opacity=0.9, fill_color=BLUE, stroke_width=8, stroke_color=WHITE, **kwargs)
        self.round_corners(0.05)
        self.set_scale_stroke_with_zoom(True)


class Hole(VGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = Square(
            side_length=1,
            fill_opacity=1,
            fill_color="#444444",
            stroke_width=0
        )
        self.cross = Cross(self.background, stroke_width=2).scale(0.95)
        points = [ORIGIN, RIGHT, UR, UP]
        self.border = VGroup(*[
            Line(points[i], points[(i + 1) % 4], stroke_width=4, stroke_color=YELLOW).scale(1.06)
            for i in range(len(points))
        ]).match_width(self.cross).scale(1.06).move_to(self.cross)
        self.add(self.background, self.cross, self.border)
        self.set_scale_stroke_with_zoom(False)


class Grid(VGroup):
    def __init__(self, n, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n = n
        self.vertical_lines = VGroup(*[Line(RIGHT * i, RIGHT * i + DOWN * n) for i in range(n + 1)])
        self.horizontal_lines = VGroup(*[Line(DOWN * i, DOWN * i + RIGHT * n) for i in range(n + 1)])
        self.lines = VGroup(self.vertical_lines, self.horizontal_lines).set_stroke(width=4, color=WHITE, opacity=0.7)
        self.lines.set_scale_stroke_with_zoom(True)

        self.background = Square(
            side_length=self.horizontal_lines.get_width(),
            fill_opacity=1,
            fill_color=GREY_D,
            stroke_width=0
        ).move_to(
            self.lines
        )
        self.tiles = VGroup()
        self.holes = VGroup()

        self.add(self.background, self.lines, self.tiles, self.holes)
        self.center()

    def position_at_coordinates(self, tile_or_hole, i, j):
        tile_or_hole.align_to(self.vertical_lines[i], LEFT).align_to(self.horizontal_lines[j], UP)

    def add_tile(self, width, height, i, j, *args, **kwargs):
        unit_size = self.get_width() / self.n
        tile = Tile(width, height, *args, **kwargs).scale(unit_size)
        self.position_at_coordinates(tile, i, j)
        self.tiles.add(tile)

    def add_hole(self, i, j, *args, **kwargs):
        unit_size = self.get_width() / self.n
        hole = Hole(*args, **kwargs).scale(unit_size)
        hole.pos = (i, j)
        self.position_at_coordinates(hole, i, j)
        self.holes.add(hole)

    def get_reasonable_tiling(self):
        occupied = [[False] * self.n for _ in range(self.n)]
        for hole in self.holes:
            occupied[hole.pos[1]][hole.pos[0]] = True

        def find_candidate_rectangles():
            heights = [0] * self.n
            candidates = []
            for row in range(self.n):
                for col in range(self.n):
                    heights[col] = 0 if occupied[row][col] else heights[col] + 1
                stack = []
                for col in range(self.n + 1):
                    h = heights[col] if col < self.n else 0
                    start = col
                    while stack and stack[-1][1] >= h:
                        idx, height = stack.pop()
                        area = height * (col - idx)
                        candidates.append((area, row - height + 1, idx, row, col - 1))
                        start = idx
                    stack.append((start, h))
            return candidates

        empty_remaining = self.n * self.n - self.n
        while empty_remaining > 0:
            candidates = find_candidate_rectangles()
            max_area = max(c[0] for c in candidates)
            good = [c for c in candidates if c[0] >= max_area * 0.75]
            area, top, left, bottom, right = random.choice(good)

            self.add_tile(right - left + 1, bottom - top + 1, left, top)
            for r in range(top, bottom + 1):
                for c in range(left, right + 1):
                    occupied[r][c] = True
            empty_remaining -= area


class RandomGrid(Grid):
    def __init__(self, n, *args, **kwargs):
        super().__init__(n, *args, **kwargs)

        hole_col = list(range(n))
        random.shuffle(hole_col)
        for row in range(n):
            self.add_hole(hole_col[row], row)


class RandomGrids(InteractiveScene):
    def construct(self):
        # Show an animation cyclying through many random grids
        num_iters = 900
        for i in range(num_iters):
            other_grid = RandomGrid(25)
            other_grid.get_reasonable_tiling()
            self.camera.frame.set_height(other_grid.get_height() * 1.1)
            for hole in other_grid.holes:
                hole.border.set_stroke(color=WHITE)
            self.add(other_grid)
            self.wait(0.4)
            if i < num_iters - 1:
                self.remove(other_grid)


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
