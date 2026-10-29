# ==============================================================================
# Scene:      RefineTowerMeaning
# Source:     videos/_2024/transformers/embedding.py (lines 2365-2467)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl RefineTowerMeaning.py RefineTowerMeaning -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DATA_DIR now points to _lib/data (get_directories()["data"]) instead of Grant's output folder (GloVe, placeholder texts)
#   - get_principle_components: sign of each principal component fixed (negative sum), because eig returns it arbitrarily depending on LAPACK and the scene's cameras are tuned to Grant's signs (without this the vectors went off screen)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Tower1.png  (_lib/assets/generated/2024/transformers/make_embedding_images.py)
#   - _lib/assets/raster_images/Tower2.png  (_lib/assets/generated/2024/transformers/make_embedding_images.py)
#   - _lib/assets/raster_images/Tower3.png  (_lib/assets/generated/2024/transformers/make_embedding_images.py)
#   - _lib/assets/raster_images/Tower4.png  (_lib/assets/generated/2024/transformers/make_embedding_images.py)
#   - _lib/assets/raster_images/EiffelTower2.png  (_lib/assets/generated/2024/transformers/make_embedding_images.py)
#   - _lib/assets/raster_images/EiffelTower3.png  (_lib/assets/generated/2024/transformers/make_embedding_images.py)
#   - _lib/assets/raster_images/MiniEiffelTower1.png  (_lib/assets/generated/2024/transformers/make_embedding_images.py)
#   - _lib/assets/raster_images/EiffelTower1.png  (misc_placeholders.py)
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


class MultipleMoleEmbeddings(Word2VecScene):
    default_frame_orientation = (0, 0)
    label_rotation = 0

    def setup(self):
        super().setup()
        self.set_floor_plane("xz")
        self.frame.add_ambient_rotation()
        self.add_plane()
        for mob in [self.plane, self.axes]:
            mob.rotate(-90 * DEGREES, RIGHT)

    def construct(self):
        # Show generic mole embedding
        frame = self.frame
        frame.reorient(-6, -6, 0, (-0.73, 1.29, -0.57), 5.27)
        phrases = VGroup(map(Text, [
            "American shrew mole",
            "One mole of carbon dioxide",
            "Take a biopsy of the mole",
        ]))
        for phrase in phrases:
            phrases.fix_in_frame()
            phrases.to_corner(UL)
            phrase["mole"][0].set_color(YELLOW)

        gen_vector = self.get_labeled_vector("mole", coords=(-2, 1.0, 1.5))
        curr_phrase = phrases[1]
        mover = curr_phrase["mole"][0]
        mover.set_backstroke(BLACK, 4)

        self.add(curr_phrase)
        self.wait()
        self.play(
            GrowArrow(gen_vector),
            TransformFromCopy(mover, gen_vector.label),
        )
        self.wait(10)

        # Show three refined meanings
        images = Group(
            ImageMobject("ShrewMole"),
            Tex(R"6.02 \times 10^{23}", font_size=24).set_color(BLUE),
            ImageMobject("LipMole"),
        )
        for image in images[::2]:
            image.set_height(0.5)
            image.set_opacity(0.75)

        colors = [GREY_BROWN, BLUE, ORANGE]
        ref_vects = VGroup(
            self.get_labeled_vector("", coords=coords)
            for coords in [
                (-1.0, -1.5, 1.5),
                (-4.0, 0.5, 1.0),
                (-0.5, 1.0, 2.5),
            ]
        )
        for vect, image, color in zip(ref_vects, images, colors):
            vect.set_color(color)
            image.next_to(vect.get_end(), UP, SMALL_BUFF)

        gen_vect_group = VGroup(gen_vector, gen_vector.label)

        self.play(
            frame.animate.reorient(-30, -5, 0, (-1.11, 1.35, -0.72), 5.27),
            LaggedStart(
                (TransformFromCopy(gen_vector, ref_vect)
                for ref_vect in ref_vects),
                lag_ratio=0.25,
                run_time=2,
            ),
            LaggedStart(
                (FadeInFromPoint(image, gen_vector.label.get_center())
                for image in images),
                lag_ratio=0.25,
                run_time=2,
                group_type=Group,
            ),
            gen_vect_group.animate.set_opacity(0.25).set_anim_args(run_time=2),
            run_time=2,
        )
        self.wait(3)

        ref_vect_groups = Group(
            Group(*pair) for pair in zip(ref_vects, images)
        )

        # Oscillate between meanings based on context
        diff_vects = VGroup(
            Arrow(gen_vector.get_end(), ref_vect.get_end(), buff=0)
            for ref_vect in ref_vects
        )
        diff_vects.set_color(GREY_B)

        last_phrase = curr_phrase
        last_diff = VGroup()
        for n, diff in enumerate(diff_vects):
            ref_vect_groups.target = ref_vect_groups.generate_target()
            ref_vect_groups.target.set_opacity(0.2)
            ref_vect_groups.target[n].set_opacity(1)
            if n != 2:
                ref_vect_groups.target[2][1].set_opacity(0.1)
            phrase = phrases[n]
            self.play(
                gen_vect_group.animate.set_opacity(1),
                MoveToTarget(ref_vect_groups),
                FadeOut(last_phrase, UP),
                FadeIn(phrase, UP),
                FadeOut(last_diff)
            )
            self.play(
                ShowCreation(diff, time_span=(1, 2)),
                TransformFromCopy(gen_vector, ref_vects[n], time_span=(1, 2)),
                ContextAnimation(
                    phrase["mole"][0], phrase,
                    direction=DOWN,
                    fix_in_frame=True,
                ),
            )
            self.wait(3)

            last_phrase = phrase
            last_diff = diff

        self.wait(5)

    def get_basis(self, model):
        basis = super().get_basis(model) * 2
        basis[2] *= -1
        return basis


