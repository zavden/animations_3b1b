# ==============================================================================
# Scene:      KingQueenExample
# Source:     videos/_2024/transformers/embedding.py (lines 1107-1382)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl KingQueenExample.py KingQueenExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DATA_DIR now points to _lib/data (get_directories()["data"]) instead of Grant's output folder (GloVe, placeholder texts)
#   - get_principle_components: sign of each principal component fixed (negative sum), because eig returns it arbitrarily depending on LAPACK and the scene's cameras are tuned to Grant's signs (without this the vectors went off screen)
# ==============================================================================

from __future__ import annotations
import gensim
from pathlib import Path
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2024/transformers/helpers.py -----

# CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
DATA_DIR = Path(get_directories()["data"], "2024/transformers/data/")


if TYPE_CHECKING:
    from typing import Optional
    from manimlib.typing import Vect3, ManimColor


class LabeledArrow(Arrow):
    def __init__(
        self,
        *args,
        label_text: Optional[str] = None,
        font_size: float = 24,
        label_buff: float = 0.1,
        direction: Optional[Vect3] = None,
        label_rotation: float = PI / 2,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        if label_text is not None:
            start, end = self.get_start_and_end()
            label = Text(label_text, font_size=font_size)
            label.set_fill(self.get_color())
            label.set_backstroke()
            label.rotate(label_rotation, RIGHT)
            if direction is None:
                direction = normalize(end - start)
            label.next_to(end, direction, buff=label_buff)
            self.label = label
        else:
            self.label = None



# ----- From _2024/transformers/embedding.py -----

def get_principle_components(data, n_components=3):
    covariance_matrix = np.cov(data, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    order_of_importance = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, order_of_importance]  # sort the columns
    # CHANGE: eig returns each eigenvector with an arbitrary sign (depending on LAPACK) and the scene's cameras are tuned to Grant's signs; the sign is fixed so that each component sums negative
    sorted_eigenvectors = np.real(sorted_eigenvectors)
    sorted_eigenvectors = sorted_eigenvectors * -np.sign(sorted_eigenvectors.sum(axis=0))
    return sorted_eigenvectors[:, :n_components]


def get_word_to_vec_model(model_name="glove-wiki-gigaword-50"):
    filename = str(Path(DATA_DIR, model_name))
    if os.path.exists(filename):
        return gensim.models.keyedvectors.KeyedVectors.load(filename)
    model = gensim.downloader.load(model_name)
    model.save(filename)
    return model


class Word2VecScene(InteractiveScene):
    default_frame_orientation = (-30, 70)

    axes_config = dict(
        x_range=(-5, 5, 1),
        y_range=(-5, 5, 1),
        z_range=(-4, 4, 1),
        width=8,
        height=8,
        depth=6.4,
    )
    label_rotation = PI / 2
    # embedding_model = "word2vec-google-news-300"
    embedding_model = "glove-wiki-gigaword-50"

    def setup(self):
        super().setup()

        # Load model
        self.model = get_word_to_vec_model(self.embedding_model)

        # Decide on basis
        self.basis = self.get_basis(self.model)

        # Add axes
        self.axes = ThreeDAxes(**self.axes_config)
        self.add(self.axes)

    def get_basis(self, model):
        return get_principle_components(model.vectors, 3).T

    def add_plane(self, color=GREY, stroke_width=1.0):
        axes = self.axes
        plane = NumberPlane(
            axes.x_range, axes.y_range,
            width=axes.get_width(),
            height=axes.get_height(),
            background_line_style=dict(
                stroke_color=color,
                stroke_width=stroke_width,
            ),
            faded_line_style=dict(
                stroke_opacity=0.25,
                stroke_width=0.5 * stroke_width,
            ),
            faded_line_ratio=1,
        )
        self.plane = plane
        self.add(plane)
        return plane

    def get_labeled_vector(
        self,
        word,
        coords=None,
        thickness=5,
        color=YELLOW,
        func_name: str | None = "E",
        buff=0.05,
        direction=None,
        label_config: dict = dict()
    ):
        # Return an arrow with word label next to it
        axes = self.axes
        if coords is None:
            coords = self.basis @ self.model[word.lower()]
        point = axes.c2p(*coords)
        label_config.update(label_buff=buff)
        if "label_rotation" not in label_config:
            label_config.update(label_rotation=self.label_rotation)
        arrow = LabeledArrow(
            axes.get_origin(),
            point,
            thickness=thickness,
            fill_color=color,
            label_text=word if func_name is None else f"{func_name}({word})",
            buff=0,
            direction=direction,
            **label_config,
        )
        arrow.always.set_perpendicular_to_camera(self.frame)
        return arrow


class KingQueenExample(Word2VecScene):
    default_frame_orientation = (20, 70)

    def get_basis(self, model):
        basis = super().get_basis(model)
        basis[1] *= 2
        return basis

    def construct(self):
        # Axes and frame
        axes = self.axes
        frame = self.frame
        self.add_plane()
        self.plane.rotate(90 * DEGREES, LEFT)
        frame.reorient(-178, 9, 178, (2.15, 1.12, 0.56), 6.84)

        # Initial word vectors
        words = ["man", "woman", "king", "queen"]
        colors = [BLUE_B, RED_B, BLUE_D, RED_D]
        directions = [UR, RIGHT, UR, LEFT]
        all_coords = np.array([self.basis @ self.model[word] for word in words])
        all_coords[:2] += DOWN
        all_coords[2:] += 4 * LEFT + 1 * DOWN + IN

        label_config = dict(
            font_size=30,
            label_rotation=0,
        )
        man, woman, king, queen = word_vects = [
            self.get_labeled_vector(
                word,
                coords=coords,
                color=color,
                buff=0.05,
                direction=direction,
                label_config=label_config,
            )
            for word, color, direction, coords in zip(words, colors, directions, all_coords)
        ]
        woman.label.shift(SMALL_BUFF * DOWN)

        fake_queen_coords = all_coords[2] - all_coords[0] + all_coords[1]  # Tweak queen for demo purposes
        fake_queen = self.get_labeled_vector(
            "queen", fake_queen_coords,
            color=colors[3],
            label_config=label_config,
        )
        fake_queen.label.shift(0.1 * LEFT + 0.2 * DOWN)

        # Equation
        equation = self.get_equation1("queen", "king", "woman", "man")
        equation.set_x(0)
        eq, minus1, ek, approx, ew, minus2, em = equation
        top_rect = FullScreenFadeRectangle().set_fill(BLACK, 1)
        top_rect.set_height(1.5, about_edge=UP, stretch=True)
        top_rect.fix_in_frame()

        for part, vect in zip([em, ew, ek, eq], word_vects):
            part.set_fill(vect.get_color())

        # Show man and woman vectors
        diff = Arrow(man.get_end(), woman.get_end(), buff=0, stroke_color=YELLOW)
        diff.set_fill(YELLOW, opacity=0.8)
        diff.set_backstroke(BLACK, 3)
        self.play(
            LaggedStart(*map(Write, [ew, minus2, em])),
            GrowArrow(woman),
            FadeInFromPoint(woman.label, man.get_center()),
            GrowArrow(man),
            FadeInFromPoint(man.label, man.get_center()),
            frame.animate.reorient(0, 0, 0, (2.04, 2.06, 0.38), 4.76).set_anim_args(run_time=6)
        )
        self.play(
            GrowArrow(diff, time_span=(1, 3)),
            frame.animate.reorient(-179, 19, 179, (2.49, 1.96, 0.4), 4.76),
            run_time=5
        )

        # Show king and fake queen
        self.add(top_rect, *equation)
        new_diff = diff.copy()
        new_diff.shift(king.get_end() - man.get_end())

        self.play(
            FadeIn(top_rect),
            *map(Write, [eq, minus1, ek, approx]),
            LaggedStart(
                TransformFromCopy(man, king),
                TransformFromCopy(man.label, king.label),
                TransformFromCopy(woman, fake_queen),
                TransformFromCopy(woman.label, fake_queen.label),
            ),
            TransformFromCopy(diff, new_diff, time_span=(2, 3)),
            frame.animate.reorient(0, 2, 0, (0.04, 1.96, -0.13), 5.51).set_anim_args(run_time=3)
        )
        self.play(
            frame.animate.reorient(-110, 10, 110, (0.22, 1.6, -0.07), 6.72),
            run_time=10
        )

        # Rearrange the equation
        for mob in [ek, approx]:
            mob.target = mob.generate_target()
        approx.target.move_to(minus1, LEFT)
        ek.target.next_to(approx.target, RIGHT)
        minus1.target = Tex("+").next_to(ek.target, RIGHT, SMALL_BUFF)
        minus1.target.move_to(midpoint(ek.target.get_right(), ew.get_left()))
        minus1.target.fix_in_frame()

        self.play(
            FadeOut(fake_queen),
            FadeOut(fake_queen.label),
            FadeOut(new_diff),
        )
        self.play(
            LaggedStartMap(MoveToTarget, [minus1, ek, approx], path_arc=PI / 2)
        )
        self.play(FlashAround(VGroup(ek, em), run_time=3, time_width=1.5))
        self.play(TransformFromCopy(diff, new_diff))

        # Search near tip
        n_circs = 5
        src_circles = Circle(radius=1e-2).set_stroke(width=5, opacity=1).replicate(n_circs)
        trg_circles = Circle(radius=1).set_stroke(width=0, opacity=1).replicate(n_circs)
        circs = VGroup(src_circles, trg_circles)
        circs.set_stroke(WHITE)
        circs.move_to(new_diff.get_end())
        self.play(
            LaggedStart(*(
                Transform(src, trg)
                for src, trg in zip(src_circles, trg_circles)
            ), lag_ratio=0.15, run_time=3)
        )
        self.play(
            FadeIn(fake_queen),
            FadeIn(fake_queen.label),
        )
        self.wait()

        # Correct it
        self.play(
            TransformFromCopy(fake_queen, queen),
            TransformFromCopy(fake_queen.label, queen.label),
            VGroup(fake_queen, fake_queen.label).animate.set_opacity(0.2),
        )
        self.play(
            FadeOut(fake_queen),
            FadeOut(fake_queen.label),
            frame.animate.reorient(103, 9, -101, (0.01, 1.45, 0.07), 6.72),
            run_time=10
        )

        # Show a few other examples
        word_pairs = [
            ("uncle", "aunt"),
            ("brother", "sister"),
            ("nephew", "niece"),
            ("father", "mother"),
            ("son", "daughter"),
        ]
        turn_animation_into_updater(
            ApplyMethod(frame.reorient, -116, 21, 114, (0.37, 1.45, 0.23), 7.59, run_time=12)
        )

        last_group = VGroup(king, queen, king.label, queen.label, new_diff)
        last_equation = equation
        for word1, word2 in word_pairs:
            new_coords = np.array([self.basis @ self.model[w] for w in [word1, word2]])
            adj_point = np.array([
                np.random.uniform(-5, 0),
                np.random.uniform(2, 4),
                np.random.uniform(-3, 3),
            ])
            new_coords += (adj_point - new_coords[0])
            vect1 = self.get_labeled_vector(word1, color=colors[2], label_config=label_config, coords=new_coords[0])
            vect2 = self.get_labeled_vector(word2, color=colors[3], label_config=label_config, coords=new_coords[1])
            vect2.put_start_and_end_on(ORIGIN, vect1.get_end() + diff.get_vector() + np.random.uniform(-0.1, 0.1, 3))
            vect2.label.next_to(vect2.get_end(), LEFT)

            new_equation = self.get_equation1(word2, word1, "woman", "man")
            new_equation.move_to(equation, RIGHT)
            new_equation.match_style(equation)
            new_equation.set_fill(opacity=1)
            new_equation.fix_in_frame()

            diff_copy = diff.copy()
            diff_copy.shift(vect1.get_end() - diff_copy.get_start())

            self.play(
                LaggedStart(
                    FadeOut(last_group),
                    GrowArrow(vect1),
                    FadeIn(vect1.label),
                    GrowArrow(vect2),
                    FadeIn(vect2.label),
                ),
                *(
                    FadeTransform(sm1, sm2)
                    for sm1, sm2 in zip(last_equation, new_equation)
                ),
            )
            self.play(TransformFromCopy(diff, diff_copy))
            self.wait(2)

            last_equation = new_equation
            last_group = VGroup(vect1, vect2, vect1.label, vect2.label, diff_copy)
        self.wait(4)

        # Flash in direction
        vect = diff.get_vector()
        color = YELLOW
        lines = Line(ORIGIN, 2 * normalize(vect)).replicate(200)
        lines.insert_n_curves(20)
        lines.set_stroke(color, 3)
        for line in lines:
            line.move_to(np.random.uniform(-3, 3, 3))
        self.play(
            LaggedStartMap(
                VShowPassingFlash, lines,
                lag_ratio=1 / len(lines),
                run_time=4
            )
        )

    def get_labeled_vector(self, *args, **kwargs):
        kwargs.update(func_name = None)
        kwargs.update(thickness=3)
        return super().get_labeled_vector(*args, **kwargs)

    def get_equation1(self, word1, word2, word3, word4, colors=None):
        equation = TexText(
            # Rf"E({word1}) - E({word2}) $\approx$ E({word3}) - E({word4})",
            Rf"{{{word1}}} - {{{word2}}} $\approx$ {{{word3}}} - {{{word4}}}",
            font_size=48
        )
        equation.fix_in_frame(True)
        equation.to_corner(UR)
        if colors:
            words = [word1, word2, word3, word4]
            for word, color in zip(words, colors):
                equation[word].set_fill(color)
        pieces = VGroup(
            equation[f"{{{word1}}}"][0],
            equation["-"][0],
            equation[f"{{{word2}}}"][0],
            equation[R"$\approx$"][0],
            equation[f"{{{word3}}}"][0],
            equation["-"][1],
            equation[f"{{{word4}}}"][0],
        )
        pieces.fix_in_frame(True)
        return pieces

    def get_equation2(self, word1, word2, word3, word4, colors=None):
        equation = TexText(
            # Rf"E({word1}) + E({word2}) - E({word3}) $\approx$ E({word4})",
            Rf"{{{word1}}} + {{{word2}}} - {{{word3}}} $\approx$ {{{word4}}}",
            font_size=48
        )
        equation.fix_in_frame(True)
        equation.to_corner(UR)
        if colors:
            words = [word1, word2, word3, word4]
            for word, color in zip(words, colors):
                equation[word].set_fill(color)
        pieces = VGroup(
            equation[f"{{{word1}}}"],
            equation["+"],
            equation[f"{{{word2}}}"],
            equation["-"],
            equation[f"{{{word3}}}"],
            equation[R"$\approx$ "],
            equation[f"{{{word4}}}"],
        )
        pieces.fix_in_frame(True)
        return pieces
