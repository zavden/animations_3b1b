# ==============================================================================
# Scene:      MLPStepsPreview
# Source:     videos/_2024/transformers/mlp.py (lines 230-374)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl MLPStepsPreview.py MLPStepsPreview -w -m --fps 15
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


def data_flying_animation(
    point,
    vect=2 * DOWN + RIGHT,
    color=GREY_C,
    max_opacity=0.75,
    font_size=48,
    fix_in_frame=False
    ):
    word = Text("Data", color=color, font_size=font_size)
    if fix_in_frame:
        word.fix_in_frame()
    return UpdateFromAlphaFunc(
        word, lambda m, a: m.move_to(
            interpolate(point, point + vect, a)
        ).set_opacity(there_and_back(a) * max_opacity)
    )


def get_data_modifying_matrix_anims(
    matrix,
    word_shape=(5, 10),
    alpha_maxes=(0.7, 0.9),
    shift_vect=2 * DOWN + RIGHT,
    run_time=3,
    fix_in_frame=False,
    font_size=48,
):
    x_min, x_max = [matrix.get_x(LEFT), matrix.get_x(RIGHT)]
    y_min, y_max = [matrix.get_y(UP), matrix.get_y(DOWN)]
    z = matrix.get_z()
    points = np.array([
        [
            interpolate(x_min, x_max, a1),
            interpolate(y_min, y_max, a2),
            z,
        ]
        for a1 in np.linspace(0, alpha_maxes[1], word_shape[1])
        for a2 in np.linspace(0, alpha_maxes[0], word_shape[0])
    ])
    return [
        LaggedStart(
            (data_flying_animation(p, vect=shift_vect, fix_in_frame=fix_in_frame, font_size=font_size)
            for p in points),
            lag_ratio=1 / len(points),
            run_time=run_time
        ),
        RandomizeMatrixEntries(matrix, run_time=run_time),
    ]


def data_modifying_matrix(scene, matrix, *args, **kwargs):
    anims = get_data_modifying_matrix_anims(matrix, *args, **kwargs)
    scene.play(*anims)


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



# ----- From _2024/transformers/mlp.py -----

