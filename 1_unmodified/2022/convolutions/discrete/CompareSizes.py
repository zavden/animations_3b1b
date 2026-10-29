# ==============================================================================
# Scene:      CompareSizes
# Source:     videos/_2022/convolutions/discrete.py (lines 1206-1297)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareSizes.py CompareSizes -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def get_aligned_pairs(group1, group2, n):
    return VGroup(*(
        VGroup(m1, m2)
        for m1 in group1
        for m2 in group2
        if m1.index + m2.index == n
    ))


def get_row_shift(top_row, low_row, n):
    min_index = low_row[0].index
    max_index = top_row[-1].index
    max_sum = min_index + max_index
    if n <= max_sum:
        x_shift = top_row[n - 2 * min_index].get_x() - low_row[0].get_x()
    else:
        x_shift = top_row[-1].get_x() - low_row[n - max_sum].get_x()
    return low_row.animate.shift(x_shift * RIGHT)


class CompareSizes(InteractiveScene):
    def construct(self):
        # Show them all!
        int_arr1 = [3, 1, 4, 1, 5, 9]
        int_arr2 = [5, 7, 7]
        conv_arr = np.convolve(int_arr1, int_arr2)

        arrays = VGroup()
        for arr in (int_arr1, int_arr2, conv_arr):
            squares = Square().get_grid(1, len(arr), buff=0)
            squares.set_height(0.7)
            squares.set_stroke(WHITE, 1)
            squares.set_fill(GREY_E, 1)
            for square, elem in zip(squares, arr):
                int_mob = Integer(elem).move_to(square)
                square.add(int_mob)
            arrays.add(squares)

        top_arr, low_arr, conv_arr = arrays

        arrays.arrange(DOWN, buff=1.0)
        arrays[:2].shift(UP)
        VGroup(*(square[0] for square in arrays[2])).set_opacity(0)

        self.add(*arrays)

        # Length labels
        braces = VGroup(*(Brace(arr, vect, buff=SMALL_BUFF) for arr, vect in zip(arrays, [UP, DOWN, DOWN])))
        brace_labels = VGroup(*(brace.get_tex(tex, buff=SMALL_BUFF) for brace, tex in zip(braces, ["n", "m", "n + m - 1"])))
        braces[1].add_updater(lambda m: m.match_x(arrays[1]))
        brace_labels[1].add_updater(lambda m: m.match_x(arrays[1]))

        self.add(braces, brace_labels)

        # Flip
        self.remove(low_arr)
        fake_arr = low_arr.deepcopy()
        fake_arr.generate_target(use_deepcopy=True)
        fake_arr.target.rotate(PI)
        for square in fake_arr.target:
            square[0].rotate(PI)
        self.play(MoveToTarget(fake_arr, path_arc=PI, lag_ratio=0.01))
        self.remove(fake_arr)
        low_arr.rotate(PI)
        for square in low_arr:
            square[0].rotate(PI)

        # March!
        for arr in (top_arr, low_arr):
            for index, square in enumerate(arr):
                square.index = index

        for n in range(len(conv_arr)):
            self.play(
                get_row_shift(top_arr, low_arr, n),
                run_time=0.5
            )
            pairs = get_aligned_pairs(top_arr, low_arr, n)
            rects = VGroup(*(
                SurroundingRectangle(pair, buff=-0.05)
                for pair in pairs
            ))
            self.add(rects)
            conv_arr[n].set_opacity(1)
            self.play(ShowIncreasingSubsets(rects, int_func=np.ceil), run_time=0.5)
            self.wait(0.25)
            self.remove(rects)

        # Truncate
        brace = braces[2]
        brace_label = brace_labels[2]

        small_brace = Brace(conv_arr[2:-2], DOWN, buff=SMALL_BUFF)
        small_brace_label = small_brace.get_text("Only consider full overlaps")

        mid_brace = Brace(conv_arr[1:-1], DOWN, buff=SMALL_BUFF)
        mid_brace_label = mid_brace.get_text("Match biggest input size")

        self.play(
            Transform(brace, small_brace),
            FadeTransform(brace_label, small_brace_label),
            conv_arr[:2].animate.set_opacity(0.25),
            conv_arr[-2:].animate.set_opacity(0.25),
        )
        self.wait()
        self.play(
            Transform(brace, mid_brace),
            FadeTransform(small_brace_label, mid_brace_label),
            conv_arr[1].animate.set_opacity(1),
            conv_arr[-2].animate.set_opacity(1),
        )
        self.wait()
