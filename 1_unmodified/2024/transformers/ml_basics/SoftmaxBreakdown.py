# ==============================================================================
# Scene:      SoftmaxBreakdown
# Source:     videos/_2024/transformers/ml_basics.py (lines 1814-2365)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl SoftmaxBreakdown.py SoftmaxBreakdown -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING
import warnings


# ----- From _2024/transformers/helpers.py -----

if TYPE_CHECKING:
    from typing import Optional
    from manimlib.typing import Vect3, ManimColor


def softmax(logits, temperature=1.0):
    logits = np.array(logits)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')  # Ignore all warnings within this block
        logits = logits - np.max(logits)  # For numerical stability
        exps = np.exp(np.divide(logits, temperature, where=temperature != 0))
    
    if np.isinf(exps).any() or np.isnan(exps).any() or temperature == 0:
        result = np.zeros_like(logits)
        result[np.argmax(logits)] = 1
        return result
    return exps / np.sum(exps)


def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


def show_matrix_vector_product(scene, matrix, vector, buff=0.25, x_max=999, fix_in_frame=False):
    # Show product
    eq = Tex("=")
    eq.set_width(0.5 * vector.get_width())
    shape = (matrix.shape[0], 1)
    rhs = NumericEmbedding(
        values=x_max * np.ones(shape),
        value_range=(-x_max, x_max),
        decimal_config=dict(include_sign=True, edge_to_fix=ORIGIN),
        ellipses_row=matrix.ellipses_row,
    )
    rhs.scale(vector.elements[0].get_height() / rhs.elements[0].get_height())
    eq.next_to(vector, RIGHT, buff=buff)
    rhs.next_to(eq, RIGHT, buff=buff)
    if fix_in_frame:
        eq.fix_in_frame()
        rhs.fix_in_frame()

    scene.play(FadeIn(eq), FadeIn(rhs.get_brackets()))

    last_rects = VGroup()
    n_rows = len(matrix.rows)
    for n, row, entry in zip(it.count(), matrix.get_rows(), rhs[:-2]):
        if matrix.ellipses_row is not None and n == (matrix.ellipses_row % n_rows):
            scene.add(entry)
        else:
            last_rects = matrix_row_vector_product(
                scene, row, vector, entry, last_rects,
                fix_in_frame=fix_in_frame
            )
    scene.play(FadeOut(last_rects))

    return eq, rhs


def matrix_row_vector_product(scene, row, vector, entry, to_fade, fix_in_frame=False):
    def get_rect(elem):
        return SurroundingRectangle(elem, buff=0.1, is_fixed_in_frame=fix_in_frame).set_stroke(YELLOW, 2)

    row_rects = VGroup(*map(get_rect, row))
    vect_rects = VGroup(*map(get_rect, vector[:-2]))
    partial_values = [0]
    for e1, e2 in zip(row, vector[:-2]):
        if not isinstance(e1, DecimalNumber) and isinstance(e2, DecimalNumber):
            increment = 0
        else:
            val1 = round(e1.get_value(), e1.num_decimal_places)
            val2 = round(e2.get_value(), e2.num_decimal_places)
            increment = val1 * val2
        partial_values.append(partial_values[-1] + increment)
    n_values = len(partial_values)

    scene.play(
        ShowIncreasingSubsets(row_rects),
        ShowIncreasingSubsets(vect_rects),
        UpdateFromAlphaFunc(entry, lambda m, a: m.set_value(
            partial_values[min(int(np.round(a * n_values)), n_values - 1)]
        )),
        FadeOut(to_fade),
        rate_func=linear,
    )

    return VGroup(row_rects, vect_rects)


class WeightMatrix(DecimalMatrix):
    def __init__(
        self,
        values: Optional[np.ndarray] = None,
        shape: tuple[int, int] = (6, 8),
        value_range: tuple[float, float] = (-9.9, 9.9),
        ellipses_row: Optional[int] = -2,
        ellipses_col: Optional[int] = -2,
        num_decimal_places: int = 1,
        bracket_h_buff: float = 0.1,
        decimal_config=dict(include_sign=True),
        low_positive_color: ManimColor = BLUE_E,
        high_positive_color: ManimColor = BLUE_B,
        low_negative_color: ManimColor = RED_E,
        high_negative_color: ManimColor = RED_B,
    ):
        if values is not None:
            shape = values.shape
        self.shape = shape
        self.value_range = value_range
        self.low_positive_color = low_positive_color
        self.high_positive_color = high_positive_color
        self.low_negative_color = low_negative_color
        self.high_negative_color = high_negative_color
        self.ellipses_row = ellipses_row
        self.ellipses_col = ellipses_col

        if values is None:
            values = np.random.uniform(*self.value_range, size=shape)

        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
        )
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            entry.set_fill(color=value_to_color(
                entry.get_value(),
                self.low_positive_color,
                self.high_positive_color,
                self.low_negative_color,
                self.high_negative_color,
                0, max(self.value_range),
            ))
        return self


