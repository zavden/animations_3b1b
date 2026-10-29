# ==============================================================================
# Scene:      LearningEmbeddings
# Source:     videos/_2024/transformers/embedding.py (lines 1019-1104)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl LearningEmbeddings.py LearningEmbeddings -w -m --fps 15
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


class LearningEmbeddings(Word2VecScene):
    def construct(self):
        # Setup
        self.add_plane()
        axes = self.axes
        plane = self.plane
        frame = self.frame
        frame.reorient(0, 90, 0)

        # Get sample words
        # phrase = "The first big idea is that as a model tweaks and tunes its weights"
        # phrase = "The big idea as a model tweaks and tunes its weights"
        phrase = "Features can be encoded with directions in a big space"
        words = [word.lower() for word in phrase.split(" ")]

        # Get initial and final states
        colors = [random_bright_color(hue_range=(0.5, 0.6)) for word in words]
        true_embeddings = np.array([
            self.basis @ self.model[word]
            for word in words
        ])
        true_embeddings -= true_embeddings.mean(0)
        true_embeddings *= 5 / np.abs(true_embeddings).max(0)

        np.random.seed(2)
        thetas = np.arange(0, TAU, TAU / len(words))
        thetas += np.random.uniform(-0.5, 0.5, thetas.size)
        amps = np.random.uniform(3, 5, thetas.size)
        initial_coords = [
            rotate_vector(amp * OUT, theta, axis=UP)
            for theta, amp in zip(thetas, amps)
        ]

        # Create word vectors
        word_vects = VGroup(*(
            self.get_labeled_vector(
                word,
                coords=coords,
                color=color,
                buff=0.05,
                func_name=None,
                label_config=dict(font_size=36)
            )
            for word, color, coords in zip(words, colors, initial_coords)
        ))
        labels = VGroup()
        for vect in word_vects:
            label = vect.label
            label.set_backstroke(BLACK, 3)
            label.vect = vect
            label.add_updater(lambda m: m.move_to(
                m.vect.get_end() + 0.25 * normalize(m.vect.get_vector())
            ))
            labels.add(label)

        self.play(
            LaggedStartMap(GrowArrow, word_vects, lag_ratio=0.2),
            LaggedStartMap(FadeIn, labels, lag_ratio=0.2),
            run_time=4
        )
        self.wait()

        # Tweak and tune weights
        turn_animation_into_updater(
            ApplyMethod(frame.reorient, 4, 72, 0, (-0.04, -0.18, -0.5), 8.00),
            run_time=8
        )
        self.progressive_nudges(word_vects, true_embeddings, 8)
        frame.clear_updaters()
        turn_animation_into_updater(
            ApplyMethod(frame.reorient, 38, 69, 0, (-0.32, 0.02, -0.54), 7.68),
            run_time=12
        )
        self.progressive_nudges(word_vects, true_embeddings, 12)

    def progressive_nudges(self, word_vects, true_embeddings, n_nudges, step_size=0.2):
        for x in range(n_nudges):
            anims = [
                vect.animate.put_start_and_end_on(
                    self.axes.get_origin(),
                    interpolate(vect.get_end(), self.axes.c2p(*embedding), step_size)
                )
                for vect, embedding in zip(word_vects, true_embeddings)
            ]
            self.play(*anims, run_time=0.5)
            self.wait(0.5)