class RefineTowerMeaning(MultipleMoleEmbeddings):
    def construct(self):
        # Set up vectors and images
        frame = self.frame
        frame.reorient(-26, -4, 0, (3.27, 1.57, 0.59), 5.28)
        frame.add_ambient_rotation(0.5 * DEGREES)

        words = VGroup(Text(word) for word in "Miniature Eiffel Tower".split(" "))
        words.scale(1.25)
        words.to_edge(UP)
        words.fix_in_frame()

        tower_images = Group(
            ImageMobject(f"Tower{n}")
            for n in range(1, 5)
        )
        eiffel_tower_images = Group(
            ImageMobject(f"EiffelTower{n}")
            for n in range(1, 4)
        )
        mini_eiffel_tower_images = Group(
            ImageMobject("MiniEiffelTower1")
        )
        image_groups = Group(
            tower_images,
            eiffel_tower_images,
            mini_eiffel_tower_images
        )

        vectors = VGroup(
            self.get_labeled_vector("", coords=coords)
            for coords in [
                (4, -1, 3.0),
                (5, -2, 1.5),
                (-3, -1, 2.5),
            ]
        )
        colors = [BLUE_D, GREY_B, GREY_C]
        for vector, color, image_group in zip(vectors, colors, image_groups):
            vector.set_color(color)
            for image in image_group:
                image.set_height(1.5)
                image.next_to(vector.get_end(), RIGHT * np.sign(vector.get_end()[0]))

        # Show tower
        tower = words[-1]
        tower.set_x(0)
        pre_tower_image = tower_images[0].copy()
        pre_tower_image.fix_in_frame()
        pre_tower_image.replace(tower, stretch=True)
        pre_tower_image.set_opacity(0)

        self.add(tower)
        self.wait()
        self.play(
            GrowArrow(vectors[0]),
            ReplacementTransform(pre_tower_image, tower_images[0]),
            run_time=2,
        )
        for ti1, ti2 in zip(tower_images, tower_images[1:]):
            self.play(
                FadeTransform(ti1, ti2),
                run_time=2
            )
        self.wait(2)

        # Eiffel tower
        words[:-1].set_opacity(0)
        eiffel_tower = words[-2:]

        self.play(
            frame.animate.reorient(-4, -7, 0, (2.95, 1.82, 0.49), 6.59),
            eiffel_tower.animate.set_opacity(1).arrange(RIGHT, aligned_edge=DOWN).to_edge(UP),
        )
        self.play(
            vectors[0].animate.set_opacity(0.25),
            tower_images[-1].animate.set_opacity(0.2),
            TransformFromCopy(vectors[0], vectors[1]),
            FadeTransform(tower_images[-1].copy(), eiffel_tower_images[0]),
            ContextAnimation(words[2], words[1], direction=DOWN, fix_in_frame=True),
            run_time=2,
        )
        for ti1, ti2 in zip(eiffel_tower_images, eiffel_tower_images[1:]):
            self.play(
                FadeTransform(ti1, ti2),
                run_time=2
            )
        self.wait(6)

        # Miniature eiffel tower
        self.play(
            frame.animate.reorient(-14, -2, 0, (-0.12, 2.21, 0.72), 7.05).set_anim_args(run_time=2),
            words.animate.set_opacity(1).arrange(RIGHT, aligned_edge=DOWN).to_edge(UP),
        )
        self.play(
            vectors[1].animate.set_opacity(0.25),
            eiffel_tower_images[-1].animate.set_opacity(0.2),
            TransformFromCopy(vectors[1], vectors[2]),
            FadeTransform(eiffel_tower_images[-1].copy(), mini_eiffel_tower_images[0]),
            ContextAnimation(words[2], words[0], direction=DOWN, fix_in_frame=True),
            run_time=2,
        )
        self.wait(10)
