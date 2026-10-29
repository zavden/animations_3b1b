"""
CL18-A: one-time ManimGL port of the Cairo-era scene bases that lived in `once_useful_constructs` / `manimlib.scene`
and `manimlib.for_3b1b_videos`, so 2018 (and earlier) scenes can subclass them:

    VectorScene, LinearTransformationScene, SampleSpaceScene, ReconfigurableScene,
    TODOStub, PatreonThanks, LogoGenerationTemplate, ShowShadows (+ helpers) and `vector_coordinate_label`.

Behaviour follows `~/Manim/manim_sep19` (Cairo, Sep 2019). The logic is the Cairo logic; only the
API calls that changed in ManimGL 1.7.2 were adapted (each adaptation carries a `CL18-A:` comment).
Exported from `cairo_compat.py` (which `manim_imports_ext.py` star-imports), so it must not wrap anything existing.
"""
import numpy as np

from manimlib import *
from manimlib.mobject.svg.old_tex_mobject import OldTex, OldTexText
from manimlib.mobject.probability import SampleSpace
from manimlib.utils.space_ops import angle_of_vector, get_norm

__all__ = [
    "X_COLOR", "Y_COLOR", "Z_COLOR", "VECTOR_LABEL_SCALE_FACTOR", "vector_coordinate_label",
    "get_det_text", "matrix_to_tex_string", "matrix_to_mobject",
    "VectorScene", "LinearTransformationScene", "SampleSpaceScene", "ReconfigurableScene",
    "TODOStub", "PatreonThanks", "LogoGenerationTemplate", "ShowShadows", "PatreonLogo",
    "get_shadow", "get_boundary_points", "get_area", "get_xy_plane_projection_point",
]

X_COLOR = GREEN_C
Y_COLOR = RED_C
Z_COLOR = BLUE_D
VECTOR_LABEL_SCALE_FACTOR = 0.8


def vector_coordinate_label(vector_mob, integer_labels=True, n_dim=2, color=WHITE):
    vect = np.array(vector_mob.get_end())
    if integer_labels:
        vect = np.round(vect).astype(int)
    vect = vect[:n_dim]
    vect = vect.reshape((n_dim, 1))
    label = Matrix(vect, add_background_rectangles_to_entries=True)
    label.scale(VECTOR_LABEL_SCALE_FACTOR)

    shift_dir = np.array(vector_mob.get_end())
    if shift_dir[0] >= 0:  # Pointing right
        shift_dir -= label.get_left() + MED_SMALL_BUFF * LEFT
    else:  # Pointing left
        shift_dir -= label.get_right() + MED_SMALL_BUFF * RIGHT
    label.shift(shift_dir)
    label.set_color(color)
    label.rect = BackgroundRectangle(label)
    label.add_to_back(label.rect)
    return label


def matrix_to_tex_string(matrix):
    matrix = np.array(matrix).astype("str")
    if matrix.ndim == 1:
        matrix = matrix.reshape((matrix.size, 1))
    n_rows, n_cols = matrix.shape
    prefix = "\\left[ \\begin{array}{%s}" % ("c" * n_cols)
    suffix = "\\end{array} \\right]"
    rows = [
        " & ".join(row)
        for row in matrix
    ]
    return prefix + " \\\\ ".join(rows) + suffix


def matrix_to_mobject(matrix):
    return OldTex(matrix_to_tex_string(matrix))


def get_det_text(matrix, determinant=None, background_rect=False, initial_scale_factor=2):
    parens = OldTex("()")
    parens.scale(initial_scale_factor)
    parens.stretch_to_fit_height(matrix.get_height())
    # CL18-A: Cairo's split() returned the two glyphs. In 2018 scenes OldTex.split() (CL18-D) already does; otherwise
    # OldTex("()") is one submobject holding the two glyphs.
    glyphs = list(parens.split())
    if len(glyphs) != 2:
        glyphs = list(parens[0])
    l_paren, r_paren = glyphs
    l_paren.next_to(matrix, LEFT, buff=0.1)
    r_paren.next_to(matrix, RIGHT, buff=0.1)
    det = OldTexText("det")
    det.scale(initial_scale_factor)
    det.next_to(l_paren, LEFT, buff=0.1)
    if background_rect:
        det.add_background_rectangle()
    det_text = VGroup(det, l_paren, r_paren)
    if determinant is not None:
        eq = OldTex("=")
        eq.next_to(r_paren, RIGHT, buff=0.1)
        result = OldTex(str(determinant))
        result.next_to(eq, RIGHT, buff=0.2)
        det_text.add(eq, result)
    return det_text


def _is_tex(mob):
    # CL18-A: Cairo checked isinstance(label, TexMobject); a label can be Tex or OldTex in GL
    return isinstance(mob, (Tex, OldTex))


def _tex_string(mob):
    # CL18-A: TexMobject.get_tex_string() is get_tex() in GL
    if hasattr(mob, "get_tex"):
        return mob.get_tex()
    return mob.get_tex_string()


