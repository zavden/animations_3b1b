# ==============================================================================
# Scene:      MJSpace
# Source:     videos/_2024/transformers/embedding.py (lines 2758-3047)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl MJSpace.py MJSpace -w -m --fps 15
# ==============================================================================

from __future__ import annotations
import tiktoken
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



# ----- From _2024/transformers/embedding.py -----

def get_token_encoding():
    return tiktoken.encoding_for_model("davinci")


def break_into_pieces(phrase_mob: Text, offsets: list[int]):
    phrase = phrase_mob.get_string()
    lhs = offsets
    rhs = [*offsets[1:], len(phrase)]
    result = []
    for lh, rh in zip(lhs, rhs):
        substr = phrase[lh:rh]
        start = phrase_mob.substr_to_path_count(phrase[:lh])
        end = start + phrase_mob.substr_to_path_count(substr)
        result.append(phrase_mob[start:end])
    return VGroup(*result)


def break_into_tokens(phrase_mob):
    tokenizer = get_token_encoding()
    tokens = tokenizer.encode(phrase_mob.get_string())
    _, offsets = tokenizer.decode_with_offsets(tokens)
    return break_into_pieces(phrase_mob, offsets)


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


def get_direction_lines(axes, direction, n_lines=500, color=YELLOW, line_length=1.0, stroke_width=3):
    line = Line(ORIGIN, line_length * normalize(direction))
    line.insert_n_curves(20).set_stroke(width=(0, stroke_width, stroke_width, stroke_width, 0))
    lines = line.replicate(n_lines)
    lines.set_color(color)
    for line in lines:
        line.move_to(axes.c2p(
            random.uniform(*axes.x_range[:2]),
            random.uniform(*axes.y_range[:2]),
            random.uniform(*axes.z_range[:2]),
        ))
    return lines


class SimpleSpaceExample(InteractiveScene):
    def construct(self):
        # Setup axes
        frame = self.frame
        plane, axes = self.add_plane_and_axes()
        frame.reorient(14, 77, 0, (2.23, 0.25, 1.13), 4.46)

        # Show an initial vector in the space
        frame.add_ambient_rotation()
        vect = Arrow(axes.c2p(0, 0, 0), axes.c2p(2, -1, 1), buff=0)
        vect.set_color(BLUE)
        vect.always.set_perpendicular_to_camera(self.frame)
        label = Text("you", font_size=24)
        # label = Text("Photo", font_size=24).set_backstroke(BLACK, 5)
        label.rotate(PI / 2, RIGHT)
        label.next_to(vect.get_center(), OUT + LEFT, buff=0)

        self.play(
            ShowCreation(vect),
            FadeIn(label, vect.get_vector())
        )
        self.wait(5)

        # Many directions -> Different kinds of meaning
        ideas = VGroup(
            Text("Part of a command"),
            Text("Affectionate"),
            Text("Sadness"),
        )
        ideas.set_backstroke(BLACK, 3)
        ideas.scale(0.35)
        ideas.rotate(PI / 2, RIGHT)

        last_idea = VGroup()
        last_direction = 1.0 * normalize(cross(RIGHT, vect.get_vector()))
        for idea in ideas:
            direction = rotate_vector(last_direction, PI / 3, vect.get_vector())
            new_vect = self.get_added_vector(vect, direction)
            new_vect.set_perpendicular_to_camera(self.frame)
            idea.next_to(new_vect.get_center(), buff=0.1)
            lines = get_direction_lines(axes, new_vect.get_vector(), color=new_vect.get_color())
            self.play(
                FadeOut(last_idea),
                ShowCreation(new_vect),
                FadeIn(idea, new_vect.get_vector()),
                LaggedStartMap(ShowCreationThenFadeOut, lines, lag_ratio=2 / len(lines), run_time=2)
            )
            self.wait(1)
            last_idea = VGroup(new_vect, idea)
            last_direction = direction
        self.play(FadeOut(last_idea))
        self.wait(5)

        # Specific ideas added onto "you"
        ideas = VGroup(
            # Text("Astronaut"),
            # Text("Riding a Horse"),
            # Text("On the moon"),
            #
            Text("needs an adjective next"),
            Text("preceded by \"that which does not kill\""),
            Text("related to growth and strength"),
            #
            # Text("River bank"),
            # Text("Beginning of a story"),
            # Text("Establishing a setting"),
        )
        ideas.scale(0.4)
        ideas.rotate(PI / 2, RIGHT)
        directions = [
            (-0.25, -1, 0.75),
            (-0.5, -0.25, 0.5),
            (1.0, -0.5, 1.0),
        ]
        orientations = [
            (11, 92, 0, (2.69, 0.55, 1.12), 6.25),
            (-8, 83, 0, (2.73, 0.56, 1.24), 6.80),
            (-14, 79, 0, (2.49, 0.61, 1.41), 7.64),
        ]

        vects = VGroup(vect)
        concepts = VGroup(label)
        for idea, direction, orientation in zip(ideas, directions, orientations):
            point = vects[-1].get_end()
            new_vect = self.get_added_vector(vects[-1], direction)
            new_vect.always.set_perpendicular_to_camera(self.frame)
            idea.next_to(new_vect.get_center())
            self.play(
                frame.animate.reorient(*orientation),
                GrowArrow(new_vect),
                FadeIn(idea, 0.5 * new_vect.get_vector())
            )
            self.wait(2)
            vects.add(new_vect)
        self.wait(15)

    def add_plane_and_axes(
        self,
        x_range=(-4, 4),
        y_range=(-4, 4),
        z_range=(-3, 3),
    ):
        axes = ThreeDAxes(x_range, y_range, z_range)
        plane = NumberPlane(
            x_range, y_range,
            background_line_style=dict(
                stroke_color=GREY_D,
                stroke_width=1
            ),
            faded_line_ratio=1,
        )
        plane.axes.set_stroke(GREY_D, 0)

        self.add(plane, axes)
        return plane, axes

    def get_added_vector(self, last_vect, direction):
        point = last_vect.get_end()
        new_vect = Arrow(point, point + direction, buff=0)
        new_vect.set_color(random_bright_color())
        new_vect.set_flat_stroke(False)
        return new_vect


