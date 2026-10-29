# ==============================================================================
# Scene:      WindmillTilings
# Source:     videos/_2026/2025_P6/p6.py (lines 554-1043)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WindmillTilings.py WindmillTilings -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Added self.add(grid) (and self.add(k_slider_group)) before grid.add_updater(update_grid): this manimgl does not add the `grid` container to the scene when animating it if its parts are already on screen, so its updater never ran, the grid stayed at k = 3 (12 tiles) and grid.tiles[1596] raised IndexError (with k = 45 there are 2112 tiles).
#   - Added self.add(grid) before the restore() of the 'Set k back to 5' section: the previous label animation breaks `grid` up into its parts, and without adding it again the updater did not lower k to 5 (the end of the video was covered by a giant tile).
#   - Grid.add_tile / Grid.add_hole use self.background.get_width() instead of self.get_width(): same value (n x n, difference < 0.001 units) but without recomputing the bounding box of the whole grid on every call (O(N^2)); with k = 45 the render went from ~1 h to ~13 min.
#
# Notes:
#   Long scene (~13 min of render, 170 s video): the slider takes k up to 45, that is a 2025 x 2025 grid with 2112 tiles, and the updater regenerates the grid on every change of k. If it is cut off by the time limit, use --timeout 2400. The root cause of the first two changes is that the user's manimgl version does not re-add to the scene an animated mobject whose parts are already on screen (Grant's does), which leaves the updaters of container mobjects without effect.
#   The published video is the one from the 360p, 10 fps test: at 720p it takes too long (more than 500 s at 360p).
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
        # CHANGE: self.background.get_width() instead of self.get_width(): same value (n x n) without recomputing the box of the whole grid on every call (O(N^2); with k = 45 the render took hours)
        unit_size = self.background.get_width() / self.n
        tile = Tile(width, height, *args, **kwargs).scale(unit_size)
        self.position_at_coordinates(tile, i, j)
        self.tiles.add(tile)

    def add_hole(self, i, j, *args, **kwargs):
        # CHANGE: same as in add_tile (self.background.get_width() instead of self.get_width())
        unit_size = self.background.get_width() / self.n
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


class RandomGrid(Grid):
    def __init__(self, n, *args, **kwargs):
        super().__init__(n, *args, **kwargs)

        hole_col = list(range(n))
        random.shuffle(hole_col)
        for row in range(n):
            self.add_hole(hole_col[row], row)


