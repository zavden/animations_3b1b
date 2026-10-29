# ==============================================================================
# Scene:      IntroduceValueMatrix
# Source:     videos/_2024/transformers/attention.py (lines 2313-2558)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/embedding.py, _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl IntroduceValueMatrix.py IntroduceValueMatrix -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Dalle3_creature.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
#   - _lib/assets/raster_images/Dalle3_creature_2.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
#   - _lib/assets/raster_images/BlueFluff.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
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


class ContextAnimation(LaggedStart):
    def __init__(
        self,
        target,
        sources,
        direction=UP,
        hue_range=(0.1, 0.3),
        time_width=2,
        min_stroke_width=0,
        max_stroke_width=5,
        lag_ratio=None,
        strengths=None,
        run_time=3,
        fix_in_frame=False,
        path_arc=PI / 2,
        **kwargs,
    ):
        arcs = VGroup()
        if strengths is None:
            strengths = np.random.random(len(sources))**2
        for source, strength in zip(sources, strengths):
            sign = direction[1] * (-1)**int(source.get_x() < target.get_x())
            arcs.add(Line(
                source.get_edge_center(direction),
                target.get_edge_center(direction),
                path_arc=sign * path_arc,
                stroke_color=random_bright_color(hue_range=hue_range),
                stroke_width=interpolate(
                    min_stroke_width,
                    max_stroke_width,
                    strength,
                )
            ))
        if fix_in_frame:
            arcs.fix_in_frame()
        arcs.shuffle()
        lag_ratio = 0.5 / len(arcs) if lag_ratio is None else lag_ratio

        super().__init__(
            *(
                VShowPassingFlash(arc, time_width=time_width)
                for arc in arcs
            ),
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )


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