# CL18-A: foreground mobjects (scene.foreground_mobjects, add_foreground_mobject) are provided for 2018 by the
# Scene.add wrapper that CL18-D put in cairo_compat.py; this module only keeps the Cairo list bookkeeping.

# --------------------------------------------------------------------------- VectorScene
class VectorScene(Scene):
    CONFIG = {
        "basis_vector_stroke_width": 6
    }

    def add_plane(self, animate=False, **kwargs):
        plane = NumberPlane(**kwargs)
        if animate:
            self.play(ShowCreation(plane, lag_ratio=0.5))
        self.add(plane)
        return plane

    def add_axes(self, animate=False, color=WHITE, **kwargs):
        axes = Axes(color=color, tick_frequency=1)
        if animate:
            self.play(ShowCreation(axes))
        self.add(axes)
        return axes

    def lock_in_faded_grid(self, dimness=0.7, axes_dimness=0.5):
        plane = self.add_plane()
        axes = plane.get_axes()
        plane.fade(dimness)
        axes.set_color(WHITE)
        axes.fade(axes_dimness)
        self.add(axes)
        # CL18-A: freeze_background() does not exist in GL (nothing to freeze: the frame is redrawn anyway)

    def get_vector(self, numerical_vector, **kwargs):
        return Arrow(
            self.plane.coords_to_point(0, 0),
            self.plane.coords_to_point(*numerical_vector[:2]),
            buff=0,
            **kwargs
        )

    def add_vector(self, vector, color=YELLOW, animate=True, **kwargs):
        if not isinstance(vector, Arrow):
            vector = Vector(vector, color=color, **kwargs)
        if animate:
            self.play(GrowArrow(vector))
        self.add(vector)
        return vector

    def write_vector_coordinates(self, vector, **kwargs):
        coords = vector_coordinate_label(vector, **kwargs)
        self.play(Write(coords))
        return coords

    def get_basis_vectors(self, i_hat_color=X_COLOR, j_hat_color=Y_COLOR):
        return VGroup(*[
            Vector(
                vect,
                color=color,
                stroke_width=self.basis_vector_stroke_width
            )
            for vect, color in [
                ([1, 0], i_hat_color),
                ([0, 1], j_hat_color)
            ]
        ])

    def get_basis_vector_labels(self, **kwargs):
        i_hat, j_hat = self.get_basis_vectors()
        return VGroup(*[
            self.get_vector_label(
                vect, label, color=color,
                label_scale_factor=1,
                **kwargs
            )
            for vect, label, color in [
                (i_hat, "\\hat{\\imath}", X_COLOR),
                (j_hat, "\\hat{\\jmath}", Y_COLOR),
            ]
        ])

    def get_vector_label(self, vector, label,
                         at_tip=False,
                         direction="left",
                         rotate=False,
                         color=None,
                         label_scale_factor=VECTOR_LABEL_SCALE_FACTOR):
        if not _is_tex(label):
            if len(label) == 1:
                label = "\\vec{\\textbf{%s}}" % label
            label = OldTex(label)
            if color is None:
                color = vector.get_color()
            label.set_color(color)
        label.scale(label_scale_factor)
        label.add_background_rectangle()

        if at_tip:
            vect = vector.get_vector()
            vect /= get_norm(vect)
            label.next_to(vector.get_end(), vect, buff=SMALL_BUFF)
        else:
            angle = vector.get_angle()
            if not rotate:
                label.rotate(-angle, about_point=ORIGIN)
            if direction == "left":
                label.shift(-label.get_bottom() + 0.1 * UP)
            else:
                label.shift(-label.get_top() + 0.1 * DOWN)
            label.rotate(angle, about_point=ORIGIN)
            label.shift((vector.get_end() - vector.get_start()) / 2)
        return label

    def label_vector(self, vector, label, animate=True, **kwargs):
        label = self.get_vector_label(vector, label, **kwargs)
        if animate:
            self.play(Write(label, run_time=1))
        self.add(label)
        return label

    def position_x_coordinate(self, x_coord, x_line, vector):
        x_coord.next_to(x_line, -np.sign(vector[1]) * UP)
        x_coord.set_color(X_COLOR)
        return x_coord

    def position_y_coordinate(self, y_coord, y_line, vector):
        y_coord.next_to(y_line, np.sign(vector[0]) * RIGHT)
        y_coord.set_color(Y_COLOR)
        return y_coord

    def coords_to_vector(self, vector, coords_start=2 * RIGHT + 2 * UP, clean_up=True):
        starting_mobjects = list(self.mobjects)
        # CL18-A: a flat list is a column vector in Cairo's Matrix; GL's Matrix wants a list of rows
        array = Matrix(np.array(vector).reshape((len(vector), 1)))
        array.shift(coords_start)
        arrow = Vector(vector)
        x_line = Line(ORIGIN, vector[0] * RIGHT)
        y_line = Line(x_line.get_end(), arrow.get_end())
        x_line.set_color(X_COLOR)
        y_line.set_color(Y_COLOR)
        x_coord, y_coord = array.get_mob_matrix().flatten()

        self.play(Write(array, run_time=1))
        self.wait()
        self.play(ApplyFunction(
            lambda x: self.position_x_coordinate(x, x_line, vector),
            x_coord
        ))
        self.play(ShowCreation(x_line))
        self.play(
            ApplyFunction(
                lambda y: self.position_y_coordinate(y, y_line, vector),
                y_coord
            ),
            FadeOut(array.get_brackets())
        )
        # CL18-A: get_mobjects_from_last_animation() does not exist in GL and its result was never used afterwards
        self.play(ShowCreation(y_line))
        self.play(ShowCreation(arrow))
        self.wait()
        if clean_up:
            self.clear()
            self.add(*starting_mobjects)

    def vector_to_coords(self, vector, integer_labels=True, clean_up=True):
        starting_mobjects = list(self.mobjects)
        show_creation = False
        if isinstance(vector, Arrow):
            arrow = vector
            vector = arrow.get_end()[:2]
        else:
            arrow = Vector(vector)
            show_creation = True
        array = vector_coordinate_label(arrow, integer_labels=integer_labels)
        x_line = Line(ORIGIN, vector[0] * RIGHT)
        y_line = Line(x_line.get_end(), arrow.get_end())
        x_line.set_color(X_COLOR)
        y_line.set_color(Y_COLOR)
        x_coord, y_coord = array.get_mob_matrix().flatten()
        x_coord_start = self.position_x_coordinate(
            x_coord.copy(), x_line, vector
        )
        y_coord_start = self.position_y_coordinate(
            y_coord.copy(), y_line, vector
        )
        brackets = array.get_brackets()

        if show_creation:
            self.play(ShowCreation(arrow))
        self.play(
            ShowCreation(x_line),
            Write(x_coord_start),
            run_time=1
        )
        self.play(
            ShowCreation(y_line),
            Write(y_coord_start),
            run_time=1
        )
        self.wait()
        self.play(
            Transform(x_coord_start, x_coord, lag_ratio=0),
            Transform(y_coord_start, y_coord, lag_ratio=0),
            Write(brackets, run_time=1),
        )
        self.wait()

        self.remove(x_coord_start, y_coord_start, brackets)
        self.add(array)
        if clean_up:
            self.clear()
            self.add(*starting_mobjects)
        return array, x_line, y_line

    def show_ghost_movement(self, vector):
        if isinstance(vector, Arrow):
            vector = vector.get_end() - vector.get_start()
        elif len(vector) == 2:
            vector = np.append(np.array(vector), 0.0)
        x_max = int(FRAME_X_RADIUS + abs(vector[0]))
        y_max = int(FRAME_Y_RADIUS + abs(vector[1]))
        # CL18-A: VMobject(*dots) -> VGroup(*dots)
        dots = VGroup(*[
            Dot(x * RIGHT + y * UP)
            for x in range(-x_max, x_max)
            for y in range(-y_max, y_max)
        ])
        dots.set_fill(BLACK, opacity=0)
        dots_halfway = dots.copy().shift(vector / 2).set_fill(WHITE, 1)
        dots_end = dots.copy().shift(vector)

        self.play(Transform(
            dots, dots_halfway, rate_func=rush_into
        ))
        self.play(Transform(
            dots, dots_end, rate_func=rush_from
        ))
        self.remove(dots)


