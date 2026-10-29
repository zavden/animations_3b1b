# ==============================================================================
# Scene:      SizeDirection
# Source:     videos/_2024/transformers/embedding.py (lines 1511-1566)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl SizeDirection.py SizeDirection -w -m --fps 15
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


class SizeDirection(Word2VecScene):
    def construct(self):
        # To illustrate "You could imagine many other directions in this space corresponding to semantic meaning"

        # Set up axes
        axes = self.axes
        frame = self.frame
        self.basis *= 1.5

        # Add vectors
        frame.reorient(35, 80, 0)
        colors = [BLUE_B, BLUE_C, BLUE_D]
        word_lists = [
            ["micrometer", "millimeter", "meter"],
            ["microgram", "milligram", "gram"],
            ["microliter", "milliliter", "liter"],
        ]
        vect_groups = VGroup(
            VGroup(
                self.get_labeled_vector(word, color=color, func_name=None)
                for word, color in zip(word_list, colors)
            )
            for word_list in word_lists
        )

        over_arrow = Arrow(2 * LEFT, 2 * RIGHT).shift(UP)
        over_arrow.set_stroke(YELLOW, width=10)
        over_words = Text("Size", font_size=72)
        over_words.set_color(YELLOW)
        over_words.set_backstroke(BLACK, 5)
        over_words.next_to(over_arrow, UP)
        annotation = VGroup(over_arrow, over_words)
        annotation.shift(LEFT)
        annotation.fix_in_frame()

        for vect_group in vect_groups:
            vect_group.labels = VGroup()
            for vect in vect_group:
                vect.label.rotate(45 * DEGREES, OUT)
                vect.label.next_to(vect.get_end(), normalize(vect.get_vector()), SMALL_BUFF)
                vect_group.labels.add(vect.label)

        self.play(
            frame.animate.reorient(49, 87, 0),
            LaggedStartMap(FadeIn, vect_groups[0], lag_ratio=0.25),
            LaggedStartMap(FadeIn, vect_groups[0].labels, lag_ratio=0.25),
            FadeIn(annotation, lag_ratio=0.1, time_span=(2, 3)),
            run_time=3
        )
        self.wait()
        for i in [0, 1]:
            self.play(
                ReplacementTransform(vect_groups[i], vect_groups[i + 1]),
                ReplacementTransform(vect_groups[i].labels, vect_groups[i + 1].labels),
            )
            self.wait()