class NumericEmbedding(WeightMatrix):
    def __init__(
        self,
        values: Optional[np.ndarray] = None,
        shape: Optional[Tuple[int, int]] = None,
        length: int = 7,
        num_decimal_places: int = 1,
        ellipses_row: int = -2,
        ellipses_col: int = -2,
        value_range: tuple[float, float] = (-9.9, 9.9),
        bracket_h_buff: float = 0.1,
        decimal_config=dict(include_sign=True),
        dark_color: ManimColor = GREY_C,
        light_color: ManimColor = WHITE,
        **kwargs,
    ):
        if values is not None:
            if len(values.shape) == 1:
                values = values.reshape((values.shape[0], 1))
            shape = values.shape
        if shape is None:
            shape = (length, 1)
        super().__init__(
            values,
            shape=shape,
            value_range=value_range,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            low_positive_color=dark_color,
            high_positive_color=light_color,
            low_negative_color=dark_color,
            high_negative_color=light_color,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
            **kwargs,
        )

        # No sign on zeros
        for entry in self.get_entries():
            if entry.get_value() == 0:
                entry[0].set_opacity(0)



# ----- From _2024/transformers/ml_basics.py -----

class SoftmaxBreakdown(InteractiveScene):
    def construct(self):
        # Show example probability distribution
        word_strs = ['Dumbledore', 'Flitwick', 'Mcgonagall', 'Quirrell', 'Snape', 'Sprout', 'Trelawney']
        words = VGroup(*(Text(word_str, font_size=30) for word_str in word_strs))
        values = np.array([-0.8, -5.0, 0.5, 1.5, 3.4, -2.3, 2.5])
        prob_values = softmax(values)
        chart = BarChart(prob_values, width=10)
        chart.bars.set_stroke(width=1)

        probs = VGroup(*(DecimalNumber(pv) for pv in prob_values))
        probs.arrange(DOWN, buff=0.25)
        probs.generate_target()
        for prob, bar in zip(probs.target, chart.bars):
            prob.scale(0.5)
            prob.next_to(bar, UP)

        for word, bar in zip(words, chart.bars):
            word.scale(0.75)
            height = word.get_height()
            word.move_to(bar.get_bottom(), LEFT)
            word.rotate(-45 * DEGREES, about_point=bar.get_bottom())
            word.shift(height * DOWN)

        chart.save_state()
        for bar in chart.bars:
            bar.stretch(0, 1, about_edge=DOWN)
        chart.set_opacity(0)

        seq_title = Text("Sequence of numbers", font_size=60)
        seq_title.next_to(probs, LEFT, buff=0.75)
        seq_title.set_color(YELLOW)
        prob_title = Text("Probability distribution", font_size=60)
        prob_title.set_color(chart.bars[3].get_color())
        prob_title.center().to_edge(UP)

        self.play(
            LaggedStartMap(FadeIn, probs, shift=0.25 * DOWN, lag_ratio=0.3),
            FadeIn(seq_title),
            run_time=1
        )
        self.wait()
        self.play(
            Restore(chart, lag_ratio=0.1),
            MoveToTarget(probs),
            FadeTransform(seq_title, prob_title),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, words),
        )
        self.wait()

        # Show constraint between 0 and 1
        index = 3
        bar = chart.bars[index]
        bar.save_state()
        prob = probs[index]
        prob.bar = bar
        max_height = chart.y_axis.get_y(UP) - chart.x_axis.get_y()
        prob.f_always.set_value(lambda: prob.bar.get_height() / max_height)
        prob.always.match_height(probs[1])
        prob.always.next_to(prob.bar, UP)

        one_line = DashedLine(*chart.x_axis.get_start_and_end())
        one_line.set_stroke(RED, 2)
        one_line.align_to(chart.y_axis, UP)

        low_line = one_line.copy()
        low_line.set_stroke(PINK, 5)
        low_line.match_y(chart.x_axis)

        self.play(FadeIn(low_line), FadeIn(one_line), FadeOut(prob_title))
        self.play(low_line.animate.match_y(one_line))
        self.play(FadeOut(low_line))
        self.wait()

        self.play(
            FadeIn(one_line, time_span=(0, 1)),
            bar.animate.set_height(max_height, about_edge=DOWN, stretch=True),
            run_time=2,
        )
        self.play(
            bar.animate.set_height(1e-4, about_edge=DOWN, stretch=True),
            run_time=2,
        )
        self.play(Restore(bar))
        self.wait()
        prob.clear_updaters()

        # Show sum
        prob_copies = probs.copy()
        prob_copies.scale(1.5)
        prob_copies.arrange(RIGHT, buff=1.0)
        prob_copies.to_edge(UP)
        prob_copies.shift(LEFT)
        plusses = VGroup(*(
            Tex("+").move_to(VGroup(p1, p2))
            for p1, p2 in zip(prob_copies, prob_copies[1:])
        ))
        equals = Tex("=").next_to(prob_copies, RIGHT)
        rhs = DecimalNumber(1.00)
        rhs.next_to(equals, RIGHT)

        self.play(
            TransformFromCopy(probs, prob_copies),
            Write(plusses),
            Write(equals),
            FadeOut(one_line),
        )
        self.play(
            LaggedStart(*(
                FadeTransform(pc.copy(), rhs)
                for pc in prob_copies
            ), lag_ratio=0.07)
        )
        self.wait()

        sum_group = VGroup(*prob_copies, *plusses, equals, rhs)
        chart_group = VGroup(chart, probs, words)

        # Show example matrix vector output
        n = len(words)
        vector = NumericEmbedding(length=n, ellipses_row=None)
        in_values = np.array([e.get_value() for e in vector.elements])
        rows = []
        for value in values:
            row = np.random.uniform(-1, 1, len(in_values))
            row *= value / np.dot(row, in_values)
            rows.append(row)
        matrix_values = np.array(rows)

        matrix = WeightMatrix(
            values=matrix_values,
            ellipses_row=None,
            ellipses_col=None,
            num_decimal_places=2,
        )
        for mob in matrix, vector:
            mob.set_height(4)
        vector.to_edge(UP).set_x(2.5)
        matrix.next_to(vector, LEFT)

        self.play(LaggedStart(
            chart_group.animate.scale(0.35).to_corner(DL),
            FadeOut(sum_group, UP),
            FadeIn(matrix, UP),
            FadeIn(vector, UP),
        ))
        eq, rhs = show_matrix_vector_product(self, matrix, vector, x_max=9)
        self.wait()

        # Comment on output
        rhs_rect = SurroundingRectangle(rhs)
        rhs_words = Text("Not at all a\nprobability distribution!")
        rhs_words.next_to(rhs_rect, DOWN)

        neg_rects = VGroup(*(
            SurroundingRectangle(entry)
            for entry in rhs.get_entries()
            if entry.get_value() < 0
        ))
        gt1_rects = VGroup(*(
            SurroundingRectangle(entry)
            for entry in rhs.get_entries()
            if entry.get_value() > 1
        ))
        VGroup(rhs_rect, neg_rects).set_stroke(RED, 4)
        gt1_rects.set_stroke(BLUE, 4)

        for rect in (*neg_rects, *gt1_rects):
            neg = rect in neg_rects
            rect.word = Text("Negative" if neg else "> 1", font_size=36)
            rect.word.match_color(rect)
            rect.word.next_to(rhs, RIGHT)
            rect.word.match_y(rect)
        neg_words = VGroup(*(r.word for r in neg_rects))
        gt1_words = VGroup(*(r.word for r in gt1_rects))

        sum_arrow = Vector(DOWN).next_to(rhs, DOWN)
        sum_sym = Tex(R"\sum", font_size=36).next_to(sum_arrow, LEFT)
        sum_num = DecimalNumber(sum(e.get_value() for e in rhs.get_entries()))
        sum_num.next_to(sum_arrow, DOWN)

        self.play(
            ShowCreation(rhs_rect),
            FadeIn(rhs_words),
        )
        self.wait()
        self.play(
            ReplacementTransform(VGroup(rhs_rect), neg_rects),
            LaggedStart(*(FadeIn(rect.word, 0.5 * RIGHT) for rect in neg_rects)),
        )
        self.wait()
        self.play(
            ReplacementTransform(neg_rects, gt1_rects),
            FadeTransformPieces(neg_words, gt1_words),
        )
        self.wait()
        self.play(
            LaggedStart(
                FadeOut(rhs_words),
                FadeOut(gt1_rects),
                FadeOut(gt1_words),
            ),
            GrowArrow(sum_arrow),
            FadeIn(sum_num, DOWN),
            FadeIn(sum_sym),
        )
        self.wait()
        self.play(*map(FadeOut, [sum_arrow, sum_sym, sum_num]))

        # Preview softmax application
        rhs.generate_target()
        rhs.target.to_edge(LEFT, buff=1.5)
        rhs.target.set_y(0)

        softmax_box = Rectangle(width=5, height=6.5)
        softmax_box.set_stroke(BLUE, 2)
        softmax_box.set_fill(BLUE_E, 0.5)
        in_arrow, out_arrow = Vector(RIGHT).replicate(2)
        in_arrow.next_to(rhs.target, RIGHT)
        softmax_box.next_to(in_arrow, RIGHT)
        out_arrow.next_to(softmax_box, RIGHT)

        softmax_label = Text("softmax", font_size=60)
        softmax_label.move_to(softmax_box)

        rhs_values = np.array([e.get_value() for e in rhs.get_entries()])
        dist = softmax(rhs_values)
        output = DecimalMatrix(dist.reshape((dist.shape[0], 1)))
        output.match_height(rhs)
        output.next_to(out_arrow, RIGHT)

        bars = chart.bars.copy()
        for bar, entry in zip(bars, output.get_entries()):
            bar.rotate(-PI / 2)
            bar.stretch(2, 0)
            bar.next_to(output)
            bar.match_y(entry)

        self.play(LaggedStart(
            FadeOut(matrix, 2 * LEFT),
            FadeOut(vector, 3 * LEFT),
            FadeOut(eq, 3.5 * LEFT),
            FadeOut(chart_group, DL),
            GrowArrow(in_arrow),
            FadeIn(softmax_box, RIGHT),
            FadeIn(softmax_label, RIGHT),
            MoveToTarget(rhs),
            GrowArrow(out_arrow),
            FadeIn(output, RIGHT),
            TransformFromCopy(chart.bars, bars),
        ), lag_ratio=0.2, run_time=2)
        self.wait()

        # Highlight larger and smaller parts
        rhs_entries = rhs.get_entries()
        changer = VGroup(rhs_entries, output.get_entries(), bars)
        changer.save_state()
        for index in range(4, 0, -1):
            changer.target = changer.saved_state.copy()
            changer.target.set_fill(border_width=0)
            for group in changer.target:
                for j, elem in enumerate(group):
                    if j != index:
                        elem.fade(0.8)
            self.play(MoveToTarget(changer))
            self.wait()
        self.play(Restore(changer))
        self.remove(changer)
        self.add(rhs, output, bars)
        self.wait()

        # Swap out for variables
        variables = VGroup(*(
            Tex(f"x_{{{n}}}", font_size=48).move_to(elem)
            for n, elem in enumerate(rhs_entries, start=1)
        ))

        self.remove(rhs_entries)
        self.play(
            LaggedStart(*(
                TransformFromCopy(entry, variable, path_arc=PI / 2)
                for entry, variable in zip(rhs_entries, variables)
            ), lag_ratio=0.1, run_time=1.0)
        )
        self.wait()

        # Exponentiate each part
        exp_parts = VGroup(*(
            Tex(f"e^{{{var.get_tex()}}}", font_size=48).move_to(var)
            for var in variables
        ))
        exp_parts.align_to(softmax_box, LEFT)
        exp_parts.shift(0.75 * RIGHT)
        exp_parts.space_out_submobjects(1.5)
        gt0s = VGroup(
            Tex(R"> 0").next_to(exp_part, aligned_edge=DOWN)
            for exp_part in exp_parts
        )

        self.play(
            softmax_label.animate.next_to(softmax_box, UP, buff=0.15),
            LaggedStart(*(
                TransformMatchingStrings(var.copy(), exp_part)
                for var, exp_part in zip(variables, exp_parts)
            ), run_time=1, lag_ratio=0.01)
        )
        self.play(LaggedStartMap(FadeIn, gt0s, shift=0.5 * RIGHT, lag_ratio=0.25, run_time=1))
        self.wait()
        self.play(FadeOut(gt0s))

        # Compute the sum
        exp_sum = Tex(R"\sum_{n=0}^{N-1} e^{x_{n}}", font_size=42)
        exp_sum[R"e^{x_{n}}"].scale(1.5, about_edge=LEFT)
        exp_sum.next_to(softmax_box.get_right(), LEFT, buff=0.75)

        lines = VGroup(*(Line(exp_part.get_right(), exp_sum.get_left(), buff=0.1) for exp_part in exp_parts))
        lines.set_stroke(TEAL, 2)

        self.play(
            LaggedStart(*(
                FadeTransform(exp_part.copy(), exp_sum)
                for exp_part in exp_parts
            ), lag_ratio=0.01),
            LaggedStartMap(ShowCreation, lines, lag_ratio=0.01),
            run_time=1
        )
        self.wait()
        self.play(FadeOut(lines))

        # Divide each part by the sum
        lil_denoms = VGroup()
        for exp_part in exp_parts:
            slash = Tex("/").match_height(exp_sum)
            slash.next_to(exp_sum, LEFT, buff=0)
            denom = VGroup(slash, exp_sum).copy()
            denom.set_height(exp_part.get_height() * 1.5)
            denom.next_to(exp_part, RIGHT, buff=0)
            lil_denoms.add(denom)
        lil_denoms.align_to(softmax_box.get_center(), LEFT)

        lines = VGroup(*(Line(exp_sum.get_left(), denom.get_center()) for denom in lil_denoms))
        lines.set_stroke(TEAL, 1)

        self.remove(exp_sum)
        self.play(
            exp_parts.animate.next_to(lil_denoms, LEFT, buff=0),
            LaggedStart(*(
                FadeTransform(exp_sum.copy(), denom)
                for denom in lil_denoms
            ), lag_ratio=0.01),
        )
        self.wait()

        # Resize box
        sm_terms = VGroup(*(
            VGroup(exp_part, denom)
            for exp_part, denom in zip(exp_parts, lil_denoms)
        ))
        sm_terms.generate_target()

        target_height = 5.0
        full_output = Group(output, bars)
        full_output.generate_target()
        full_output.target.set_height(target_height, about_edge=RIGHT)
        full_output.target.shift(1.5 * LEFT)
        equals = Tex("=")
        equals.next_to(full_output.target, LEFT)

        softmax_box.generate_target()
        softmax_box.target.set_width(3.0, stretch=True)
        VGroup(softmax_box.target, sm_terms.target).set_height(target_height + 0.5).next_to(equals, LEFT)

        rhs.generate_target()
        rhs_entries.become(variables)
        self.remove(variables)
        rhs.target.set_height(target_height)
        rhs.target.next_to(softmax_box.target, LEFT, buff=1.5)

        self.play(
            softmax_label.animate.next_to(softmax_box.target, UP),
            MoveToTarget(softmax_box),
            MoveToTarget(sm_terms),
            MoveToTarget(full_output),
            MoveToTarget(rhs),
            FadeTransform(out_arrow, equals),
            in_arrow.animate.become(
                Arrow(rhs.target, softmax_box.target).match_style(in_arrow)
            ),
        )
        self.wait()

        # Set up updaters
        output_entries = output.get_entries()
        bar_width_ratio = bars.get_width() / max(o.get_value() for o in output_entries)
        temp_tracker = ValueTracker(1)

        def update_outs(output_entries):
            inputs = [entry.get_value() for entry in rhs_entries]
            outputs = softmax(inputs, temp_tracker.get_value())
            for entry, output in zip(output_entries, outputs):
                entry.set_value(output)

        def update_bars(bars):
            for bar, entry in zip(bars, output_entries):
                width = max(bar_width_ratio * entry.get_value(), 1e-3)
                bar.set_width(width, about_edge=LEFT, stretch=True)

        output_entries.clear_updaters().save_state()
        bars.clear_updaters().save_state()
        output_entries.add_updater(update_outs)
        bars.add_updater(update_bars)

        self.add(bars, output_entries)

        # Tweak values
        index_value_pairs = [
            (6, 4.0),
            (4, 4.2),
            (2, 4.0),
            (0, 6.0),
            (4, 9.9)
        ]
        # index_value_pairs = [  # For emphasizing a max
        #     (3, 8.5),
        #     (6, 8.0),
        #     (2, 8.1),
        #     (0, 9.0),
        # ]
        for index, value in index_value_pairs:
            entry = rhs_entries[index]
            rect = SurroundingRectangle(entry)
            rect.set_stroke(BLUE if value > entry.get_value() else RED, 3)
            self.play(
                ChangeDecimalToValue(entry, value),
                FadeIn(rect, time_span=(0, 1)),
                run_time=4
            )
            self.play(FadeOut(rect))

        # Add temperature
        frame = self.frame
        temp_color = RED
        new_title = Text("softmax with temperature")
        new_title["temperature"].set_color(temp_color)
        get_t = temp_tracker.get_value
        t_line = NumberLine(
            (0, 10, 0.2),
            tick_size=0.025,
            big_tick_spacing=1,
            longer_tick_multiple=2.0,
            width=4
        )
        t_line.set_stroke(width=1.5)
        t_line.next_to(softmax_box, UP)
        t_tri = ArrowTip(angle=-90 * DEGREES)
        t_tri.set_color(temp_color)
        t_tri.set_height(0.2)
        t_label = Tex("T = 0.00", font_size=36)
        t_label.rhs = t_label.make_number_changeable("0.00")
        t_label["T"].set_color(temp_color)
        t_tri.add_updater(lambda m: m.move_to(t_line.n2p(get_t()), DOWN))
        t_label.add_updater(lambda m: m.rhs.set_value(get_t()))
        t_label.add_updater(lambda m: m.next_to(t_tri, UP, buff=0.1, aligned_edge=LEFT))
        t_label.update()

        new_title.next_to(t_label, UP, buff=0.5).match_x(softmax_box)

        self.play(
            frame.animate.move_to(0.75 * UP),
            TransformMatchingStrings(softmax_label, new_title),
            FadeIn(t_line),
            FadeIn(t_tri),
            FadeIn(t_label),
            run_time=1
        )

        # Change formula
        template = Tex(R"e^{x_{0} / T} / \sum_{n=0}^{N - 1} e^{x_n / T}")
        template["T"].set_color(temp_color)
        template["/"][1].scale(1.9, about_edge=LEFT)
        template[R"\sum_{n=0}^{N - 1}"][0].scale(0.7, about_edge=RIGHT)
        index_part = template.make_number_changeable("0")

        new_sm_terms = VGroup()
        all_Ts = VGroup()
        for n, term in enumerate(sm_terms, start=1):
            template.replace(term, dim_to_match=1)
            index_part.set_value(n)
            new_term = template.copy()
            all_Ts.add(*new_term["T"])
            new_sm_terms.add(new_term)

        self.play(
            LaggedStart(*(
                FadeTransform(old_term, new_term)
                for old_term, new_term in zip(sm_terms, new_sm_terms)
            )),
            LaggedStart(*(
                TransformFromCopy(t_label[0], t_mob[0])
                for t_mob in all_Ts
            )),
        )
        self.wait()

        # Oscilate between values
        for value in [4, 10, 2]:
            self.play(temp_tracker.animate.set_value(value), run_time=8)
            self.wait()
        self.play(temp_tracker.animate.set_value(0), run_time=3)
        max_rects = VGroup(
            SurroundingRectangle(rhs.get_entries()[4]),
            SurroundingRectangle(VGroup(output.get_entries()[4], bars[4])),
        )
        self.play(LaggedStartMap(ShowCreationThenFadeOut, max_rects))
        self.wait()
        for value in [5, 1, 7]:
            self.play(temp_tracker.animate.set_value(value), run_time=4)
            self.wait()

        # Describe logits
        prob_arrows, logit_arrows = (
            VGroup(*(
                Vector(-vect).next_to(entry, vect, buff=0.25)
                for entry in matrix.get_entries()
            ))
            for matrix, vect in [(output, RIGHT), (rhs, LEFT)]
        )
        prob_arrows.next_to(bars, RIGHT)
        prob_rects = VGroup(*map(SurroundingRectangle, output.get_entries()))
        logit_rects = VGroup(*map(SurroundingRectangle, rhs.get_entries()))
        VGroup(prob_rects, logit_rects).set_stroke(width=1)

        prob_words = Text("Probabilities")
        prob_words.next_to(output, UP, buff=0.25)
        logit_words = Text("Logits")
        logit_words.next_to(rhs, UP, buff=0.25)

        logit_group = VGroup(logit_arrows, logit_words, logit_rects)
        logit_group.set_color(TEAL)
        prob_group = VGroup(prob_arrows, prob_words, prob_rects)
        prob_group.set_color(YELLOW)

        for arrows, word, rects in [prob_group, logit_group]:
            self.play(
                t_line.animate.set_y(3.35),
                Write(word),
                Write(rects, stroke_width=5, stroke_color=rects[0].get_stroke_color(), lag_ratio=0.3, run_time=3),
            )
            self.wait()
