# ==============================================================================
# Scene:      ContrastConvolutionToMultiplication
# Source:     videos/_2022/convolutions/discrete.py (lines 1738-1859)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContrastConvolutionToMultiplication.py ContrastConvolutionToMultiplication -w -m --fps 15
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


class ContrastConvolutionToMultiplication(InteractiveScene):
    def construct(self):
        # Set up divide
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.set_stroke(GREY, 2)

        kw = dict(font_size=60)
        conv_name = Text("Convolution", **kw)
        mult_name = Text("Multiplication", **kw)
        conv_name.set_x(-FRAME_WIDTH / 4).to_edge(UP)
        mult_name.set_x(FRAME_WIDTH / 4).to_edge(UP)

        self.add(v_line)
        self.add(conv_name)
        self.add(mult_name)

        # Set up arrays
        arr1 = np.arange(1, 6)
        arr2 = np.arange(6, 11)
        conv = np.convolve(arr1, arr2)
        prod = arr1 * arr2
        quart = FRAME_WIDTH / 4

        left_arrays, right_arrays = (
            VGroup(*(
                self.get_array_mobject(arr, color)
                for arr, color in [(arr1, BLUE), (arr2, YELLOW)]
            )).arrange(DOWN, buff=1.0).move_to(vect * quart + UP)
            for vect in [LEFT, RIGHT]
        )

        conv_array = self.get_array_mobject(conv, color=TEAL)
        prod_array = self.get_array_mobject(prod, color=TEAL)
        conv_array.next_to(left_arrays, DOWN, buff=1.5)
        prod_array.next_to(right_arrays, DOWN, buff=1.5)

        self.add(left_arrays)
        self.add(right_arrays)

        # Show convolution
        top_arr = left_arrays[0]
        low_arr = left_arrays[1]
        low_arr.generate_target()
        low_arr.target.rotate(PI, about_point=low_arr.elements[0].get_center())
        for elem in low_arr.target[1:-1]:
            elem.rotate(PI)
        low_arr.target[2:-2:2].set_y(low_arr[1].get_y(DOWN))
        self.play(
            FadeIn(VGroup(conv_array[0], conv_array[-1])),
            MoveToTarget(low_arr, path_arc=PI),
        )
        for n, elem in enumerate(conv_array.elements):
            pairs = get_aligned_pairs(top_arr.elements, low_arr.elements, n)

            self.play(
                get_row_shift(top_arr.elements, low_arr.elements, n),
                MaintainPositionRelativeTo(low_arr[::2], low_arr.elements),
                run_time=0.25
            )

            lines = VGroup(*(Line(m1, m2, buff=0.1) for m1, m2 in pairs))
            lines.set_stroke(TEAL, 1)

            self.add(lines, elem)

            tally = 0
            for (m1, m2), line in zip(pairs, lines):
                tally += m1.get_value() * m2.get_value()
                lines.set_stroke(width=1)
                line.set_stroke(width=4)
                elem.set_value(tally)
                self.wait(0.25)
            self.wait(0.25)
            self.remove(lines)
            self.add(conv_array[2 * n + 2])
        self.wait()

        # Show multiplication
        low_arr = right_arrays[0]
        top_arr = right_arrays[1]
        lines = VGroup(*(
            Line(e1, e2, buff=0.1)
            for e1, e2 in zip(top_arr.elements, low_arr.elements)
        ))
        lines.set_stroke(TEAL, 1)

        self.play(
            FadeIn(VGroup(prod_array[0], prod_array[-1])),
            FadeIn(lines),
        )
        for n, elem in enumerate(prod_array.elements):
            lines.set_stroke(width=1)
            lines[n].set_stroke(width=4)
            self.add(elem)
            self.add(prod_array[2 * n + 2])
            self.wait(0.5)
        self.play(FadeOut(lines))

    def get_array_mobject(self, array, color=WHITE, font_size=48):
        kw = dict(font_size=font_size)
        result = VGroup(OldTex("[", **kw))
        commas = VGroup()
        elements = VGroup()
        for index, elem in enumerate(array):
            int_mob = Integer(elem, **kw)
            int_mob.index = index
            elements.add(int_mob)
            result.add(int_mob)
            comma = OldTex(",", **kw)
            commas.add(comma)
            result.add(comma)
        result.remove(commas[-1])
        commas.remove(commas[-1])
        result.add(OldTex("]", **kw))
        result.arrange(RIGHT, buff=0.1)
        commas.set_y(result[1].get_y(DOWN))

        elements.set_color(color)
        result.elements = elements
        result.commas = commas

        return result
