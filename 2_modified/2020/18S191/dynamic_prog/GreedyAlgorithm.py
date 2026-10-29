# ==============================================================================
# Scene:      GreedyAlgorithm
# Source:     videos/_2020/18S191/dynamic_prog.py (lines 42-106)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GreedyAlgorithm.py GreedyAlgorithm -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - np.array(list(mobjects)) treated each Mobject as a sequence (shape (36, 0)); an object array is filled by hand
# ==============================================================================

from manim_imports_ext import *

def get_value_grid(n_rows=6, n_cols=6):
    random.seed(1)
    boxes = VGroup(*[Square() for x in range(n_rows * n_cols)])
    # CHANGE: np.array(list(mobjects)) treated each Mobject as a sequence (shape (36, 0)); an object array is filled by hand
    array = np.empty(len(boxes), dtype=object)
    for _i, _box in enumerate(boxes):
        array[_i] = _box
    array = array.reshape((n_rows, n_cols))
    boxes.array = array
    boxes.arrange_in_grid(n_rows, n_cols, buff=0)
    boxes.set_height(5)
    boxes.to_edge(DOWN)
    boxes.shift(UP)
    boxes.set_stroke(BLUE_D, 2)
    for box in boxes:
        value = DecimalNumber(
            np.round(random.random(), 1),
            num_decimal_places=1
        )
        box.set_fill(WHITE, opacity=0.8 * value.get_value())
        box.value = value
        value.match_height(box)
        value.scale(0.3)
        value.move_to(box)
        box.add(value)
    boxes.array[5, 1].value.set_value(0.4)  # Tweaking for examples
    return boxes


def get_box_highlight(box, color=PINK, stroke_width=8, opacity=0.25):
    highlight = SurroundingRectangle(box, buff=0)
    highlight.set_fill(color, opacity)
    highlight.set_stroke(color, stroke_width)
    return highlight


class GreedyAlgorithm(Scene):
    def construct(self):
        n_rows, n_cols = 6, 6
        boxes = get_value_grid(n_rows, n_cols)
        self.add(boxes)

        last_sum_term = boxes[0].value.copy()
        last_sum_term.to_edge(UP)
        last_sum_term.set_x(-5)
        sum_terms = VGroup()
        to_fade = VGroup()

        (i, j) = (0, 3)
        while i < n_rows:
            box = boxes.array[i, j]
            value = box.value
            box_highlight = get_box_highlight(box)
            sum_term = VGroup(
                OldTex("+"),
                value.copy()
            )
            if i == 0:
                sum_term[0].set_opacity(0)
            sum_term.arrange(RIGHT, buff=0.2)
            sum_term.next_to(last_sum_term, RIGHT, buff=0.2)
            sum_terms.add(sum_term)
            last_sum_term = sum_term

            self.play(
                FadeIn(box_highlight),
                FadeIn(sum_term),
                *map(FadeOut, to_fade)
            )

            i += 1
            # Find new j
            if i < n_rows:
                next_boxes = VGroup()
                for nj in range(j - 1, j + 2):
                    next_boxes.add(boxes.array[i, clip(nj, 0, n_cols - 1)])

                next_highlights = VGroup()
                for nb in next_boxes:
                    next_highlights.add(get_box_highlight(nb, stroke_width=4))

                self.play(FadeIn(next_highlights))

                min_box_index = np.argmin([b.value.get_value() for b in next_boxes])
                j = j - 1 + min_box_index
                j = clip(j, 0, n_cols - 1)  # Am I doing this right?
                to_fade = next_highlights

        final_sum = VGroup(
            OldTex("="),
            DecimalNumber(
                sum([np.round(st[1].get_value(), 1) for st in sum_terms]),
                height=sum_terms.get_height(),
                num_decimal_places=1,
            ).set_color(YELLOW)
        )
        final_sum.arrange(RIGHT, buff=0.2)
        final_sum.next_to(sum_terms, RIGHT, buff=0.2)

        self.play(Write(final_sum))
        self.wait()