# --------------------------------------------------------------------------- LinearTransformationScene
class LinearTransformationScene(VectorScene):
    CONFIG = {
        "include_background_plane": True,
        "include_foreground_plane": True,
        "foreground_plane_kwargs": {
            "x_max": FRAME_WIDTH / 2,
            "x_min": -FRAME_WIDTH / 2,
            "y_max": FRAME_WIDTH / 2,
            "y_min": -FRAME_WIDTH / 2,
            "faded_line_ratio": 0
        },
        "background_plane_kwargs": {
            "color": GREY,
            "axis_config": {
                "stroke_color": GREY_B,  # CL18-A: Cairo LIGHT_GREY (#BBBBBB) is GREY_B in GL
            },
            "number_line_config": {
                "color": GREY,
            },
            "background_line_style": {
                "stroke_color": GREY,
                "stroke_width": 1,
            },
        },
        "show_coordinates": False,
        "show_basis_vectors": True,
        "basis_vector_stroke_width": 6,
        "i_hat_color": X_COLOR,
        "j_hat_color": Y_COLOR,
        "leave_ghost_vectors": False,
        "t_matrix": [[3, 0], [1, 2]],
    }

    def setup(self):
        # The has_already_setup attr is to not break all the old Scenes
        if hasattr(self, "has_already_setup"):
            return
        self.has_already_setup = True
        self.background_mobjects = []
        self.foreground_mobjects = []
        self.transformable_mobjects = []
        self.moving_vectors = []
        self.transformable_labels = []
        self.moving_mobjects = []

        self.t_matrix = np.array(self.t_matrix)
        self.background_plane = NumberPlane(
            **self.background_plane_kwargs
        )

        if self.show_coordinates:
            self.background_plane.add_coordinates()
        if self.include_background_plane:
            self.add_background_mobject(self.background_plane)
        if self.include_foreground_plane:
            self.plane = NumberPlane(**self.foreground_plane_kwargs)
            self.add_transformable_mobject(self.plane)
        if self.show_basis_vectors:
            self.basis_vectors = self.get_basis_vectors(
                i_hat_color=self.i_hat_color,
                j_hat_color=self.j_hat_color,
            )
            self.moving_vectors += list(self.basis_vectors)
            self.i_hat, self.j_hat = self.basis_vectors
            self.add(self.basis_vectors)

    def add_special_mobjects(self, mob_list, *mobs_to_add):
        for mobject in mobs_to_add:
            if mobject not in mob_list:
                mob_list.append(mobject)
                self.add(mobject)

    def add_background_mobject(self, *mobjects):
        self.add_special_mobjects(self.background_mobjects, *mobjects)

    # TODO, this conflicts with Scene.add_fore
    def add_foreground_mobject(self, *mobjects):
        self.add_special_mobjects(self.foreground_mobjects, *mobjects)

    def add_transformable_mobject(self, *mobjects):
        self.add_special_mobjects(self.transformable_mobjects, *mobjects)

    def add_moving_mobject(self, mobject, target_mobject=None):
        mobject.target = target_mobject
        self.add_special_mobjects(self.moving_mobjects, mobject)

    def get_unit_square(self, color=YELLOW, opacity=0.3, stroke_width=3):
        square = self.square = Rectangle(
            color=color,
            width=self.plane.get_x_unit_size(),
            height=self.plane.get_y_unit_size(),
            stroke_color=color,
            stroke_width=stroke_width,
            fill_color=color,
            fill_opacity=opacity
        )
        square.move_to(self.plane.coords_to_point(0, 0), DL)
        return square

    def add_unit_square(self, animate=False, **kwargs):
        square = self.get_unit_square(**kwargs)
        if animate:
            self.play(
                DrawBorderThenFill(square),
                Animation(Group(*self.moving_vectors))
            )
        self.add_transformable_mobject(square)
        self.bring_to_front(*self.moving_vectors)
        self.square = square
        return self

    def add_vector(self, vector, color=YELLOW, **kwargs):
        vector = VectorScene.add_vector(
            self, vector, color=color, **kwargs
        )
        self.moving_vectors.append(vector)
        return vector

    def write_vector_coordinates(self, vector, **kwargs):
        coords = VectorScene.write_vector_coordinates(self, vector, **kwargs)
        self.add_foreground_mobject(coords)
        return coords

    def add_transformable_label(
            self, vector, label,
            transformation_name="L",
            new_label=None,
            **kwargs):
        label_mob = self.label_vector(vector, label, **kwargs)
        if new_label:
            label_mob.target_text = new_label
        else:
            label_mob.target_text = "%s(%s)" % (
                transformation_name,
                _tex_string(label_mob)
            )
        label_mob.vector = vector
        label_mob.kwargs = kwargs
        if "animate" in label_mob.kwargs:
            label_mob.kwargs.pop("animate")
        self.transformable_labels.append(label_mob)
        return label_mob

    def add_title(self, title, scale_factor=1.5, animate=False):
        if not isinstance(title, Mobject):
            title = OldTexText(title).scale(scale_factor)
        title.to_edge(UP)
        title.add_background_rectangle()
        if animate:
            self.play(Write(title))
        self.add_foreground_mobject(title)
        self.title = title
        return self

    def get_matrix_transformation(self, matrix):
        return self.get_transposed_matrix_transformation(np.array(matrix).T)

    def get_transposed_matrix_transformation(self, transposed_matrix):
        transposed_matrix = np.array(transposed_matrix)
        if transposed_matrix.shape == (2, 2):
            new_matrix = np.identity(3)
            new_matrix[:2, :2] = transposed_matrix
            transposed_matrix = new_matrix
        elif transposed_matrix.shape != (3, 3):
            raise Exception("Matrix has bad dimensions")
        return lambda point: np.dot(point, transposed_matrix)

    def get_piece_movement(self, pieces):
        start = VGroup(*pieces)
        target = VGroup(*[mob.target for mob in pieces])
        if self.leave_ghost_vectors:
            self.add(start.copy().fade(0.7))
        return Transform(start, target, lag_ratio=0)

    def get_moving_mobject_movement(self, func):
        for m in self.moving_mobjects:
            if m.target is None:
                m.target = m.copy()
            target_point = func(m.get_center())
            m.target.move_to(target_point)
        return self.get_piece_movement(self.moving_mobjects)

    def get_vector_movement(self, func):
        for v in self.moving_vectors:
            v.target = Vector(func(v.get_end()), color=v.get_color())
            # CL18-A: Cairo shrank the tip of tiny arrows with get_tip().scale_in_place(norm); a GL arrow is a
            # single filled shape that already caps its tip length by max_tip_length_to_length_ratio.
        return self.get_piece_movement(self.moving_vectors)

    def get_transformable_label_movement(self):
        for l in self.transformable_labels:
            l.target = self.get_vector_label(
                l.vector.target, l.target_text, **l.kwargs
            )
        return self.get_piece_movement(self.transformable_labels)

    def apply_matrix(self, matrix, **kwargs):
        self.apply_transposed_matrix(np.array(matrix).T, **kwargs)

    def apply_inverse(self, matrix, **kwargs):
        self.apply_matrix(np.linalg.inv(matrix), **kwargs)

    def apply_transposed_matrix(self, transposed_matrix, **kwargs):
        func = self.get_transposed_matrix_transformation(transposed_matrix)
        if "path_arc" not in kwargs:
            net_rotation = np.mean([
                angle_of_vector(func(RIGHT)),
                angle_of_vector(func(UP)) - np.pi / 2
            ])
            kwargs["path_arc"] = net_rotation
        self.apply_function(func, **kwargs)

    def apply_inverse_transpose(self, t_matrix, **kwargs):
        t_inv = np.linalg.inv(np.array(t_matrix).T).T
        self.apply_transposed_matrix(t_inv, **kwargs)

    def apply_nonlinear_transformation(self, function, **kwargs):
        self.plane.prepare_for_nonlinear_transform()
        self.apply_function(function, **kwargs)

    def apply_function(self, function, added_anims=[], **kwargs):
        if "run_time" not in kwargs:
            kwargs["run_time"] = 3
        anims = [
            ApplyPointwiseFunction(function, t_mob)
            for t_mob in self.transformable_mobjects
        ] + [
            self.get_vector_movement(function),
            self.get_transformable_label_movement(),
            self.get_moving_mobject_movement(function),
        ] + [
            Animation(f_mob)
            for f_mob in self.foreground_mobjects
        ] + added_anims
        self.play(*anims, **kwargs)


