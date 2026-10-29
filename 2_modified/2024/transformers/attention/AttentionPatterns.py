# ==============================================================================
# Scene:      AttentionPatterns
# Source:     videos/_2024/transformers/attention.py (lines 10-1449)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl AttentionPatterns.py AttentionPatterns -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Dalle3_fluffy.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
#   - _lib/assets/raster_images/Dalle3_blue.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
#   - _lib/assets/raster_images/Dalle3_creature.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
#   - _lib/assets/raster_images/Dalle3_verdant.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
#   - _lib/assets/raster_images/Dalle3_forest.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
#   - _lib/assets/raster_images/BlueFluff.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
#   - _lib/assets/raster_images/VerdantForest.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
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



# ----- From _2024/transformers/attention.py -----

class AttentionPatterns(InteractiveScene):
    def construct(self):
        # Add sentence
        phrase = " a fluffy blue creature roamed the verdant forest"
        phrase_mob = Text(phrase)
        phrase_mob.move_to(2 * UP)
        words = list(filter(lambda s: s.strip(), phrase.split(" ")))
        word2mob: Dict[str, VMobject] = {
            word: phrase_mob[" " + word][0]
            for word in words
        }
        word_mobs = VGroup(*word2mob.values())

        self.play(
            LaggedStartMap(FadeIn, word_mobs, shift=0.5 * UP, lag_ratio=0.25)
        )
        self.wait()

        # Create word rects
        word2rect: Dict[str, VMobject] = dict()
        for word in words:
            rect = SurroundingRectangle(word2mob[word])
            rect.set_height(phrase_mob.get_height() + SMALL_BUFF, stretch=True)
            rect.match_y(phrase_mob)
            rect.set_stroke(GREY, 2)
            rect.set_fill(GREY, 0.2)
            word2rect[word] = rect

        # Adjectives updating noun
        adjs = ["fluffy", "blue", "verdant"]
        nouns = ["creature", "forest"]
        others = ["a", "roamed", "the"]
        adj_mobs, noun_mobs, other_mobs = [
            VGroup(word2mob[substr] for substr in group)
            for group in [adjs, nouns, others]
        ]
        adj_rects, noun_rects, other_rects = [
            VGroup(word2rect[substr] for substr in group)
            for group in [adjs, nouns, others]
        ]
        adj_rects.set_submobject_colors_by_gradient(BLUE_C, BLUE_D, GREEN)
        noun_rects.set_color(GREY_BROWN).set_stroke(width=3)
        kw = dict()
        adj_arrows = VGroup(
            Arrow(
                adj_mobs[i].get_top(), noun_mobs[j].get_top(),
                path_arc=-150 * DEGREES, buff=0.1, stroke_color=GREY_B
            )
            for i, j in [(0, 0), (1, 0), (2, 1)]
        )

        self.play(
            LaggedStartMap(DrawBorderThenFill, adj_rects),
            Animation(adj_mobs),
        )
        self.wait()
        self.play(
            LaggedStartMap(DrawBorderThenFill, noun_rects),
            Animation(noun_mobs),
            LaggedStartMap(ShowCreation, adj_arrows, lag_ratio=0.2, run_time=1.5),
        )
        kw = dict(time_width=2, max_stroke_width=10, lag_ratio=0.2, path_arc=150 * DEGREES)
        self.play(
            ContextAnimation(noun_mobs[0], adj_mobs[:2], strengths=[1, 1], **kw),
            ContextAnimation(noun_mobs[1], adj_mobs[2:], strengths=[1], **kw),
        )
        self.wait()

        # Show embeddings
        all_rects = VGroup(*adj_rects, *noun_rects, *other_rects)
        all_rects.sort(lambda p: p[0])
        embeddings = VGroup(
            NumericEmbedding(length=10).set_width(0.5).next_to(rect, DOWN, buff=1.5)
            for rect in all_rects
        )
        emb_arrows = VGroup(
            Arrow(all_rects[0].get_bottom(), embeddings[0].get_top()).match_x(rect)
            for rect in all_rects
        )
        for index, vect in [(5, LEFT), (6, RIGHT)]:
            embeddings[index].shift(0.1 * vect)
            emb_arrows[index].shift(0.05 * vect)

        self.play(
            FadeIn(other_rects),
            Animation(word_mobs),
            LaggedStartMap(GrowArrow, emb_arrows),
            LaggedStartMap(FadeIn, embeddings, shift=0.5 * DOWN),
            FadeOut(adj_arrows)
        )
        self.wait()

        # Mention dimension of embedding
        frame = self.frame
        brace = Brace(embeddings[0], LEFT, buff=SMALL_BUFF)
        dim_value = Integer(12288)
        dim_value.next_to(brace, LEFT)
        dim_value.set_color(YELLOW)

        self.play(
            GrowFromCenter(brace),
            CountInFrom(dim_value, 0),
            frame.animate.move_to(LEFT)
        )
        self.wait()

        # Ingest meaning and and position
        images = Group(
            ImageMobject(f"Dalle3_{word}").set_height(1.1).next_to(word2rect[word], UP)
            for word in ["fluffy", "blue", "creature", "verdant", "forest"]
        )
        image_vects = VGroup(embeddings[i] for i in [1, 2, 3, 6, 7])

        self.play(
            LaggedStartMap(FadeIn, images, scale=2, lag_ratio=0.05)
        )
        self.play(
            LaggedStart(
                (self.bake_mobject_into_vector_entries(image, vect, group_type=Group)
                for image, vect in zip(images, image_vects)),
                group_type=Group,
                lag_ratio=0.2,
                run_time=4,
                remover=True
            ),
        )
        self.wait()
        self.add(embeddings, images)

        # Show positions
        pos_labels = VGroup(
            Integer(n, font_size=36).next_to(rect, DOWN, buff=0.1)
            for n, rect in enumerate(all_rects, start=1)
        )
        pos_labels.set_color(TEAL)

        self.play(
            LaggedStart(
                (arrow.animate.scale(0.7, about_edge=DOWN)
                for arrow in emb_arrows),
                lag_ratio=0.1,
            ),
            LaggedStartMap(FadeIn, pos_labels, shift=0.25 * DOWN, lag_ratio=0.1)
        )
        self.play(
            LaggedStart(
                (self.bake_mobject_into_vector_entries(pos, vect)
                for pos, vect in zip(pos_labels, embeddings)),
                lag_ratio=0.2,
                run_time=4,
                remover=True
            ),
        )
        self.wait()

        # Collapse vectors
        template = Tex(R"\vec{\textbf{E}}_{0}")
        template[0].scale(1.5, about_edge=DOWN)
        dec = template.make_number_changeable(0)
        emb_syms = VGroup()
        for n, rect in enumerate(all_rects, start=1):
            dec.set_value(n)
            sym = template.copy()
            sym.next_to(rect, DOWN, buff=0.75)
            sym.set_color(GREY_A)
            emb_syms.add(sym)
        for subgroup in [emb_syms[:4], emb_syms[4:]]:
            subgroup.arrange_to_fit_width(subgroup.get_width())

        emb_arrows.target = emb_arrows.generate_target()

        for rect, arrow, sym in zip(all_rects, emb_arrows.target, emb_syms):
            x_min = rect.get_x(LEFT)
            x_max = rect.get_x(RIGHT)
            low_point = sym[0].get_top()
            if x_min < low_point[0] < x_max:
                top_point = np.array([low_point[0], rect.get_y(DOWN), 0])
            else:
                top_point = rect.get_bottom()
            arrow.become(Arrow(top_point, low_point, buff=SMALL_BUFF))

        all_brackets = VGroup(emb.get_brackets() for emb in embeddings)
        for brackets in all_brackets:
            brackets.target = brackets.generate_target()
            brackets.target.stretch(0, 1, about_edge=UP)
            brackets.target.set_fill(opacity=0)

        ghost_syms = emb_syms.copy()
        ghost_syms.set_opacity(0)

        self.play(
            frame.animate.set_x(0).set_anim_args(run_time=2),
            LaggedStart(
                (AnimationGroup(
                    LaggedStart(
                        (FadeTransform(entry, sym)
                        for entry in embedding.get_columns()[0]),
                        lag_ratio=0.01,
                        group_type=Group
                    ),
                    MoveToTarget(brackets),
                    group_type=Group,
                )
                for sym, embedding, brackets in zip(ghost_syms, embeddings, all_brackets)),
                group_type=Group
            ),
            LaggedStartMap(FadeIn, emb_syms, shift=UP),
            brace.animate.stretch(0.25, 1, about_edge=UP).set_opacity(0),
            FadeOut(dim_value, 0.25 * UP),
            MoveToTarget(emb_arrows, lag_ratio=0.1, run_time=2),
            LaggedStartMap(FadeOut, pos_labels, shift=UP),
        )
        emb_arrows.refresh_bounding_box(recurse_down=True)  # Why?
        self.clear()
        self.add(emb_arrows, all_rects, word_mobs, images, emb_syms)
        self.wait()

        # Preview desired updates
        emb_sym_primes = VGroup(
            sym.copy().add(Tex("'").move_to(sym.get_corner(UR) + 0.05 * DL))
            for sym in emb_syms
        )
        emb_sym_primes.shift(2 * DOWN)
        emb_sym_primes.set_color(TEAL)

        full_connections = VGroup()
        for i, sym1 in enumerate(emb_syms, start=1):
            for j, sym2 in enumerate(emb_sym_primes, start=1):
                line = Line(sym1.get_bottom(), sym2.get_top(), buff=SMALL_BUFF)
                line.set_stroke(GREY_B, width=random.random()**2, opacity=random.random()**0.25)
                if (i, j) in [(2, 4), (3, 4), (4, 4), (7, 8), (8, 8)]:
                    line.set_stroke(WHITE, width=2 + random.random(), opacity=1)
                full_connections.add(line)

        blue_fluff = ImageMobject("BlueFluff")
        verdant_forest = ImageMobject("VerdantForest")
        for n, image in [(3, blue_fluff), (7, verdant_forest)]:
            image.match_height(images)
            image.scale(1.2)
            image.next_to(emb_sym_primes[n], DOWN, buff=MED_SMALL_BUFF)

        self.play(
            ShowCreation(full_connections, lag_ratio=0.01, run_time=2),
            LaggedStart(
                (TransformFromCopy(sym1, sym2)
                for sym1, sym2 in zip(emb_syms, emb_sym_primes)),
                lag_ratio=0.05,
            ),
        )
        self.wait()
        self.play(LaggedStart(
            LaggedStart(
                (FadeTransform(im.copy(), blue_fluff, remover=True)
                for im in images[:3]),
                lag_ratio=0.02,
                group_type=Group
            ),
            LaggedStart(
                (FadeTransform(im.copy(), verdant_forest, remover=True)
                for im in images[3:]),
                lag_ratio=0.02,
                group_type=Group
            ),
            lag_ratio=0.5,
            run_time=2
        ))
        self.add(blue_fluff, verdant_forest)
        self.wait()

        # Show black box that matrix multiples can be added to
        in_arrows = VGroup(
            Vector(0.25 * DOWN, max_width_to_length_ratio=12.0).next_to(sym, DOWN, SMALL_BUFF)
            for sym in emb_syms
        )
        box = Rectangle(15.0, 3.0)
        box.set_fill(GREY_E, 1)
        box.set_stroke(WHITE, 1)
        box.next_to(in_arrows, DOWN, SMALL_BUFF)
        out_arrows = in_arrows.copy()
        out_arrows.next_to(box, DOWN)

        self.play(
            FadeIn(box, 0.25 * DOWN),
            LaggedStartMap(FadeIn, in_arrows, shift=0.25 * DOWN, lag_ratio=0.025),
            LaggedStartMap(FadeIn, out_arrows, shift=0.25 * DOWN, lag_ratio=0.025),
            FadeOut(full_connections),
            emb_sym_primes.animate.next_to(out_arrows, DOWN, SMALL_BUFF),
            MaintainPositionRelativeTo(blue_fluff, emb_sym_primes),
            MaintainPositionRelativeTo(verdant_forest, emb_sym_primes),
            frame.animate.set_height(10).move_to(4 * UP, UP),
        )
        self.wait()

        # Clear the board
        self.play(
            frame.animate.set_height(8).move_to(2 * UP).set_anim_args(run_time=1.5),
            LaggedStartMap(FadeOut, Group(
                *images, in_arrows, box, out_arrows, emb_sym_primes,
                blue_fluff, verdant_forest,
            ), lag_ratio=0.1)
        )

        # Ask questions
        word_groups = VGroup(VGroup(*pair) for pair in zip(all_rects, word_mobs))
        for group in word_groups:
            group.save_state()
        q_bubble = SpeechBubble("Any adjectives\nin front of me?")
        q_bubble.move_tip_to(word2rect["creature"].get_top())

        a_bubbles = SpeechBubble("I am!", direction=RIGHT).replicate(2)
        a_bubbles[1].flip()
        a_bubbles[0].move_tip_to(word2rect["fluffy"].get_top())
        a_bubbles[1].move_tip_to(word2rect["blue"].get_top())

        self.play(
            FadeIn(q_bubble),
            word_groups[:3].animate.fade(0.75),
            word_groups[4:].animate.fade(0.75),
        )
        self.wait()
        self.play(LaggedStart(
            Restore(word_groups[1]),
            Restore(word_groups[2]),
            *map(Write, a_bubbles),
            lag_ratio=0.5
        ))
        self.wait()

        # Associate questions with vectors
        a_bubbles.save_state()
        q_arrows = VGroup(
            Vector(0.75 * DOWN).next_to(sym, DOWN, SMALL_BUFF)
            for sym in emb_syms
        )
        q_vects = VGroup(
            NumericEmbedding(length=7).set_height(2).next_to(arrow, DOWN)
            for arrow in q_arrows
        )
        question = q_bubble.content


        index = words.index("creature")
        q_vect = q_vects[index]
        q_arrow = q_arrows[index]
        self.play(LaggedStart(
            FadeOut(q_bubble.body, DOWN),
            question.animate.scale(0.75).next_to(q_vect, RIGHT),
            FadeIn(q_vect, DOWN),
            GrowArrow(q_arrow),
            frame.animate.move_to(ORIGIN),
            a_bubbles.animate.fade(0.5),
        ))
        self.play(
            self.bake_mobject_into_vector_entries(question, q_vect)
        )
        self.wait()

        # Label query vector
        brace = Brace(q_vect, LEFT, SMALL_BUFF)
        query_word = Text("Query")
        query_word.set_color(YELLOW)
        query_word.next_to(brace, LEFT, SMALL_BUFF)
        dim_text = Text("128-dimensional", font_size=36)
        dim_text.set_color(YELLOW)
        dim_text.next_to(brace, LEFT, SMALL_BUFF)
        dim_text.set_y(query_word.get_y(DOWN))

        self.play(
            GrowFromCenter(brace),
            FadeIn(query_word, 0.25 * LEFT),
        )
        self.wait()
        self.play(
            query_word.animate.next_to(dim_text, UP, SMALL_BUFF),
            FadeIn(dim_text, 0.1 * DOWN),
        )
        self.wait()

        # Show individual matrix product
        e_vect = NumericEmbedding(length=12)
        e_vect.match_width(q_vect)
        e_vect.next_to(q_vect, DR, buff=1.5)
        matrix = WeightMatrix(shape=(7, 12))
        matrix.match_height(q_vect)
        matrix.next_to(e_vect, LEFT)
        e_label_copy = emb_syms[index].copy()
        e_label_copy.next_to(e_vect, UP)
        q_vect.save_state()
        ghost_q_vect = NumericEmbedding(length=7).match_height(q_vect)
        ghost_q_vect.get_columns().set_opacity(0)
        ghost_q_vect.get_brackets().space_out_submobjects(1.75)
        ghost_q_vect.next_to(e_vect, RIGHT, buff=0.7)

        mat_brace = Brace(matrix, UP)
        mat_label = Tex("W_Q")
        mat_label.next_to(mat_brace, UP, SMALL_BUFF)
        mat_label.set_color(YELLOW)

        self.play(
            frame.animate.set_height(11).move_to(all_rects, UP).shift(0.35 * UP),
            FadeOut(a_bubbles),
            FadeInFromPoint(e_vect, emb_syms[index].get_center()),
            FadeInFromPoint(matrix, q_arrow.get_center()),
            TransformFromCopy(emb_syms[index], e_label_copy),
            FadeOut(q_vect),
            TransformFromCopy(q_vect, ghost_q_vect),
            MaintainPositionRelativeTo(question, q_vect),
        )
        self.play(
            GrowFromCenter(mat_brace),
            FadeIn(mat_label, 0.1 * UP),
        )
        self.remove(ghost_q_vect)
        eq, rhs = show_matrix_vector_product(self, matrix, e_vect)

        new_q_vect = rhs.deepcopy()
        new_q_vect.move_to(q_vect, LEFT)

        self.play(
            TransformFromCopy(rhs, new_q_vect, path_arc=PI / 2),
            question.animate.next_to(new_q_vect, RIGHT)
        )
        self.wait()

        # Collapse query vector
        q_sym_template = Tex(R"\vec{\textbf{Q}}_0", font_size=48)
        q_sym_template[0].scale(1.5, about_edge=DOWN)
        q_sym_template.set_color(YELLOW)
        subscript = q_sym_template.make_number_changeable(0)
        q_syms = VGroup()
        for n, arrow in enumerate(q_arrows, start=1):
            subscript.set_value(n)
            sym = q_sym_template.copy()
            sym.next_to(arrow, DOWN, SMALL_BUFF)
            q_syms.add(sym)

        mat_label2 = mat_label.copy()

        q_sym = q_syms[index]
        low_q_sym = q_sym.copy()
        low_q_sym.next_to(rhs, UP)

        self.play(LaggedStart(
            LaggedStart(
                (FadeTransform(entry, q_sym, remover=True)
                for entry in new_q_vect.get_columns()[0]),
                lag_ratio=0.01,
                group_type=Group,
            ),
            new_q_vect.get_brackets().animate.stretch(0, 1, about_edge=UP).set_opacity(0),
            FadeOutToPoint(query_word, q_sym.get_center()),
            FadeOutToPoint(dim_text, q_sym.get_center()),
            FadeOut(brace),
            question.animate.next_to(q_sym, DOWN),
            FadeIn(low_q_sym, UP),
            lag_ratio=0.1,
        ))
        self.remove(new_q_vect)
        self.add(q_sym)
        self.play(
            mat_label2.animate.scale(0.9).next_to(q_arrow, RIGHT, buff=0.15),
        )
        self.wait()

        # E to Q rects
        e_rects = VGroup(map(SurroundingRectangle, [emb_syms[index], e_vect]))
        q_rects = VGroup(map(SurroundingRectangle, [q_sym, rhs]))
        e_rects.set_stroke(TEAL, 3)
        q_rects.set_stroke(YELLOW, 3)
        self.play(ShowCreation(e_rects, lag_ratio=0.2))
        self.wait()
        self.play(Transform(e_rects, q_rects))
        self.wait()
        self.play(FadeOut(e_rects))

        # Add other query vectors
        remaining_q_arrows = VGroup(*q_arrows[:index], *q_arrows[index + 1:])
        remaining_q_syms = VGroup(*q_syms[:index], *q_syms[index + 1:])
        wq_syms = VGroup(
            Tex(R"W_Q", font_size=30).next_to(arrow, RIGHT, buff=0.1)
            for arrow in q_arrows
        )
        wq_syms.set_color(YELLOW)
        subscripts = VGroup(e_label_copy[-1], low_q_sym[-1][0])
        for subscript in subscripts:
            i_sym = Tex("i")
            i_sym.replace(subscript)
            i_sym.scale(0.75)
            i_sym.match_style(subscript)
            subscript.target = i_sym

        self.play(
            LaggedStartMap(GrowArrow, remaining_q_arrows),
            LaggedStartMap(FadeIn, remaining_q_syms, shift=0.1 * DOWN),
            ReplacementTransform(VGroup(mat_label2), wq_syms, lag_ratio=0.01, run_time=2),
            question.animate.shift(0.25 * DOWN),
            *map(Restore, word_groups),
            *map(MoveToTarget, subscripts),
        )
        self.wait()

        # Emphasize model weights
        self.play(
            LaggedStartMap(FlashAround, matrix.get_entries(), lag_ratio=1e-2),
            RandomizeMatrixEntries(matrix),
        )
        data_modifying_matrix(self, matrix, word_shape=(3, 8))
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, VGroup(
                matrix, mat_brace, mat_label,
                e_vect, e_label_copy, eq, rhs,
                low_q_sym
            ), shift=0.2 * DR)
        )
        self.wait()

        # Move question
        noun_q_syms = VGroup(q_syms[words.index(word)] for word in ["creature", "forest"])

        self.play(
            question.animate.shift(0.25 * DOWN).match_x(noun_q_syms)
        )

        noun_q_lines = VGroup(
            Line(question.get_corner(v), sym.get_corner(-v) + 0.25 * v)
            for sym, v in zip(noun_q_syms, [UL, UR])
        )
        noun_q_lines.set_stroke(GREY, 1)
        self.play(ShowCreation(noun_q_lines, lag_ratio=0))
        self.wait()

        # Set up keys
        key_word_groups = word_groups.copy()
        key_word_groups.arrange(DOWN, buff=0.75, aligned_edge=RIGHT)
        key_word_groups.next_to(q_syms, DL, buff=LARGE_BUFF)
        key_word_groups.shift(3.0 * LEFT)
        key_emb_syms = emb_syms.copy()

        k_sym_template = Tex(R"\vec{\textbf{K}}_0", font_size=48)
        k_sym_template[0].scale(1.5, about_edge=DOWN)
        k_sym_template.set_color(TEAL)
        subscript = k_sym_template.make_number_changeable(0)

        k_syms = VGroup()
        key_emb_arrows = VGroup()
        wk_arrows = VGroup()
        wk_syms = VGroup()
        for group, emb_sym, n in zip(key_word_groups, key_emb_syms, it.count(1)):
            emb_arrow = Vector(0.5 * RIGHT)
            emb_arrow.next_to(group, RIGHT, SMALL_BUFF)
            emb_sym.next_to(emb_arrow, RIGHT, SMALL_BUFF)
            wk_arrow = Vector(0.75 * RIGHT)
            wk_arrow.next_to(emb_sym, RIGHT)
            wk_sym = Tex("W_k", font_size=30)
            wk_sym.set_fill(TEAL, border_width=1)
            wk_sym.next_to(wk_arrow, UP)
            subscript.set_value(n)
            k_sym = k_sym_template.copy()
            k_sym.next_to(wk_arrow, RIGHT, buff=MED_SMALL_BUFF)

            key_emb_arrows.add(emb_arrow)
            wk_arrows.add(wk_arrow)
            wk_syms.add(wk_sym)
            k_syms.add(k_sym)

        self.remove(question, noun_q_lines)
        self.play(
            frame.animate.move_to(2.5 * LEFT + 2.75 * DOWN),
            TransformFromCopy(word_groups, key_word_groups),
            TransformFromCopy(emb_arrows, key_emb_arrows),
            TransformFromCopy(emb_syms, key_emb_syms),
            run_time=2,
        )
        self.play(
            LaggedStartMap(GrowArrow, wk_arrows),
            LaggedStartMap(FadeIn, wk_syms, shift=0.1 * UP),
        )
        self.play(LaggedStart(
            (TransformFromCopy(e_sym, k_sym)
            for e_sym, k_sym in zip(key_emb_syms, k_syms)),
            lag_ratio=0.05,
        ))
        self.wait()

        # Isolate examples
        fade_rects = VGroup(
            BackgroundRectangle(VGroup(key_word_groups[0], wk_syms[0], k_syms[0])),
            BackgroundRectangle(VGroup(key_word_groups[3:], wk_syms[3:], k_syms[3:])),
            BackgroundRectangle(wq_syms[2]),
            BackgroundRectangle(VGroup(word_groups[:3], q_syms[:3])),
            BackgroundRectangle(VGroup(word_groups[4:], q_syms[4:])),
        )
        fade_rects.set_fill(BLACK, 0.75)
        fade_rects.set_stroke(BLACK, 3, 1)
        q_bubble = SpeechBubble("Any adjectives\nin front of me?")
        q_bubble.flip(RIGHT)
        q_bubble.next_to(q_syms[3][-1], DOWN, SMALL_BUFF, LEFT)
        a_bubbles = SpeechBubble("I'm an adjective!\nI'm there!").replicate(2)
        a_bubbles[0].pin_to(k_syms[1])
        a_bubbles[1].pin_to(k_syms[2])
        a_bubbles[1].flip(RIGHT, about_edge=DOWN)
        a_bubbles[1].shift(0.5 * DOWN)

        self.add(fade_rects, word_groups[3])
        self.play(FadeIn(fade_rects))
        self.play(FadeIn(q_bubble, lag_ratio=0.1))
        self.play(FadeIn(a_bubbles, lag_ratio=0.05))
        self.wait()

        # Show example key matrix
        matrix = WeightMatrix(shape=(7, 12))
        matrix.set_width(5)
        matrix.next_to(k_syms, UP, buff=2.0, aligned_edge=RIGHT)
        mat_rect = SurroundingRectangle(matrix, buff=MED_SMALL_BUFF)
        lil_rect = SurroundingRectangle(wk_syms[1])
        lines = VGroup(
            Line(lil_rect.get_corner(v + UP), mat_rect.get_corner(v + DOWN))
            for v in [LEFT, RIGHT]
        )
        VGroup(mat_rect, lil_rect, *lines).set_stroke(GREY_A, 1)

        self.play(ShowCreation(lil_rect))
        self.play(
            ShowCreation(lines, lag_ratio=0),
            TransformFromCopy(lil_rect, mat_rect),
            FadeInFromPoint(matrix, lil_rect.get_center()),
        )
        self.wait()
        data_modifying_matrix(self, matrix, word_shape=(3, 8))
        self.play(
            LaggedStartMap(FadeOut, VGroup(matrix, mat_rect, lines, lil_rect), run_time=1)
        )
        self.play(
            LaggedStartMap(FadeOut, VGroup(q_bubble, *a_bubbles), lag_ratio=0.25)
        )
        self.wait()

        # Draw grid
        emb_arrows.refresh_bounding_box(recurse_down=True)
        q_groups = VGroup(
            VGroup(group[i] for group in [
                emb_arrows, emb_syms, wq_syms, q_arrows, q_syms
            ])
            for i in range(len(emb_arrows))
        )
        q_groups.target = q_groups.generate_target()
        q_groups.target.arrange_to_fit_width(12, about_edge=LEFT)
        q_groups.target.shift(0.25 * DOWN)

        word_groups.target = word_groups.generate_target()
        for word_group, q_group in zip(word_groups.target, q_groups.target):
            word_group.scale(0.7)
            word_group.next_to(q_group[0], UP, SMALL_BUFF)

        h_lines = VGroup()
        v_buff = 0.5 * (key_word_groups[0].get_y(DOWN) - key_word_groups[1].get_y(UP))
        for kwg in key_word_groups:
            h_line = Line(LEFT, RIGHT).set_width(20)
            h_line.next_to(kwg, UP, buff=v_buff)
            h_line.align_to(key_word_groups, LEFT)
            h_lines.add(h_line)

        v_lines = VGroup()
        h_buff = 0.5
        for q_group in q_groups.target:
            v_line = Line(UP, DOWN).set_height(14)
            v_line.next_to(q_group, LEFT, buff=h_buff, aligned_edge=UP)
            v_lines.add(v_line)
        v_lines.add(v_lines[-1].copy().next_to(q_groups.target, RIGHT, 0.5, UP))

        grid_lines = VGroup(*h_lines, *v_lines)
        grid_lines.set_stroke(GREY_A, 1)

        self.play(
            frame.animate.set_height(15, about_edge=UP).set_x(-2).set_anim_args(run_time=3),
            MoveToTarget(q_groups),
            MoveToTarget(word_groups),
            ShowCreation(h_lines, lag_ratio=0.2),
            ShowCreation(v_lines, lag_ratio=0.2),
            FadeOut(fade_rects),
        )

        # Take all dot products
        dot_prods = VGroup()
        for k_sym in k_syms:
            for q_sym in q_syms:
                square_center = np.array([q_sym.get_x(), k_sym.get_y(), 0])
                dot = Tex(R".", font_size=72)
                dot.move_to(square_center)
                dot.set_fill(opacity=0)
                dot_prod = VGroup(k_sym.copy(), dot, q_sym.copy())
                dot_prod.target = dot_prod.generate_target()
                dot_prod.target.arrange(RIGHT, buff=0.15)
                dot_prod.target.scale(0.65)
                dot_prod.target.move_to(square_center)
                dot_prod.target.set_fill(opacity=1)
                dot_prods.add(dot_prod)

        self.play(
            LaggedStartMap(MoveToTarget, dot_prods, lag_ratio=0.025, run_time=4)
        )
        self.wait()

        # Show grid of dots
        dots = VGroup(
            VGroup(Dot().match_x(q_sym).match_y(k_sym) for q_sym in q_syms)
            for k_sym in k_syms
        )
        for n, row in enumerate(dots, start=1):
            for k, dot in enumerate(row, start=1):
                dot.set_fill(GREY_C, 0.8)
                dot.set_width(random.random())
                dot.target = dot.generate_target()
                dot.target.set_width(0.1 + 0.2 * random.random())
                if (n, k) in [(2, 4), (3, 4), (7, 8)]:
                    dot.target.set_width(0.8 + 0.2 * random.random())
        flat_dots = VGroup(*it.chain(*dots))

        self.play(
            dot_prods.animate.set_fill(opacity=0.75),
            LaggedStartMap(GrowFromCenter, flat_dots)
        )
        self.wait()
        self.play(LaggedStartMap(MoveToTarget, flat_dots, lag_ratio=0.01))
        self.wait()

        # Resize to reflect true pattern
        k_groups = VGroup(
            VGroup(group[i] for group in [
                key_word_groups, key_emb_arrows,
                key_emb_syms, wk_syms, wk_arrows, k_syms
            ])
            for i in range(len(emb_arrows))
        )
        for q_group, word_group in zip(q_groups, word_groups):
            q_group.add_to_back(word_group)
        self.add(k_groups, q_groups, Point())

        k_fade_rects = VGroup(map(BackgroundRectangle, k_groups))
        q_fade_rects = VGroup(map(BackgroundRectangle, q_groups))
        for rect in (*k_fade_rects, *q_fade_rects):
            rect.scale(1.05)
            rect.set_fill(BLACK, 0.8)

        self.play(
            frame.animate.move_to([-4.33, -2.4, 0.0]).set_height(9.52),
            FadeIn(k_fade_rects[:1]),
            FadeIn(k_fade_rects[3:]),
            FadeIn(q_fade_rects[:3]),
            FadeIn(q_fade_rects[4:]),
            run_time=2
        )
        self.wait()

        k_rects = VGroup(map(SurroundingRectangle, k_groups[1:3]))
        k_rects.set_stroke(TEAL, 2)
        q_rects = VGroup(SurroundingRectangle(q_groups[3]))
        q_rects.set_stroke(YELLOW, 2)

        self.play(
            ShowCreation(k_rects, lag_ratio=0.5, run_time=2),
            LaggedStartMap(
                FlashAround, k_groups[1:3],
                color=TEAL,
                time_width=2,
                lag_ratio=0.25,
                run_time=3
            ),
        )
        self.wait()
        self.play(TransformFromCopy(k_rects, q_rects))
        self.wait()

        # Show numerical dot product
        high_dot_prods = VGroup(dot_prods[8 + 3], dot_prods[2 * 8 + 3])
        dots_to_grow = VGroup(dots[1][3], dots[2][3])
        numerical_dot_prods = VGroup(
            VGroup(
                DecimalNumber(
                    np.random.uniform(-100, 10),
                    include_sign=True,
                    font_size=42,
                    num_decimal_places=1,
                    edge_to_fix=ORIGIN,
                ).move_to(dot)
                for dot in row
            )
            for row in dots
        )
        for n, row in enumerate(numerical_dot_prods):
            row[n].set_value(5 * random.random())  # Add some self relevance
        flat_numerical_dot_prods = VGroup(*it.chain(*numerical_dot_prods))
        for ndp in flat_numerical_dot_prods:
            ndp.set_fill(interpolate_color(RED_E, GREY_C, random.random()))
        high_numerical_dot_prods = VGroup(
            numerical_dot_prods[1][3],
            numerical_dot_prods[2][3],
            numerical_dot_prods[6][7],
        )
        for hdp in high_numerical_dot_prods:
            hdp.set_value(92 + 2 * random.random())
            hdp.set_color(WHITE)
        low_numerical_dot_prod = numerical_dot_prods[5][3]
        low_numerical_dot_prod.set_value(-31.4)
        low_numerical_dot_prod.set_fill(RED_D)

        self.play(
            *(dtg.animate.scale(1.25) for dtg in dots_to_grow),
            *(CountInFrom(ndp, run_time=1) for ndp in high_numerical_dot_prods[:2]),
            *(VFadeIn(ndp) for ndp in high_numerical_dot_prods[:2]),
            *(FadeOut(dot_prod, run_time=0.5) for dot_prod in dot_prods),
        )
        self.wait()

        # Show "attends to"
        att_arrow = Arrow(k_rects.get_top(), q_rects.get_left(), path_arc=-90 * DEGREES)
        att_words = TexText("``Attends to''", font_size=72)
        att_words.next_to(att_arrow.pfp(0.4), UL)

        self.play(
            ShowCreation(att_arrow),
            Write(att_words),
        )
        self.wait()
        self.play(FadeOut(att_words), FadeOut(att_arrow))

        # Contrast with "the" and "creature"
        self.play(
            frame.animate.move_to([-2.79, -3.66, 0.0]).set_height(12.29),
            *(k_rect.animate.surround(k_groups[5]) for k_rect in k_rects),
            FadeIn(k_fade_rects[1:3]),
            FadeOut(k_fade_rects[5]),
            run_time=2,
        )
        self.play(
            CountInFrom(low_numerical_dot_prod),
            VFadeIn(low_numerical_dot_prod),
            FadeOut(dots[5][3]),
        )
        self.wait()

        # Zoom out on full grid
        self.play(
            frame.animate.move_to([-1.5, -4.8, 0.0]).set_height(15).set_anim_args(run_time=3),
            LaggedStart(
                FadeOut(k_rects),
                FadeOut(q_rects),
                FadeOut(k_fade_rects[:5]),
                FadeOut(k_fade_rects[6:]),
                FadeOut(q_fade_rects[:3]),
                FadeOut(q_fade_rects[4:]),
                FadeOut(dots),
                LaggedStartMap(FadeIn, numerical_dot_prods),
                Animation(high_numerical_dot_prods.copy(), remover=True),
                Animation(low_numerical_dot_prod.copy(), remover=True),
            )
        )
        self.wait()

        # Focus on one column
        ndp_columns = VGroup(
            VGroup(row[i] for row in numerical_dot_prods)
            for i in range(len(numerical_dot_prods[0]))
        )
        col_rect = SurroundingRectangle(ndp_columns[3], buff=0.25)
        col_rect.set_stroke(YELLOW, 2)
        weight_words = Text("We want these to\nact like weights", font_size=96)
        weight_words.set_backstroke(BLACK, 8)
        weight_words.next_to(col_rect, RIGHT, buff=MED_LARGE_BUFF)
        weight_words.match_y(h_lines[2])

        index = words.index("creature")
        self.play(
            ShowCreation(col_rect),
            grid_lines.animate.set_stroke(opacity=0.5),
            ndp_columns[:index].animate.set_opacity(0.35),
            ndp_columns[index + 1:].animate.set_opacity(0.35),
            FadeIn(weight_words, lag_ratio=0.1)
        )
        self.wait()

        # Show softmax of each columns
        self.set_floor_plane("xz")
        col_arrays = [np.array([num.get_value() for num in col]) for col in ndp_columns]
        softmax_arrays = list(map(softmax, col_arrays))
        softmax_cols = VGroup(
            VGroup(DecimalNumber(v) for v in softmax_array)
            for softmax_array in softmax_arrays
        )
        sm_arrows = VGroup()
        sm_labels = VGroup()
        sm_rects = VGroup()
        for sm_col, col in zip(softmax_cols, ndp_columns):
            for sm_val, val in zip(sm_col, col):
                sm_val.move_to(val)
            sm_col.save_state()
            sm_col.shift(6 * OUT)
            sm_rect = SurroundingRectangle(sm_col)
            sm_rect.match_style(col_rect)
            VGroup(sm_col, sm_rect).rotate(30 * DEGREES, DOWN)
            arrow = Arrow(col, sm_col.get_center() + SMALL_BUFF * RIGHT + IN)
            label = Text("softmax", font_size=72)
            label.set_backstroke(BLACK, 5)
            label.rotate(90 * DEGREES, DOWN)
            label.next_to(arrow, UP)
            sm_arrows.add(arrow)
            sm_labels.add(label)
            sm_rects.add(sm_rect)

        index = words.index("creature")
        self.play(
            frame.animate.reorient(-47, -7, 0, (-2.48, -5.84, -1.09), 20),
            GrowArrow(sm_arrows[index], time_span=(1, 2)),
            FadeIn(sm_labels[index], lag_ratio=0.1, time_span=(1, 2)),
            TransformFromCopy(ndp_columns[index], softmax_cols[index], time_span=(1.5, 3)),
            TransformFromCopy(col_rect, sm_rects[index], time_span=(1.5, 3)),
            FadeOut(weight_words),
            run_time=3
        )
        self.wait()

        remaining_indices = [*range(index), *range(index + 1, len(ndp_columns))]
        last_index = index
        for index in remaining_indices:
            self.play(
                ndp_columns[last_index].animate.set_opacity(0.35),
                ndp_columns[index].animate.set_opacity(1),
                col_rect.animate.move_to(ndp_columns[index]),
                softmax_cols[last_index].animate.set_opacity(0.25),
                *map(FadeOut, [sm_rects[last_index], sm_arrows[last_index], sm_labels[last_index]]),
            )
            self.play(
                GrowArrow(sm_arrows[index]),
                FadeIn(sm_labels[index], lag_ratio=0.1),
                TransformFromCopy(ndp_columns[index], softmax_cols[index]),
                TransformFromCopy(col_rect, sm_rects[index]),
            )
            last_index = index

        self.play(
            FadeOut(col_rect),
            *map(FadeOut, [sm_rects[last_index], sm_arrows[last_index], sm_labels[last_index]]),
        )
        self.wait()
        self.play(
            frame.animate.reorient(0, 0, 0, (-2.64, -4.8, 0.0), 14.54),
            LaggedStartMap(Restore, softmax_cols, lag_ratio=0.1),
            FadeOut(ndp_columns, time_span=(0, 1.5)),
            run_time=3,
        )
        self.wait()

        # Label attention pattern
        for n, row in enumerate(dots):
            if n not in [3, 7]:
                row[n].set_width(0.7 + 0.2 * random.random())
        dots[1][3].set_width(0.6 + 0.1 * random.random())
        dots[2][3].set_width(0.6 + 0.1 * random.random())
        dots[6][7].set_width(0.9 + 0.1 * random.random())

        pattern_words = Text("Attention\nPattern", font_size=120)
        pattern_words.move_to(grid_lines, UL).shift(LEFT)

        self.play(
            FadeOut(softmax_cols, lag_ratio=0.001),
            FadeIn(dots, lag_ratio=0.001),
            Write(pattern_words),
            run_time=2
        )
        self.wait()

        # Preview masking
        masked_dots = VGroup()
        for n, row in enumerate(dots):
            masked_dots.add(*row[:n])
        mask_rects = VGroup()
        for dot in masked_dots:
            mask_rect = Square(0.5)
            mask_rect.set_stroke(RED, 2)
            mask_rect.move_to(dot)
            mask_rects.add(mask_rect)

        lag_ratio=1.0 / len(mask_rects)
        self.play(ShowCreation(mask_rects, lag_ratio=lag_ratio))
        self.play(
            LaggedStart(
                (dot.animate.scale(0) for dot in masked_dots),
                lag_ratio=lag_ratio
            )
        )
        self.play(
            FadeOut(mask_rects, lag_ratio=lag_ratio)
        )
        self.wait()

        # Set aside keys and queries
        pattern = VGroup(grid_lines, dots)
        for group in q_groups:
            group.sort(lambda p: -p[1])
            group.target = group.generate_target()
            m3 = len(group) - 3
            group.target[m3:].scale(0, about_edge=DOWN)
            group.target[:m3].move_to(group, DOWN)

        self.play(
            frame.animate.move_to((-2.09, -5.59, 0.0)).set_height(12.95).set_anim_args(run_time=3),
            LaggedStartMap(MoveToTarget, q_groups),
            FadeOut(pattern_words),
            v_lines.animate.stretch(0.95, 1, about_edge=DOWN),
        )
        self.play(
            LaggedStartMap(FadeOut, k_syms, shift=0.5 * DOWN, lag_ratio=0.1),
            LaggedStartMap(FadeOut, wk_syms, shift=0.5 * DOWN, lag_ratio=0.1),
        )
        self.wait()

        # Add values
        value_color = RED
        big_wv_sym = Tex(R"W_V", font_size=90)
        big_wv_sym.set_color(value_color)
        big_wv_sym.next_to(h_lines, UP, MED_LARGE_BUFF, LEFT)
        wv_word = Text("Value matrix", font_size=90)
        wv_word.next_to(big_wv_sym, UP, MED_LARGE_BUFF)
        wv_word.set_color(value_color)

        wv_arrows = wk_arrows
        v_sym_template = Tex(R"\vec{\textbf{V}}_{0}")
        v_sym_template[0].scale(1.5, about_edge=DOWN)
        v_sym_template.set_fill(value_color, border_width=1)
        subscript = v_sym_template.make_number_changeable("0")

        wv_syms = VGroup()
        v_syms = VGroup()
        for n, arrow in enumerate(wv_arrows, start=1):
            wv_sym = Tex("W_V", font_size=36)
            wv_sym.set_fill(value_color, border_width=1)
            wv_sym.next_to(arrow, UP, buff=0.2, aligned_edge=LEFT)
            subscript.set_value(n)
            v_sym = v_sym_template.copy()
            v_sym.next_to(arrow, RIGHT, MED_SMALL_BUFF)

            v_syms.add(v_sym)
            wv_syms.add(wv_sym)

        self.play(
            FadeIn(big_wv_sym, 0.5 * DOWN),
            FadeIn(wv_word, lag_ratio=0.1),
        )
        self.play(
            LaggedStart(
                (TransformFromCopy(big_wv_sym, wv_sym)
                for wv_sym in wv_syms),
                lag_ratio=0.15,
            ),
            run_time=3
        )
        self.play(
            LaggedStart(
                (TransformFromCopy(e_sym, v_sym)
                for e_sym, v_sym in zip(key_emb_syms, v_syms)),
                lag_ratio=0.15,
            ),
        )
        self.wait()
        self.play(
            FadeTransform(v_syms, k_syms),
            FadeTransform(wv_syms, wk_syms),
            rate_func=there_and_back_with_pause,
            run_time=3,
        )
        self.remove(k_syms, wk_syms)
        self.add(v_syms, wv_syms)
        self.wait()

        # Show column of weights
        index = words.index("creature")
        weighted_sum_cols = VGroup()
        for sm_col in softmax_cols:
            weighted_sum_col = VGroup()
            for weight, v_sym in zip(sm_col, v_syms):
                product = VGroup(weight, v_sym.copy())
                product.target = product.generate_target()
                product.target.arrange(RIGHT)
                product.target[1].shift(UP * (
                    product.target[0].get_y(DOWN) -
                    product.target[1][1].get_y(DOWN)
                ))
                product.target.scale(0.75)
                product.target.move_to(weight)
                product.target.set_fill(
                    opacity=clip(0.6 + weight.get_value(), 0, 1)
                )
                weighted_sum_col.add(product)
            weighted_sum_cols.add(weighted_sum_col)

        self.play(
            FadeOut(dots, lag_ratio=0.1),
            FadeIn(q_fade_rects[:index]),
            FadeIn(q_fade_rects[index + 1:]),
            FadeIn(softmax_cols[index]),
        )
        self.wait()
        self.play(
            LaggedStartMap(MoveToTarget, weighted_sum_cols[index])
        )
        self.wait()

        # Emphasize fluffy and blue weights
        rects = VGroup(
            key_word_groups[i][0].copy()
            for i in [1, 2]
        )
        alt_rects = VGroup(
            SurroundingRectangle(value, buff=SMALL_BUFF)
            for value in (* softmax_cols[index][:1], *softmax_cols[index][3:])
        )
        alt_rects.set_stroke(RED, 1)
        self.play(
            LaggedStart(
                (rect.animate.surround(value)
                for rect, value in zip(rects, softmax_cols[index][1:3])),
                lag_ratio=0.2,
            )
        )
        self.wait()
        self.play(Transform(rects, alt_rects))
        self.wait()
        self.play(FadeOut(rects, lag_ratio=0.1))

        # Show sum (Start re-rendering here, 151)
        emb_sym = emb_syms[index]
        ws_col = weighted_sum_cols[index]
        creature = images[2]
        creature.set_height(1.5)
        creature.next_to(word_groups[index], UP)

        emb_sym.target = emb_sym.generate_target()
        emb_sym.target.scale(1.25, about_edge=UP)
        sum_rect = SurroundingRectangle(emb_sym.target)
        sum_rect.set_stroke(YELLOW, 2)
        sum_rect.target = sum_rect.generate_target()
        sum_rect.target.surround(ws_col, buff=MED_SMALL_BUFF)
        plusses = VGroup()
        for m1, m2 in zip(ws_col, ws_col[1:]):
            plus = Tex(R"+", font_size=72)
            plus.move_to(midpoint(m1.get_bottom(), m2.get_top()))
            plusses.add(plus)

        self.play(
            frame.animate.reorient(0, 0, 0, (-2.6, -4.79, 0.0), 15.07).set_anim_args(run_time=2),
            MoveToTarget(emb_sym),
            ShowCreation(sum_rect),
            FadeIn(creature, UP),
            FadeOut(wv_word),
            FadeOut(big_wv_sym),
        )
        self.add(Point(), q_fade_rects[index + 1:])  # Hack
        self.wait()
        self.play(
            frame.animate.reorient(0, 0, 0, (-2.9, -6.5, 0.0), 19).set_anim_args(run_time=2),
            MoveToTarget(sum_rect, run_time=2),
            Write(plusses),
        )
        self.wait()

        # Show Delta E
        low_eqs = VGroup(
            Tex("=", font_size=72).rotate(PI / 2).next_to(wsc[-1].target, DOWN, buff=0.5)
            for wsc in weighted_sum_cols
        )
        low_eqs.set_color(YELLOW)
        delta_Es = VGroup()
        for emb_sym, eq in zip(emb_syms, low_eqs):
            delta = Tex(R"\Delta")
            delta.match_height(emb_sym[1])
            delta.next_to(emb_sym[1], LEFT, buff=0, aligned_edge=DOWN)
            delta_E = VGroup(delta, emb_sym.copy())
            delta_E.set_color(YELLOW)
            delta_E.set_height(0.8)
            delta_E.next_to(eq, DOWN)
            delta_Es.add(delta_E)

        self.play(
            LaggedStart(
                (FadeTransform(term.copy(), delta_Es[index])
                for term in weighted_sum_cols[index]),
                lag_ratio=0.05,
                group_type=Group
            ),
            Write(low_eqs[index])
        )
        self.wait()

        # Add Delta E
        creature_group = Group(creature, q_groups[index]).copy()
        creature_group.target = creature_group.generate_target()
        creature_group.target.scale(1.5)
        creature_group.target.next_to(h_lines, RIGHT, buff=4.0)
        creature_group.target.align_to(creature, UP)
        right_plus = Tex("+", font_size=96)
        right_eq = Tex("=", font_size=120).rotate(PI / 2)
        right_plus.next_to(creature_group.target, DOWN)
        creature_delta_E = delta_Es[index].copy()
        creature_delta_E.target = creature_delta_E.generate_target()
        creature_delta_E.target.set_height(1.0)
        creature_delta_E.target.next_to(right_plus, DOWN)
        right_eq.next_to(creature_delta_E.target, DOWN, MED_LARGE_BUFF)
        E_prime = emb_sym_primes[index].copy()
        E_prime.set_height(1.25)
        E_prime.next_to(right_eq, DOWN, MED_LARGE_BUFF)
        blue_fluff.set_height(2.5)
        blue_fluff.next_to(E_prime, DOWN, MED_LARGE_BUFF)

        self.play(LaggedStart(
            frame.animate.reorient(0, 0, 0, (4.96, -5.61, 0.0), 19.00),
            MoveToTarget(creature_group),
            FadeTransform(sum_rect.copy(), right_plus),
            MoveToTarget(creature_delta_E),
            run_time=2,
            lag_ratio=0.1
        ))
        self.wait()
        self.play(
            FadeTransform(creature_group[1][-4].copy(), E_prime),
            FadeTransform(creature_delta_E.copy(), E_prime),
            Write(right_eq),
            FadeTransform(creature_group[0].copy(), blue_fluff, path_arc=-PI / 2, run_time=2)
        )
        self.wait()

        right_sum_group = Group(
            creature_group, right_plus, creature_delta_E,
            right_eq, E_prime, blue_fluff
        )

        # Show all column sums
        plus_groups = VGroup(
            plusses.copy().match_x(col[0].target)
            for col in weighted_sum_cols
        )
        plus_groups.set_fill(GREY_C, 1)

        for col in softmax_cols:
            for value in col:
                value.set_fill(
                    opacity=clip(0.6 + value.get_value(), 0, 1)
                )

        self.play(LaggedStart(
            right_sum_group.animate.fade(0.75),
            FadeOut(sum_rect),
            FadeOut(creature),
            FadeOut(q_fade_rects[:index]),
            FadeOut(q_fade_rects[index + 1:]),
            FadeIn(softmax_cols[:index]),
            FadeIn(softmax_cols[index + 1:]),
            plusses.animate.set_fill(GREY_C, 1),
            run_time=2,
        ))
        self.play(
            LaggedStart(
                (LaggedStartMap(MoveToTarget, col)
                for col in weighted_sum_cols),
                lag_ratio=0.1
            ),
            v_lines.animate.set_stroke(GREY_A, 4, 1),
            *(
                e_sym.animate.scale(1.25, about_edge=UP)
                for e_sym in (*emb_syms[:index], *emb_syms[index + 1:])
            ),
        )

        other_indices = [*range(index), *range(index + 1, len(plus_groups))]
        self.play(LaggedStart(
            (LaggedStart(
                FadeIn(plus_groups[j], lag_ratio=0.1),
                Write(low_eqs[j]),
                LaggedStart(
                    (FadeTransform(ws.copy(), delta_Es[j])
                    for ws in weighted_sum_cols[j]),
                    lag_ratio=0.05,
                    group_type=Group
                ),
                lag_ratio=0.05,
            )
            for j in other_indices),
            lag_ratio=0.1,
            group_type=Group
        ))
        self.wait()

        # Add all deltas to embeddings
        equations = VGroup()
        equation_targets = VGroup()
        for E, dE, Ep in zip(emb_syms.copy(), delta_Es.copy(), emb_sym_primes):
            Ep.match_height(E)
            plus = Tex("+", font_size=96)
            eq = Tex("=", font_size=96).rotate(PI / 2)
            equation = VGroup(E, plus, dE, eq, Ep)
            equation.target = equation.generate_target()
            for mob in equation.target[::2]:
                mob.set_height(0.8)
            equation.target.arrange(DOWN)
            for mob in [Ep, plus, eq]:
                mob.set_opacity(0)
                mob.move_to(dE)
            equations.add(equation)
            equation_targets.add(equation.target)

        equation_targets.scale(1.25)
        equation_targets.arrange(RIGHT, buff=0.75)
        equation_targets.next_to(h_lines, RIGHT, buff=1.5)
        equation_targets.match_y(h_lines)

        self.play(
            frame.animate.reorient(0, 0, 0, (9.5, -7.17, 0.0), 20.33),
            LaggedStartMap(MoveToTarget, equations, lag_ratio=0.05),
            FadeTransform(right_sum_group, equation_targets[index]),
            run_time=2.0
        )
        self.wait()

        result_rect = SurroundingRectangle(
            VGroup(eq[-1] for eq in equations),
            buff=0.25
        )
        result_rect.set_stroke(TEAL, 3)
        self.play(
            ShowCreation(result_rect)
        )
        self.wait()

    def bake_mobject_into_vector_entries(self, mob, vector, path_arc=30 * DEGREES, group_type=None):
        entries = vector.get_entries()
        mob_copies = mob.replicate(len(entries))
        return AnimationGroup(
            LaggedStart(
                (FadeOutToPoint(mc, entry.get_center(), path_arc=path_arc)
                for mc, entry in zip(mob_copies, entries)),
                lag_ratio=0.05,
                group_type=group_type,
                run_time=2,
                remover=True
            ),
            RandomizeMatrixEntries(
                vector,
                rate_func=lambda t: clip(smooth(2 * t - 1), 0, 1),
                run_time=2
            ),
        )

    def scrap():
        # To be inserted after Show grid of dots sections
        self.remove(dot_prods)
        np.random.seed(time.gmtime().tm_sec)
        pattern = np.random.normal(0, 1, (8, 8))
        for n in range(len(pattern[0])):
            pattern[:, n][n + 1:] = -np.inf
            pattern[:, n] = softmax(pattern[:, n])
        for row, arr in zip(dots, pattern):
            for dot, value in zip(row, arr):
                dot.set_width(value**0.5)
        dots.set_fill(GREY_B, 1)
        return

        ### To be inserted in "Show softmax" section
        np.random.seed(time.gmtime().tm_sec)
        softmax_arrays = np.random.normal(0, 1, (8, 8))
        for n in range(len(softmax_arrays[0])):
            softmax_arrays[:, n][n + 1:] = -np.inf
            softmax_arrays[:, n] = softmax(softmax_arrays[:, n])
        softmax_arrays = softmax_arrays.T
        ###

    def thumbnail():
        ### Thumbnail design, insert in the middle of softmax show columns ###
        self.remove(q_groups)
        self.add(q_syms)
        out_dots = VGroup()
        for col in softmax_cols:
            for value in col:
                dot = Dot(radius=0.35)
                dot.move_to(value)
                dot.set_fill(WHITE, opacity=interpolate(0.1, 0.9, value.get_value()))
                out_dots.add(dot)
        out_dots.shift(2 * OUT)
        out_dots.set_stroke(WHITE, 2, 0.25)
        self.remove(softmax_cols)
        self.remove(sm_rects[last_index])
        self.add(out_dots)
        index = 3
        ndp_columns[-1].set_opacity(0.25)
        ndp_columns[index].set_opacity(1)
        sm_label_group = VGroup(sm_arrows[last_index], sm_labels[last_index])
        sm_label_group.match_x(ndp_columns[index])
        sm_label_group[1].scale(1.5, about_edge=DOWN)
        sm_label_group[1].set_fill(border_width=0)
        col_rect.match_x(ndp_columns[index])
        col_rect.set_flat_stroke(False)
        sm_col = col_rect.copy()
        # sm_col.set_width(out_dots[0].get_width() + 0.2)
        sm_col.match_z(out_dots)
        sm_col.set_flat_stroke(False)
        self.add(sm_col)
        self.remove(sm_labels[last_index])
        sm_arrows[last_index].set_stroke(width=10)
        sm_arrows[last_index].shift(OUT)

        grid_lines.set_stroke(WHITE, 2)
        v_lines.set_height(12, about_edge=DOWN, stretch=True)

        frame.set_field_of_view(35 * DEGREES)
        frame.reorient(-52, -2, 0, (-1.74, -7.1, -0.03), 14.72)
        ###

        ### To be inserted before Set aside keys and queries
        frame.move_to([-4.62, -5.04, 0.0]).set_height(14.5)
        self.remove(pattern_words)

        for dot in dots.family_members_with_points():
            value = dot.get_radius() / 0.5
            dot.set_fill(WHITE, opacity=value**0.75)
            dot.set_width(1)

        title = Text("Attention", font_size=250)
        title.set_fill(border_width=2)
        title.next_to(q_syms, LEFT, LARGE_BUFF, DOWN)
        title.shift(0.5 * UP)
        # self.add(title)

        q_syms.set_fill(border_width=1.5)
        k_syms.set_fill(border_width=1.5)
        for q in q_syms:
            q.scale(1.5, about_edge=DOWN)
        for k in k_syms:
            k.scale(1.5, about_edge=RIGHT)

        self.remove(word_groups, q_arrows, emb_arrows, emb_syms, wq_syms)
        VGroup(key_word_groups, key_emb_syms, key_emb_arrows, wk_arrows, wk_syms).shift(0.25 * LEFT)
