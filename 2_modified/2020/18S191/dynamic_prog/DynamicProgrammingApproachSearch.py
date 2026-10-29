# ==============================================================================
# Scene:      DynamicProgrammingApproachSearch
# Source:     videos/_2020/18S191/dynamic_prog.py (lines 182-252)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DynamicProgrammingApproachSearch.py DynamicProgrammingApproachSearch -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - np.array(list(mobjects)) treated each Mobject as a sequence (shape (36, 0)); an object array is filled by hand
#   - the box has only one submobject (the value); index 1 from the old version does not exist
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


class DynamicProgrammingApproachSearch(Scene):
    def construct(self):
        n_rows = 6
        n_cols = 6
        boxes = get_value_grid(n_rows, n_cols)
        boxes.to_corner(DL)
        boxes.shift(UP)
        self.add(boxes)

        new_boxes = get_value_grid(n_rows, n_cols)
        new_boxes.to_corner(DR)
        new_boxes.shift(UP)
        for box in new_boxes:
            box.set_fill(opacity=0)
            box.value.set_fill(opacity=0)
        self.add(new_boxes)

        left_title = OldTexText("Energy")
        right_title = OldTexText("Minimal energy to bottom")
        left_title.next_to(boxes, UP)
        right_title.next_to(new_boxes, UP)

        self.add(left_title, right_title)

        op_factor = 0.5

        movers = VGroup()
        for j in range(n_cols):
            box = boxes.array[n_rows - 1, j]
            new_box = new_boxes.array[n_rows - 1, j]
            new_box.generate_target()
            new_box.target.match_style(box)
            new_box.target.set_fill(TEAL, opacity=op_factor * new_box.value.get_value())
            # CHANGE: the box has only one submobject (the value); index 1 of the old version does not exist
            new_box.target[0].set_fill(WHITE, 1)
            movers.add(new_box)

        self.play(LaggedStartMap(MoveToTarget, movers))
        self.wait()

        for i in range(n_rows - 2, -1, -1):
            for j in range(n_cols):
                box = boxes.array[i, j]
                new_box = new_boxes.array[i, j]
                box_highlight = get_box_highlight(box)
                new_box_highlight = get_box_highlight(new_box)
                boxes_below = [
                    new_boxes.array[i + 1, j]
                    for j in range(j - 1, j + 2)
                    if 0 <= j < n_cols
                ]
                index = np.argmin([bb.value.get_value() for bb in boxes_below])
                low_box = boxes_below[index]
                low_box_highlight = get_box_highlight(low_box, stroke_width=3)
                low_box_highlight.fade(0.5)

                new_box.value.set_value(new_box.value.get_value() + low_box.value.get_value())
                new_box.generate_target()
                new_box.target.set_fill(TEAL, opacity=op_factor * new_box.value.get_value())
                new_box.target[0].set_fill(WHITE, 1)

                self.play(
                    FadeIn(box_highlight),
                    FadeIn(new_box_highlight),
                    FadeIn(low_box_highlight),
                    MoveToTarget(new_box),
                )
                self.play(
                    FadeOut(box_highlight),
                    FadeOut(new_box_highlight),
                    FadeOut(low_box_highlight),
                )