class MLPStepsPreview(InteractiveScene):
    def construct(self):
        # Setup framing
        background = FullScreenRectangle()
        top_frame, low_frame = frames = Rectangle(7, 3.25).replicate(2)
        frames.arrange(DOWN, buff=0.5)
        frames.to_edge(LEFT)
        frames.set_fill(BLACK, 1)
        frames.set_stroke(WHITE, 2)

        titles = VGroup(
            VGroup(Text("Structure:"), Text("Easy")),
            VGroup(Text("Emergent behavior:"), Text("Exceedingly challenging")),
        )
        for title, frame, color in zip(titles, frames, [GREEN, RED]):
            title.scale(2)
            for part in title:
                part.set_max_width(6)
            title.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            title.next_to(frame, RIGHT, buff=0.5)
            title[1].set_color(color)

        titles[0].save_state()
        top_frame.save_state()
        top_frame.set_shape(8, 6).center().to_edge(LEFT)
        titles[0].next_to(top_frame, RIGHT, buff=0.5)

        self.add(background)
        self.add(top_frame)
        self.add(titles[0][0])

        # Add all steps
        arrows = Vector(2.2 * RIGHT).get_grid(1, 3, buff=0.25)
        arrows.move_to(top_frame)
        up_proj = WeightMatrix(shape=(10, 6))
        down_proj = WeightMatrix(shape=(6, 10))
        VGroup(up_proj, down_proj).match_width(arrows[0])
        up_proj.next_to(arrows[0], UP, buff=MED_SMALL_BUFF)
        down_proj.next_to(arrows[2], UP, buff=MED_SMALL_BUFF)

        axes = Axes((-4, 4), (0, 4))
        graph = axes.get_graph(lambda x: max(0, x))
        graph.set_stroke(YELLOW, 5)
        plot = VGroup(axes, graph)
        plot.set_width(arrows[0].get_width() * 0.75)
        plot.next_to(arrows[1], UP, buff=MED_SMALL_BUFF)

        labels = VGroup(*map(Text, ["Linear", "ReLU", "Linear"]))
        for label, arrow in zip(labels, arrows):
            label.next_to(arrow, DOWN)

        structure = VGroup(arrows, labels, VGroup(up_proj, plot, down_proj))

        self.play(
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.5),
            LaggedStartMap(FadeIn, labels, shift=0.5 * RIGHT, lag_ratio=0.5),
            Write(titles[0][1])
        )
        self.play(LaggedStart(
            FadeIn(up_proj, shift=0.5 * UP),
            FadeIn(down_proj, shift=0.5 * UP),
            lag_ratio=0.5
        ))
        self.play(FadeIn(plot, lag_ratio=1e-2))
        self.wait(3)

        # Reference emergent structure

        self.play(
            Restore(top_frame),
            Restore(titles[0]),
            structure.animate.set_width(0.9 * top_frame.saved_state.get_width()).move_to(top_frame.saved_state),
            FadeIn(low_frame, DOWN),
            FadeIn(titles[1][0], DOWN),
        )
        self.play(
            Write(titles[1][1], stroke_color=RED)
        )

        # Data flying
        kw = dict(font_size=16, shift_vect=0.5 * DOWN + 0.5 * RIGHT, word_shape=(5, 5))
        data_modifying_matrix(self, up_proj, **kw)
        data_modifying_matrix(self, down_proj, **kw)
        self.wait()

        # Swap out for toy example
        toy_example_title = Text("Motivating Toy Example", font_size=54)
        toy_example_title.next_to(titles[1][0], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        strike = Line().replace(titles[1][0])
        strike.set_stroke(RED, 8)

        low_matrices = VGroup(up_proj, down_proj)
        top_matrices = low_matrices.copy()
        low_matrices.generate_target()
        low_matrices.target.scale(1.75).arrange(RIGHT, buff=0.5)
        low_matrices.target.move_to(low_frame, DOWN).shift(MED_SMALL_BUFF * UP)

        self.play(
            ShowCreation(strike),
            FadeOut(titles[1][1]),
            titles[1][0].animate.set_opacity(0.5)
        )
        self.add(top_matrices)
        self.play(
            MoveToTarget(low_matrices),
            FadeIn(toy_example_title, DOWN)
        )
        self.wait()

        # Write down fact
        row_rect = SurroundingRectangle(low_matrices[0].get_rows()[0], buff=0.1)
        col_rect = SurroundingRectangle(low_matrices[1].get_columns()[0], buff=0.1)
        VGroup(row_rect, col_rect).set_stroke(WHITE, 1)
        fact = Text("Michael Jordan plays Basketball", font_size=36)
        fact.next_to(frames[1].get_top(), DOWN)
        fact.align_to(low_matrices, LEFT)
        mj, bb = fact["Michael Jordan"], fact["plays Basketball"]
        mj_brace = Brace(mj, DOWN, buff=0.1)
        bb_brace = Brace(bb, DOWN).match_y(mj_brace)
        mj_arrow = Arrow(row_rect, mj_brace, buff=0.05)
        bb_arrow = Arrow(col_rect.get_top(), bb_brace, buff=0.05)

        row_cover = BackgroundRectangle(low_matrices[0].get_rows()[1:], buff=0.05)
        col_cover = BackgroundRectangle(low_matrices[1].get_columns()[1:], buff=0.05)
        VGroup(row_cover, col_cover).set_fill(BLACK, 0.75)

        self.play(LaggedStart(
            FadeIn(row_cover),
            FadeIn(row_rect),
            GrowFromCenter(mj_brace),
            FadeIn(mj, 0.5 * UP)
        ))
        self.play(
            FadeIn(col_cover),
            FadeIn(col_rect),
            GrowArrow(bb_arrow),
            GrowFromCenter(bb_brace),
            FadeIn(bb, 0.5 * UP)
        )
        self.add(*low_matrices, row_cover, col_cover, row_rect, col_rect)
        self.play(
            RandomizeMatrixEntries(low_matrices[0]),
            RandomizeMatrixEntries(low_matrices[1]),
        )
        self.wait()
