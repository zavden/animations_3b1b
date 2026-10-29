# ==============================================================================
# Scene:      ShowNearestNeighborsToNavy
# Source:     videos/_2024/transformers/embedding.py (lines 1705-1707)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ShowNearestNeighborsToNavy.py ShowNearestNeighborsToNavy -w -m --fps 15
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


def find_nearest_words(model, vector, n=20):
    data = model.vectors
    indices = np.argsort(((data - vector)**2).sum(1))
    return [model.index_to_key[i] for i in indices[:n]]


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


class ShowNearestNeighbors(Word2VecScene):
    seed_word = "tower"
    color = YELLOW
    n_shown = 10
    frame_height = 4
    frame_center = (2.18, 0.09, 0.72)
    frame_orientation = (-21, 87, 0)
    wait_time_per_example = 0.5

    def construct(self):
        # Setup
        frame = self.frame
        frame.reorient(*self.frame_orientation, self.frame_center, self.frame_height)
        frame.add_updater(lambda f, dt: f.increment_theta(dt * DEGREES))
        self.add_plane()

        # Add seed
        word = self.seed_word.lower()
        seed_vect = self.get_labeled_vector(word, color=self.color)
        seed_group = VGroup(seed_vect, seed_vect.label)
        self.add(seed_group)

        # Add neighbors
        nearest_words = self.get_nearest_words(word)
        neighbors = VGroup(*(
            self.get_labeled_vector(
                word,
                # coords=seed_vect.get_end() + np.random.uniform(-0.5, 0.5, 3),
                color=WHITE
            )
            for word in nearest_words
        ))
        for neighbor in neighbors:
            neighbor.label.scale(0.75, about_edge=LEFT)
            neighbor.label.set_fill(border_width=0)
            neighbor.add(neighbor.label)

        # Description
        title = Text(f"Embeddings closest to E({self.seed_word})")
        underline = Underline(title)
        items = VGroup(*(
            Text(f"E({word})", font_size=36)
            for word in nearest_words
        ))
        items.arrange(DOWN, aligned_edge=LEFT)
        items.next_to(underline, DOWN, buff=0.5)
        items.align_to(title["E"][-1], LEFT)
        items.set_backstroke(BLACK, 8)

        desc = VGroup(title, underline, items)
        desc.fix_in_frame()
        desc.to_corner(UR)

        self.add(title, underline)

        # Add them all
        last_neighbor = VectorizedPoint()
        for item, neighbor in zip(items, neighbors):
            faded_last_neighbor = last_neighbor.copy()
            faded_last_neighbor.set_opacity(0.2)
            self.add(faded_last_neighbor, seed_group, neighbor)
            self.play(
                FadeIn(item),
                FadeIn(neighbor),
                FadeOut(last_neighbor),
                FadeIn(faded_last_neighbor),
            )
            last_neighbor = neighbor
            self.wait(self.wait_time_per_example)
        self.play(last_neighbor.animate.set_opacity(0.2))

        self.wait(10)

    def get_nearest_words(self, word):
        return find_nearest_words(self.model, self.model[word], self.n_shown + 1)[1:]

    def animate_in_neighbors(self, neighbors):
        # Old
        to_fade = VGroup()
        for neighbor in neighbors:
            neighbor.label.set_fill(border_width=0)
            self.add(to_fade, neighbor.label, seed_vect, seed_vect.label)
            self.play(
                FadeIn(neighbor),
                FadeIn(neighbor.label),
                to_fade.animate.set_opacity(0.25),
            )
            to_fade = VGroup(neighbor, neighbor.label)
        self.add(to_fade, neighbor.label, seed_vect, seed_vect.label)
        self.play(to_fade.animate.set_opacity(0.2))
        self.wait(5)


class ShowNearestNeighborsToNavy(ShowNearestNeighbors):
    seed_word = "navy"
    color = RED