# --------------------------------------------------------------------------- SampleSpaceScene
class SampleSpaceScene(Scene):
    def get_sample_space(self, **config):
        self.sample_space = SampleSpace(**config)
        return self.sample_space

    def add_sample_space(self, **config):
        self.add(self.get_sample_space(**config))

    def get_division_change_animations(
        self, sample_space, parts, p_list,
        dimension=1,
        new_label_kwargs=None,
        **kwargs
    ):
        if new_label_kwargs is None:
            new_label_kwargs = {}
        anims = []
        p_list = sample_space.complete_p_list(p_list)
        space_copy = sample_space.copy()

        vect = DOWN if dimension == 1 else RIGHT
        parts.generate_target()
        for part, p in zip(parts.target, p_list):
            part.replace(space_copy, stretch=True)
            part.stretch(p, dimension)
        parts.target.arrange(vect, buff=0)
        parts.target.move_to(space_copy)
        anims.append(MoveToTarget(parts))
        if hasattr(parts, "labels") and parts.labels is not None:
            label_kwargs = parts.label_kwargs
            label_kwargs.update(new_label_kwargs)
            new_braces, new_labels = sample_space.get_subdivision_braces_and_labels(
                parts.target, **label_kwargs
            )
            anims += [
                Transform(parts.braces, new_braces),
                Transform(parts.labels, new_labels),
            ]
        return anims

    def get_horizontal_division_change_animations(self, p_list, **kwargs):
        assert(hasattr(self.sample_space, "horizontal_parts"))
        return self.get_division_change_animations(
            self.sample_space, self.sample_space.horizontal_parts, p_list,
            dimension=1,
            **kwargs
        )

    def get_vertical_division_change_animations(self, p_list, **kwargs):
        assert(hasattr(self.sample_space, "vertical_parts"))
        return self.get_division_change_animations(
            self.sample_space, self.sample_space.vertical_parts, p_list,
            dimension=0,
            **kwargs
        )

    def get_conditional_change_anims(
        self, sub_sample_space_index, value, post_rects=None,
        **kwargs
    ):
        parts = self.sample_space.horizontal_parts
        sub_sample_space = parts[sub_sample_space_index]
        anims = self.get_division_change_animations(
            sub_sample_space, sub_sample_space.vertical_parts, value,
            dimension=0,
            **kwargs
        )
        if post_rects is not None:
            anims += self.get_posterior_rectangle_change_anims(post_rects)
        return anims

    def get_top_conditional_change_anims(self, *args, **kwargs):
        return self.get_conditional_change_anims(0, *args, **kwargs)

    def get_bottom_conditional_change_anims(self, *args, **kwargs):
        return self.get_conditional_change_anims(1, *args, **kwargs)

    def get_prior_rectangles(self):
        return VGroup(*[
            self.sample_space.horizontal_parts[i].vertical_parts[0]
            for i in range(2)
        ])

    def get_posterior_rectangles(self, buff=MED_LARGE_BUFF):
        prior_rects = self.get_prior_rectangles()
        areas = [
            rect.get_width() * rect.get_height()
            for rect in prior_rects
        ]
        total_area = sum(areas)
        total_height = prior_rects.get_height()

        post_rects = prior_rects.copy()
        for rect, area in zip(post_rects, areas):
            rect.stretch_to_fit_height(total_height * area / total_area)
            rect.stretch_to_fit_width(
                area / rect.get_height()
            )
        post_rects.arrange(DOWN, buff=0)
        post_rects.next_to(
            self.sample_space, RIGHT, buff
        )
        return post_rects

    def get_posterior_rectangle_braces_and_labels(
        self, post_rects, labels, direction=RIGHT, **kwargs
    ):
        return self.sample_space.get_subdivision_braces_and_labels(
            post_rects, labels, direction, **kwargs
        )

    def update_posterior_braces(self, post_rects):
        braces = post_rects.braces
        labels = post_rects.labels
        for rect, brace, label in zip(post_rects, braces, labels):
            brace.stretch_to_fit_height(rect.get_height())
            brace.next_to(rect, RIGHT, SMALL_BUFF)
            label.next_to(brace, RIGHT, SMALL_BUFF)

    def get_posterior_rectangle_change_anims(self, post_rects):
        def update_rects(rects):
            new_rects = self.get_posterior_rectangles()
            Transform(rects, new_rects).update(1)
            if hasattr(rects, "braces"):
                self.update_posterior_braces(rects)
            return rects

        anims = [UpdateFromFunc(post_rects, update_rects)]
        if hasattr(post_rects, "braces"):
            anims += list(map(Animation, [
                post_rects.labels, post_rects.braces
            ]))
        return anims


