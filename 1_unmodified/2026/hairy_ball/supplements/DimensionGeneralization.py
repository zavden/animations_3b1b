# ==============================================================================
# Scene:      DimensionGeneralization
# Source:     videos/_2026/hairy_ball/supplements.py (lines 741-830)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DimensionGeneralization.py DimensionGeneralization -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DimensionGeneralization(InteractiveScene):
    def construct(self):
        # Set up grid
        row_labels = VGroup(
            Text("Dimension"),
            Text("Can you\ncomb a ball?"),
        )
        n_cols = 15
        cells = Square().get_grid(2, 1, buff=0).get_grid(1, n_cols, buff=0)
        cells.set_height(2.6)
        cells[0].set_width(row_labels.get_width() + MED_LARGE_BUFF, stretch=True, about_edge=RIGHT)
        cells.to_corner(UL, buff=LARGE_BUFF)
        for label, cell in zip(row_labels, cells[0]):
            label.move_to(cell)

        dim_labels = VGroup()
        mark_labels = VGroup()
        for n, cell in zip(it.count(2), cells[1:]):
            dim_label = Integer(n)
            mark_label = Checkmark().set_color(GREEN) if n % 2 == 0 else Exmark().set_color(RED)
            mark_label.set_height(0.5 * cell[1].get_height())
            dim_label.move_to(cell[0])
            mark_label.move_to(cell[1])

            dim_labels.add(dim_label)
            mark_labels.add(mark_label)

        self.add(cells[:3], row_labels, dim_labels[:2], mark_labels[1])
        self.play(
            LaggedStartMap(FadeIn, cells[3:], lag_ratio=0.5),
            LaggedStartMap(FadeIn, dim_labels[2:], lag_ratio=0.5),
            run_time=3
        )
        self.wait()

        # Show two
        self.play(Write(mark_labels[0]))
        self.wait()

        # General dimensions
        frame = self.frame
        for i in [0, 1]:
            self.play(
                LaggedStart(
                    (TransformFromCopy(mark_labels[i], mark_label, path_arc=30 * DEG)
                    for mark_label in mark_labels[i + 2::2]),
                    lag_ratio=0.25,
                ),
                frame.animate.reorient(0, 0, 0, (4.15, -2.53, 0.0), 12.34),
                run_time=3
            )
            self.wait()

        # Show determinants
        last_det = VGroup()
        highlight_rect = SurroundingRectangle(cells[1], buff=0)
        highlight_rect.set_opacity(0).shift(LEFT)
        for dim in range(2, 12):
            det_tex = self.get_det_neg_tex(dim)
            det_tex.scale(1.5)
            det_tex.move_to(5 * DOWN).to_edge(LEFT, LARGE_BUFF)
            rect = SurroundingRectangle(cells[dim - 1], buff=0)
            rect.set_stroke(YELLOW, 5)

            self.play(
                Transform(highlight_rect, rect),
                FadeIn(det_tex),
                FadeOut(last_det),
            )
            self.wait()
            last_det = det_tex

    def get_det_neg_tex(self, dim):
        mat = IntegerMatrix(-1 * np.identity(dim))
        det_text = Text("det")
        mat.set_max_height(5 * det_text.get_height())
        lp, rp = parens = Tex(R"()")
        parens.stretch(2, 1)
        parens.match_height(mat)
        lp.next_to(mat, LEFT, buff=0.1)
        rp.next_to(mat, RIGHT, buff=0.1)
        det_text.next_to(parens, LEFT, SMALL_BUFF)

        sign = ["+", "-"][dim % 2]
        rhs = Tex(Rf"= {sign}1")
        rhs.next_to(rp, RIGHT, SMALL_BUFF)
        rhs[1:].set_color([GREEN, RED][dim % 2])

        result = VGroup(det_text, lp, mat, rp, rhs)
        return result