class WindmillTilings(InteractiveScene):
    def construct(self):
        # Add a grid with k = 5
        min_k = 5
        max_k = 45

        grid = OptimalGrid(min_k).align_to(ORIGIN, DL)
        for hole in grid.holes:
            hole.border.set_color(WHITE)
        self.add(grid)
        self.camera.frame.move_to(grid).set_height(grid.get_height() * 1.4)
        self.camera.frame.save_state()
        self.wait(2)

        # Change it to k = 4
        new_grid = OptimalGrid(4).align_to(ORIGIN, DL)
        for hole in new_grid.holes:
            hole.border.set_color(WHITE)
        grid.holes.set_z_index(100)
        self.add(grid)
        self.play(
            self.camera.frame.animate(run_time=1).move_to(new_grid).set_height(new_grid.get_height() * 1.4),
            ReplacementTransform(grid.background, new_grid.background),
            ReplacementTransform(grid.lines, new_grid.lines),
            ReplacementTransform(grid.main_tiles, new_grid.main_tiles),
            ReplacementTransform(grid.ur_tiles, new_grid.ur_tiles),
            ReplacementTransform(grid.dr_tiles, new_grid.dr_tiles),
            ReplacementTransform(grid.dl_tiles, new_grid.dl_tiles),
            ReplacementTransform(grid.ul_tiles, new_grid.ul_tiles),
            ReplacementTransform(grid.holes, new_grid.holes)
        )
        grid = new_grid
        self.wait(2)

        # Show the new dimensions
        x_length_label = Tex("16", font_size=180).next_to(grid, DOWN, buff=1)
        y_length_label = x_length_label.copy().next_to(grid, LEFT, buff=1)
        brace1 = Brace(grid, DOWN)
        brace2 = Brace(grid, LEFT)
        self.play(GrowFromEdge(brace1, UP), GrowFromEdge(brace2, RIGHT), FadeIn(VGroup(x_length_label, y_length_label)))
        self.wait(2)

        # Count the holes
        circles = VGroup(*[
            Circle(radius=0.8, stroke_width=3, stroke_color=PURE_GREEN).move_to(hole)
            for hole in grid.holes
        ])
        hole_numbers = VGroup(*[
            Tex(str(i + 1), font_size=90).next_to(hole, UP, buff=0.7)
            for i, hole in enumerate(grid.holes)
        ])
        grid.save_state()
        self.play(
            AnimationGroup(
                AnimationGroup(
                    grid.background.animate.set_opacity(0.2),
                    grid.lines.animate.set_opacity(0.2),
                    grid.tiles.animate.set_opacity(0.2),
                    grid.holes.animate.shift(0)
                ),
                AnimationGroup(*[
                    AnimationGroup(
                        ShowCreation(circle),
                        FadeIn(num, shift=UP * 0.4), lag_ratio=0.1)
                    for circle, num in zip(circles, hole_numbers)
                ], lag_ratio=0.05), lag_ratio=0.1)
        )
        self.wait(2)
        self.play(
            FadeOut(VGroup(x_length_label, y_length_label, brace1, brace2, circles, hole_numbers)),
            grid.animate.restore()
        )

        # Change it to k = 3
        new_grid = OptimalGrid(3).align_to(ORIGIN, DL)
        for hole in new_grid.holes:
            hole.border.set_color(WHITE)
        grid.holes.set_z_index(100)
        self.add(grid)
        self.play(
            self.camera.frame.animate(run_time=1).move_to(new_grid).set_height(new_grid.get_height() * 1.4),
            ReplacementTransform(grid.background, new_grid.background),
            ReplacementTransform(grid.lines, new_grid.lines),
            ReplacementTransform(grid.main_tiles, new_grid.main_tiles),
            ReplacementTransform(grid.ur_tiles, new_grid.ur_tiles),
            ReplacementTransform(grid.dr_tiles, new_grid.dr_tiles),
            ReplacementTransform(grid.dl_tiles, new_grid.dl_tiles),
            ReplacementTransform(grid.ul_tiles, new_grid.ul_tiles),
            ReplacementTransform(grid.holes, new_grid.holes)
        )
        grid = new_grid
        self.wait(2)

        # Show the new dimensions again
        x_length_label = Tex("9", font_size=100).next_to(grid, DOWN, buff=0.7)
        y_length_label = x_length_label.copy().next_to(grid, LEFT, buff=0.7)
        brace1 = Brace(grid, DOWN)
        brace2 = Brace(grid, LEFT)
        self.play(GrowFromEdge(brace1, UP), GrowFromEdge(brace2, RIGHT), FadeIn(VGroup(x_length_label, y_length_label)))
        self.wait(2)
        self.play(FadeOut(VGroup(x_length_label, y_length_label, brace1, brace2)))

        # Generalize
        tile = grid.tiles[1]
        grid.save_state()
        k_label_1 = Tex("k", font_size=100).next_to(tile, DOWN, buff=0.7)
        k_label_2 = k_label_1.copy().next_to(tile, LEFT, buff=0.7)
        brace1 = Brace(tile, DOWN)
        brace2 = Brace(tile, LEFT)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    grid.background.animate.set_opacity(0.1),
                    grid.lines.animate.set_opacity(0.1),
                    *[t.animate.set_opacity(0.1 if t != tile else t.get_opacity()) for t in grid.tiles],
                    grid.holes.animate.set_opacity(0.1)
                ),
                AnimationGroup(
                    GrowFromEdge(brace1, UP),
                    GrowFromEdge(brace2, RIGHT),
                    FadeIn(VGroup(k_label_1, k_label_2))
                ), lag_ratio=0.4)
        )

        # Add a slider
        k_tracker = ValueTracker(3)
        x_range = [0, 50, 1]
        k_slider = NumberLine(
            x_range=x_range,
            width=3,
            include_numbers=True,
            numbers_to_exclude=[x for x in range(x_range[0], x_range[1], x_range[2]) if x % 10 != 0],
            longer_tick_multiple=10
        )
        for i, tick in enumerate(k_slider.ticks):
            if i % 10 != 0:
                tick.scale(0.4).set_stroke(width=1.5)
        k_display = Tex("k = 2").next_to(k_slider, UP, buff=0.7)
        k_value = k_display.make_number_changeable("2")
        k_value.add_updater(lambda m: m.set_value(round(k_tracker.get_value())))
        k_triangle = Triangle(fill_opacity=1, fill_color=TEAL, stroke_width=0).stretch(1.5, 1).set_width(0.2).rotate(PI)
        k_triangle.align_to(k_slider[0].get_center(), DOWN)
        k_triangle.add_updater(lambda m: m.set_x(k_slider.n2p(round(k_tracker.get_value()))[0]))
        rect = BackgroundRectangle(VGroup(k_slider, k_display, k_triangle), buff=0.1).round_corners(0.2)
        k_slider_group = VGroup(rect, k_slider, k_display, k_triangle)
        k_slider_group.fix_in_frame().set_anti_alias_width(0).to_corner(UL, buff=0.2).set_scale_stroke_with_zoom(True)
        self.play(FadeIn(k_slider_group))
        self.play(
            grid.animate.restore(),
            FadeOut(VGroup(k_label_1, k_label_2, brace1, brace2))
        )

        # Switch to dynamic updating
        def update_grid(grid):
            new_k = round(k_tracker.get_value())
            if new_k - grid.k != 0:
                grid.k = new_k
                grid.become(OptimalGrid(new_k).align_to(ORIGIN, DL))
                for hole in grid.holes:
                    hole.border.set_color(WHITE)

                for hole in grid.holes:
                    hole.border.set_stroke(width=5 * new_k**(-1 / 3), color=interpolate_color(WHITE, RED, min(1, (new_k - 3) / 7)))
                for tile in grid.tiles:
                    tile.add_updater(lambda m: m.set_stroke(width=1.5 * new_k**1.5))
        # CHANGE: explicitly add the `grid` container to the scene (and the slider to the front). This manimgl does not
        # CHANGE: add `grid` when animating it if its parts are already on screen, so its updater never ran
        # CHANGE: and the grid stayed at k = 3 (grid.tiles[1596] failed with IndexError).
        self.add(grid)
        self.add(k_slider_group)
        grid.add_updater(update_grid)

        # Increase k to 10
        next_k = 10
        self.play(
            k_tracker.animate(run_time=5).set_value(next_k),
            self.camera.frame.animate(run_time=5).move_to([next_k * next_k * 0.5, next_k * next_k * 0.5, 0]).set_height(1.4 * next_k * next_k)
        )
        grid.suspend_updating()

        # Show the new size: k^2 x k^2
        x_length_label = Tex(R"k^2", font_size=900).next_to(grid, DOWN, buff=5)
        y_length_label = x_length_label.copy().next_to(grid, LEFT, buff=5)
        self.play(Write(x_length_label), Write(y_length_label), run_time=2)
        self.wait(2)
        self.play(FadeOut(VGroup(brace1, brace2, x_length_label, y_length_label)))

        # Increase k to 45
        grid.resume_updating()
        self.play(
            k_tracker.animate(run_time=5).set_value(max_k),
            self.camera.frame.animate(run_time=5).reorient(-13, 40, 0, (654.42, 252.66, 461.53), 1315.09)
        )
        grid.suspend_updating()
        self.wait(2)

        # Show the new size
        x_length_label = Tex(R"2025\\=45^2", font_size=12000).next_to(grid, DOWN, buff=50)
        y_length_label = x_length_label.copy().next_to(grid, LEFT, buff=60)
        brace1 = Brace(grid, DOWN)
        brace2 = Brace(grid, LEFT)
        self.play(GrowFromEdge(brace1, UP), GrowFromEdge(brace2, RIGHT), Write(x_length_label["2025"]), Write(y_length_label["2025"]))
        self.wait(2)
        self.play(
            FadeIn(
                x_length_label["=45^2"].set_color(
                    YELLOW
                ).next_to(
                    x_length_label["2025"], RIGHT, buff=30
                ).align_to(
                    x_length_label["2025"], DOWN
                )
            ),
            FadeIn(
                y_length_label["=45^2"].set_color(
                    YELLOW
                ).next_to(
                    y_length_label["2025"], DOWN, buff=40
                )
            )
        )
        self.wait(2)
        self.play(FadeOut(VGroup(x_length_label, y_length_label, brace1, brace2)))

        # Pan the camera around
        grid.save_state()
        self.add(k_slider_group)
        grid.holes.set_scale_stroke_with_zoom(False)
        self.play(
            self.camera.frame.animate.reorient(7, 46, 0, (1110.17, 171.23, 372.81), 1109.67), run_time=10)
        self.play(
            grid.tiles.animate.set_stroke(width=40),
            grid.holes.animate.set_stroke(width=0.5),
            self.camera.frame.animate.reorient(-24, 62, 0, (214.22, 294.13, -91.55), 379.46), run_time=10)
        self.play(
            # grid.animate.restore(),
            grid.tiles.animate.set_stroke(width=80),
            grid.holes.animate.set_stroke(width=4),
            self.camera.frame.animate.reorient(-27, 65, 0, (631.07, 270.25, 216.58), 180.95), run_time=10)

        # Reset the camera to the original position and show the labels for k
        tile = grid.tiles[1596]
        k_label_1 = Tex("k", font_size=5000).next_to(tile, DOWN, buff=20)
        k_label_2 = k_label_1.copy().next_to(tile, LEFT, buff=20)

        x_length_label = Tex(R"k^2", font_size=12000).next_to(grid, DOWN, buff=50)
        y_length_label = x_length_label.copy().next_to(grid, LEFT, buff=50)
        self.add(x_length_label, y_length_label)

        k_slider_group.set_z_index(1000)
        self.add(k_slider_group)
        self.play(
            AnimationGroup(
                self.camera.frame.animate(run_time=10).reorient(-18, 58, 0, (973.79, 650.28, -62.57), 1754.60),
                AnimationGroup(
                    AnimationGroup(
                        grid.background.animate.set_opacity(0.1),
                        grid.lines.animate.set_opacity(0.1),
                        *[t.animate.set_opacity(0.1 if t != tile else t.get_opacity()) for t in grid.tiles],
                        grid.holes.animate.set_opacity(0.1).set_stroke(width=0.5)
                    ),
                    FadeIn(VGroup(k_label_1, k_label_2)), lag_ratio=0.4, run_time=2.5), lag_ratio=0.15)
        )
        grid.holes.set_scale_stroke_with_zoom(True)

        # Set k back to 5
        # CHANGE: add `grid` to the scene again: the previous label animation breaks it up into its parts
        # CHANGE: and this manimgl does not re-add it by itself when animating it with restore(), so its updater (k -> 5) did not run.
        self.add(grid)
        self.play(
            grid.animate.restore(),
            FadeOut(VGroup(k_label_1, k_label_2, x_length_label, y_length_label))
        )
        grid.resume_updating()
        self.play(
            k_tracker.animate(run_time=2).set_value(5),
            self.camera.frame.animate(run_time=2).restore()
        )
        grid.suspend_updating()
        self.wait(1)

        # Count the number of square tiles
        new_grid = OptimalGrid(k=5).match_width(grid).move_to(grid)
        for hole in new_grid.holes:
            hole.border.set_color(WHITE)
        self.remove(grid)
        grid = new_grid
        update_grid(grid)
        self.add(grid)
        main_tiles = grid.main_tiles
        edge_tiles = VGroup(
            *grid.ul_tiles,
            *grid.ur_tiles,
            *grid.dr_tiles,
            *grid.dl_tiles
        )
        main_tile_numbers = VGroup(*[
            Tex(str(i + 1), font_size=150).set_color(BLACK).move_to(tile)
            for i, tile in enumerate(main_tiles)
        ])
        grid.save_state()
        holes = grid.holes
        holes.add_updater(lambda m: self.bring_to_front(m))
        self.play(
            VGroup(grid.lines, *[tile for tile in edge_tiles]).animate.set_opacity(0.1),
            AnimationGroup(*[
                AnimationGroup(
                    tile.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.1).set_fill(opacity=0.5),
                    GrowFromCenter(num, run_time=0.8)
                )
                for tile, num in zip(main_tiles, main_tile_numbers)
            ], lag_ratio=0.1)
        )
        holes.suspend_updating()
        self.wait(2)

        # Generalize
        self.play(
            AnimationGroup(*[
                num.animate.become(
                    Dot(radius=0.2).set_color(BLACK).move_to(tile) if i < 16 - 1 - 3 else
                    Tex("(k - 1)^2", font_size=120).set_color(BLACK).move_to(tile)
                )
                for i, (tile, num) in enumerate(zip(main_tiles[3:], main_tile_numbers[3:]))
            ])
        )
        self.wait(1)

        # Save the value (k - 1)^2
        main_tile_count = main_tile_numbers[-1].copy().scale(
            1.9
        ).align_to(
            grid, UP
        ).set_x(
            0.5 * (grid.get_right()[0] + self.camera.frame.get_right()[0])
        ).set_color(
            TEAL_A
        )
        self.play(TransformFromCopy(main_tile_numbers[-1], main_tile_count, path_arc=-PI * 0.2), run_time=1.5)
        self.wait(1)

        # Switch focus to the tiles around the edges
        holes.resume_updating()
        self.play(
            grid.animate.restore(),
            main_tiles.animate.set_opacity(0.5),
            FadeOut(main_tile_numbers), run_time=2)
        holes.suspend_updating()
        self.wait(2)

        # Count the edge tiles
        edge_tile_numbers = VGroup(*[
            Tex(str(i % 4 + 1), font_size=100).set_color(BLACK).move_to(tile)
            for i, tile in enumerate(edge_tiles)
        ])
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    tile.animate(rate_func=there_and_back).set_color(YELLOW).scale(1.1).set_fill(opacity=0.5),
                    GrowFromCenter(num, run_time=0.8)
                )
                for tile, num in zip(edge_tiles, edge_tile_numbers)
            ], lag_ratio=0.2)
        )
        self.wait(2)

        # Generalize the edge tile count
        self.play(
            AnimationGroup(*[
                num.animate.become(
                    Tex(R"\cdots", font_size=100).set_color(BLACK).move_to(tile) if i % 4 == 2 else
                    Tex("k - 1", font_size=100).set_color(BLACK).move_to(tile) if i % 4 == 3 else
                    num
                )
                for i, (tile, num) in enumerate(zip(edge_tiles, edge_tile_numbers))
            ])
        )
        self.wait(1)

        # Save the value 4(k - 1)
        edge_tile_count = Tex(
            R"+4(k - 1)"
        )
        edge_tile_count[1:].set_color(TEAL_D)
        edge_tile_count.scale(
            main_tile_count[0].get_height() / edge_tile_count[2].get_height()
        ).next_to(
            main_tile_count, DOWN, buff=0.6
        ).align_to(
            main_tile_count[-2], RIGHT
        )
        edge_tile_count[0].shift(LEFT * 0.16)
        k_minus_1_copies = VGroup(*[edge_tile_count[3:-1].copy() for _ in range(4)])
        self.play(
            AnimationGroup(*[
                TransformMatchingShapes(
                    edge_tile_numbers[4 * i + 3].copy(),
                    k_minus_1_copies[i],
                    path_arc=-PI * 0.2
                )
                for i in range(4)
            ]), run_time=1.5)
        self.play(FadeIn(VGroup(edge_tile_count[:3], edge_tile_count[-1])))
        self.play(FadeOut(k_minus_1_copies[1:]))
        self.remove(k_minus_1_copies)
        self.add(edge_tile_count)
        self.wait(1)

        # Focus on the formula
        formula_group = VGroup(main_tile_count, edge_tile_count)
        self.clear()
        self.add(k_slider_group, grid, edge_tile_numbers, formula_group)
        formula_group.generate_target()
        formula_group.target.arrange(buff=0.4)
        formula_group.target.match_y(self.camera.frame).shift(UP * 4).align_to(formula_group, RIGHT).shift(LEFT)
        formula_group.target[1].align_to(formula_group.target[0], DOWN)
        self.play(
            FadeOut(k_slider_group, shift=LEFT * 3),
            VGroup(grid, edge_tile_numbers).animate.shift(LEFT * 14),
            MoveToTarget(formula_group, path_arc=PI * 0.2), run_time=2)

        # Expand it
        expanded_version_intermediate = Tex("= k^2 - 2k + 1 + 4k - 4")
        expanded_version_intermediate.scale(
            formula_group[0][1].get_height() / expanded_version_intermediate[1].get_height()
        ).next_to(
            formula_group, DOWN, buff=0.8
        )
        expanded_version_intermediate[:8].align_to(formula_group[0], RIGHT).set_color(TEAL_A)
        expanded_version_intermediate[0].set_color(WHITE)
        expanded_version_intermediate[8].match_x(formula_group[1][0])
        expanded_version_intermediate[9:].align_to(formula_group[1][1:], LEFT).set_color(TEAL_D)
        self.play(
            AnimationGroup(
                FadeIn(expanded_version_intermediate[0]),
                TransformMatchingShapes(formula_group[0].copy(), expanded_version_intermediate[1:8], run_time=1.2),
                TransformMatchingShapes(formula_group[1][0].copy(), expanded_version_intermediate[8], run_time=1),
                TransformMatchingShapes(formula_group[1][1:].copy(), expanded_version_intermediate[9:], run_time=1.2), lag_ratio=0.2)
        )
        self.wait(1)

        # Simplify
        expanded_version = Tex("= k^2 + 2k - 3")
        expanded_version.match_height(
            expanded_version_intermediate
        ).next_to(
            expanded_version_intermediate, DOWN, buff=0.8
        ).align_to(
            expanded_version_intermediate, LEFT
        )
        self.play(
            AnimationGroup(
                TransformMatchingShapes(expanded_version_intermediate[:3].copy(), expanded_version[:3], run_time=1.2),
                TransformMatchingShapes(
                    VGroup(expanded_version_intermediate[3:6], expanded_version_intermediate[9:11]).copy(),
                    expanded_version[3:6], run_time=1.2),
                TransformMatchingShapes(
                    VGroup(expanded_version_intermediate[6:8], expanded_version_intermediate[11:13]).copy(),
                    expanded_version[6:8], run_time=1.2), lag_ratio=0.2)
        )

        # Circle the final count
        final_count = expanded_version[1:]
        rect = SurroundingRectangle(final_count, buff=0.4, fill_opacity=0, stroke_width=3, stroke_color=YELLOW)
        self.play(ShowCreation(rect, run_time=2), FadeOut(edge_tile_numbers), grid.animate.restore().move_to(grid))
        self.wait(2)

        # Compare the conjectured optimal arrangement with other random arrangements
        grid.generate_target()
        final_count.generate_target()
        VGroup(final_count.target, grid.target).arrange(DOWN, buff=2.5).match_x(grid).match_y(self.camera.frame)
        edge_tile_numbers.set_z_index(100)
        self.play(
            AnimationGroup(
                FadeOut(VGroup(formula_group, expanded_version_intermediate, expanded_version[0], rect)),
                AnimationGroup(
                    MoveToTarget(grid, run_time=1),
                    MoveToTarget(final_count, path_arc=PI * 0.4, run_time=1.5)
                ), lag_ratio=0.3)
        )

        num_iters = 100
        for i in range(num_iters):
            other_grid = RandomGrid(int(k_tracker.get_value()**2)).match_y(grid).set_x(2 * self.camera.frame.get_x() - grid.get_x())
            for hole in other_grid.holes:
                hole.border.set_stroke(color=WHITE)
            self.add(other_grid)
            if i == 0:
                qms = TexText("???").match_height(final_count).match_y(final_count).match_x(other_grid)
                self.play(FadeIn(VGroup(other_grid, qms)), run_time=0.4)
            elif i == 26:
                arrow1 = Arrow(ORIGIN, RIGHT * 4, thickness=17).set_color(YELLOW).next_to(final_count, LEFT, buff=1)
                arrow2 = arrow1.copy().rotate(PI).next_to(final_count, RIGHT, buff=1)
                self.play(FadeIn(arrow1, shift=RIGHT), FadeIn(arrow2, shift=LEFT))
            else:
                self.wait(0.4)
            if i < num_iters - 1:
                self.remove(other_grid)


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
