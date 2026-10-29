# ==============================================================================
# Scene:      ErdosSzekeresV2
# Source:     videos/_2026/2025_P6/p6.py (lines 1985-3424)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ErdosSzekeresV2.py ErdosSzekeresV2 -w -m --fps 15
# ==============================================================================

import tempfile
import os
import random
from manim_imports_ext import *
from scipy.spatial.transform import Slerp

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


class ErdosSzekeresV2(InteractiveScene):
    def construct(self):
        # Add the grid
        n = 16
        grid = Grid(n).set_width(6)
        self.add(grid)
        hole_positions = [7, 9, 15, 0, 2, 4, 12, 8, 6, 13, 5, 1, 14, 10, 3, 11]
        for i, j in enumerate(hole_positions):
            grid.add_hole(i, j)
        for hole in grid.holes:
            hole.border.set_color(WHITE)
        grid.get_reasonable_tiling()
        grid.tiles.set_stroke(width=3)
        self.wait(1)

        # Change it into the n = 12 version
        for n in range(15, 9, -1):
            self.wait(0.25)
            self.remove(grid)
            grid = Grid(n).set_width(6)
            self.add(grid)
            hole_positions = np.random.permutation(list(range(n)))
            if n == 10:
                hole_positions = [8, 7, 5, 3, 2, 9, 0, 6, 4, 1]
            for i, j in enumerate(hole_positions):
                grid.add_hole(i, j)
            for hole in grid.holes:
                hole.border.set_color(WHITE)
            grid.get_reasonable_tiling()
            grid.tiles.set_stroke(width=3)
        self.clear()
        self.add(grid)

        # Number the holes according to their height
        nums_color = BLUE_B
        values = [n - j for j in hole_positions]
        nums = VGroup(*[
            Integer(j, font_size=40).set_color(BLUE_B).next_to(grid.holes[i], UP, buff=0.15)
            for i, j in enumerate(values)
        ])
        bar_color = BLUE
        column_highlights = VGroup(*[
            VGroup(*[
                Tile(1, 1).match_width(grid.holes[0])
                .set_fill(bar_color, opacity=0)
                .set_stroke(bar_color, opacity=0)
                for _ in range(height)
            ]).arrange(UP, buff=0).match_x(hole).align_to(hole, UP)
            for height, hole in zip(values, grid.holes)
        ])
        self.add(column_highlights)
        n_color = YELLOW
        brace = Brace(grid, UP, buff=0.8)
        label = brace.get_tex("N", font_size=60).set_color(n_color)
        self.camera.frame.save_state()
        self.play(
            grid.background.animate.fade(0.9),
            grid.lines.animate.fade(0.9),
            grid.tiles.animate.fade(0.9),
            AnimationGroup(
                AnimationGroup(*[
                    AnimationGroup(
                        Succession(
                            AnimationGroup(*[
                                square.copy().animate(rate_func=there_and_back).set_fill(GREEN, opacity=1)
                                for square in column
                            ], lag_ratio=0.05),
                            FadeOut(column)
                        ),
                        FadeIn(num, shift=UP * 0.2, run_time=0.7), lag_ratio=0.1)
                    for num, column in zip(nums, column_highlights)
                ], lag_ratio=0.1),
                AnimationGroup(
                    self.camera.frame.animate(run_time=1.5).scale(1.1).shift(UP * 0.7),
                    AnimationGroup(
                        GrowFromEdge(brace, DOWN),
                        Write(label)
                    ), lag_ratio=0.2), lag_ratio=0.5)
        )
        self.remove(column_highlights)

        # Make the bar chart
        base = Line(LEFT, RIGHT).set_width(nums.get_width() * 1.1).align_to(grid, DOWN)
        bars = VGroup(*[
            Rectangle(
                width=column.get_width() * 0.9,
                height=column.get_height(),
                fill_opacity=1,
                fill_color=bar_color,
                stroke_width=0
            ).match_x(column)
            for column in column_highlights
        ]).align_to(base, DOWN)
        for bar in bars:
            bar.align_to(base, DOWN)
        chart = VGroup(bars, base)

        for bar in bars:
            bar.save_state()
            bar.stretch_to_fit_height(0.001).align_to(base, DOWN)
        self.play(
            FadeOut(grid, run_time=3),
            VGroup(brace, label).animate(run_time=2).shift(DOWN * 0.3),
            AnimationGroup(*[
                AnimationGroup(
                    FadeOut(num, shift=UP * 0.3),
                    bar.animate.restore(), lag_ratio=0.1, run_time=2)
                for num, bar in zip(nums, bars)
            ]),
            ShowCreation(base, run_time=1)
        )

        # Define helpers for indicating LIS/LDS
        increasing_sequence_color = GREEN_D
        decreasing_sequence_color = RED_D
        marker_thickness = 0.5 * min(bar.get_height() for bar in bars)

        def marker_rect(bar, color, level):
            r = Rectangle(
                width=bar.get_width(), height=marker_thickness,
                fill_opacity=1, fill_color=color, stroke_width=0
            )
            r.match_x(bar)
            top = bar.get_top()[1]
            r.set_y(top - marker_thickness * (level + 0.5))
            return r

        # Define subsequence helper functions
        increasing_sequence_color = GREEN_D
        decreasing_sequence_color = RED_D

        def longest_increasing_subsequence_indices(seq):
            n_terms = len(seq)
            lengths = [1] * n_terms
            prev = [-1] * n_terms
            for i in range(n_terms):
                for j in range(i):
                    if seq[j] < seq[i] and lengths[j] + 1 > lengths[i]:
                        lengths[i] = lengths[j] + 1
                        prev[i] = j
            end = max(range(n_terms), key=lambda i: lengths[i])
            indices = []
            while end != -1:
                indices.append(end)
                end = prev[end]
            return list(reversed(indices))

        def longest_decreasing_subsequence_indices(seq):
            return longest_increasing_subsequence_indices([-x for x in seq])

        def maximal_longest_increasing_subsequences(seq, include_length_1=False):
            remaining_indices = list(range(len(seq)))
            all_sequences = []
            while remaining_indices:
                remaining_values = [seq[i] for i in remaining_indices]
                local_lis = longest_increasing_subsequence_indices(remaining_values)
                global_lis = [remaining_indices[i] for i in local_lis]
                all_sequences.append(global_lis)
                used = set(global_lis)
                remaining_indices = [i for i in remaining_indices if i not in used]
            if not include_length_1:
                all_sequences = [s for s in all_sequences if len(s) > 1]
            return all_sequences

        def maximal_longest_decreasing_subsequences(seq, include_length_1=False):
            remaining_indices = list(range(len(seq)))
            all_sequences = []
            while remaining_indices:
                remaining_values = [seq[i] for i in remaining_indices]
                local_lds = longest_decreasing_subsequence_indices(remaining_values)
                global_lds = [remaining_indices[i] for i in local_lds]
                all_sequences.append(global_lds)
                used = set(global_lds)
                remaining_indices = [i for i in remaining_indices if i not in used]
            if not include_length_1:
                all_sequences = [s for s in all_sequences if len(s) > 1]
            return all_sequences

        left_to_right = sorted(zip(values, bars), key=lambda triple: triple[1].get_x())
        values, bars = [v for v, _ in left_to_right], VGroup(*[b for _, b in left_to_right])
        base.add_updater(lambda m: self.bring_to_front(m))

        # --- Dot-nesting registry -------------------------------------------------
        # Each sequence path now places a dot at every included bar (not just the
        # first), so it's unambiguous which bars are actually part of a run even
        # when several points happen to be collinear. When two paths share a bar,
        # whichever one's dot is *prepared* second (i.e. whichever gets drawn/added
        # second) is shrunk so it nests visibly inside the one already there.
        # Paths must release their claim on a bar (via release_path_dots /
        # release_dots_recursive) once they're faded out, so later, unrelated
        # paths on the same physical bar objects go back to full size.
        DOT_RADIUS = 0.1
        DOT_SHRINK_FACTOR = 0.6
        dot_stacks = {}  # id(bar) -> list of {"token", "radius"} dicts, in registration order
        _dot_token_counter = [0]

        def register_dot(bar):
            key = id(bar)
            stack = dot_stacks.setdefault(key, [])
            radius = DOT_RADIUS if not stack else min(e["radius"] for e in stack) * DOT_SHRINK_FACTOR
            _dot_token_counter[0] += 1
            token = _dot_token_counter[0]
            stack.append({"token": token, "radius": radius})
            return radius, token

        def release_dot(bar, token):
            key = id(bar)
            stack = dot_stacks.get(key, [])
            dot_stacks[key] = [e for e in stack if e["token"] != token]
            if key in dot_stacks and not dot_stacks[key]:
                del dot_stacks[key]

        def prepare_path_dots(path):
            # Resolves final dot sizes (nesting inside any dot already
            # registered on a shared bar) and resizes the dots in place.
            # Must be called exactly once per path, at the moment it's about
            # to appear on screen -- whether via path_creation_animation or
            # a direct self.add/FadeIn.
            dots, line, tip = path
            for dot in dots:
                radius, token = register_dot(dot.bar)
                dot.dot_token = token
                dot.set_width(radius * 2)

        def release_path_dots(path):
            dots, line, tip = path
            for dot in dots:
                token = getattr(dot, "dot_token", None)
                if token is not None:
                    release_dot(dot.bar, token)

        def release_dots_recursive(mobject):
            if getattr(mobject, "is_sequence_path", False):
                release_path_dots(mobject)
            else:
                for sub in mobject:
                    release_dots_recursive(sub)
        # ----------------------------------------------------------------------------

        def sequence_path(bars, indices, color):
            points = [bars[i].get_top() for i in indices]
            line = VMobject()
            tip = VGroup()
            if len(points) >= 2:
                tip_length = 0.3
                tip_width = 0.3
                direction = normalize(points[-1] - points[-2])
                perp = np.array([-direction[1], direction[0], 0])
                tip_base_center = points[-1] - tip_length * direction
                line.set_points_as_corners(points[:-1] + [tip_base_center])
                tip = Polygon(
                    points[-1],
                    tip_base_center + (tip_width / 2) * perp,
                    tip_base_center - (tip_width / 2) * perp,
                    fill_color=color,
                    fill_opacity=1,
                    stroke_width=0,
                )
                tip.direction = direction
            else:
                line.set_points_as_corners(points)
            line.set_stroke(color, width=9)
            dots = VGroup(*[
                Dot(radius=DOT_RADIUS).set_color(color).move_to(point)
                for point in points
            ])
            for dot, i in zip(dots, indices):
                dot.bar = bars[i]
            path = VGroup(dots, line, tip).set_stroke(opacity=0.85)
            path.is_sequence_path = True
            return path

        def path_creation_animation(path):
            dots, line, tip = path
            prepare_path_dots(path)
            animations = [AnimationGroup(*[GrowFromCenter(dot) for dot in dots]), ShowCreation(line)]
            if len(tip.get_points()) > 0:
                animations.append(FadeIn(tip, shift=tip.direction * 0.2))
            return AnimationGroup(*animations, lag_ratio=0.3)

        # Draw the subsequences
        self.play(
            FadeOut(VGroup(brace, label)),
            self.camera.frame.animate.restore(),
        )
        self.wait(2)
        all_increasing_indices = maximal_longest_increasing_subsequences(values)
        all_decreasing_indices = maximal_longest_decreasing_subsequences(values)

        increasing_paths = VGroup(*[
            sequence_path(bars, indices, increasing_sequence_color)
            for indices in all_increasing_indices
        ])
        decreasing_paths = VGroup(*[
            sequence_path(bars, indices, decreasing_sequence_color)
            for indices in all_decreasing_indices
        ])
        self.play(
            AnimationGroup(*[
                path_creation_animation(path)
                for path in decreasing_paths
            ], lag_ratio=0.1)
        )
        self.wait(0.4)
        self.play(
            AnimationGroup(*[
                path_creation_animation(path)
                for path in increasing_paths
            ], lag_ratio=0.1)
        )
        self.wait(1)
        self.play(FadeOut(increasing_paths), FadeOut(decreasing_paths))
        release_dots_recursive(VGroup(increasing_paths, decreasing_paths))

        # Show a permutation with a long decreasing subsequence but a short increasing one
        new_bar_heights = [9, 7, 4, 10, 1, 8, 6, 3, 2, 5]
        permutation = [values.index(i) for i in new_bar_heights]
        for i, bar in enumerate(bars):
            bars[permutation[i]].generate_target()
            bars[permutation[i]].target.match_x(bar)
        self.play(AnimationGroup(*[MoveToTarget(bar) for bar in bars]))

        # Highlight the decreasing sequences, then the increasing ones
        left_to_right = sorted(zip(values, bars), key=lambda triple: triple[1].get_x())
        values, bars = [v for v, _ in left_to_right], VGroup(*[b for _, b in left_to_right])
        base.add_updater(lambda m: self.bring_to_front(m))

        all_decreasing_indices_2 = maximal_longest_decreasing_subsequences(values)
        all_increasing_indices_2 = maximal_longest_increasing_subsequences(values)

        # Built in the order they'll actually be revealed (increasing first,
        # then decreasing), so any bar shared between the two gets its
        # decreasing dot correctly nested inside the increasing one.
        increasing_paths_2 = VGroup(*[
            sequence_path(bars, indices, increasing_sequence_color)
            for indices in all_increasing_indices_2
        ])
        decreasing_paths_2 = VGroup(*[
            sequence_path(bars, indices, decreasing_sequence_color)
            for indices in all_decreasing_indices_2
        ])

        self.play(
            AnimationGroup(*[
                path_creation_animation(path)
                for path in increasing_paths_2
            ], lag_ratio=0.1)
        )
        self.wait(0.4)
        self.play(
            AnimationGroup(*[
                path_creation_animation(path)
                for path in decreasing_paths_2
            ], lag_ratio=0.1)
        )
        self.wait(1)

        # Show some random permutations
        inequality = Tex(
            R"\frac{\text{LIS} + \text{LDS}}{2} \ge \sqrt{N}",
            font_size=80,
            tex_to_color_map={"LIS": increasing_sequence_color, "LDS": decreasing_sequence_color, "N": n_color}
        ).shift(RIGHT * 7 + UP * 1)

        value_expr = inequality.copy()
        value_expr.next_to(inequality, DOWN, buff=1.0)
        lis_placeholder = value_expr["LIS"].set_opacity(0)
        lds_placeholder = value_expr["LDS"].set_opacity(0)
        n_placeholder = value_expr["N"].set_opacity(0)
        lis_anchor = lis_placeholder.get_center()
        lds_anchor = lds_placeholder.get_center()
        n_anchor = n_placeholder.get_center()
        value_expr.remove(lis_placeholder, lds_placeholder, n_placeholder)

        def make_lis_value(val):
            mob = Integer(val, font_size=80).set_color(increasing_sequence_color)
            mob.move_to(lis_anchor)
            return mob

        def make_lds_value(val):
            mob = Integer(val, font_size=80).set_color(decreasing_sequence_color)
            mob.move_to(lds_anchor)
            return mob

        n_value = Integer(n, font_size=70).set_color(n_color)
        n_value.move_to(n_anchor)

        lis_value = make_lis_value(len(longest_increasing_subsequence_indices(values)))
        lds_value = make_lds_value(len(longest_decreasing_subsequence_indices(values)))

        self.set_camera_target_position(0, 0, 0, (3.35, 0.38, 0.00), 9.25)
        self.play(
            FadeIn(inequality),
            FadeIn(value_expr),
            FadeIn(lis_value),
            FadeIn(lds_value),
            FadeIn(n_value),
            FadeOut(decreasing_paths_2[1:]),
            FadeOut(increasing_paths_2[1:])
        )
        release_dots_recursive(VGroup(decreasing_paths_2[1:], increasing_paths_2[1:]))
        self.wait(1)
        self.play(FadeOut(VGroup(decreasing_paths_2[0], increasing_paths_2[0])))
        release_dots_recursive(VGroup(decreasing_paths_2[0], increasing_paths_2[0]))

        num_iters = 10
        for _ in range(num_iters):
            new_bar_heights = np.random.permutation(list(range(1, n + 1)))
            permutation = [values.index(i) for i in new_bar_heights]
            for i, bar in enumerate(bars):
                bars[permutation[i]].generate_target()
                bars[permutation[i]].target.match_x(bar)
            self.play(AnimationGroup(*[MoveToTarget(bar) for bar in bars]), run_time=0.7)
            left_to_right = sorted(zip(values, bars), key=lambda triple: triple[1].get_x())
            values, bars = [v for v, _ in left_to_right], VGroup(*[b for _, b in left_to_right])
            base.add_updater(lambda m: self.bring_to_front(m))

            lis_indices = longest_increasing_subsequence_indices(values)
            lds_indices = longest_decreasing_subsequence_indices(values)
            lis = sequence_path(bars, lis_indices, increasing_sequence_color)
            lds = sequence_path(bars, lds_indices, decreasing_sequence_color)

            new_lis_value = make_lis_value(len(lis_indices))
            new_lds_value = make_lds_value(len(lds_indices))
            self.play(
                path_creation_animation(lis),
                path_creation_animation(lds),
                FadeOut(lis_value), FadeIn(new_lis_value),
                FadeOut(lds_value), FadeIn(new_lds_value), run_time=1.2)
            lis_value, lds_value = new_lis_value, new_lds_value

            self.play(FadeOut(lis), FadeOut(lds), run_time=0.7)
            release_dots_recursive(VGroup(lis, lds))
        self.wait(1)
        self.play(
            self.camera.frame.animate.restore(),
            FadeOut(VGroup(inequality, value_expr, lis_value, lds_value))
        )

        # Show (LIS, LDS) = (N, 1)
        new_bar_heights = []
        for i in range(1, n + 1):
            new_bar_heights.append(i)
        permutation = [values.index(i) for i in new_bar_heights]
        for i, bar in enumerate(bars):
            bars[permutation[i]].generate_target()
            bars[permutation[i]].target.match_x(bar)
        self.play(AnimationGroup(*[MoveToTarget(bar) for bar in bars]))
        left_to_right = sorted(zip(values, bars), key=lambda triple: triple[1].get_x())
        values, bars = [v for v, _ in left_to_right], VGroup(*[b for _, b in left_to_right])
        base.add_updater(lambda m: self.bring_to_front(m))

        # List the numbers in order from 1 up to n
        nums = VGroup(*[
            (
                Tex(str(i)).set_color(nums_color) if i < n - 1 else
                Tex(R"\cdots").set_color(nums_color).scale(0.7) if i == n - 1 else
                Tex("N").set_color(YELLOW)
            ).next_to(bars[i - 1], UP, buff=0.35)
            for i in range(1, n + 1)
        ])
        self.play(AnimationGroup(*[FadeIn(num, shift=UP * 0.2) for num in nums], lag_ratio=0.2), run_time=3)
        self.wait(1)

        all_increasing_indices = maximal_longest_increasing_subsequences(values, include_length_1=True)
        all_decreasing_indices = maximal_longest_decreasing_subsequences(values, include_length_1=True)

        increasing_paths = VGroup(*[
            sequence_path(bars, indices, increasing_sequence_color)
            for indices in all_increasing_indices
        ])
        decreasing_paths = VGroup(*[
            sequence_path(bars, indices, decreasing_sequence_color)
            for indices in all_decreasing_indices
        ])

        self.play(
            AnimationGroup(*[
                path_creation_animation(path)
                for path in increasing_paths
            ], lag_ratio=0.1)
        )
        self.wait(0.4)
        self.play(
            AnimationGroup(*[
                path_creation_animation(path)
                for path in decreasing_paths
            ], lag_ratio=0.1)
        )

        # Save the pair (n, 1)
        pair1 = Tex("(N, 1)", font_size=37).to_corner(UL, buff=0.8)
        pair1[1:-3].set_color(increasing_sequence_color)
        pair1[-2].set_color(decreasing_sequence_color)
        table_label = Tex(
            R"(\text{LIS},\ \text{LDS})",
            tex_to_color_map={"LIS": increasing_sequence_color, "LDS": decreasing_sequence_color}
        ).set_width(
            pair1.get_width() * 1.2
        ).next_to(pair1, UP)
        self.play(Write(pair1), FadeIn(table_label))
        self.play(FadeOut(decreasing_paths), FadeOut(increasing_paths), FadeOut(nums))
        release_dots_recursive(VGroup(increasing_paths, decreasing_paths))

        # Show (LIS, LDS) = (N/2, 2)
        new_bar_heights = []
        for i in range(n // 2):
            new_bar_heights.append(2 * (i + 1))
        for i in range(n // 2):
            new_bar_heights.append(2 * i + 1)
        permutation = [values.index(i) for i in new_bar_heights]
        for i, bar in enumerate(bars):
            bars[permutation[i]].generate_target()
            bars[permutation[i]].target.match_x(bar)
        self.play(AnimationGroup(*[MoveToTarget(bar) for bar in bars]))

        # List the numbers
        nums = VGroup(*[
            Tex(str(i)).set_color(nums_color).next_to(bars[i - 1], UP, buff=0.35)
            for i in range(1, n + 1)
        ])
        nums_left_to_right = sorted(nums, key=lambda m: m.get_x())
        self.play(AnimationGroup(*[FadeIn(num, shift=UP * 0.2) for num in nums_left_to_right], lag_ratio=0.2), run_time=5)
        self.wait(1)

        left_to_right = sorted(zip(values, bars), key=lambda triple: triple[1].get_x())
        values, bars = [v for v, _ in left_to_right], VGroup(*[b for _, b in left_to_right])
        base.add_updater(lambda m: self.bring_to_front(m))

        # Show the new paths
        all_increasing_indices = maximal_longest_increasing_subsequences(values, include_length_1=True)
        all_decreasing_indices = maximal_longest_decreasing_subsequences(values, include_length_1=True)

        increasing_paths = VGroup(*[
            sequence_path(bars, indices, increasing_sequence_color)
            for indices in all_increasing_indices
        ])
        decreasing_paths = VGroup(*[
            sequence_path(bars, indices, decreasing_sequence_color)
            for indices in all_decreasing_indices
        ])

        length_labels_increasing = VGroup(*[
            Tex(R"\frac{N}{2}").set_color(GREEN).next_to(path.get_center(), DR).set_stroke(width=8, color=BLACK, behind=True)
            for path in increasing_paths
        ])
        self.play(
            AnimationGroup(*[
                path_creation_animation(path)
                for path in increasing_paths
            ], lag_ratio=0.1)
        )
        self.wait(1)
        self.play(
            AnimationGroup(*[
                FadeIn(label, shift=RIGHT * 0.3, run_time=2)
                for label in length_labels_increasing
            ], lag_ratio=0.1)
        )
        self.wait(0.4)
        length_labels_decreasing = VGroup(*[
            Tex(R"2").set_color(RED).next_to(path.get_center(), UR).set_stroke(width=8, color=BLACK, behind=True)
            for path in decreasing_paths
        ])
        self.play(
            AnimationGroup(*[
                path_creation_animation(path)
                for path in decreasing_paths
            ], lag_ratio=0.1)
        )
        self.wait(1)
        self.play(
            AnimationGroup(*[
                FadeIn(label, shift=UP * 0.3, run_time=2)
                for label in length_labels_decreasing
            ], lag_ratio=0.1)
        )

        # Save the pair (N/2, 2)
        pair2 = Tex(R"\left(\frac{N}{2}, 2\right)").match_width(pair1).next_to(pair1, DOWN)
        pair2[1:-3].set_color(increasing_sequence_color)
        pair2[-2].set_color(decreasing_sequence_color)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    TransformMatchingShapes(length_labels_increasing.copy(), pair2[1:-3]),
                    TransformMatchingShapes(length_labels_decreasing.copy(), pair2[-2])
                ),
                FadeIn(VGroup(pair2[0], pair2[-3], pair2[-1])), lag_ratio=0.7)
        )
        self.wait(1)
        self.play(FadeOut(VGroup(decreasing_paths, length_labels_decreasing)))
        release_dots_recursive(decreasing_paths)
        self.wait(2)

        # Show the case where N is odd
        bar_11 = bars[0].copy().stretch_to_fit_height(
            bars[5].get_height() * 11
        ).next_to(
            bars, RIGHT, buff=bars[1].get_left()[0] - bars[0].get_right()[0]
        ).align_to(
            bars, DOWN
        )
        bars.generate_target()
        bar_11.generate_target()
        VGroup(bars.target, bar_11.target).match_width(bars).match_x(bars).align_to(bars, DOWN)
        bar_11.set_opacity(0)
        bars.save_state()
        bar_11.save_state()

        all_increasing_indices_new = [
            [0, 1, 2, 3, 4],
            [5, 6, 7, 8, 9, 10]
        ]
        increasing_paths_new = VGroup(*[
            sequence_path(VGroup(*bars.target, bar_11.target), indices, increasing_sequence_color)
            for indices in all_increasing_indices_new
        ])
        length_labels_increasing_new = VGroup(*[
            Tex(R"\frac{N}{2}" if i == 0 else R"\left\lceil\frac{N}{2}\right\rceil").set_color(
                GREEN
            ).next_to(
                path.get_center(), DR
            ).set_stroke(
                width=8, color=BLACK, behind=True
            )
            for i, path in enumerate(increasing_paths_new)
        ])
        increasing_paths.set_z_index(100)
        new_values = [2, 4, 6, 8, 10, 1, 3, 5, 7, 9, 11]
        nums = VGroup(*[sorted(nums, key=lambda m: m.get_x())])
        new_nums = VGroup(*[Tex(str(value)).set_color(nums_color).next_to(bar, UP) for value, bar in zip(new_values, list(bars.target) + [bar_11.target])])
        self.play(
            MoveToTarget(bars),
            MoveToTarget(bar_11),
            ReplacementTransform(increasing_paths, increasing_paths_new, run_time=1),
            TransformMatchingShapes(length_labels_increasing, length_labels_increasing_new, run_time=1),
            ReplacementTransform(nums, new_nums[:-1]),
            FadeIn(new_nums[-1], shift=DL * 0.5)
        )
        release_dots_recursive(increasing_paths)
        self.wait(2)
        bars = VGroup(*bars, bar_11)
        values += [11]
        self.play(FadeOut(VGroup(increasing_paths_new, length_labels_increasing_new, new_nums)))

        # Show (LIS, LDS) = (N/3, 3)
        n = 11
        k = 3
        new_bar_heights = []
        for j in range(k):
            new_bar_heights += [i for i in range(1, n + 1) if (i + j) % k == 0]

        permutation = [values.index(i) for i in new_bar_heights]
        for i, bar in enumerate(bars):
            bars[permutation[i]].generate_target()
            bars[permutation[i]].target.match_x(bar)
        self.play(AnimationGroup(*[MoveToTarget(bar) for bar in bars]))
        self.wait(1)

        left_to_right = sorted(zip(values, bars), key=lambda triple: triple[1].get_x())
        values, bars = [v for v, _ in left_to_right], VGroup(*[b for _, b in left_to_right])
        base.add_updater(lambda m: self.bring_to_front(m))

        all_increasing_indices = []
        section = []
        start_index = 0
        for i in range(k):
            finish_index = start_index + (n // k if i < (-n) % k else n // k + 1)
            section.append([new_bar_heights.index(h) for h in new_bar_heights[start_index:finish_index]])
            start_index = finish_index
        all_increasing_indices += section
        all_decreasing_indices = maximal_longest_decreasing_subsequences(values, include_length_1=True)

        increasing_paths = VGroup(*[
            sequence_path(bars, indices, increasing_sequence_color)
            for indices in all_increasing_indices
        ])
        decreasing_paths = VGroup(*[
            sequence_path(bars, indices, decreasing_sequence_color)
            for indices in all_decreasing_indices
        ])

        length_labels_increasing = VGroup(*[
            Tex(R"\frac{N}{" + str(k) + "}" if n % k > i + 1 else R"\left\lceil\frac{N}{" + str(k) + R"}\right\rceil", font_size=35).set_color(
                GREEN
            ).next_to(
                path.get_center(), LEFT
            ).set_stroke(
                width=8, color=BLACK, behind=True
            )
            for i, path in enumerate(increasing_paths)
        ])
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    path_creation_animation(path),
                    FadeIn(label, shift=RIGHT * 0.3), lag_ratio=0.3)
                for path, label in zip(increasing_paths, length_labels_increasing)
            ], lag_ratio=0.1)
        )
        self.wait(0.4)
        length_labels_decreasing = VGroup(*[
            Tex(str(len(indices))).set_color(RED).next_to(path.get_center(), UR).set_stroke(width=8, color=BLACK, behind=True)
            for path, indices in zip(decreasing_paths, all_decreasing_indices)
        ])
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    path_creation_animation(path),
                    FadeIn(label, shift=UP * 0.3), lag_ratio=0.3)
                for path, label in zip(decreasing_paths, length_labels_decreasing)
            ], lag_ratio=0.1)
        )
        self.wait(1)

        # Save the pair (N/3, 3)
        pair3 = Tex(R"\left(\frac{N}{" + str(k) + "}, " + str(k) + R"\right)").match_width(pair1).next_to(pair2, DOWN)
        pair3[1:-3].set_color(increasing_sequence_color)
        pair3[-2].set_color(decreasing_sequence_color)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    TransformMatchingShapes(length_labels_increasing.copy(), pair3[1:-3]),
                    TransformMatchingShapes(length_labels_decreasing.copy(), pair3[-2])
                ),
                FadeIn(VGroup(pair3[0], pair3[-3], pair3[-1])), lag_ratio=0.7)
        )
        self.wait(1)
        self.play(FadeOut(VGroup(decreasing_paths, length_labels_decreasing, increasing_paths, length_labels_increasing)))
        release_dots_recursive(VGroup(increasing_paths, decreasing_paths))
        self.wait(0.3)

        # Show the entire family of examples
        pairs = VGroup(table_label, pair1, pair2, pair3)
        for k in range(4, 7):
            self.remove(VGroup(decreasing_paths, increasing_paths))
            release_dots_recursive(VGroup(decreasing_paths, increasing_paths))
            new_bar_heights = []
            for j in range(k):
                new_bar_heights += [i for i in range(1, n + 1) if (i + j) % k == 0]

            permutation = [values.index(i) for i in new_bar_heights]
            bars.generate_target()
            for i, bar in enumerate(bars):
                bars.target[permutation[i]].match_x(bar)
            bars.become(bars.target)

            left_to_right = sorted(zip(values, bars), key=lambda triple: triple[1].get_x())
            values, bars = [v for v, _ in left_to_right], VGroup(*[b for _, b in left_to_right])
            base.add_updater(lambda m: self.bring_to_front(m))

            all_increasing_indices = []
            section = []
            start_index = 0
            for i in range(k):
                finish_index = start_index + (n // k if i < (-n) % k else n // k + 1)
                section.append([new_bar_heights.index(h) for h in new_bar_heights[start_index:finish_index]])
                start_index = finish_index
            all_increasing_indices += section
            all_decreasing_indices = maximal_longest_decreasing_subsequences(values, include_length_1=True)

            increasing_paths = VGroup(*[
                sequence_path(bars, indices, increasing_sequence_color)
                for indices in all_increasing_indices
            ])
            decreasing_paths = VGroup(*[
                sequence_path(bars, indices, decreasing_sequence_color)
                for indices in all_decreasing_indices
            ])
            for path in increasing_paths:
                prepare_path_dots(path)
            for path in decreasing_paths:
                prepare_path_dots(path)

            next_pair = Tex(R"\left(\frac{N}{" + str(k) + "}, " + str(k) + R"\right)").match_width(pair1).next_to(pairs[-1], DOWN)
            next_pair[1:-3].set_color(increasing_sequence_color)
            next_pair[-2].set_color(decreasing_sequence_color)
            pairs.add(next_pair)
            self.add(increasing_paths, decreasing_paths)
            self.play(FadeIn(next_pair), run_time=0.1)
            self.wait(1)
        vdots = Tex(R"\vdots").next_to(pairs, DOWN)
        self.play(Write(vdots, run_time=0.7))

        # Conjecture that LIS*LDS >= N
        base.clear_updaters()
        chart = VGroup(bars, base)
        self.play(
            FadeOut(VGroup(chart, increasing_paths, decreasing_paths), shift=RIGHT * 3),
            VGroup(pairs, vdots).animate.scale(1.2).set_y(0).set_x(1), run_time=2)
        release_dots_recursive(VGroup(increasing_paths, decreasing_paths))
        brace = Brace(pairs[1:], RIGHT)
        label = brace.get_tex(
            R"\text{LIS} \cdot \text{LDS} \ge N",
            tex_to_color_map={"LIS": increasing_sequence_color, "LDS": decreasing_sequence_color, "N": n_color},
            font_size=50,
            buff=0.3
        )
        self.play(GrowFromEdge(brace, LEFT), Write(label), run_time=2)
        self.wait(2)

        # Build a square k^2-bar chart in the residue-block pattern (shared by k = 3..6)
        frame = self.camera.frame
        bottom_margin = 0.5
        brace_headroom = 1.3  # room for the N-brace/label above the chart
        square_side = frame.get_height() - bottom_margin - brace_headroom
        bars_bottom_y = frame.get_bottom()[1] + bottom_margin

        def build_square_chart(k):
            n_local = k**2
            heights = []
            for j in range(k):
                heights += [i for i in range(1, n_local + 1) if (i + j) % k == 0]
            bw = square_side / (n_local - 0.1)
            new_bars = VGroup(*[
                Rectangle(
                    width=bw * 0.9,
                    height=(h / n_local) * square_side,
                    fill_opacity=1,
                    fill_color=bar_color,
                    stroke_width=0,
                )
                for h in heights
            ]).arrange(RIGHT, buff=bw * 0.1, aligned_edge=DOWN)
            new_bars.move_to(ORIGIN)
            new_bars.set_y(bars_bottom_y + square_side / 2)
            new_base = Line(LEFT, RIGHT).set_width(new_bars.get_width() * 1.05)
            new_base.match_x(new_bars)
            new_base.set_y(bars_bottom_y)
            new_chart = VGroup(new_bars, new_base)
            return new_chart, new_bars, new_base, heights

        def add_square_braces(new_bars):
            n_brace = Brace(new_bars, UP)
            n_label = n_brace.get_tex(
                "N = k^2",
                tex_to_color_map={"N": n_color, "k": TEAL},
                font_size=50
            )
            return VGroup(n_brace, n_label)

        def add_square_subsequences(new_bars, heights, k):
            # Each residue class is a contiguous block of exactly k bars
            # (since n_local = k^2 divides evenly by k), so every maximal
            # increasing run is just a consecutive chunk of size k, and by
            # construction every maximal decreasing run also has length k.
            all_increasing_indices = [
                list(range(block * k, (block + 1) * k))
                for block in range(k)
            ]
            all_decreasing_indices = maximal_longest_decreasing_subsequences(heights, include_length_1=True)

            increasing_paths = VGroup(*[
                sequence_path(new_bars, indices, increasing_sequence_color)
                for indices in all_increasing_indices
            ])
            decreasing_paths = VGroup(*[
                sequence_path(new_bars, indices, decreasing_sequence_color)
                for indices in all_decreasing_indices
            ])
            for path in increasing_paths:
                prepare_path_dots(path)
            for path in decreasing_paths:
                prepare_path_dots(path)

            return VGroup(increasing_paths, decreasing_paths)

        # Bring in the chart already arranged as n = 9 = 3^2 in the k=3 pattern
        base.clear_updaters()
        new_chart, bars, base, heights = build_square_chart(3)
        current_chart = new_chart
        current_braces = add_square_braces(bars)
        current_subsequences = add_square_subsequences(bars, heights, 3)
        values = heights
        n = 9
        self.play(
            AnimationGroup(
                FadeOut(VGroup(pairs, vdots, brace, label), shift=LEFT * 7, run_time=2),
                FadeIn(VGroup(new_chart, current_braces, current_subsequences), shift=LEFT * 7, run_time=1.5), lag_ratio=0.3)
        )
        self.wait(0.5)

        # Now show a square chart of k^2 bars in this same pattern, for k = 4, 5, 6
        for k in range(4, 7):
            new_chart, new_bars, new_base, heights = build_square_chart(k)
            self.remove(current_chart)
            self.add(new_chart)
            self.remove(current_braces)
            current_braces = add_square_braces(new_bars)
            self.add(current_braces)
            self.remove(current_subsequences)
            release_dots_recursive(current_subsequences)
            current_subsequences = add_square_subsequences(new_bars, heights, k)
            for sequences in current_subsequences:
                for s in sequences:
                    s[1].set_stroke(width=4)
            self.add(current_subsequences)
            current_chart = new_chart
            bars, base, values = new_bars, new_base, heights
            n = k**2
            self.wait(1)

        # Fade it to a grid
        grid = OptimalGrid(6).match_width(bars).align_to(bars, DOWN)
        grid.tiles.set_stroke(width=3)
        for hole in grid.holes:
            hole.border.set_stroke(width=3, color=WHITE)
        self.play(FadeIn(grid.holes.set_z_index(100)), FadeOut(current_subsequences), run_time=2)
        release_dots_recursive(current_subsequences)
        self.play(FadeOut(new_chart), FadeIn(VGroup(grid.background, grid.tiles)), run_time=2)
        self.wait(1)

        # Ambiently flip through random permutations, landing on the main example for the rest of the scene
        self.clear()
        dot_stacks.clear()
        self.camera.frame.restore()
        n = 9
        chart_width = 6
        chart_height = 5.8
        bar_width = chart_width / n
        final_heights = [6, 5, 2, 4, 1, 9, 8, 7, 3]

        values = list(np.random.permutation(list(range(1, n + 1))))
        bars = VGroup(*[
            Rectangle(
                width=bar_width * 0.9,
                height=(h / n) * chart_height,
                fill_opacity=1,
                fill_color=bar_color,
                stroke_width=0,
            )
            for h in values
        ]).arrange(RIGHT, buff=bar_width * 0.1, aligned_edge=DOWN)
        bars.move_to(ORIGIN).to_edge(DOWN, buff=1.0)
        base = Line(LEFT, RIGHT).set_width(bars.get_width() * 1.05).match_x(bars).next_to(bars, DOWN, buff=0)
        chart = VGroup(bars, base)

        self.add(chart)
        base.add_updater(lambda m: self.bring_to_front(m))
        self.wait(0.5)

        num_lead_in_iters = 45
        for i in range(num_lead_in_iters):
            is_last = (i == num_lead_in_iters - 1)
            if is_last:
                new_bar_heights = final_heights
            else:
                new_bar_heights = list(np.random.permutation(list(range(1, n + 1))))
                while new_bar_heights == values:
                    new_bar_heights = list(np.random.permutation(list(range(1, n + 1))))
            permutation = [values.index(h) for h in new_bar_heights]
            for i2, bar in enumerate(bars):
                bars[permutation[i2]].generate_target()
                bars[permutation[i2]].target.match_x(bar)
            self.play(AnimationGroup(*[MoveToTarget(bar) for bar in bars]), run_time=0.6)
            left_to_right = sorted(zip(values, bars), key=lambda pair: pair[1].get_x())
            values, bars = [v for v, _ in left_to_right], VGroup(*[b for _, b in left_to_right])
            base.add_updater(lambda m: self.bring_to_front(m))

            lis_indices = longest_increasing_subsequence_indices(values)
            lds_indices = longest_decreasing_subsequence_indices(values)
            lis_path = sequence_path(bars, lis_indices, increasing_sequence_color)
            lds_path = sequence_path(bars, lds_indices, decreasing_sequence_color)
            self.play(
                path_creation_animation(lis_path),
                path_creation_animation(lds_path), run_time=0.9)
            self.wait(0.5)
            self.play(FadeOut(lis_path), FadeOut(lds_path), run_time=0.5)
            release_dots_recursive(VGroup(lis_path, lds_path))

        heights = values
        nums = VGroup(*[
            Integer(h, font_size=40).set_color(nums_color).next_to(bar, UP, buff=0.38)
            for h, bar in zip(heights, bars)
        ])
        self.play(FadeIn(nums))
        base.add_updater(lambda m: self.bring_to_front(m))
        self.wait(1)

        # Focus on one of the bars
        focus_index = 3
        focus_bar = bars[focus_index]
        arrow = Arrow(ORIGIN, DOWN * 1.5, thickness=5).set_color(YELLOW).next_to(focus_bar, UP, buff=1.5)
        self.play(
            AnimationGroup(*[
                VGroup(bar, num).animate.set_opacity(0.1)
                for bar, num in zip(bars[focus_index + 1:], nums[focus_index + 1:])
            ]),
            GrowArrow(arrow)
        )

        # Highlight its longest increasing and decreasing subsequences
        increasing_indices = [2, 3]
        increasing_path = sequence_path(bars, increasing_indices, increasing_sequence_color)
        self.play(path_creation_animation(increasing_path))
        self.wait(1)
        lis_text = Tex(R"\text{LIS}: 2", font_size=110).set_color(increasing_sequence_color)
        lds_text = Tex(R"\text{LDS}: 3", font_size=110).set_color(decreasing_sequence_color)
        lds_text.next_to(lis_text, DOWN, buff=0.6).align_to(lis_text, LEFT)
        VGroup(lis_text, lds_text).set_y(0).to_edge(RIGHT, buff=1.5)
        base.suspend_updating()
        self.play(
            AnimationGroup(
                VGroup(chart, nums, arrow, increasing_path).animate.to_edge(LEFT, buff=1.5),
                Write(lis_text), lag_ratio=0.6, run_time=1.5)
        )
        base.resume_updating()
        self.wait(1)
        decreasing_indices = [0, 1, 3]
        decreasing_path = sequence_path(bars, decreasing_indices, decreasing_sequence_color)
        self.play(path_creation_animation(decreasing_path))
        self.wait(1)
        self.play(Write(lds_text), run_time=1.5)
        self.wait(1)
        self.wait(2)

        # Save the values as a pair of numbers below the bar
        pair = Tex("(2, 3)", font_size=30).next_to(focus_bar, DOWN)
        pair[1].set_color(increasing_sequence_color)
        pair[3].set_color(decreasing_sequence_color)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    TransformFromCopy(lis_text[-1], pair[1]),
                    TransformFromCopy(lds_text[-1], pair[3]), run_time=2),
                FadeIn(VGroup(pair[0], pair[2], pair[4])), lag_ratio=0.7)
        )
        self.wait(2)

        # Switch focus back to the full chart
        chart = VGroup(bars, base)
        base.clear_updaters()
        chart.generate_target()
        chart.target.set_opacity(1).stretch(1.5, 0).center()
        nums.generate_target()
        nums.target.set_opacity(1)
        for num, bar in zip(nums.target, chart.target[0]):
            num.match_x(bar)
        pair.generate_target()
        pair.target.match_x(chart.target[0][3]).scale(1.3)

        increasing_path.set_z_index(100)
        decreasing_path.set_z_index(100)
        self.play(
            FadeOut(arrow, shift=UP),
            FadeOut(VGroup(lis_text, lds_text), run_time=1),
            MoveToTarget(chart, run_time=2),
            MoveToTarget(nums, run_time=2),
            MoveToTarget(pair, run_time=2),
            FadeOut(increasing_path, shift=RIGHT * 0.08, run_time=0.6),
            FadeOut(decreasing_path, shift=RIGHT * 0.08, run_time=0.6)
        )
        release_dots_recursive(VGroup(increasing_path, decreasing_path))
        base.add_updater(lambda m: self.bring_to_front(m))
        self.wait(2)

        # Show that all the numbers are distinct
        self.remove(pair)
        self.wait(1)
        circles = VGroup(*[Circle(radius=0.35, fill_opacity=0, stroke_width=3, stroke_color=YELLOW).move_to(num) for num in nums])
        self.play(AnimationGroup(*[ShowCreation(circle) for circle in circles], lag_ratio=0.1))
        self.wait(2)
        self.play(FadeOut(circles))

        # Add the (LIS, LDS) pair for each bar
        lis_lds_lengths = [(1, 1), (1, 2), (1, 3), (2, 3), (1, 4), (3, 1), (3, 2), (3, 3), (2, 4)]
        pairs = VGroup(*[
            Tex(F"({lis}, {lds})").match_height(pair).match_y(pair).match_x(bar)
            for (lis, lds), bar in zip(lis_lds_lengths, bars)
        ])
        self.add(pairs[focus_index])
        for i, pair in enumerate(pairs):
            pair[1].set_color(increasing_sequence_color)
            pair[3].set_color(decreasing_sequence_color)
            pair.save_state()
            if i != focus_index:
                pair.scale(1.2).set_opacity(0)
            else:
                pair.set_opacity(1)
        self.play(
            AnimationGroup(*[
                pair.animate.restore()
                for pair in list(pairs[:focus_index]) + list(pairs[focus_index + 1:])
            ], lag_ratio=0.2), run_time=3.6)
        self.wait(2)

        # Do another example
        bars.save_state()
        nums.save_state()
        pairs.save_state()
        focus_index = 6
        focus_bar = bars[focus_index]
        arrow = Arrow(ORIGIN, DOWN * 1.1, thickness=4).set_color(YELLOW).next_to(focus_bar, UP, buff=0.85)
        self.play(
            VGroup(
                *[
                    VGroup(bar, num)
                    for bar, num in zip(bars[focus_index + 1:], nums[focus_index + 1:])
                ],
                pairs[:focus_index],
                pairs[focus_index + 1:]
            ).animate.set_opacity(0.1),
            GrowArrow(arrow)
        )
        increasing_indices = [2, 3, 6]
        increasing_path = sequence_path(bars, increasing_indices, increasing_sequence_color)
        self.play(path_creation_animation(increasing_path))
        self.wait(1)
        decreasing_indices = [5, 6]
        decreasing_path = sequence_path(bars, decreasing_indices, decreasing_sequence_color)
        self.play(path_creation_animation(decreasing_path))
        self.wait(1)
        self.play(
            bars.animate.restore(), nums.animate.restore(), pairs.animate.restore(),
            FadeOut(arrow), FadeOut(increasing_path), FadeOut(decreasing_path), run_time=2
        )
        release_dots_recursive(VGroup(increasing_path, decreasing_path))
        self.wait(1)

        # Indicate pairs to show uniqueness
        self.play(AnimationGroup(*[Indicate(pair) for pair in pairs], lag_ratio=0.1), run_time=3)

        # Save the full chart
        original_chart_group = VGroup(chart, nums, pairs).copy()

        # Bring in an arbitrary pair of bars
        bar1 = bars[1].copy()
        bar2 = bar1.copy()
        VGroup(bar1, bar2).arrange(buff=2).align_to(bars[0], DOWN)
        self.play(
            AnimationGroup(
                FadeOut(VGroup(bars, nums, pairs)),
                FadeIn(VGroup(bar1, bar2)), lag_ratio=0.2), run_time=3)
        self.wait(2)

        # Write an arbitrary pair of values for the LIS and LDS for that bar
        pair = Tex("(x, y)", tex_to_color_map={"x": increasing_sequence_color, "y": decreasing_sequence_color}).match_height(pairs[0]).match_y(pairs[0]).match_x(bar1)
        self.play(FadeIn(pair))

        # Make the second bar taller
        stretch_factor = 1.2
        self.play(
            bar1.animate.stretch(1 / stretch_factor, 1).align_to(bar1, DOWN),
            bar2.animate.stretch(stretch_factor, 1).align_to(bar2, DOWN), run_time=0.7)
        self.play(
            bar1.animate.stretch(stretch_factor**2, 1).align_to(bar1, DOWN),
            bar2.animate.stretch(1 / stretch_factor**2, 1).align_to(bar2, DOWN), run_time=0.7)
        self.play(
            bar1.animate.stretch(1 / stretch_factor**3, 1).align_to(bar1, DOWN),
            bar2.animate.stretch(stretch_factor**3, 1).align_to(bar2, DOWN), run_time=2)
        pair2 = Tex("(x', y')", tex_to_color_map={"x'": increasing_sequence_color, "y'": decreasing_sequence_color}).match_height(pairs[0]).match_y(pairs[0]).match_x(bar2)
        self.play(FadeIn(pair2))
        self.wait(1)

        # Show a generic tail of bars behind the first bar
        heights_tail = [2, 6, 5, 3]
        heights_tail = [h * 0.6 for h in heights_tail]
        tail = VGroup(*[
            bar1.copy().stretch_to_fit_width(0.5).stretch_to_fit_height(height)
            for height in heights_tail
        ]).arrange(
            buff=0.1
        ).next_to(
            bar1, LEFT, buff=0.2
        )
        tail_opacity = 0.4
        for bar in tail:
            bar.align_to(
                bar1, DOWN
            ).set_opacity(
                tail_opacity
            )
        cdots = Tex(R"\cdots", font_size=100).match_y(bar1)

        self.play(
            AnimationGroup(
                *[
                    FadeIn(bar)
                    for bar in tail
                ],
                Write(cdots, run_time=1.5), lag_ratio=0.1),
        )
        self.wait(2)

        # Show the increasing subsequence of length x
        increasing_sequence = VGroup(tail[0], tail[3], bar1)
        increasing_path = sequence_path(increasing_sequence, range(len(increasing_sequence)), increasing_sequence_color)
        brace = Brace(increasing_sequence, UP).shift(UP * 0.1)
        label = brace.get_tex("x", font_size=60).set_color(increasing_sequence_color).shift(UP * 0.2)
        self.play(
            AnimationGroup(*[
                bar.animate.set_opacity(1)
                for bar in increasing_sequence
            ], lag_ratio=0.1),
            path_creation_animation(increasing_path),
            GrowFromEdge(brace, DOWN),
            Write(label)
        )
        self.wait(2)

        # Extend the increasing sequence to the second bar
        brace.generate_target()
        label.generate_target()
        extended_brace = Brace(VGroup(increasing_sequence, bar2), UP).shift(UP * 0.1)
        extended_label = extended_brace.get_tex(R"x' \ge x + 1", font_size=60).set_color(increasing_sequence_color).shift(UP * 0.2)
        part1 = extended_label[:3]
        part2 = extended_label[3:]
        part2.save_state()
        part2.match_x(extended_brace)
        extended_increasing_sequence = VGroup(*increasing_sequence, bar2)
        extended_increasing_path = sequence_path(extended_increasing_sequence, range(len(extended_increasing_sequence)), increasing_sequence_color)
        self.play(
            TransformFromCopy(brace, extended_brace),
            TransformMatchingShapes(label.copy(), part2),
            Transform(increasing_path.set_z_index(100), extended_increasing_path.set_z_index(100)), run_time=2)
        self.wait(1)
        self.play(part2.animate.restore(), FadeIn(part1, shift=RIGHT * 0.5))

        # Save the example
        case1 = VGroup(
            tail, bar1, bar2, increasing_path, base, pair, pair2,
            brace, label, extended_brace, extended_label, cdots
        ).copy()

        # Make the second bar shorter
        increasing_path.set_z_index(100)
        self.play(
            FadeOut(VGroup(brace, label, extended_brace, extended_label)),
            FadeOut(increasing_path),
            tail.animate.set_opacity(tail_opacity),
            bar2.animate.stretch_to_fit_height(0.6 * bar1.get_height()).align_to(bar2, DOWN)
        )
        self.wait(2)

        # Show the decreasing subsequence of length y
        decreasing_sequence = VGroup(tail[1], tail[2], bar1)
        decreasing_path = sequence_path(decreasing_sequence, range(len(decreasing_sequence)), decreasing_sequence_color)
        brace = Brace(decreasing_sequence, UP)
        label = brace.get_tex("y", font_size=60).set_color(decreasing_sequence_color)
        self.play(
            AnimationGroup(*[
                bar.animate.set_opacity(1)
                for bar in decreasing_sequence
            ], lag_ratio=0.1),
            path_creation_animation(decreasing_path),
            GrowFromEdge(brace, DOWN),
            Write(label)
        )
        self.wait(2)

        # Extend the decreasing sequence to the second bar
        brace.generate_target()
        label.generate_target()
        extended_brace = Brace(VGroup(decreasing_sequence, bar2), UP).align_to(case1[-3], UP)
        extended_label = extended_brace.get_tex(R"y' \ge y + 1", font_size=60).set_color(decreasing_sequence_color).align_to(case1[-2], UP)
        part1 = extended_label[:3]
        part2 = extended_label[3:]
        part2.save_state()
        part2.match_x(extended_brace)
        extended_decreasing_sequence = VGroup(*decreasing_sequence, bar2)
        extended_decreasing_path = sequence_path(extended_decreasing_sequence, range(len(extended_decreasing_sequence)), decreasing_sequence_color)
        self.play(
            TransformFromCopy(brace, extended_brace),
            TransformMatchingShapes(label.copy(), part2),
            Transform(decreasing_path, extended_decreasing_path), run_time=2)
        self.wait(1)
        self.play(part2.animate.restore(), FadeIn(part1, shift=RIGHT * 0.5))

        # Save the second example
        case2 = VGroup(
            tail, bar1, bar2, decreasing_path, base, pair, pair2,
            brace, label, extended_brace, extended_label, cdots
        )

        # Show both examples side by side
        case1.clear_updaters()
        base.clear_updaters()
        case1[1:4].set_z_index(400)
        case2.generate_target()
        VGroup(case1, case2.target).scale(0.63).arrange(buff=0.7)
        case2.target.align_to(case1, DOWN)
        case2[1:4].set_z_index(400)
        case1_label = TexText("Case 1").next_to(case1, DOWN, buff=1)
        case2_label = TexText("Case 2").next_to(case2.target, DOWN, buff=1)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeIn(case1, shift=RIGHT * 5),
                    MoveToTarget(case2)
                ),
                LaggedStartMap(FadeIn, VGroup(case1_label, case2_label), lag_ratio=0.2, shift=UP * 1.5, run_time=0.8), lag_ratio=0.1), run_time=3)

        # Bring back the original chart
        original_chart_group.clear_updaters()
        self.play(
            FadeOut(VGroup(case1, case2, case1_label, case2_label), shift=DOWN * 7),
            FadeIn(original_chart_group, shift=DOWN * 7), run_time=1.5)
        chart, nums, pairs = original_chart_group[0], original_chart_group[1], original_chart_group[2]
        self.wait(0.5)

        # Indicate pairs again to show uniqueness
        self.play(AnimationGroup(*[Indicate(pair) for pair in pairs], lag_ratio=0.1), run_time=3)
        self.wait(2)

        # Put each pair of numbers on a coordinate grid
        number_plane = NumberPlane(
            x_range=[0, 5],
            y_range=[0, 5]
        ).set_width(4.5).to_edge(RIGHT, buff=1)
        number_plane.remove(number_plane.faded_lines)
        x_labels = number_plane.add_coordinate_labels(x_values=[1, 2, 3, 4, 5], y_values=[], font_size=30, direction=DOWN)
        y_labels = number_plane.add_coordinate_labels(x_values=[], y_values=[1, 2, 3, 4, 5], font_size=30, direction=LEFT)
        x_labels.set_color(increasing_sequence_color)
        y_labels.set_color(decreasing_sequence_color)
        points = Group(*[
            Group(GlowDot(), TrueDot()).set_color(n_color).move_to(number_plane.c2p(x, y))
            for (x, y) in lis_lds_lengths
        ])
        point_labels = pairs.copy()
        for point, label in zip(points, point_labels):
            label.scale(0.6).next_to(point, UR, buff=-0.1)
        self.play(
            original_chart_group.animate(run_time=2).scale(0.55).to_edge(LEFT, buff=1),
            FadeIn(number_plane, shift=LEFT * 6, run_time=2),
            AnimationGroup(*[
                AnimationGroup(
                    TransformFromCopy(pair, label, path_arc=-PI * 0.2),
                    FadeIn(point), lag_ratio=0.6, run_time=2 + i * 0.2)
                for i, (point, pair, label) in enumerate(zip(points, pairs, point_labels))
            ])
        )
        self.wait(1)

        # Draw a rectangle bounding the points
        unit_size = number_plane.background_lines[1].get_y() - number_plane.background_lines[0].get_y()
        rect = Rectangle(
            width=unit_size * 3,
            height=unit_size * 4,
            fill_opacity=0.4,
            fill_color=TEAL,
            stroke_width=4,
            stroke_color=TEAL
        ).align_to(number_plane.c2p(0, 0), DL)
        self.bring_to_back(rect)
        self.play(
            DrawBorderThenFill(rect, stroke_width=6), run_time=2)
        self.wait(2)

        # Show the dimensions
        width_brace = Brace(rect, DOWN, buff=0.5)
        width_label = width_brace.get_tex(R"\text{LIS}").set_color(increasing_sequence_color)
        bars, base = chart
        base.add_updater(lambda m: self.bring_to_front(m))

        increasing_indices = [2, 3, 7]
        decreasing_indices = [0, 1, 3, 8]
        increasing_path = sequence_path(bars, increasing_indices, increasing_sequence_color)
        self.play(
            GrowFromEdge(width_brace, UP),
            Write(width_label),
            path_creation_animation(increasing_path)
        )
        self.wait(1)

        height_brace = Brace(rect, LEFT, buff=0.5)
        height_label = height_brace.get_tex(R"\text{LDS}").set_color(decreasing_sequence_color)
        decreasing_path = sequence_path(bars, decreasing_indices, decreasing_sequence_color)
        self.play(
            GrowFromEdge(height_brace, RIGHT),
            Write(height_label),
            path_creation_animation(decreasing_path)
        )
        self.wait(1)

        # Circle the lattice points
        lattice_points = VGroup()
        for i in range(3):
            for j in range(4):
                point = Circle(
                    radius=0.15, stroke_width=3, stroke_color=WHITE
                ).move_to(number_plane.c2p(i + 1, j + 1))
                lattice_points.add(point)
        self.play(AnimationGroup(*[ShowCreation(point) for point in lattice_points], lag_ratio=0.15))

        # Write the inequality up top
        inequality = Tex(
            R"\text{LIS} \cdot \text{LDS} \ge N",
            font_size=64,
            tex_to_color_map={"LIS": increasing_sequence_color, "LDS": decreasing_sequence_color, "N": n_color}
        ).to_edge(UP, buff=0.6)
        self.play(
            AnimationGroup(
                TransformMatchingShapes(width_label.copy(), inequality["LIS"], path_arc=-PI * 0.35),
                TransformMatchingShapes(height_label.copy(), inequality["LDS"], path_arc=-PI * 0.2),
                GrowFromCenter(inequality[R"\cdot"], path_arc=-PI * 0.3),
                Write(inequality[R"\ge N"]), lag_ratio=0.3, run_time=2)
        )

    def set_camera_target_position(
        self,
        theta_degrees=None,
        phi_degrees=None,
        gamma_degrees=None,
        center=None,
        height=None,
        drift_time=2.0,
    ):
        frame = self.camera.frame
        frame.clear_updaters()
        initial_orientation = frame.get_orientation()
        initial_height = frame.get_height()
        initial_eye = frame.get_implied_camera_location()
        target_frame = frame.copy()
        target_frame.reorient(theta_degrees, phi_degrees, gamma_degrees, center, height)
        target_orientation = target_frame.get_orientation()
        target_height = target_frame.get_height()
        target_eye = target_frame.get_implied_camera_location()
        fovy = frame.get_field_of_view()
        slerp = Slerp([0, 1], Rotation.concatenate([initial_orientation, target_orientation]))
        drift_time = max(drift_time, 1e-4)
        elapsed = 0.0

        def update_camera(f, dt):
            nonlocal elapsed
            elapsed += dt
            t = min(elapsed / drift_time, 1.0)
            alpha = smooth(t)
            current_orientation = slerp(alpha)
            current_height = interpolate(initial_height, target_height, alpha)
            current_eye = interpolate(initial_eye, target_eye, alpha)
            focal_distance = 0.5 * current_height / np.tan(0.5 * fovy)
            to_camera = current_orientation.as_matrix().T[2]
            current_center = current_eye - focal_distance * to_camera
            f.set_orientation(current_orientation)
            f.move_to(current_center)
            f.set_height(current_height)
            if t >= 1.0:
                f.remove_updater(update_camera)
        frame.add_updater(update_camera)


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