# --------------------------------------------------------------------------- ReconfigurableScene
class ReconfigurableScene(Scene):
    """
    Note, this seems to no longer work as intented (same note as the Cairo original).
    """
    CONFIG = {
        "allow_recursion": True,
    }

    def setup(self):
        self.states = []
        self.num_recursions = 0

    def transition_to_alt_config(
        self,
        return_to_original_configuration=True,
        transformation_kwargs=None,
        **new_config
    ):
        from cairo_compat import cairo_nested_scene
        if transformation_kwargs is None:
            transformation_kwargs = {}
        original_state = self.get_state()
        state_copy = original_state.copy()
        self.states.append(state_copy)
        if not self.allow_recursion:
            return
        # CL18-A: in Cairo, Scene.__init__ ran construct(); a nested scene needs cairo_nested_scene
        alt_scene = cairo_nested_scene(
            self.__class__,
            allow_recursion=False,
            **new_config
        )
        alt_state = alt_scene.states[len(self.states) - 1]

        if return_to_original_configuration:
            self.clear()
            self.transition_between_states(
                state_copy, alt_state,
                **transformation_kwargs
            )
            self.transition_between_states(
                state_copy, original_state,
                **transformation_kwargs
            )
            self.clear()
            self.add(*original_state)
        else:
            self.transition_between_states(
                original_state, alt_state,
                **transformation_kwargs
            )
            self.__dict__.update(new_config)

    def get_state(self):
        # Want to return a mobject that maintains the most
        # structure.  The way to do that is to extract only
        # those that aren't inside another.
        # CL18-A: Mobject(*mobs) -> Group(*mobs)
        return Group(*self.get_top_level_mobjects())

    def transition_between_states(self, start_state, target_state, **kwargs):
        self.play(Transform(start_state, target_state, **kwargs))
        self.wait()


