# ==============================================================================
# Scene:      ErdosSzekeres
# Source:     videos/_2026/2025_P6/p6.py (lines 1087-1982)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ErdosSzekeres.py ErdosSzekeres -w -m --fps 15
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


class ErdosSzekeres(InteractiveScene):
    def construct(self):
        # Add a grid
        n = 9
        grid = Grid(n).set_width(6)
        self.add(grid)
        hole_positions = [3, 4, 7, 5, 8, 0, 1, 2, 6]
        for i, j in enumerate(hole_positions):
            grid.add_hole(i, j)
        grid.add_tile(5, 3, 0, 0)
        grid.add_tile(3, 1, 6, 0)
        grid.add_tile(1, 2, 5, 1)
        grid.add_tile(2, 1, 7, 1)
        grid.add_tile(1, 1, 6, 2)
        grid.add_tile(1, 4, 8, 2)
        grid.add_tile(1, 1, 1, 3)
        grid.add_tile(6, 2, 2, 3)
        grid.add_tile(1, 5, 0, 4)
        grid.add_tile(2, 2, 1, 5)
        grid.add_tile(4, 3, 4, 5)
        grid.add_tile(1, 2, 3, 6)
        grid.add_tile(1, 1, 1, 7)
        grid.add_tile(1, 2, 8, 7)
        grid.add_tile(3, 1, 1, 8)
        grid.add_tile(3, 1, 5, 8)
        grid.tiles.set_stroke(width=3)
        for hole in grid.holes:
            hole.border.set_color(WHITE)

        # Number the holes according to their height
        nums_color = BLUE_B
        values = [n - j for j in hole_positions]
        nums = VGroup(*[
            Integer(j).set_color(BLUE_B).next_to(grid.holes[i], UP, buff=0.15)
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
                            ], lag_ratio=0.1),
                            FadeOut(column)
                        ),
                        FadeIn(num, shift=UP * 0.2, run_time=0.7), lag_ratio=0.1)
                    for num, column in zip(nums, column_highlights)
                ], lag_ratio=0.2),
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

        for num, bar in zip(nums, bars):
            num.generate_target()
            num.target.next_to(bar, UP, buff=0.2)
            bar.save_state()
            bar.stretch_to_fit_height(0.001).align_to(base, DOWN)
        self.play(
            self.camera.frame.animate.restore(),
            FadeOut(VGroup(brace, label)),
            FadeOut(grid, run_time=3),
            AnimationGroup(*[
                AnimationGroup(
                    MoveToTarget(num),
                    bar.animate.restore(), lag_ratio=0.1, run_time=2)
                for num, bar in zip(nums, bars)
            ]),
            ShowCreation(base, run_time=1)
        )
        self.wait(2)

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

        # Show a permutation with a long increasing subsequence
        bars.save_state()
        nums.save_state()
        permutation = [4, 2, 3, 8, 0, 7, 1, 6, 5]
        for i, (bar, num) in enumerate(zip(bars, nums)):
            bars[permutation[i]].generate_target()
            nums[permutation[i]].generate_target()
            bars[permutation[i]].target.match_x(bar)
            nums[permutation[i]].target.match_x(bars[permutation[i]].target)
        self.play(
            AnimationGroup(*[MoveToTarget(bar) for bar in bars]),
            AnimationGroup(*[MoveToTarget(num) for num in nums])
        )

        # Highlight the increasing subsequence, then the decreasing one
        bars_left_to_right = VGroup(*sorted(bars, key=lambda bar: bar.get_x()))
        nums_left_to_right = VGroup(*sorted(nums, key=lambda num: num.get_x()))
        base.add_updater(lambda m: self.bring_to_front(m))
        increasing_indices = [0, 1, 2, 4, 5, 7, 8]
        increasing_sequence = VGroup(*[
            bars_left_to_right[i]
            for i in increasing_indices
        ])
        increasing_markers = VGroup(*[
            marker_rect(bar, increasing_sequence_color, 0)
            for bar in increasing_sequence
        ])
        self.play(
            AnimationGroup(*[
                FadeIn(marker, run_time=0.3)
                for marker in increasing_markers
            ], lag_ratio=0.3)
        )
        self.wait(0.4)
        decreasing_indices = [5, 6]
        decreasing_sequence = VGroup(*[
            bars_left_to_right[i]
            for i in decreasing_indices
        ])
        decreasing_markers = VGroup(*[
            marker_rect(bar, decreasing_sequence_color, 1 if i in increasing_indices else 0)
            for i, bar in zip(decreasing_indices, decreasing_sequence)
        ])
        self.play(
            AnimationGroup(*[
                FadeIn(marker, run_time=0.7)
                for marker in decreasing_markers
            ], lag_ratio=0.3)
        )
        self.wait(1)
        self.play(FadeOut(increasing_markers), FadeOut(decreasing_markers))

        # Show a permutation with a long decreasing subsequence
        permutation = [7, 8, 5, 4, 6, 1, 3, 2, 0]
        for i, (bar, num) in enumerate(zip(bars_left_to_right, nums_left_to_right)):
            bars_left_to_right[permutation[i]].generate_target()
            nums_left_to_right[permutation[i]].generate_target()
            bars_left_to_right[permutation[i]].target.match_x(bar)
            nums_left_to_right[permutation[i]].target.match_x(bars_left_to_right[permutation[i]].target)
        self.play(
            AnimationGroup(*[MoveToTarget(bar) for bar in bars_left_to_right]),
            AnimationGroup(*[MoveToTarget(num) for num in nums_left_to_right])
        )

        # Highlight the decreasing subsequence, then the increasing one
        bars_left_to_right = VGroup(*sorted(bars, key=lambda bar: bar.get_x()))
        decreasing_indices = [1, 2, 3, 4, 7, 8]
        decreasing_sequence = VGroup(*[
            bars_left_to_right[i]
            for i in decreasing_indices
        ])
        decreasing_markers_dict = {
            i: marker_rect(bars_left_to_right[i], decreasing_sequence_color, 0)
            for i in decreasing_indices
        }
        decreasing_markers = VGroup(*decreasing_markers_dict.values())
        self.play(
            AnimationGroup(*[
                FadeIn(marker, run_time=0.3)
                for marker in decreasing_markers
            ], lag_ratio=0.3)
        )
        self.wait(0.4)
        increasing_indices = [5, 6, 7]
        increasing_sequence = VGroup(*[
            bars_left_to_right[i]
            for i in increasing_indices
        ])
        increasing_markers = VGroup(*[
            marker_rect(bar, increasing_sequence_color, 0)
            for bar in increasing_sequence
        ])
        shared_indices = [i for i in increasing_indices if i in decreasing_indices]
        self.play(
            AnimationGroup(*[
                FadeIn(marker, run_time=0.3)
                for marker in increasing_markers
            ], lag_ratio=0.3),
            AnimationGroup(*[
                decreasing_markers_dict[i].animate.shift(DOWN * marker_thickness)
                for i in shared_indices
            ])
        )
        self.wait(1)

        # Flash through many other permutations, highlighting their LIS and LDS
        self.remove(increasing_markers, decreasing_markers)
        slot_xs = sorted(bar.get_x() for bar in bars)

        def get_extreme_subsequence_slots(seq, increasing=True):
            n = len(seq)
            lengths = [1] * n
            prev = [-1] * n
            for i in range(n):
                for j in range(i):
                    better = (seq[j] < seq[i]) if increasing else (seq[j] > seq[i])
                    if better and lengths[j] + 1 > lengths[i]:
                        lengths[i] = lengths[j] + 1
                        prev[i] = j
            end = max(range(n), key=lambda i: lengths[i])
            slots = []
            while end != -1:
                slots.append(end)
                end = prev[end]
            return set(slots)

        n_flashes = 30
        prev_perm = None
        markers = VGroup()
        self.add(markers)
        camera_shift_iter = 5
        inequality = Tex(
            R"\text{LIS} \cdot \text{LDS} \ge N",
            font_size=80,
            tex_to_color_map={"LIS": increasing_sequence_color, "LDS": decreasing_sequence_color, "N": n_color}
        ).shift(RIGHT * 7 + UP * 1)

        value_font_size = 80
        value_row_y = inequality.get_bottom()[1] - 1
        lis_value = None
        lds_value = None

        def make_lis_value(val):
            mob = Integer(val, font_size=value_font_size).set_color(increasing_sequence_color)
            mob.match_x(inequality["LIS"])
            mob.set_y(value_row_y)
            return mob

        def make_lds_value(val):
            mob = Integer(val, font_size=value_font_size).set_color(decreasing_sequence_color)
            mob.match_x(inequality["LDS"])
            mob.set_y(value_row_y)
            return mob

        for i in range(n_flashes):
            perm = np.random.permutation(9).tolist()
            while perm == prev_perm:
                perm = np.random.permutation(9).tolist()
            prev_perm = perm

            for slot, bar_index in enumerate(perm):
                bars[bar_index].set_x(slot_xs[slot])
                nums[bar_index].set_x(slot_xs[slot])

            heights_in_order = [values[bar_index] for bar_index in perm]
            lis_slots = get_extreme_subsequence_slots(heights_in_order, increasing=True)
            lds_slots = get_extreme_subsequence_slots(heights_in_order, increasing=False)
            lis_val = len(lis_slots)
            lds_val = len(lds_slots)

            self.remove(markers)
            markers = VGroup()
            for slot, bar_index in enumerate(perm):
                bar = bars[bar_index]
                is_lis = slot in lis_slots
                is_lds = slot in lds_slots
                if is_lis:
                    markers.add(marker_rect(bar, increasing_sequence_color, 0))
                if is_lds:
                    markers.add(marker_rect(bar, decreasing_sequence_color, 1 if is_lis else 0))
            self.add(markers)

            if lis_value is not None:
                self.remove(lis_value)
                lis_value = make_lis_value(lis_val)
                self.add(lis_value)
            if lds_value is not None:
                self.remove(lds_value)
                lds_value = make_lds_value(lds_val)
                self.add(lds_value)

            if i == camera_shift_iter:
                self.set_camera_target_position(0, 0, 0, (3.35, 0.38, 0.00), 9.25)
                lis_value = make_lis_value(lis_val)
                self.play(FadeIn(inequality["LIS"]), FadeIn(lis_value))
            elif i == camera_shift_iter + 3:
                cdot_value = Tex(R"\cdot", font_size=value_font_size)
                cdot_value.match_x(inequality[R"\cdot"])
                cdot_value.set_y(value_row_y)
                lds_value = make_lds_value(lds_val)
                self.play(
                    FadeIn(inequality[R"\cdot"]),
                    FadeIn(cdot_value),
                    FadeIn(inequality["LDS"]),
                    FadeIn(lds_value)
                )
            elif i == camera_shift_iter + 8:
                geq_value = Tex(R"\ge", font_size=value_font_size)
                geq_value.match_x(inequality[-2])
                geq_value.set_y(value_row_y)
                n_value = Tex(str(n), font_size=value_font_size).set_color(n_color)
                n_value.match_x(inequality[-1])
                n_value.set_y(value_row_y)
                self.play(
                    FadeIn(inequality[-2:]),
                    FadeIn(geq_value),
                    FadeIn(n_value),
                    GrowFromEdge(brace, UP),
                    Write(label)
                )
            else:
                self.wait(1)

        # Switch to the main example for the rest of the scene
        self.clear()
        self.camera.frame.restore()
        self.add(chart, nums)
        bars.restore()
        nums.restore()
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
        increasing_sequence = VGroup(*[
            bars[i]
            for i in increasing_indices
        ])
        increasing_markers = VGroup(*[
            marker_rect(bar, increasing_sequence_color, 0)
            for bar in increasing_sequence
        ])
        self.play(
            AnimationGroup(*[
                FadeIn(marker)
                for marker in increasing_markers
            ], lag_ratio=0.3)
        )
        self.wait(1)
        lis_text = Tex(R"\text{LIS}: 2", font_size=110).set_color(increasing_sequence_color)
        lds_text = Tex(R"\text{LDS}: 3", font_size=110).set_color(decreasing_sequence_color)
        lds_text.next_to(lis_text, DOWN, buff=0.6).align_to(lis_text, LEFT)
        VGroup(lis_text, lds_text).set_y(0).to_edge(RIGHT, buff=1.5)
        base.suspend_updating()
        self.play(
            AnimationGroup(
                VGroup(chart, nums, arrow, increasing_markers).animate.to_edge(LEFT, buff=1.5),
                Write(lis_text), lag_ratio=0.6, run_time=1.5)
        )
        base.resume_updating()
        self.wait(1)
        decreasing_indices = [0, 1, 3]
        decreasing_sequence = VGroup(*[
            bars[i]
            for i in decreasing_indices
        ])
        decreasing_markers = VGroup(*[
            marker_rect(bar, decreasing_sequence_color, 1 if i in increasing_indices else 0)
            for i, bar in zip(decreasing_indices, decreasing_sequence)
        ])
        self.play(
            AnimationGroup(*[
                FadeIn(marker)
                for marker in decreasing_markers
            ], lag_ratio=0.3)
        )
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
        base.clear_updaters()
        chart.generate_target()
        chart.target.set_opacity(1).stretch(1.5, 0).center()
        nums.generate_target()
        nums.target.set_opacity(1)
        for num, bar in zip(nums.target, chart.target[0]):
            num.match_x(bar)
        pair.generate_target()
        pair.target.match_x(chart.target[0][3]).scale(1.3)

        increasing_markers.set_z_index(100)
        decreasing_markers.set_z_index(100)
        self.play(
            FadeOut(VGroup(arrow, lis_text, lds_text), run_time=1),
            MoveToTarget(chart, run_time=2),
            MoveToTarget(nums, run_time=2),
            MoveToTarget(pair, run_time=2),
            FadeOut(increasing_markers, shift=RIGHT * 0.08, run_time=0.6),
            FadeOut(decreasing_markers, shift=RIGHT * 0.08, run_time=0.6)
        )
        base.add_updater(lambda m: self.bring_to_front(m))
        self.wait(2)

        # Show that all the numbers are distinct
        if False:
            self.remove(pair)
            self.wait(1)
            circles = VGroup(*[Circle(radius=0.35, fill_opacity=0, stroke_width=3, stroke_color=YELLOW).move_to(num) for num in nums])
            self.play(AnimationGroup(*[ShowCreation(circle) for circle in circles], lag_ratio=0.1))

        # Add the (LIS, LDS) pair for each bar
        lis_lds_lengths = [(1, 1), (1, 2), (1, 3), (2, 3), (1, 4), (3, 1), (3, 2), (3, 3), (2, 4)]
        pairs = VGroup(*[
            Tex(F"({lis}, {lds})").match_height(pair).match_y(pair).match_x(bar)
            for (lis, lds), bar in zip(lis_lds_lengths, bars)
        ])
        pair_4 = pair
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
        self.remove(pair_4)
        self.add(pairs)
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
        increasing_sequence = VGroup(*[
            bars[i]
            for i in increasing_indices
        ])
        increasing_markers = VGroup(*[
            marker_rect(bar, increasing_sequence_color, 0)
            for bar in increasing_sequence
        ])
        self.play(
            AnimationGroup(*[
                FadeIn(marker)
                for marker in increasing_markers
            ], lag_ratio=0.3)
        )
        self.wait(1)
        decreasing_indices = [5, 6]
        decreasing_sequence = VGroup(*[
            bars[i]
            for i in decreasing_indices
        ])
        decreasing_markers = VGroup(*[
            marker_rect(bar, decreasing_sequence_color, 1 if i in increasing_indices else 0)
            for i, bar in zip(decreasing_indices, decreasing_sequence)
        ])
        self.play(
            AnimationGroup(*[
                FadeIn(marker)
                for marker in decreasing_markers
            ], lag_ratio=0.3)
        )
        self.wait(1)
        self.play(
            bars.animate.restore(), nums.animate.restore(), pairs.animate.restore(),
            FadeOut(arrow), FadeOut(increasing_markers), FadeOut(decreasing_markers), run_time=2
        )
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
        heights = [2, 6, 5, 3]
        heights = [h * 0.6 for h in heights]
        tail = VGroup(*[
            bar1.copy().stretch_to_fit_width(0.5).stretch_to_fit_height(height)
            for height in heights
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

        # Recompute marker thickness
        marker_thickness = 0.5 * min(
            b.get_height() for b in [tail[0], tail[1], tail[2], tail[3], bar1]
        )

        # Show the increasing subsequence of length x
        increasing_sequence = VGroup(tail[0], tail[3], bar1)
        increasing_markers = VGroup(*[
            marker_rect(bar, increasing_sequence_color, 0)
            for bar in increasing_sequence
        ])
        brace = Brace(increasing_sequence, UP).shift(UP * 0.1)
        label = brace.get_tex("x", font_size=60).set_color(increasing_sequence_color).shift(UP * 0.2)
        self.play(
            AnimationGroup(*[
                bar.animate.set_opacity(1)
                for bar in increasing_sequence
            ], lag_ratio=0.1),
            AnimationGroup(*[
                FadeIn(marker)
                for marker in increasing_markers
            ], lag_ratio=0.1),
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
        bar2_increasing_marker = marker_rect(bar2, increasing_sequence_color, 0)
        increasing_markers.add(bar2_increasing_marker)
        self.play(
            TransformFromCopy(brace, extended_brace),
            TransformMatchingShapes(label.copy(), part2),
            FadeIn(bar2_increasing_marker), run_time=2)
        self.wait(1)
        self.play(part2.animate.restore(), FadeIn(part1, shift=RIGHT * 0.5))

        # Save the example
        case1 = VGroup(
            tail, bar1, bar2, increasing_markers, base, pair, pair2,
            brace, label, extended_brace, extended_label, cdots
        ).copy()

        # Make the second bar shorter
        increasing_markers.set_z_index(100)
        self.play(
            FadeOut(VGroup(brace, label, extended_brace, extended_label)),
            FadeOut(increasing_markers[:-1]),
            FadeOut(increasing_markers[-1], shift=DOWN * 3),
            tail.animate.set_opacity(tail_opacity),
            bar2.animate.stretch_to_fit_height(0.6 * bar1.get_height()).align_to(bar2, DOWN)
        )
        self.wait(2)

        # Show the decreasing subsequence of length 7
        decreasing_sequence = VGroup(tail[1], tail[2], bar1)
        decreasing_markers = VGroup(*[
            marker_rect(bar, decreasing_sequence_color, 0)
            for bar in decreasing_sequence
        ])
        brace = Brace(decreasing_sequence, UP)
        label = brace.get_tex("y", font_size=60).set_color(decreasing_sequence_color)
        self.play(
            AnimationGroup(*[
                bar.animate.set_opacity(1)
                for bar in decreasing_sequence
            ], lag_ratio=0.1),
            AnimationGroup(*[
                FadeIn(marker)
                for marker in decreasing_markers
            ], lag_ratio=0.1),
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
        bar2_decreasing_marker = marker_rect(bar2, decreasing_sequence_color, 0)
        decreasing_markers.add(bar2_decreasing_marker)
        self.play(
            TransformFromCopy(brace, extended_brace),
            TransformMatchingShapes(label.copy(), part2),
            FadeIn(bar2_decreasing_marker), run_time=2)
        self.wait(1)
        self.play(part2.animate.restore(), FadeIn(part1, shift=RIGHT * 0.5))

        # Save the second example
        case2 = VGroup(
            tail, bar1, bar2, decreasing_markers, base, pair, pair2,
            brace, label, extended_brace, extended_label, cdots
        )

        # Show both examples side by side
        case1.clear_updaters()
        base.clear_updaters()
        case1[1:3].set_stroke(width=3, color=YELLOW, behind=True)
        case1[1:4].set_z_index(400)
        case2.generate_target()
        case2.target[1:3].set_stroke(width=3, color=YELLOW)
        case2.set_stroke(behind=True)
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
        # Bars have since been scaled down (coordinate-grid step), so
        # recompute the marker thickness to match their current size.
        marker_thickness = 0.5 * min(bar.get_height() for bar in bars)

        increasing_indices = [2, 3, 7]
        decreasing_indices = [0, 1, 3, 8]
        increasing_markers = VGroup(*[
            marker_rect(bars[i], increasing_sequence_color, 0)
            for i in increasing_indices
        ])
        self.play(
            GrowFromEdge(width_brace, UP),
            Write(width_label),
            AnimationGroup(*[
                FadeIn(marker)
                for marker in increasing_markers
            ], lag_ratio=0.1)
        )
        self.wait(1)

        height_brace = Brace(rect, LEFT, buff=0.5)
        height_label = height_brace.get_tex(R"\text{LDS}").set_color(decreasing_sequence_color)
        decreasing_markers = VGroup(*[
            marker_rect(bars[i], decreasing_sequence_color, 1 if i in increasing_indices else 0)
            for i in decreasing_indices
        ])
        self.play(
            GrowFromEdge(height_brace, RIGHT),
            Write(height_label),
            AnimationGroup(*[
                FadeIn(marker)
                for marker in decreasing_markers
            ], lag_ratio=0.1)
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
        inequality.scale(0.8).set_x(0).to_edge(UP, buff=0.6)
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