class MJSpace(SimpleSpaceExample):
    def construct(self):
        # Set up axes
        frame = self.frame
        plane, axes = self.add_plane_and_axes()
        axes.set_stroke(width=1)
        frame.add_ambient_rotation()

        # Show vectors landing in the space
        sentence = Text("Michael Jordan plays the sport of basketball", font_size=36)
        sentence.to_edge(UP)
        tokens = break_into_tokens(sentence)
        token_rects = get_piece_rectangles(tokens, leading_spaces=True, h_buff=0)
        arrs = VGroup(
            NumericEmbedding().scale(0.25).next_to(rect, DOWN, buff=1.0)
            for rect in token_rects
        )
        arrows = VGroup(Arrow(rect, arr, buff=0.1) for rect, arr in zip(token_rects, arrs))
        vects = VGroup(
            Vector(np.random.uniform(-3, 3, 3))
            for arr in arrs
        )
        vects.set_stroke(GREY_B)
        vects.fix_in_frame()

        VGroup(token_rects, tokens, arrows, arrs).fix_in_frame()

        frame.reorient(-18, 86, 0, (0.21, 0.12, 3.56), 11.65)
        self.add(token_rects, tokens)
        self.play(
            LaggedStartMap(FadeIn, arrs, shift=DOWN, lag_ratio=0.1),
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            frame.animate.reorient(11, 76, 0, ORIGIN, FRAME_HEIGHT),
            FadeOut(VGroup(token_rects, tokens, arrows), UP, time_span=(1, 2)),
            LaggedStart(
                (Transform(arrow, vect)
                for arrow, vect in zip(arrs, vects)),
                lag_ratio=0.05,
            ),
            run_time=3
        )
        self.remove(arrs)
        self.add(vects)
        self.wait()
        self.play(LaggedStart(
            (vect.animate.scale(0, about_point=vect.get_start())
            for vect in vects),
            lag_ratio=0.05,
            remover=True
        ))

        # Show three directions
        colors = [YELLOW, RED, "#F88158"]
        all_coords = [normalize([-1, -1, 1])]
        all_coords.append(normalize(cross(all_coords[0], IN)))
        all_coords.append(-normalize(cross(all_coords[0], all_coords[1])))
        all_coords = np.array(all_coords)[[0, 2, 1]]
        labels = VGroup(*map(Text, ["First Name Michael", "Last Name Jordan", "Basketball"]))
        label_directions = [LEFT + OUT, IN, RIGHT + OUT]

        vect_groups = VGroup()
        vects = VGroup()
        for coords, label, color, direction in zip(all_coords, labels, colors, label_directions):
            vect = Vector(2.0 * coords)
            vect.set_color(color)
            vect.always.set_perpendicular_to_camera(self.frame)
            label.scale(0.5)
            label.rotate(PI / 2, RIGHT)
            label.set_color(color)
            label.next_to(vect.get_end(), direction, buff=0.1)
            label.set_fill(border_width=0.5)
            label.set_backstroke(BLACK, 4)
            vects.add(vect)
            vect_groups.add(VGroup(vect, label))

        orientations = [
            (17, 76, 0),
            (17, 80, 0),
            (-16, 77, 0),
        ]

        for vect, label, orientation in zip(vects, labels, orientations):
            lines = get_direction_lines(axes, vect.get_vector(), color=vect.get_color())
            self.play(
                GrowArrow(vect),
                FadeIn(label, vect.get_vector()),
                frame.animate.reorient(*orientation),
            )
            self.play(
                LaggedStartMap(ShowCreationThenFadeOut, lines, lag_ratio=2 / len(lines))
            )
            self.wait(2)

        # Bring in "plucked out" vector
        emb_coords = 2.0 * all_coords[:2].sum(0)
        emb = Vector(emb_coords)
        emb.always.set_perpendicular_to_camera(self.frame)
        emb.set_flat_stroke(False)
        emb_label = Tex(R"\vec{\textbf{E}}", font_size=30)
        emb_label.rotate(89 * DEGREES, RIGHT)
        emb_label.add_updater(lambda m: m.move_to(1.1 * emb.get_end()))
        emb_label.suspend_updating()

        self.play(
            frame.animate.reorient(7, 66, 0).set_anim_args(run_time=2),
            FadeIn(emb, shift=2 * (IN + LEFT)),
            FadeIn(emb_label, shift=2 * (IN + LEFT)),
        )
        self.wait()

        # Set up dot product display
        def get_proj_point(vect1, vect2):
            v1 = vect1.get_end()
            v2 = vect2.get_end()
            return v2 * np.dot(v1, v2) / np.dot(v2, v2)

        def get_dot_product_lines(vect, proj_line_color=GREY_A):
            dashed_line = always_redraw(
                lambda: Line(emb.get_end(), get_proj_point(emb, vect)).set_stroke(WHITE, 2).set_anti_alias_width(10)
            )
            proj_line = always_redraw(
                lambda: Line(ORIGIN, get_proj_point(emb, vect)).set_stroke(proj_line_color, width=4, opacity=0.75)
            )
            return dashed_line, proj_line

        m_dashed_line, m_proj_line = get_dot_product_lines(vects[0])

        formula = Tex(R"\vec{\textbf{E}} \cdot \big(\overrightarrow{\text{First Name Michael}}\big) = ", font_size=36)
        formula[3:-1].set_color(YELLOW)
        formula.to_corner(UL)
        formula.fix_in_frame()
        rhs = DecimalNumber(font_size=42)
        rhs.fix_in_frame()
        rhs.next_to(formula[-1], RIGHT, buff=0.15)
        rhs.target_vect = vects[0]
        rhs.add_updater(lambda m: m.set_value(np.dot(m.target_vect.get_end(), emb.get_end()) / 4.0))

        m_proj_line.suspend_updating()
        self.play(
            ShowCreation(m_dashed_line),
            TransformFromCopy(Line(ORIGIN, emb.get_end(), flat_stroke=False), m_proj_line),
            FadeIn(formula, UP),
            vect_groups[1:].animate.set_opacity(0.25),
        )
        m_proj_line.resume_updating()
        self.play(
            TransformFromCopy(rhs.copy().unfix_from_frame().set_opacity(0).move_to(m_proj_line), rhs),
        )
        emb_label.resume_updating()
        for _ in range(2):
            self.play(
                emb.animate.put_start_and_end_on(ORIGIN, [-2.5, -2.0, -0.5]),
                rate_func=wiggle,
                run_time=5
            )
        self.wait(2)
        self.play(emb.animate.put_start_and_end_on(axes.get_origin(), 1.5 * all_coords[1:3].sum(0)), run_time=3)
        self.play(frame.animate.reorient(26, 68, 0), run_time=2 )
        self.play(emb.animate.put_start_and_end_on(ORIGIN, [1.0, -1.5, -1.0]), run_time=3)
        self.wait(2)
        self.play(
            frame.animate.reorient(-4, 73, 0),
            emb.animate.put_start_and_end_on(ORIGIN, emb_coords),
            run_time=3
        )
        self.wait(5)

        # Dotting against L.N. Jordan
        j_dashed_line, j_proj_line = get_dot_product_lines(vects[1])
        j_paren = Tex(R"\big(\overrightarrow{\text{Last Name Jordan}}\big) = ", font_size=36)
        j_paren[:-1].set_color(RED)
        m_paren = formula[3:]
        m_paren.fix_in_frame()
        j_paren.move_to(m_paren, LEFT)
        j_paren.fix_in_frame()
        rhs.target_vect = vects[1]

        self.play(
            frame.animate.reorient(15, 97, 0),
            FadeOut(m_paren, UP, time_span=(1, 2)),
            FadeIn(j_paren, UP, time_span=(1, 2)),
            rhs.animate.next_to(j_paren, RIGHT, buff=0.15).set_anim_args(time_span=(1, 2)),
            LaggedStart(
                vect_groups[0].animate.set_opacity(0.25),
                vect_groups[1].animate.set_opacity(1),
                FadeOut(m_dashed_line),
                FadeOut(m_proj_line),
                lag_ratio=0.25,
                run_time=2
            )
        )
        j_proj_line.suspend_updating()
        self.play(
            ShowCreation(j_dashed_line),
            TransformFromCopy(Line(ORIGIN, emb.get_end(), flat_stroke=False), j_proj_line),
        )
        j_proj_line.resume_updating()
        self.play(
            emb.animate.put_start_and_end_on(ORIGIN, [-1.5, -1.5, 0]).set_anim_args(run_time=3, rate_func=there_and_back)
        )
        self.wait()

        # Dotting against basketball
        b_dashed_line, b_proj_line = get_dot_product_lines(vects[2])
        b_paren = Tex(R"\big(\overrightarrow{\text{Basketball}}\big) = ", font_size=36)
        b_paren[:-1].set_color(vects[2].get_color())
        b_paren.move_to(m_paren, LEFT)
        b_paren.fix_in_frame()
        rhs.suspend_updating()

        self.play(
            frame.animate.reorient(2, 65, 0),
            FadeOut(j_paren, UP),
            FadeIn(b_paren, UP),
            rhs.animate.next_to(b_paren[-1], RIGHT, buff=0.2).set_value(0),
            FadeOut(j_dashed_line),
            FadeOut(j_proj_line),
            vect_groups[1].animate.set_opacity(0.25),
            vect_groups[2].animate.set_opacity(1.0),
        )
        self.wait()

        rhs.target_vect = vects[2]
        rhs.resume_updating()
        self.add(b_dashed_line, b_proj_line)
        self.play(
            emb.animate.put_start_and_end_on(ORIGIN, [0.6, -2.2, 0]),
            rate_func=there_and_back,
            run_time=6,
        )
        self.wait(3)

        # Emphasize dot products with first two names
        self.play(
            frame.animate.reorient(5, 85, 0).set_anim_args(run_time=2),
            FadeOut(formula[:3]),
            FadeOut(b_paren),
            FadeOut(rhs),
            FadeOut(b_dashed_line),
            FadeOut(b_proj_line),
            vect_groups[:2].animate.set_opacity(1),
            vect_groups[2].animate.set_opacity(0.25),
        )
        self.wait()
        self.play(
            ShowCreation(m_dashed_line),
            ShowCreation(m_proj_line),
        )
        self.wait()
        self.play(
            ShowCreation(j_dashed_line),
            ShowCreation(j_proj_line),
        )
        self.wait(20)
        self.play(
            *map(FadeOut, [j_dashed_line, j_proj_line, m_dashed_line, m_proj_line, emb, emb_label]),
        )

        # Show sum of the first two names
        j_vect_copy, m_vect_copy = vect_copies = vects[:2].copy()
        vect_copies.clear_updaters()
        vect_copies.set_stroke(opacity=0.5)
        j_vect_copy.shift(vects[1].get_vector())
        m_vect_copy.shift(vects[0].get_vector())
        emb.put_start_and_end_on(axes.get_origin(), m_vect_copy.get_end())

        self.play(frame.animate.reorient(-6, 78, 0), run_time=2)
        self.play(LaggedStart(
            TransformFromCopy(vects[1], m_vect_copy),
            TransformFromCopy(vects[0], j_vect_copy),
            lag_ratio=0.5
        ))
        self.play(GrowArrow(emb))
        self.wait(4)

        # Show the basketball direction
        self.play(
            *map(FadeOut, [m_vect_copy, j_vect_copy, emb])
        )
        self.play(
            frame.animate.reorient(-19, 77, 0, (1.32, -0.22, -0.12), 3.75),
            vect_groups[:2].animate.set_opacity(0.25),
            vect_groups[2][0].animate.set_opacity(1.0),
            vect_groups[2][1].animate.set_opacity(1.0),
            run_time=2
        )
        self.wait(20)