# --------------------------------------------------------------------------- common_scenes.py bases
class TODOStub(Scene):
    CONFIG = {
        "message": ""
    }

    def construct(self):
        self.add(OldTexText("TODO: %s" % self.message))
        self.wait()


class PatreonThanks(Scene):
    """
    The Cairo original (manimlib/for_3b1b_videos/common_scenes.py) was already broken (it reads
    `self.specific_patronds`, a typo, and float group counts). Here it works as intended: Morty-less
    version (no pi creature) that shows the patron names in groups under the Patreon logo area.
    """
    CONFIG = {
        "specific_patrons": [],
        "max_patron_group_size": 20,
        "patron_scale_val": 0.8,
    }

    def construct(self):
        patrons = [OldTexText(name) for name in self.specific_patrons]
        if not patrons:
            self.wait()
            return
        num_groups = int(np.ceil(len(patrons) / self.max_patron_group_size))
        indices = (len(patrons) * np.linspace(0, 1, num_groups + 1)).astype('int')
        patron_groups = [
            VGroup(*patrons[i:j])
            for i, j in zip(indices, indices[1:])
        ]
        title = OldTexText("Special thanks to these supporters").scale(0.9)
        title.to_edge(UP)
        self.add(title)

        for group in patron_groups:
            half = len(group) // 2
            left_group = VGroup(*group[:half])
            right_group = VGroup(*group[half:])
            for subgroup, vect in (left_group, LEFT), (right_group, RIGHT):
                subgroup.arrange(DOWN, aligned_edge=LEFT)
                subgroup.scale(self.patron_scale_val)
                subgroup.to_edge(vect)
        last_group = None
        for group in patron_groups:
            if last_group is not None:
                self.play(FadeOut(last_group))
            self.play(LaggedStartMap(FadeIn, group, run_time=2))
            self.wait(2)
            last_group = group
        self.play(FadeOut(last_group))


