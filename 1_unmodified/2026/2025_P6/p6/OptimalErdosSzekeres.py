# ==============================================================================
# Scene:      OptimalErdosSzekeres
# Source:     videos/_2026/2025_P6/p6.py (lines 3427-3675)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OptimalErdosSzekeres.py OptimalErdosSzekeres -w -m --fps 15
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


class OptimalGrid(Grid):
    def __init__(self, k, *args, **kwargs):
        self.k = k
        n = k * k
        super().__init__(n, *args, **kwargs)

        # Holes
        for i in range(n):
            self.add_hole(k - 1 - i // k + (i % k) * k, i)

        # Main tiles
        for i in range((k - 1) * (k - 1)):
            self.add_tile(k, k, k - 1 - i // (k - 1) + (i % (k - 1)) * k, i + i // (k - 1) + 1)
        self.main_tiles = VGroup(*self.tiles)

        # Upper-right tiles
        for j in range(1, k):
            self.add_tile(k, j, j * k, 0)
        self.ur_tiles = VGroup(*self.tiles[len(self.main_tiles):])

        # Lower-right tiles
        for j in range(1, k):
            self.add_tile(j, k, n - j, j * k)
        self.dr_tiles = VGroup(*self.tiles[len(self.main_tiles) + len(self.ur_tiles):])

        # Lower-left tiles
        for j in range(1, k):
            self.add_tile(k, j, n - (j + 1) * k, n - j)
        self.dl_tiles = VGroup(*self.tiles[len(self.main_tiles) + len(self.ur_tiles) + len(self.dr_tiles):])

        # Upper-left tiles
        for j in range(1, k):
            self.add_tile(j, k, 0, n - (j + 1) * k)
        self.ul_tiles = VGroup(*self.tiles[len(self.main_tiles) + len(self.ur_tiles) + len(self.dr_tiles) + len(self.dl_tiles):])


class OptimalErdosSzekeres(InteractiveScene):
    def construct(self):
        # Add a grid
        k = 3
        grid = OptimalGrid(k).set_width(6)
        self.add(grid)
        grid.tiles.set_stroke(width=3)
        for hole in grid.holes:
            hole.border.set_color(WHITE)

        # Label N = k^2
        n_color = YELLOW
        k_color = TEAL
        brace = Brace(grid, UP)
        label = brace.get_tex("N = k^2", font_size=60, tex_to_color_map={"N": n_color, "k": k_color}).shift(UP * 0.2)
        self.camera.frame.save_state()
        self.play(
            AnimationGroup(
                self.camera.frame.animate(run_time=1.5).scale(1.1).shift(UP * 0.5),
                AnimationGroup(
                    GrowFromEdge(brace, DOWN),
                    Write(label), lag_ratio=0.2), lag_ratio=0.2)
        )

        # Focus on the Xs
        self.play(
            grid.background.animate.fade(0.9),
            grid.lines.animate.fade(0.9),
            grid.tiles.animate.fade(0.9),
            run_time=2)
        self.wait(2)

        # Show all possible LISs
        increasing_sequence_color = GREEN_D
        decreasing_sequence_color = RED_D
        increasing_sequences = [
            [6, 3, 0],
            [6, 3, 1],
            [6, 3, 2],
            [6, 4, 1],
            [6, 4, 2],
            [6, 5, 2]
        ]
        paths = VGroup()
        for s in increasing_sequences:
            path = VMobject()
            for i in range(len(s) - 1):
                path.append_vectorized_mobject(Line(grid.holes[s[i]].get_center(), grid.holes[s[i + 1]].get_center()))
            paths.add(path)
            path.set_stroke(width=6, color=increasing_sequence_color)
        for path, s in zip(paths, increasing_sequences):
            self.add(path)
            grid.holes.save_state()
            for i in s:
                grid.holes[i].border.set_stroke(color=increasing_sequence_color)
            self.wait(1)
            self.remove(path)
            grid.holes.restore()
        self.wait(2)

        # Increase the size of the grid
        for k in range(4, 7):
            self.remove(grid)
            grid = OptimalGrid(k).set_width(6)
            grid.background.fade(0.9)
            grid.lines.fade(0.9)
            grid.tiles.fade(0.9)
            grid.tiles.set_stroke(width=3)
            grid.holes.set_stroke(width=2)
            for hole in grid.holes:
                hole.border.set_color(WHITE)
            self.add(grid)
            self.wait(0.1)
        self.wait(2)
        grid.save_state()

        # Divide the holes up into k groups of k
        holes_sorted_by_y = VGroup(*sorted(grid.holes, key=lambda hole: hole.get_y()))
        groups_increasing = VGroup(*[
            holes_sorted_by_y[i * k:(i + 1) * k]
            for i in range(k)
        ])
        rect = Rectangle(
            width=5.5,
            height=0.45,
            fill_opacity=0,
            stroke_width=3,
            stroke_color=k_color
        ).round_corners(0.2)
        x, y, _ = groups_increasing[0][-1].get_center() - groups_increasing[0][0].get_center()
        group_rects_increasing = VGroup(*[rect.copy().rotate(np.arctan2(y, x)).move_to(group) for group in groups_increasing])
        self.remove(grid.holes)
        self.add(grid.holes)
        self.play(AnimationGroup(*[FadeIn(rect) for rect in group_rects_increasing], lag_ratio=0.2))

        # Label the groups
        brace1 = Brace(groups_increasing, np.array([x, y, 0])).set_color(k_color)
        label1 = brace1.get_tex("k").set_color(k_color)
        brace_1_group = VGroup(brace1, label1)
        brace_1_group.save_state()
        self.play(FadeIn(brace_1_group))
        self.wait(1)
        brace2 = Brace(groups_increasing, np.array([-y, x, 0])).set_color(k_color)
        label2 = brace2.get_tex("k").set_color(k_color)
        brace_2_group = VGroup(brace2, label2)
        brace_2_group.save_state()
        self.play(FadeIn(brace_2_group))
        self.wait(2)
        self.play(brace_2_group.animate.fade(1))

        # Build up an increasing subsequence
        increasing_sequence = [30, 25, 21, 15, 9, 5]
        increasing_path = VGroup()
        for i in range(len(increasing_sequence) - 1):
            increasing_path.add(
                Line(
                    grid.holes[increasing_sequence[i]].get_center(), grid.holes[increasing_sequence[i + 1]].get_center()
                ).set_stroke(
                    width=5, color=increasing_sequence_color
                )
            )

        # for line in increasing_path:
        #     self.play(ShowCreation(line), run_time = 0.7)

        for line in increasing_path[:-1]:
            self.play(ShowCreation(line), run_time=2)
            self.wait(0.5)
        self.wait(2)

        # # Show a decreasing segment
        # decreasing_segment = Line(
        #     grid.holes[increasing_sequence[-2]].get_center(), grid.holes[increasing_sequence[-2] + 1].get_center()
        # ).set_stroke(
        #     width = 5, color = decreasing_sequence_color
        # )
        # self.play(ShowCreation(decreasing_segment), run_time = 2.2)
        # self.wait(1.5)

        # Complete the real path
        self.play(ShowCreation(increasing_path[-1]), run_time=2)
        self.wait(1)

        # Add labels of 1 through k on top of the holes
        labels_increasing = VGroup(*[
            Tex(
                str(i) if i < k - 1 else R"\cdots" if i == k - 1 else "k"
            ).next_to(
                grid.holes[increasing_sequence[i - 1]], UP + LEFT * 0.1 if i < k - 1 else UP, buff=0.2
            ).set_color(
                k_color
            ).set_stroke(
                width=10, color=BLACK, behind=True
            )
            for i in range(1, k + 1)
        ])
        brace_label_group = VGroup(brace, label)
        brace_label_group.save_state()
        self.play(
            grid.animate.fade(0.8),
            brace_label_group.animate.fade(0.8),
            group_rects_increasing.animate.fade(0.8),
            AnimationGroup(*[FadeIn(label, shift=UP * 0.2) for label in labels_increasing], lag_ratio=0.2)
        )
        self.wait(2)

        # Show the decreasing subsequence case
        holes_sorted_by_x = VGroup(*sorted(grid.holes, key=lambda hole: hole.get_x()))
        groups_decreasing = VGroup(*[
            holes_sorted_by_x[i * k:(i + 1) * k]
            for i in range(k)
        ])
        x, y, _ = groups_decreasing[0][-1].get_center() - groups_decreasing[0][0].get_center()
        group_rects_decreasing = VGroup(*[rect.copy().rotate(np.arctan2(y, x)).move_to(group) for group in groups_decreasing])
        increasing_path_group = VGroup(increasing_path, labels_increasing)
        increasing_path_group.save_state()
        self.remove(grid.holes)
        self.add(grid.holes)
        self.play(
            brace_label_group.animate.restore(),
            grid.animate.restore(),
            FadeOut(group_rects_increasing),
            brace_1_group.animate.fade(1),
            increasing_path_group.animate.fade(1),
            brace_2_group.animate.restore(),
            AnimationGroup(*[FadeIn(rect) for rect in group_rects_decreasing], lag_ratio=0.2)
        )

        # Build up an decreasing subsequence
        decreasing_sequence = [6, 7, 14, 27, 34, 35]
        decreasing_path = VMobject()
        for i in range(len(decreasing_sequence) - 1):
            decreasing_path.append_vectorized_mobject(
                Line(
                    grid.holes[decreasing_sequence[i]].get_center(), grid.holes[decreasing_sequence[i + 1]].get_center()
                )
            )
            decreasing_path.set_stroke(
                width=5, color=decreasing_sequence_color
            )

        labels_decreasing = VGroup(*[
            Tex(
                str(i) if i < k - 1 else R"\cdots" if i == k - 1 else "k"
            ).next_to(
                grid.holes[decreasing_sequence[i - 1]], UP + RIGHT * 0.1
            ).set_color(
                k_color
            ).set_stroke(
                width=10, color=BLACK, behind=True
            )
            for i in range(1, k + 1)
        ])
        self.play(
            ShowCreation(decreasing_path, run_time=3),
            grid.animate.fade(0.8),
            brace_label_group.animate.fade(0.8),
            group_rects_decreasing.animate.fade(0.8),
            AnimationGroup(*[FadeIn(label, shift=UP * 0.2) for label in labels_decreasing], lag_ratio=0.2, run_time=3)
        )
        self.wait(2)

        # Show the product
        equation = Tex(R"k \cdot k = k^2 = N", font_size=80).shift(RIGHT * 7 + UP * 0.7)
        equation["k"][0].set_color(increasing_sequence_color)
        equation["k"][1].set_color(decreasing_sequence_color)
        equation["k"][2].set_color(k_color)
        equation["N"].set_color(n_color)

        increasing_path_group.generate_target()
        increasing_path_group.target.restore()
        increasing_path_group.target[1].set_fill(color=increasing_sequence_color)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(VGroup(brace_1_group, brace_2_group)),
                    FadeOut(group_rects_decreasing),
                    brace_label_group.animate.restore(),
                    MoveToTarget(increasing_path_group),
                    labels_decreasing.animate.set_fill(color=decreasing_sequence_color),
                    grid.animate.restore(),
                    self.camera.frame.animate.shift(RIGHT * 3.2), run_time=2),
                AnimationGroup(
                    ReplacementTransform(labels_increasing[-1].copy().set_stroke(width=0), equation[0]),
                    GrowFromCenter(equation[1]),
                    ReplacementTransform(labels_decreasing[-1].copy().set_stroke(width=0), equation[2]),
                    FadeIn(equation[3:6]),
                    FadeIn(equation[6:]), lag_ratio=0.4), lag_ratio=0.3)
        )


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
