# ==============================================================================
# Scene:      ThumbnailIdea1
# Source:     videos/_2026/2025_P6/p6.py (lines 4039-4062)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThumbnailIdea1.py ThumbnailIdea1 -w -m --fps 15
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


class ThumbnailIdea1(InteractiveScene):
    def construct(self):
        # Add problems
        problems = VGroup()
        for i in range(6):
            rect = Rectangle(width=6, height=1.5, fill_opacity=1, fill_color=GREEN, stroke_width=10, stroke_color=BLACK).round_corners(0.3)
            label = TexText(R"\text{P}" + str(i + 1), font_size=120).set_color(BLACK)
            label.set_z_index(1)
            problem = VGroup(rect, label)
            problems.add(problem)
        problems[-1][0].set_fill(color=RED)
        problems.arrange(DOWN, buff=0.2).set_height(FRAME_HEIGHT * 0.9).to_edge(LEFT, buff=1).fix_in_frame().set_z_index(100)
        self.add(problems)

        # Add a random grid
        random.seed(2)
        self.camera.frame.reorient(-28, 55, 0, (-16.09, -0.07, -17.96), 49.76)
        grid = RandomGrid(100)
        grid.get_reasonable_tiling()
        self.add(grid)
        for hole in grid.holes:
            hole.border.set_opacity(0)
            hole.cross.set_opacity(0)
            hole.background.set_color(RED_D).set_stroke(width=2)


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
