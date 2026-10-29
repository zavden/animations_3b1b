# ==============================================================================
# Scene:      RicherEmbedding
# Source:     videos/_2024/transformers/embedding.py (lines 2081-2227)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl RicherEmbedding.py RicherEmbedding -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

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



# ----- From _2024/transformers/embedding.py -----

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


def break_into_words(phrase_mob):
    offsets = [m.start() for m in re.finditer(" ", phrase_mob.get_string())]
    return break_into_pieces(phrase_mob, [0, *offsets])


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


class RicherEmbedding(InteractiveScene):
    def construct(self):
        # Add phrase
        phrase = Text("The King doth wake tonight and takes his rouse ...")
        phrase.to_edge(UP)
        words = break_into_words(phrase)
        rects = get_piece_rectangles(words)
        king_index = 1

        words.fix_in_frame()
        rects.fix_in_frame()

        self.add(words)

        # Setup axes
        self.set_floor_plane("xz")
        frame = self.frame
        frame.reorient(9, -6, 0)
        axes = ThreeDAxes((-5, 5), (-2, 2), (-5, 5))
        axes.shift(DOWN)
        plane = NumberPlane(
            (-5, 5), (-5, 5),
            background_line_style=dict(stroke_width=1, stroke_color=BLUE_E),
            faded_line_ratio=1,
        )
        plane.axes.set_stroke(GREY)
        plane.set_flat_stroke(False)
        plane.rotate(PI / 2, RIGHT)
        plane.move_to(axes)

        self.add(axes)
        self.add(plane)

        # Embed the word
        king_rect = rects[king_index]
        vector = Vector([-1, 1, 1])
        vector.shift(axes.get_origin())
        vector.match_color(king_rect)
        vector.set_flat_stroke(False)
        label = Text("King", font_size=24)
        label.next_to(vector.get_end(), normalize(vector.get_vector()), buff=0.1)

        self.play(DrawBorderThenFill(king_rect))
        self.play(
            TransformFromCopy(words[king_index], label),
            GrowArrow(vector),
        )
        self.wait(3)

        # Mention position
        index_labels = VGroup(*(
            Integer(n + 1, font_size=36).next_to(rect, DOWN, buff=0.2)
            for n, rect in enumerate(rects)
        ))
        index_labels.fix_in_frame()
        idx_vect, idx_label = self.get_added_vector(
            vector.get_end(), 0.5 * (RIGHT + OUT), "Pos. 2", TEAL,
            next_to_direction=UP,
            font_size=16
        )
        idx_label.rotate(45 * DEGREES, DOWN)
        idx_label.set_backstroke(BLACK, 1)

        self.play(
            LaggedStartMap(FadeIn, index_labels, shift=0.5 * DOWN),
        )
        self.play(
            TransformFromCopy(index_labels[king_index].set_backstroke(), idx_label),
            GrowArrow(idx_vect),
            frame.animate.reorient(-28, -22, 0).set_anim_args(run_time=3)
        )
        self.play(
            frame.animate.reorient(-11, -4, 0),
            LaggedStartMap(FadeOut, index_labels, lag_ratio=0.05, shift=0.5 * DOWN, time_span=(6, 7)),
            run_time=7
        )

        # Show king ingesting context
        self.play(
            LaggedStart(*(
                ContextAnimation(
                    words[king_index],
                    [*words[:king_index], *words[king_index + 1:]],
                    direction=DOWN,
                    fix_in_frame=True,
                    time_width=3,
                    min_stroke_width=3,
                    lag_ratio=0.05,
                    path_arc=PI / 3,
                )
                for n in range(3)
            ), lag_ratio=0.5),
            frame.animate.reorient(-5, -12, 0),
            run_time=5,
        )

        # Knock in many directions
        new_labeled_vector_args = [
            ([2, 1, 0], "lived in Scotland", None, DR),
            ([0, -1, -1], "murdered predecessor", None, RIGHT),
            ([-1.5, 1, -2], "in Shakespearean language", None, RIGHT),
        ]
        new_labeled_vects = VGroup()
        last_vect = idx_vect
        for args in new_labeled_vector_args:
            new_labeled_vects.add(self.get_added_vector(
                last_vect.get_end(), *args
            ))
            last_vect = new_labeled_vects[-1][0]
            last_vect.apply_depth_test()


        (vect1, label1), (vect2, label2), (vect3, label3) = new_labeled_vects
        self.play(
            GrowArrow(vect1),
            FadeIn(label1, 0.5 * DOWN),
            frame.animate.reorient(2, -16, 0, (0.6, -0.04, 0.02), 6.01).set_anim_args(run_time=8),
        )
        self.play(
            GrowArrow(vect2),
            FadeIn(label2, 0.5 * DOWN),
            frame.animate.reorient(35, -23, 0, (0.6, -0.04, 0.02), 6.01).set_anim_args(run_time=5),
        )
        self.play(
            GrowArrow(vect3),
            FadeIn(label3, 0.5 * DOWN),
            frame.animate.reorient(20, -29, 0, (0.61, 0.01, 0.0), 6.10).set_anim_args(run_time=5),
        )
        self.play(
            frame.animate.reorient(-19, -25, 0, (0.61, 0.01, 0.0), 6.10),
            run_time=5
        )

    def get_added_vector(self, curr_tip, direction, label, color=None, next_to_direction=UP, buff=0.1, font_size=24):
        if color is None:
            color = random_bright_color(hue_range=(0.45, 0.65))
        vect = Vector(direction)
        vect.set_color(color)
        vect.set_flat_stroke(False)
        vect.shift(curr_tip)
        text = Text(label, font_size=font_size)
        text.set_backstroke(BLACK, 4)
        text.next_to(vect.get_center(), next_to_direction, buff=buff)
        text.set_fill(border_width=0)

        result = VGroup(vect, text)
        return result