class RandomizeMatrixEntries(Animation):
    def __init__(self, matrix, **kwargs):
        self.matrix = matrix
        self.entries = matrix.get_entries()
        self.start_values = [entry.get_value() for entry in self.entries]
        self.target_values = np.random.uniform(
            matrix.value_range[0],
            matrix.value_range[1],
            len(self.entries)
        )
        super().__init__(matrix, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        for index, entry in enumerate(self.entries):
            start = self.start_values[index]
            target = self.target_values[index]
            sub_alpha = self.get_sub_alpha(alpha, index, len(self.entries))
            entry.set_value(interpolate(start, target, sub_alpha))
        self.matrix.reset_entry_colors()



# ----- From _2024/transformers/embedding.py -----

def get_piece_rectangles(
    phrase_pieces,
    h_buff=0.05,
    v_buff=0.1,
    fill_opacity=0.15,
    fill_color=None,
    stroke_width=1,
    stroke_color=None,
    hue_range=(0.5, 0.6),
    leading_spaces=False,
):
    rects = VGroup()
    height = phrase_pieces.get_height() + 2 * v_buff
    last_right_x = phrase_pieces.get_x(LEFT)
    for piece in phrase_pieces:
        left_x = last_right_x if leading_spaces else piece.get_x(LEFT)
        right_x = piece.get_x(RIGHT)
        fill = random_bright_color(hue_range) if fill_color is None else fill_color
        stroke = fill if stroke_color is None else stroke_color
        rect = Rectangle(
            width=right_x - left_x + 2 * h_buff,
            height=height,
            fill_color=fill,
            fill_opacity=fill_opacity,
            stroke_color=stroke,
            stroke_width=stroke_width
        )
        if leading_spaces:
            rect.set_x(left_x, LEFT)
        else:
            rect.move_to(piece)
        rect.set_y(0)
        rects.add(rect)

        last_right_x = right_x

    rects.match_y(phrase_pieces)
    return rects



# ----- From _2024/transformers/attention.py -----

class IntroduceValueMatrix(InteractiveScene):
    def setup(self):
        self.fix_new_entries_in_frame = False
        super().setup()

    def construct(self):
        # Initialized axes
        frame = self.frame
        self.set_floor_plane("xz")
        axes = ThreeDAxes((-4, 4), (-4, 4), (-4, 4))
        plane = NumberPlane(
            (-4, 4), (-4, 4),
            background_line_style=dict(
                stroke_color=GREY,
                stroke_width=1,
                stroke_opacity=0.5,
            )
        )
        plane.axes.set_opacity(0)
        plane.rotate(PI / 2, RIGHT)
        axes.add(plane)

        frame.reorient(5, -4, 0, (-4.66, 2.07, 0.04), 12.48)
        # frame.add_ambient_rotation()
        self.add(axes)

        # Add word pair
        words = VGroup(Text("blue"), Text("fluffy"), Text("creature"))
        words.scale(1.5)
        words.arrange(RIGHT, aligned_edge=UP)
        words.to_edge(UP)
        words.to_edge(LEFT, buff=0)
        rects = get_piece_rectangles(words, h_buff=0.1)
        rects[0].set_color(BLUE)
        rects[1].set_color(TEAL)
        rects[2].set_color(ORANGE)
        arrows = VGroup(Vector(DOWN).next_to(rect, DOWN) for rect in rects)
        embs = VGroup(
            NumericEmbedding(length=8).set_height(4.0).next_to(arrow, DOWN)
            for arrow in arrows
        )

        blue_group = VGroup(rects[0], words[0], arrows[0], embs[0])
        blue_group.set_opacity(0)

        self.fix_new_entries_in_frame = True
        self.add(rects)
        self.add(words)
        self.add(arrows)
        self.add(embs)

        # Add word vectors
        creature_vect = self.get_labeled_vector(axes, (-2, 3, 1), ORANGE, "Dalle3_creature")
        with_fluffy_vect = self.get_labeled_vector(axes, (2, 3, 1), GREY_BROWN, "Dalle3_creature_2")
        with_blue_vect = self.get_labeled_vector(axes, (1, 2, 4), BLUE, "BlueFluff")

        self.wait()
        self.fix_new_entries_in_frame = False
        self.play(
            FadeTransform(words[1].copy(), creature_vect[1]),
            TransformFromCopy(
                Arrow(embs[1].get_bottom(), embs[1].get_top(), buff=0).fix_in_frame().set_stroke(width=10, opacity=0.25),
                creature_vect[0],
            )
        )
        self.add(creature_vect)

        # Show influence
        diff_vect = Arrow(
            creature_vect[0].get_end(),
            with_fluffy_vect[0].get_end(),
            buff=0
        )
        diff_vect.scale(0.95)
        self.fix_new_entries_in_frame = False
        self.play(
            FadeTransform(creature_vect[1].copy(), with_fluffy_vect[1]),
            TransformFromCopy(creature_vect[0], with_fluffy_vect[0]),
            run_time=3,
        )
        self.add(with_fluffy_vect)
        self.play(GrowArrow(diff_vect, run_time=2))

        self.fix_new_entries_in_frame = True
        self.play(
            RandomizeMatrixEntries(embs[2], time_span=(1, 5)),
            LaggedStart(
                (ContextAnimation(entry, embs[1].get_entries(), path_arc=10 * DEGREES, lag_ratio=0.1)
                for entry in embs[2].get_entries()),
                lag_ratio=0.01,
                run_time=5,
            ),
        )
        self.wait()

        # Make room
        corner_group = VGroup(rects, words, arrows, embs)
        self.play(
            frame.animate.reorient(10, -7, 0, (-8.33, -0.79, 0.37), 16.82),
            corner_group.animate.set_height(3).to_edge(UP, buff=0.25).set_x(-2),
            run_time=2
        )

        # Show value matrix
        matrix = WeightMatrix(shape=(8, 8))
        matrix.set_height(2.75)
        matrix.to_corner(DL)
        matrix_brace = Brace(matrix, UP)
        matrix_label = Tex("W_V")
        matrix_label.next_to(matrix_brace, UP)
        matrix_label.set_color(RED)

        fluff_emb = embs[1]
        in_vect_rect = SurroundingRectangle(fluff_emb)
        in_vect_rect.set_stroke(TEAL, 2)
        in_vect = fluff_emb.copy()
        in_vect.match_height(matrix)
        in_vect.next_to(matrix, RIGHT, SMALL_BUFF)
        in_vect_path = self.get_top_vect_to_low_vect_path(fluff_emb, in_vect, TEAL)

        self.fix_new_entries_in_frame = True
        self.play(
            FadeIn(matrix, lag_ratio=1e-3),
            GrowFromCenter(matrix_brace),
            FadeIn(matrix_label, shift=0.25 * UP)
        )
        self.play(ShowCreation(in_vect_rect))
        self.play(
            ShowCreation(in_vect_path),
            TransformFromCopy(fluff_emb, in_vect, path_arc=-20 * DEGREES),
            run_time=2
        )

        # Show matrix product
        eq, rhs = show_matrix_vector_product(self, matrix, in_vect)
        self.wait()

        # Position value vect
        value_rect = SurroundingRectangle(rhs)
        value_rect.set_stroke(RED, 2)
        value_label = Text("Value")
        value_label.next_to(value_rect, RIGHT)
        value_label.set_color(RED)
        value_label.set_backstroke()
        self.fix_new_entries_in_frame = True
        self.play(
            ShowCreation(value_rect),
            FadeIn(value_label, lag_ratio=0.1)
        )
        self.wait()

        value_label2 = value_label.copy()
        value_label2.set_backstroke(BLACK, 5)
        value_label2.scale(1.5)
        value_label2.next_to(diff_vect, UP, MED_SMALL_BUFF)
        value_label2.unfix_from_frame()

        self.fix_new_entries_in_frame = False
        self.play(
            frame.animate.reorient(29, -2, 0, (-7.48, 1.91, 1.21), 11.89),
            FadeInFromPoint(value_label2, np.array([-4, -5, 0])),
            TransformFromCopy(value_rect, diff_vect),
            run_time=2
        )
        self.wait()

        # Show blue
        blue_group.target = blue_group.generate_target()
        blue_group.target[0].set_stroke(opacity=1)
        blue_group.target[0].set_fill(opacity=0.2)
        blue_group.target[1:].set_opacity(1)
        blue_group.target.shift(0.2 * LEFT)

        blue_path = self.get_top_vect_to_low_vect_path(blue_group.target, in_vect, BLUE)
        blue_emb = blue_group[3]
        blue_in_vect = blue_emb.copy().set_opacity(1)
        blue_in_vect.replace(in_vect)

        self.fix_new_entries_in_frame = True
        self.play(
            MoveToTarget(blue_group),
            LaggedStartMap(FadeOut, VGroup(
                in_vect_path, in_vect_rect,
                rhs, value_rect, value_label,
                value_label2,
            )),
            run_time=1
        )
        self.play(
            TransformFromCopy(blue_emb, blue_in_vect),
            ShowCreation(blue_path),
            FadeOut(in_vect, 3 * DOWN),
            run_time=1.5
        )
        eq, rhs2 = show_matrix_vector_product(self, matrix, blue_in_vect)

        # Show in diagram
        diff2 = Arrow(
            with_fluffy_vect[0].get_end(),
            with_blue_vect[0].get_end(),
            buff=0.05
        )
        diff2.set_flat_stroke(False)
        rhs_rect = SurroundingRectangle(rhs2)
        rhs_rect.set_stroke(RED, 2)

        self.fix_new_entries_in_frame = True
        self.play(ShowCreation(rhs_rect))
        self.fix_new_entries_in_frame = False
        self.add(diff2)
        self.play(
            TransformFromCopy(rhs_rect, diff2),
            FadeIn(diff2),
            frame.animate.reorient(-16, -3, 0, (-6.41, 2.78, 1.37), 13.21),
            TransformFromCopy(with_fluffy_vect[0], with_blue_vect[0]),
            FadeTransform(with_fluffy_vect[1].copy(), with_blue_vect[1]),
            run_time=2,
        )
        frame.add_ambient_rotation(2 * DEGREES)
        self.wait(8)


    def get_top_vect_to_low_vect_path(self, top_vect, low_vect, color, top_buff=0.1, low_buff=0.2, bezier_factor=1.5):
        result = CubicBezier(
            top_vect.get_bottom() + top_buff * DOWN,
            top_vect.get_bottom() + bezier_factor * DOWN,
            low_vect.get_top() + bezier_factor * UP,
            low_vect.get_top() + low_buff * UP,
        )
        result.set_stroke(color, 3)
        return result

    def get_labeled_vector(self, axes, coords, color, image_name, image_height=1.0):
        vect = Arrow(axes.get_origin(), axes.c2p(*coords), buff=0)
        vect.set_color(color)
        image = ImageMobject(image_name)
        image.set_height(image_height)
        image.next_to(vect.get_end(), UP, MED_SMALL_BUFF)

        return Group(vect, image)

    def add(self, *mobjects):
        if self.fix_new_entries_in_frame:
            for mob in mobjects:
                mob.fix_in_frame()
        super().add(*mobjects)