class LogoGenerationTemplate(Scene):
    """
    CL18-A: the Cairo class draws the 3b1b `Logo` (an eye made of pi-creature-like parts) and the channel name,
    and subclasses add `get_logo_animations`. The Logo is a brand asset of the channel and is not reproduced
    here: `Logo` is replaced by a plain circle "eye" placeholder (generic shapes only), the name is typeset text.
    """
    def setup(self):
        self.frame.shift(DOWN)
        self.logo = Circle(radius=1.0, stroke_color=BLUE_D, stroke_width=6, fill_opacity=0)
        self.logo.add(Dot(ORIGIN, radius=0.3, color=GREY_BROWN))
        name = OldTexText("Channel name")
        name.scale(2.5)
        name.next_to(self.logo, DOWN, buff=MED_LARGE_BUFF)
        name.set_sheen(-0.2, DR)
        self.channel_name = name

    def construct(self):
        logo = self.logo
        name = self.channel_name

        self.play(
            Write(name, run_time=3),
            *self.get_logo_animations(logo)
        )
        self.wait()

    def get_logo_animations(self, logo):
        return []  # For subclasses


# --------------------------------------------------------------------------- ShowShadows (active_projects/shadows.py)
# Filled in below once the 3D camera behaviour is checked (CL18-A, step 3).
def get_shadow(mobject, opacity=0.5):
    result = mobject.deepcopy()
    result.apply_function(lambda p: [p[0], p[1], 0])
    color = interpolate_color(
        mobject.get_fill_color(), BLACK,
        mobject.get_fill_opacity()
    )
    result.set_fill(color, opacity=opacity)
    result.set_stroke(BLACK, 0.5, opacity=opacity)
    result.set_shading(0, 0, 0)  # CL18-A: set_shade_in_3d(False) -> no shading in GL
    return result


def get_boundary_points(shadow, n_points=20):
    points = shadow.get_all_points()  # CL18-A: get_points_defining_boundary() -> all points of the family
    return np.array([
        points[np.argmax(np.dot(points, vect.T))]
        for vect in compass_directions(n_points)
    ])


def get_area(planar_mobject):
    boundary = get_boundary_points(planar_mobject, 100)
    xs = boundary[:, 0]
    ys = boundary[:, 1]
    dxs = np.append(xs[-1], xs[:-1]) - xs
    dys = np.append(ys[-1], ys[:-1]) - ys
    return abs(sum([
        0.5 * (x * dy - y * dx)
        for x, dx, y, dy in zip(xs, dxs, ys, dys)
    ]))


def get_xy_plane_projection_point(p1, p2):
    """
    Draw a line from source to p1 to p2.  Where does it
    intersect the xy plane?
    """
    vect = p2 - p1
    return p1 - (p1[2] / vect[2]) * vect


