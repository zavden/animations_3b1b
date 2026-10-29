# ==============================================================================
# Scene:      ShowGPT3Numbers
# Source:     videos/_2024/transformers/ml_basics.py (lines 1174-1663)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ShowGPT3Numbers.py ShowGPT3Numbers -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - np.product no longer exists in numpy 2: np.prod is used (3 uses)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/OpenAI.svg  (_lib/assets/generated/2024/transformers/make_ml_basics_data.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2024/transformers/helpers.py -----

if TYPE_CHECKING:
    from typing import Optional
    from manimlib.typing import Vect3, ManimColor


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


class Dial(VGroup):
    def __init__(
        self,
        radius=0.5,
        relative_tick_size=0.2,
        value_range=(0, 1, 0.1),
        initial_value=0,
        arc_angle=270 * DEGREES,
        stroke_width=2,
        stroke_color=WHITE,
        needle_color=BLUE,
        needle_stroke_width=5.0,
        value_to_color_config=dict(),
        set_anim_streak_color=TEAL,
        set_anim_streak_width=4,
        set_value_anim_streak_density=6,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.value_range = value_range
        self.value_to_color_config = value_to_color_config
        self.set_anim_streak_color = set_anim_streak_color
        self.set_anim_streak_width = set_anim_streak_width
        self.set_value_anim_streak_density = set_value_anim_streak_density

        # Main dial
        self.arc = Arc(arc_angle / 2, -arc_angle, radius=radius)
        self.arc.rotate(90 * DEGREES, about_point=ORIGIN)

        low, high, step = value_range
        n_values = int(1 + (high - low) / step)
        tick_points = map(self.arc.pfp, np.linspace(0, 1, n_values))
        self.ticks = VGroup(*(
            Line((1.0 - relative_tick_size) * point, point)
            for point in tick_points
        ))
        self.bottom_point = VectorizedPoint(radius * DOWN)
        for mob in self.arc, self.ticks:
            mob.set_stroke(stroke_color, stroke_width)

        self.add(self.arc, self.ticks, self.bottom_point)

        # Needle
        self.needle = Line()
        self.needle.set_stroke(
            color=needle_color,
            width=[needle_stroke_width, 0]
        )
        self.add(self.needle)

        # Initialize
        self.set_value(initial_value)

    def value_to_point(self, value):
        low, high, step = self.value_range
        alpha = inverse_interpolate(low, high, value)
        return self.arc.pfp(alpha)

    def set_value(self, value):
        self.needle.put_start_and_end_on(
            self.get_center(),
            self.value_to_point(value)
        )
        self.needle.set_color(value_to_color(
            value,
            min_value=self.value_range[0],
            max_value=self.value_range[1],
            **self.value_to_color_config
        ))

    def animate_set_value(self, value, **kwargs):
        kwargs.pop("path_arc", None)
        center = self.get_center()
        points = [self.needle.get_end(), self.value_to_point(value)]
        vects = [point - center for point in points]
        angle1, angle2 = [
            (angle_of_vector(vect) + TAU / 4) % TAU - TAU / 4
            for vect in vects
        ]
        path_arc = angle2 - angle1

        density = self.set_value_anim_streak_density
        radii = np.linspace(0, 0.5 * self.get_width(), density + 1)[1:]
        diff_arcs = VGroup(*(
            Arc(
                angle1, angle2 - angle1,
                radius=radius,
                arc_center=center,
            )
            for radius in radii
        ))
        diff_arcs.set_stroke(self.set_anim_streak_color, self.set_anim_streak_width)

        return AnimationGroup(
            self.animate.set_value(value).set_anim_args(path_arc=path_arc, **kwargs),
            *(
                VShowPassingFlash(diff_arc, time_width=1.5, **kwargs)
                for diff_arc in diff_arcs
            )
        )

    def get_random_value(self):
        low, high, step = self.value_range
        return interpolate(low, high, random.random())



# ----- From _2024/transformers/ml_basics.py -----

class ShowGPT3Numbers(InteractiveScene):
    def construct(self):
        # Title
        gpt3_label = Text("GPT-3", font="Consolas", font_size=72)
        openai_logo = SVGMobject("OpenAI.svg")
        openai_logo.set_fill(WHITE)
        openai_logo.set_height(2.0 * gpt3_label.get_height())
        title = VGroup(openai_logo, gpt3_label)
        title.arrange(RIGHT)
        title.to_edge(UP)

        self.add(title)

        # 175b weights
        n_param = 175_181_291_520
        weights_count = Integer(n_param, color=BLUE)
        weights_text = VGroup(Text("Total parameters:"), weights_count)
        weights_text.arrange(RIGHT, buff=MED_SMALL_BUFF)
        weights_text.next_to(title, DOWN, buff=1.0)
        weights_arrow = Arrow(weights_count, gpt3_label, stroke_width=6, buff=0.2)

        param_shape = (8, 24)
        pre_dials = Dial().get_grid(*param_shape)
        dial_matrix = MobjectMatrix(
            pre_dials, *param_shape,
            ellipses_row=-2,
            ellipses_col=-2,
        )
        dial_matrix.set_width(FRAME_WIDTH)
        dial_matrix.next_to(weights_text, DOWN, buff=MED_SMALL_BUFF)

        dials = dial_matrix.get_entries()
        dots = dial_matrix.get_ellipses()

        self.play(
            FadeIn(weights_text[:-1], time_span=(0, 3)),
            CountInFrom(weights_count, 0),
            GrowArrow(weights_arrow, time_span=(0, 3)),
            LaggedStartMap(FadeIn, pre_dials, scale=3, lag_ratio=0.1),
            run_time=10,
        )
        self.play(
            LaggedStart(
                (dial.animate_set_value(dial.get_random_value())
                for dial in dials),
                lag_ratio=1.0 / len(dials),
                run_time=5
            )
        )
        self.wait()

        # Change name to weights
        new_name = Text("Total weights: ")
        new_name.move_to(weights_text[0], RIGHT)

        self.play(
            Transform(weights_text[0]["Total"][0], new_name["Total"][0]),
            Transform(weights_text[0]["parameters:"][0], new_name["weights:"][0]),
        )
        self.wait()

        # Organize dials into matrices
        mat_text = Text("Organized into 27,938 matrices")
        mat_text["27,938"].set_color(TEAL)
        mat_text.next_to(weights_text, DOWN, buff=MED_SMALL_BUFF)
        mat_text.shift((weights_count.get_x(LEFT) - mat_text["27,938"].get_x(LEFT)) * RIGHT)

        mat_grid_shape = n, m = (3, 7)
        # CHANGE: np.product does not exist in numpy 2; np.prod is used
        matrices = VGroup(
            WeightMatrix(shape=(5, 5))
            for n in range(np.prod(mat_grid_shape))
        )
        matrices.arrange_in_grid(
            *mat_grid_shape,
            v_buff_ratio=0.3,
            h_buff_ratio=0.2,
        )
        matrices.set_width(FRAME_WIDTH - 1)
        mat_dots = VGroup(
            *(
                Tex(R"\dots").next_to(mat, RIGHT)
                for mat in matrices[m - 1::m]
            ),
            *(
                Tex(R"\vdots").next_to(mat, DOWN)
                for mat in matrices[-m:]
            )
        )
        matrices_group = VGroup(matrices, mat_dots)
        matrices_group.set_width(FRAME_WIDTH - 1)
        matrices_group.next_to(mat_text, DOWN, buff=0.5)
        matrices_group.set_x(0)
        all_entries = VGroup(
            entry
            for mat in matrices
            for row in mat.get_rows()
            for entry in row
        )

        pre_entries = []
        height = all_entries[0].get_height()
        for n, entry in enumerate(all_entries):
            index = n * len(dials) // len(all_entries)
            dial = dials[min(index, len(dials) - 1)].copy()
            dial.target = dial.generate_target()
            dial.target.set_height(height)
            dial.target.move_to(entry)
            pre_entries.append(dial)
        pre_entries = VGroup(*pre_entries)

        self.remove(dial_matrix)
        lag_ratio = 1 / len(all_entries)
        self.play(
            Write(mat_text),
            LaggedStartMap(MoveToTarget, pre_entries, lag_ratio=lag_ratio),
            TransformFromCopy(dots, mat_dots),
            *(FadeIn(mat.get_brackets()) for mat in matrices)
        )
        self.play(
            FadeOut(pre_entries, lag_ratio=0.2 * lag_ratio),
            FadeIn(all_entries, lag_ratio=0.2 * lag_ratio),
            run_time=2
        )
        self.add(matrices)
        self.wait()

        # Show 8 different categories
        count_text = VGroup(weights_text, mat_text)
        title_scale_factor = 0.75
        count_text.target = count_text.generate_target()
        count_text.target.scale(title_scale_factor)
        count_text.target.to_edge(UP, MED_SMALL_BUFF).to_edge(LEFT)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH)
        h_line.next_to(count_text.target, DOWN).set_x(0)
        h_line.insert_n_curves(10)
        h_line.set_stroke(width=[0, 3, 3, 3, 0])

        category_names = VGroup(*map(TexText, [
            "Embedding",
            "Key",
            "Query",
            # "Value",  # Dumb alignment hack
            # "Output",
            R"Value$_\downarrow$",
            R"Value$_\uparrow$",
            "Up-projection",
            "Down-projection",
            "Unembedding",
        ]))
        # category_names[3][-1].set_fill(BLACK)  # Dumb alignment hack
        category_names.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        category_names.set_height(5.5)
        category_names.next_to(h_line, DOWN, buff=MED_LARGE_BUFF)
        category_names.to_edge(LEFT, buff=0.5)
        category_names.set_fill(border_width=0.2)

        mat_index = 0
        counts = [1, * 6 * [3], 1]
        mat_groups = VGroup()
        for name, count, dots in zip(category_names, counts, mat_dots):
            new_mat_index = mat_index + count
            mat_group = matrices[mat_index:new_mat_index]
            mat_index = new_mat_index

            mat_group.target = mat_group.generate_target()
            if len(mat_group) > 1:
                mat_group.target.add(*mat_group.copy())
            mat_group.target.arrange(RIGHT, buff=LARGE_BUFF)
            mat_group.target.set_height(0.25)
            mat_group.target.next_to(category_names, RIGHT)
            mat_group.target.match_y(name)

            dots.target = dots.generate_target()
            if dots.get_width() < dots.get_height():
                dots.target.rotate(90 * DEGREES)
            dots.target.next_to(mat_group.target, RIGHT)
            mat_groups.add(mat_group)
        mat_dots[0].target.set_opacity(0)
        mat_dots[7].target.set_opacity(0)

        n_groups = len(category_names)
        self.play(LaggedStart(
            MoveToTarget(count_text),
            title.animate.scale(title_scale_factor).next_to(count_text.target, RIGHT, LARGE_BUFF),
            FadeOut(weights_arrow),
            GrowFromCenter(h_line),
            FadeIn(category_names),
            LaggedStart(map(MoveToTarget, mat_groups), lag_ratio=0.05),
            LaggedStart(map(MoveToTarget, mat_dots[:n_groups]), lag_ratio=0.05),
            LaggedStart(map(FadeOut, mat_dots[n_groups:]), lag_ratio=0.05),
            FadeOut(matrices[sum(counts):]),
        ))

        # Add lines
        h_lines = Line(LEFT, RIGHT).set_width(13).replicate(n_groups)
        h_lines.set_stroke(WHITE, 1, 0.5)
        for name, line in zip(category_names, h_lines):
            line.next_to(name, DOWN, buff=0.1, aligned_edge=LEFT)
            name.line = line
        v_line = Line(
            mat_groups.get_corner(DL) + 0.5 * DOWN,
            mat_groups.get_corner(UL) + 0.25 * UP,
        )
        v_line.shift(SMALL_BUFF * LEFT)
        v_line.match_style(h_lines)

        self.play(
            Write(h_lines),
            Write(v_line),
        )
        self.wait()

        # Prepare expressions for parameter counts
        const_to_value = {
            "n_vocab": 50_257,
            "d_embed": 12_288,
            "d_query": 128,
            "d_value": 128,
            "n_heads": 96,
            "n_layers": 96,
            "n_neurons": 4 * 12_288,
        }
        const_lists = [
            ["d_embed", "n_vocab"],
            ["d_query", "d_embed", "n_heads", "n_layers",],
            ["d_query", "d_embed", "n_heads", "n_layers",],
            ["d_value", "d_embed", "n_heads", "n_layers",],
            ["d_embed", "d_value", "n_heads", "n_layers"],
            ["n_neurons", "d_embed", "n_layers"],
            ["d_embed", "n_neurons", "n_layers"],
            ["n_vocab", "d_embed"],
        ]

        def get_product_expression(category, consts, font_size=30, suffix=None):
            values = [const_to_value[const] for const in consts]
            # CHANGE: np.product does not exist in numpy 2; np.prod is used
            result = np.prod(values)
            result_str = "{:,}".format(result)
            expr = VGroup()
            expr = Text(
                " * ".join(consts) + " = " + result_str,
                font_size=font_size,
            )
            expr.next_to(v_line, RIGHT)
            expr.align_to(category.line, DOWN)
            expr.shift(0.25 * expr.get_height() * UP)
            expr.rhs = expr[result_str]
            expr.rhs.set_color(BLUE)

            counts = VGroup(
                Integer(
                    const_to_value[const],
                    font_size=0.8 * font_size,
                )
                for const in consts
            )
            counts.next_to(expr, UP, buff=0.05)
            for count, const in zip(counts, consts):
                count.match_x(expr[const])
            counts.set_fill(GREY_B)

            result = VGroup(expr, counts)

            if suffix is not None:
                label = Text(suffix)
                label.match_height(expr)
                label.next_to(expr, RIGHT, buff=MED_SMALL_BUFF)
                result.add(label)

            return result

        product_expressions = VGroup(
            get_product_expression(category, consts)
            for category, consts in zip(category_names, const_lists)
        )
        exprs = [pe[0] for pe in product_expressions]
        counts = [pe[1] for pe in product_expressions]

        # Embedding
        def highlight_category(*indices):
            category_names.target = category_names.generate_target()
            category_names.target.set_fill(opacity=0.15, border_width=0)
            for index in indices:
                category_names.target[index].set_fill(opacity=1, border_width=0.5)
            return MoveToTarget(category_names)

        self.play(
            FadeOut(mat_groups),
            FadeOut(mat_dots[1:7]),
            highlight_category(0)
        )
        self.play(
            FadeIn(exprs[0]),
            FadeIn(counts[0], 0.25 * UP),
        )
        self.wait()

        # Unembedding
        total = Integer(2 * 12_288 * 50_257)
        total.to_edge(RIGHT, buff=1.0)
        total.set_color(BLUE)
        total_box = SurroundingRectangle(total, buff=0.25)
        total_box.set_fill(BLACK, 1)
        total_box.set_stroke(WHITE, 2)
        lines = VGroup(*(Line(exprs[i].get_right(), total_box) for i in [0, 7]))
        lines.set_stroke(BLUE, 2)

        self.play(
            highlight_category(0, 7),
            TransformMatchingStrings(exprs[0].copy(), exprs[7]),
            TransformFromCopy(counts[0][0].copy(), counts[7][1]),
            TransformFromCopy(counts[0][1].copy(), counts[7][0]),
            run_time=2
        )
        self.wait()
        self.play(
            ShowCreation(lines, lag_ratio=0),
            FadeIn(total_box),
            FadeTransform(exprs[0][-11:].copy(), total),
            FadeTransform(exprs[7][-11:].copy(), total),
        )
        self.wait()
        self.play(FlashAround(weights_count, time_width=1.5, run_time=2))
        self.wait()
        self.play(
            FadeOut(lines),
            FadeOut(total_box),
            FadeOut(total),
        )
        self.wait()

        # Attention matrices
        covered_categories = [0, 7]
        att_categories = [1, 2, 3, 4]
        per_head_factors = [
            ["d_query", "d_embed"],
            ["d_query", "d_embed"],
            ["d_value", "d_embed"],
            ["d_embed", "d_value"],
        ]
        per_head_exprs = VGroup(
            get_product_expression(name, factors, suffix="per head")
            for name, factors in zip(category_names[1:5], per_head_factors)
        )
        per_layer_exprs = VGroup(
            get_product_expression(name, factors + ["n_heads"], suffix="per layer")
            for name, factors in zip(category_names[1:5], per_head_factors)
        )
        full_att_exprs = product_expressions[1:5]
        for group in [per_head_exprs, per_layer_exprs, full_att_exprs]:
            sum_box = SurroundingRectangle(
                VGroup(expr[0].rhs for expr in group)
            )
            sum_box.set_stroke(BLUE, 2)
            # CHANGE: np.product does not exist in numpy 2; np.prod is used
            sum_label = Integer(sum(
                np.prod(list(count.get_value() for count in expr[1]))
                for expr in group
            ))
            sum_label.set_color(BLUE)
            sum_label.next_to(sum_box, DOWN)
            sum_box.add(sum_label)
            group.sum_box = sum_box

        self.play(
            *(
                product_expressions[i].animate.set_fill(opacity=0.25, border_width=0)
                for i in covered_categories
            ),
            highlight_category(att_categories[0]),
            FadeIn(per_head_exprs[0], shift=0.5 * RIGHT)
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, per_head_exprs[1:], shift=0.5 *DOWN, lag_ratio=0.5),
            highlight_category(*att_categories),
        )
        self.wait()
        self.play(FadeIn(per_head_exprs.sum_box, run_time=3, rate_func=there_and_back_with_pause))
        self.wait()
        self.play(
            FadeOut(per_head_exprs),
            FadeIn(per_layer_exprs),
        )
        self.wait()
        self.play(FadeIn(per_layer_exprs.sum_box, run_time=3, rate_func=there_and_back_with_pause))
        self.wait()
        self.play(
            FadeOut(per_layer_exprs),
            FadeIn(full_att_exprs),
        )
        self.wait()
        self.play(FadeIn(full_att_exprs.sum_box))
        self.wait()

        # Compare with total weights
        total_weights_rect = SurroundingRectangle(weights_count)
        total_weights_rect.set_stroke(BLUE_B, 2)
        box = full_att_exprs.sum_box.copy()
        box.remove(box.submobjects[0])
        self.play(Transform(box, total_weights_rect))
        self.wait()
        self.play(
            FadeOut(box),
            FadeOut(full_att_exprs.sum_box),
        )
        self.wait()

        # MLP matrices
        mlp_categories = [5, 6]
        mlp_exprs = product_expressions[5:7]
        per_layer_exprs = VGroup(
            get_product_expression(category_names[i], const_lists[i][:2], suffix="per layer")
            for i in mlp_categories
        )

        self.play(
            full_att_exprs.animate.set_fill(opacity=0.25, border_width=0),
            highlight_category(*mlp_categories),
        )
        self.wait()
        self.play(FadeIn(per_layer_exprs[0]))
        self.wait()
        self.play(
            TransformMatchingStrings(per_layer_exprs[0][0].copy(), per_layer_exprs[1][0]),
            TransformFromCopy(per_layer_exprs[0][1][0], per_layer_exprs[1][1][1]),
            TransformFromCopy(per_layer_exprs[0][1][1], per_layer_exprs[1][1][0]),
            TransformFromCopy(per_layer_exprs[0][2], per_layer_exprs[1][2]),
            run_time=1
        )
        self.wait()
        self.play(
            FadeOut(per_layer_exprs),
            FadeIn(mlp_exprs),
        )
        self.wait()

        # Sum up MLP right hand sides
        rhs_rect = SurroundingRectangle(VGroup(expr[0].rhs for expr in mlp_exprs))
        rhs_rect.set_stroke(BLUE, 2)
        rhs_rect.stretch(1.2, 1, about_edge=DOWN)
        c2v = const_to_value
        mlp_total = Integer(2 * c2v["n_neurons"] * c2v["d_embed"] * c2v["n_layers"])
        mlp_total.next_to(rhs_rect)
        mlp_total.set_color(BLUE)
        mlp_total_rect = BackgroundRectangle(mlp_total)
        mlp_total_rect.set_fill(BLACK, 1)

        self.play(
            FadeIn(rhs_rect),
            FadeIn(mlp_total_rect),
            FadeTransform(mlp_exprs[0][0].rhs.copy(), mlp_total),
            FadeTransform(mlp_exprs[1][0].rhs.copy(), mlp_total),
        )
        self.wait()

        # Align all right hand sides
        self.play(
            category_names.animate.set_fill(opacity=1, border_width=0.5),
            product_expressions.animate.set_fill(opacity=1, border_width=0.5),
        )

        all_rhss = VGroup(
            VGroup(expr[0]["="][0], expr[0].rhs)
            for expr in product_expressions
        )
        all_rhss.target = all_rhss.generate_target()
        for mob in all_rhss.target:
            mob.align_to(product_expressions, RIGHT)
            mob.shift(0.5 * RIGHT)
        all_rhss_rect = SurroundingRectangle(all_rhss.target)
        all_rhss_rect.match_style(rhs_rect)

        self.play(
            FadeOut(mlp_total_rect, RIGHT),
            FadeOut(mlp_total, RIGHT),
            ReplacementTransform(rhs_rect, all_rhss_rect),
            MoveToTarget(all_rhss)
        )
        self.wait()

        # Move weights count
        self.play(LaggedStart(
            h_line.animate.scale(0.5, about_edge=LEFT),
            weights_text.animate.arrange(DOWN).scale(1.5).next_to(all_rhss_rect, UP),
            FadeOut(mat_text, LEFT),
            title.animate.to_edge(LEFT, buff=2.5),
            lag_ratio=0.2,
            run_time=2
        ))
        self.wait()
