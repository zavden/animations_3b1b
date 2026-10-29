# ==============================================================================
# Scene:      RecrusiveExhaustiveSearch
# Source:     videos/_2020/18S191/dynamic_prog.py (lines 109-179)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RecrusiveExhaustiveSearch.py RecrusiveExhaustiveSearch -w -m --fps 15
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


class RecrusiveExhaustiveSearch(Scene):
    def construct(self):
        n_rows = 6
        n_cols = 6
        boxes = get_value_grid(n_rows, n_cols)
        self.add(boxes)

        seam = [
            (i, 3)
            for i in range(n_rows)
        ]

        def get_seam_sum(seam):
            terms = VGroup(*[boxes.array[i, j].value.copy() for (i, j) in seam])
            row = VGroup()
            for term in terms[:-1]:
                row.add(term)
                row.add(OldTex("+"))
            row.add(terms[-1])
            row.add(OldTex("="))
            sum_term = DecimalNumber(sum([t.get_value() for t in terms]), num_decimal_places=1)
            sum_term.match_height(terms[0])
            sum_term.set_color(YELLOW)
            row.add(sum_term)
            row.arrange(RIGHT, buff=0.15)
            row.to_edge(UP)
            return row

        def get_highlighted_seam(seam):
            return VGroup(*[
                get_box_highlight(boxes.array[i, j])
                for (i, j) in seam
            ])

        def get_all_seams(seam_starts, n_rows=n_rows, n_cols=n_cols):
            if seam_starts[0][-1][0] == n_rows - 1:
                return seam_starts
            new_seams = []
            for seam in seam_starts:
                i, j = seam[-1]
                # Adjacent j values below (i, j)
                js = []
                if j > 0:
                    js.append(j - 1)
                js.append(j)
                if j < n_cols - 1:
                    js.append(j + 1)

                for j_prime in js:
                    new_seams.append([*seam, (i + 1, j_prime)])
            return get_all_seams(new_seams, n_rows, n_cols)

        all_seams = get_all_seams([[(0, 3)]])

        curr_min_energy = np.inf
        curr_best_seam = VGroup()
        for seam in all_seams:
            ss = get_seam_sum(seam)
            hs = get_highlighted_seam(seam)

            energy = ss[-1].get_value()
            if energy < curr_min_energy:
                curr_min_energy = energy
                curr_best_seam = VGroup(ss, hs)

            self.add(ss, hs)
            self.wait(0.05)
            self.remove(ss, hs)

        self.add(curr_best_seam)
        self.wait()