class ShowShadows(ThreeDScene):
    """
    Port of active_projects/shadows.py::ShowShadows (the file is not in the 3b1b/videos repo, 2018 sphere_area imports
    it with `from _2018.shadows import *`). A solid hangs over a plane and its xy-shadow is redrawn as the solid
    is reoriented with three Euler-angle trackers.
    """
    CONFIG = {
        "object_center": [0, 0, 3],
        "area_label_center": [0, -1.5, 0],
        "surface_area": 6.0,
        "num_reorientations": 10,
        "frame_center": [0, 0, 0.5],
        "initial_orientation_config": {
            "phi": 60 * DEGREES,
            "theta": -120 * DEGREES,
        }
    }

    def setup(self):
        # CL18-A: Cairo camera_config light_source_start_point / frame_center: GL has no light source object in the
        # camera; the frame center is applied to the camera frame.
        self.frame.move_to(np.array(self.frame_center, dtype=float))
        self.add_plane()
        self.setup_orientation_trackers()
        self.setup_object_and_shadow()
        self.add_shadow_area_label()
        self.add_surface_area_label()

    def add_plane(self):
        plane = self.plane = Rectangle(
            width=FRAME_WIDTH,
            height=24.2,
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.35,
        )
        plane.set_sheen(0.2, DR)
        # CL18-A: NumberPlane(color=, secondary_color=, y_radius=, secondary_line_ratio=) -> GL arguments
        grid = NumberPlane(
            x_range=(-7, 7, 1),
            y_range=(-int(plane.get_height() / 2), int(plane.get_height() / 2), 1),
            background_line_style=dict(stroke_color=GREY_B, stroke_width=1),
            axis_config=dict(stroke_color=GREY_B, stroke_width=1),
            faded_line_ratio=0,
        )
        plane.add(grid)
        plane.add(VectorizedPoint(10 * IN))
        plane.set_shade_in_3d(True, z_index_as_group=True)
        self.add(plane)

    def setup_orientation_trackers(self):
        # Euler angles
        self.alpha_tracker = ValueTracker(0)
        self.beta_tracker = ValueTracker(0)
        self.gamma_tracker = ValueTracker(0)

    def setup_object_and_shadow(self):
        self.obj3d = always_redraw(self.get_reoriented_object)
        self.shadow = always_redraw(lambda: get_shadow(self.obj3d))

    def add_shadow_area_label(self):
        text = OldTexText("Shadow area: ")
        decimal = DecimalNumber(0)
        label = VGroup(text, decimal)
        label.arrange(RIGHT)
        label.scale(1.5)
        label.move_to(self.area_label_center - decimal.get_center())
        self.shadow_area_label = label
        self.shadow_area_decimal = decimal

        decimal.add_updater(
            lambda d: d.set_value(get_area(self.shadow))
        )
        decimal.add_updater(
            lambda d: self.add_fixed_in_frame_mobjects(d)
        )

        self.add_fixed_in_frame_mobjects(label)
        self.add(label)
        self.add(decimal)

    def add_surface_area_label(self):
        text = OldTexText("Surface area: ")
        decimal = DecimalNumber(self.surface_area)
        label = VGroup(text, decimal)
        label.arrange(RIGHT)
        label.scale(1.25)
        label.set_fill(YELLOW)
        label.set_stroke(BLACK, 3, background=True)
        label.next_to(self.obj3d, RIGHT, LARGE_BUFF)
        label.shift(MED_LARGE_BUFF * IN)
        self.surface_area_label = label
        self.add_fixed_orientation_mobjects(label)

    def construct(self):
        # Show creation
        obj3d = self.obj3d.copy()
        obj3d.clear_updaters()
        temp_shadow = always_redraw(lambda: get_shadow(obj3d))
        self.add(temp_shadow)
        self.move_camera(
            **self.initial_orientation_config,
            added_anims=[
                LaggedStartMap(DrawBorderThenFill, obj3d)
            ],
            run_time=2
        )
        self.begin_ambient_camera_rotation(0.01)
        self.remove(obj3d, temp_shadow)

        average_label = self.get_average_label()
        # Reorient
        self.add(self.obj3d, self.shadow)
        for n in range(self.num_reorientations):
            self.randomly_reorient()
            if n == 3:
                self.add_fixed_in_frame_mobjects(average_label)
                self.play(Write(average_label, run_time=2))
            else:
                self.wait()

    def randomly_reorient(self, run_time=3):
        a, b, c = TAU * np.random.random(3)
        self.play(
            self.alpha_tracker.animate.set_value(a),
            self.beta_tracker.animate.set_value(b),
            self.gamma_tracker.animate.set_value(c),
            run_time=run_time
        )

    #
    def get_object(self):
        cube = Cube()
        cube.set_height(1)
        cube.set_stroke(WHITE, 0.5)
        return cube

    def get_reoriented_object(self):
        obj3d = self.get_object()
        angles = [
            self.alpha_tracker.get_value(),
            self.beta_tracker.get_value(),
            self.gamma_tracker.get_value(),
        ]
        vects = [OUT, RIGHT, OUT]

        center = self.object_center
        obj3d.move_to(center)
        for angle, vect in zip(angles, vects):
            obj3d.rotate(angle, vect, about_point=center)
        return obj3d

    def get_average_label(self):
        rect = SurroundingRectangle(
            self.shadow_area_decimal,
            buff=SMALL_BUFF,
            color=RED,
        )
        words = OldTexText(
            "Average", "=",
            "$\\frac{\\text{Surface area}}{4}$"
        )
        words.scale(1.5)
        words[0].match_color(rect)
        words[2].set_color(self.surface_area_label[0].get_fill_color())
        words.set_stroke(BLACK, 3, background=True)
        words.next_to(
            rect, DOWN,
            index_of_submobject_to_align=0,
        )
        return VGroup(rect, words)


class PatreonLogo(VGroup):
    """
    CL18-A: the Patreon mark is a brand logo (tier 3: replaced, not reproduced). Stand-in: a coral heart drawn
    by code with the same colour, size (width 4) and `family_members_with_points()` use as the Cairo SVGMobject.
    """
    def __init__(self, width=4, fill_color="#F96854", **kwargs):
        super().__init__(**kwargs)
        heart = ParametricCurve(
            lambda t: np.array([
                16 * np.sin(t) ** 3,
                13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t),
                0,
            ]),
            t_range=(0, TAU, 0.05),
        )
        heart.set_fill(fill_color, 1)
        heart.set_stroke(width=0)
        heart.make_smooth()
        self.add(heart)
        self.set_width(width)
        self.center()
