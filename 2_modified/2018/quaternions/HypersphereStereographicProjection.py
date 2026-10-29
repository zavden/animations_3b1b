# ==============================================================================
# Scene:      HypersphereStereographicProjection
# Source:     videos/_2018/quaternions.py (lines 4680-5096)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HypersphereStereographicProjection.py HypersphereStereographicProjection -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - QuaternionTracker kept its 4-vector as mobject points; GL points are 3D and ValueTracker holds an arbitrary-length value, so it is stored in ValueTracker.value
#   - removed CONFIG "dim": 4, which the CONFIG shim turned into Mobject.dim and broke bounding boxes (the 4-vector now lives in ValueTracker.value)
# ==============================================================================

from manim_imports_ext import *

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return np.array([w, x, y, z])


def stereo_project_point(point, axis=0, r=1, max_norm=10000):
    point = fdiv(point * r, point[axis] + r)
    point[axis] = 0
    norm = get_norm(point)
    if norm > max_norm:
        point *= max_norm / norm
    return point


class CheckeredCircle(Circle):
    CONFIG = {
        "n_pieces": 16,
        "colors": [BLUE_E, BLUE_C],
        "stroke_width": 5,
    }

    def __init__(self, **kwargs):
        Circle.__init__(self, **kwargs)
        pieces = self.get_pieces(self.n_pieces)
        self.set_points(np.zeros((0, 3)))
        self.add(*pieces)
        n_colors = len(self.colors)
        for i, color in enumerate(self.colors):
            self[i::n_colors].set_color(color)


class StereoProjectedSphere(Sphere):
    CONFIG = {
        "stereo_project_config": {
            "axis": 2,
        },
        "max_r": 32,
        "max_width": FRAME_WIDTH,
        "max_height": FRAME_WIDTH,
        "max_depth": FRAME_WIDTH,
        "radius": 1,
    }

    def __init__(self, rotation_matrix=None, **kwargs):
        digest_config(self, kwargs)
        if rotation_matrix is None:
            rotation_matrix = np.identity(3)
        self.rotation_matrix = rotation_matrix

        self.stereo_project_config["r"] = self.radius
        ParametricSurface.__init__(
            self, self.post_projection_func, **kwargs
        )
        self.submobjects.sort(
            key=lambda m: -m.get_width()
        )
        self.fade_far_out_submobjects()

    def post_projection_func(self, u, v):
        point = self.radius * Sphere.func(self, u, v)
        rot_point = np.dot(point, self.rotation_matrix.T)
        result = stereo_project_point(
            rot_point, **self.stereo_project_config
        )
        epsilon = 1e-4
        if np.any(np.abs(result) == np.inf) or np.any(np.isnan(result)):
            return self.func(u + epsilon, v)
        return result

    def fade_far_out_submobjects(self, **kwargs):
        max_r = kwargs.get("max_r", self.max_r)
        max_width = kwargs.get("max_width", self.max_width)
        max_height = kwargs.get("max_height", self.max_height)
        max_depth = kwargs.get("max_depth", self.max_depth)
        for submob in self.submobjects:
            violations = [
                np.any(np.apply_along_axis(get_norm, 1, submob.get_anchors()) > max_r),
                submob.get_width() > max_width,
                submob.get_height() > max_height,
                submob.get_depth() > max_depth
            ]
            if any(violations):
                # self.remove(submob)
                submob.fade(1)
        return self


class StereoProjectedSphereFromHypersphere(StereoProjectedSphere):
    CONFIG = {
        "stereo_project_config": {
            "axis": 0,
        },
        "radius": 2,
        "multiply_from_right": False,
    }

    def __init__(self, quaternion=None, null_axis=0, **kwargs):
        if quaternion is None:
            quaternion = np.array([1, 0, 0, 0])
        self.quaternion = quaternion
        self.null_axis = null_axis
        ParametricSurface.__init__(self, self.q_mult_projection_func, **kwargs)
        self.fade_far_out_submobjects()

    def q_mult_projection_func(self, u, v):
        point = list(Sphere.func(self, u, v))
        point.insert(self.null_axis, 0)
        if self.multiply_from_right:
            post_q_mult = q_mult(point, self.quaternion)
        else:
            post_q_mult = q_mult(self.quaternion, point)
        projected = list(self.radius * stereo_project_point(
            post_q_mult, **self.stereo_project_config
        ))
        if np.any(np.abs(projected) == np.inf):
            return self.func(u + 0.001, v)
        ignored_axis = self.stereo_project_config["axis"]
        projected.pop(ignored_axis)
        return np.array(projected)


class StereoProjectedCircleFromHypersphere(CheckeredCircle):
    CONFIG = {
        "n_pieces": 48,
        "radius": 2,
        "max_length": 3 * FRAME_WIDTH,
        "max_r": 50,
        "basis_vectors": [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ],
        "multiply_from_right": False,
    }

    def __init__(self, quaternion=None, **kwargs):
        CheckeredCircle.__init__(self, **kwargs)
        if quaternion is None:
            quaternion = [1, 0, 0, 0]
        self.quaternion = quaternion
        self.pre_positioning_matrix = self.get_pre_positioning_matrix()
        self.apply_function(self.projection)
        self.remove_large_pieces()
        self.set_shade_in_3d(True)

    def get_pre_positioning_matrix(self):
        v1, v2 = [np.array(v) for v in self.basis_vectors]
        v1 = normalize(v1)
        v2 = v2 - np.dot(v1, v2) * v1
        v2 = normalize(v2)
        return np.array([v1, v2]).T

    def projection(self, point):
        q1 = self.quaternion
        q2 = np.dot(self.pre_positioning_matrix, point[:2]).flatten()
        if self.multiply_from_right:
            new_q = q_mult(q2, q1)
        else:
            new_q = q_mult(q1, q2)
        projected = stereo_project_point(
            new_q, axis=0, r=self.radius,
        )
        if np.any(projected == np.inf) or np.any(np.isnan(projected)):
            epsilon = 1e-6
            return self.projection(rotate_vector(point, epsilon))
        return projected[1:]

    def remove_large_pieces(self):
        for piece in self:
            length = get_norm(piece.get_points()[0] - piece.get_points()[-1])
            violations = [
                length > self.max_length,
                get_norm(piece.get_center()) > self.max_r,
            ]
            if any(violations):
                piece.fade(1)


class QuaternionTracker(ValueTracker):
    CONFIG = {
        # CHANGE: removed CONFIG "dim": 4, which the CONFIG shim turned into Mobject.dim and broke bounding boxes (the 4-vector now lives in ValueTracker.value)
        "force_unit": True,
    }

    # CHANGE: QuaternionTracker kept its 4-vector as mobject points; GL points are 3D and ValueTracker holds an arbitrary-length value, so it is stored in ValueTracker.value
    def __init__(self, four_vector=None, **kwargs):
        if four_vector is None:
            four_vector = np.array([1, 0, 0, 0])
        ValueTracker.__init__(self, np.array(four_vector, dtype=float), **kwargs)
        if self.force_unit:
            self.add_updater(lambda q: q.normalize())

    def set_value(self, vector):
        self.value[:] = np.array(vector, dtype=float).reshape(4)
        return self

    def get_value(self):
        return self.value

    def normalize(self):
        self.set_value(normalize(
            self.get_value(),
            fall_back=np.array([1, 0, 0, 0])
        ))
        return self


class HypersphereStereographicProjection(SpecialThreeDScene):
    CONFIG = {
        # "fancy_dot": False,
        "fancy_dot": True,
        "initial_quaternion_sample_values": [
            [0, 1, 0, 0],
            [-1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 1, -1, 1],
        ],
        "unit_labels_scale_factor": 1,
    }

    def construct(self):
        self.setup_axes()
        self.introduce_quaternion_label()
        self.show_one()
        self.show_unit_sphere()
        self.show_quaternions_with_nonzero_real_part()
        self.emphasize_only_units()
        self.show_reference_spheres()

    def setup_axes(self):
        axes = self.axes = self.get_axes()
        axes.set_stroke(width=1)
        self.add(axes)
        self.move_camera(
            **self.get_default_camera_position(),
            run_time=0
        )
        self.begin_ambient_camera_rotation(rate=0.01)

    def introduce_quaternion_label(self):
        q_tracker = QuaternionTracker()
        coords = [
            DecimalNumber(0, color=color, include_sign=sign, edge_to_fix=RIGHT)
            for color, sign in zip(
                [YELLOW, GREEN, RED, BLUE],
                [False, True, True, True],
            )
        ]
        label = VGroup(
            coords[0], VectorizedPoint(),
            coords[1], OldTex("i"),
            coords[2], OldTex("j"),
            coords[3], OldTex("k"),
        )
        label.arrange(RIGHT, buff=SMALL_BUFF)
        label.to_corner(UR)

        def update_label(label):
            self.remove_fixed_in_frame_mobjects(label)
            quat = q_tracker.get_value()
            for value, coord in zip(quat, label[::2]):
                coord.set_value(value)
            self.add_fixed_in_frame_mobjects(label)
            return label

        label.add_updater(update_label)
        self.pink_dot_label = label

        def get_pq_point():
            point = self.project_quaternion(q_tracker.get_value())
            if get_norm(point) > 100:
                return point * 100 / get_norm(point)
            return point

        pq_dot = self.get_dot()
        pq_dot.add_updater(lambda d: d.move_to(get_pq_point()))
        dot_radius = pq_dot.get_width() / 2

        def get_pq_line():
            point = get_pq_point()
            norm = get_norm(point)
            origin = self.axes.coords_to_point(0, 0, 0)
            if norm > dot_radius:
                point -= origin
                point *= (norm - dot_radius) / norm
                point += origin
            result = Line(origin, point)
            result.set_stroke(width=1)
            return result

        pq_line = get_pq_line()
        pq_line.add_updater(lambda cl: cl.become(get_pq_line()))

        self.add(q_tracker, label, pq_line, pq_dot)

        self.q_tracker = q_tracker
        self.q_label = label
        self.pq_line = pq_line
        self.pq_dot = pq_dot

        rect = SurroundingRectangle(label, color=WHITE)
        self.add_fixed_in_frame_mobjects(rect)
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.remove_fixed_orientation_mobjects(rect)

        for value in self.initial_quaternion_sample_values:
            self.set_quat(value)
            self.wait()

    def show_one(self):
        q_tracker = self.q_tracker

        one_label = OldTex("1")
        one_label.rotate(TAU / 4, RIGHT)
        one_label.next_to(ORIGIN, IN + RIGHT, SMALL_BUFF)
        one_label.set_shade_in_3d(True)
        one_label.set_background_stroke(width=0)

        self.play(
            ApplyMethod(
                q_tracker.set_value, [1, 0, 0, 0],
                run_time=2
            ),
            FadeInFromDown(one_label)
        )
        self.wait(4)

    def show_unit_sphere(self):
        sphere = self.sphere = self.get_projected_sphere(
            quaternion=[1, 0, 0, 0], null_axis=0,
            solid=False,
            stroke_width=0.5
        )
        self.specially_color_sphere(sphere)
        labels = self.get_unit_labels()
        labels.remove(labels[3])

        real_part = self.q_label[0]
        brace = Brace(real_part, DOWN)
        words = OldTexText("Real part zero")
        words.next_to(brace, DOWN, SMALL_BUFF, LEFT)

        self.play(Write(sphere))
        self.play(LaggedStartMap(
            FadeInFrom, labels,
            lambda m: (m, IN)
        ))
        self.add_fixed_in_frame_mobjects(brace, words)
        self.set_quat(
            [0, 1, 0, 0],
            added_anims=[
                GrowFromCenter(brace),
                Write(words),
            ]
        )
        self.wait()
        self.set_quat([0, 1, -1, 1])
        self.wait(2)
        self.set_quat([0, -1, -1, 1])
        self.wait(2)
        self.set_quat([0, 0, 0, 1])
        self.wait(2)
        self.set_quat([0, 0, -1, 0])
        self.wait(2)
        self.set_quat([0, 1, 0, 0])
        self.wait(2)
        self.play(FadeOut(words))
        self.remove_fixed_in_frame_mobjects(words)

        self.real_part_brace = brace

    def show_quaternions_with_nonzero_real_part(self):
        # Positive real part
        self.set_quat(
            [1, 1, 2, 0],
            added_anims=[
                ApplyMethod(
                    self.sphere.copy().scale, 0,
                    remover=True
                )
            ]
        )
        self.wait(2)
        self.set_quat([4, 0, -1, -1])
        self.wait(2)
        # Negative real part
        self.set_quat(
            [-1, 1, 2, 0],
            added_anims=[
                ApplyFunction(
                    lambda s: s.scale(10).fade(1),
                    self.sphere.copy(),
                    remover=True
                )
            ]
        )
        self.wait(2)
        self.set_quat([-2, 0, -1, 1])
        self.wait(2)
        self.set_quat([-1, 1, 0, 0])
        self.move_camera(theta=-160 * DEGREES, run_time=3)
        self.set_quat([-1, 0.001, 0, 0])
        self.wait(2)

    def emphasize_only_units(self):
        q_label = self.q_label
        brace = self.real_part_brace

        brace.target = Brace(q_label, DOWN, buff=SMALL_BUFF)
        words = OldTexText(
            "Only those where \\\\",
            "$w^2 + x^2 + y^2 + z^2 = 1$"
        )
        words.next_to(brace.target, DOWN, SMALL_BUFF)

        self.add_fixed_in_frame_mobjects(words)
        self.play(
            MoveToTarget(brace),
            Write(words)
        )
        self.set_quat([1, 1, 1, 1])
        self.wait(2)
        self.set_quat([1, 1, -1, 1])
        self.wait(2)
        self.set_quat([-1, 1, -1, 1])
        self.wait(8)
        self.play(FadeOut(brace), FadeOut(words))
        self.remove_fixed_in_frame_mobjects(brace, words)

    # TODO
    def show_reference_spheres(self):
        sphere = self.sphere
        self.move_camera(
            phi=60 * DEGREES,
            theta=-150 * DEGREES,
            added_anims=[
                self.q_tracker.set_value, [1, 0, 0, 0]
            ]
        )
        sphere_ijk = self.get_projected_sphere(null_axis=0)
        sphere_1jk = self.get_projected_sphere(null_axis=1)
        sphere_1ik = self.get_projected_sphere(null_axis=2)
        sphere_1ij = self.get_projected_sphere(null_axis=3)
        circle = StereoProjectedCircleFromHypersphere(axes=[0, 1])

        circle_words = OldTexText(
            "Circle through\\\\", "$1, i, -1, -i$"
        )
        sphere_1ij_words = OldTexText(
            "Sphere through\\\\", "$1, i, j, -1, -i, -j$"
        )
        sphere_1jk_words = OldTexText(
            "Sphere through\\\\", "$1, j, k, -1, -j, -k$"
        )
        sphere_1ik_words = OldTexText(
            "Sphere through\\\\", "$1, i, k, -1, -i, -k$"
        )
        for words in [circle_words, sphere_1ij_words, sphere_1jk_words, sphere_1ik_words]:
            words.to_corner(UL)
            self.add_fixed_in_frame_mobjects(words)

        self.play(
            ShowCreation(circle),
            Write(circle_words),
        )
        self.set_quat([0, 1, 0, 0])
        self.set_quat([1, 0, 0, 0])
        self.remove(sphere)
        sphere_ijk.match_style(sphere)
        self.add(sphere_ijk)

        # Show xy plane
        self.play(
            FadeOut(circle_words, DOWN),
            FadeInFromDown(sphere_1ij_words),
            FadeOut(circle),
            sphere_ijk.set_stroke, {"width": 0.0}
        )
        self.play(Write(sphere_1ij))
        self.wait(10)
        return

        # Show yz plane
        self.play(
            FadeOut(sphere_1ij_words, DOWN),
            FadeInFromDown(sphere_1jk_words),
            sphere_1ij.set_fill, BLUE_E, 0.25,
            sphere_1ij.set_stroke, {"width": 0.0},
            Write(sphere_1jk)
        )
        self.wait(5)

        # Show xz plane
        self.play(
            FadeOut(sphere_1jk_words, DOWN),
            FadeInFromDown(sphere_1ik_words),
            sphere_1jk.set_fill, GREEN_E, 0.25,
            sphere_1jk.set_stroke, {"width": 0.0},
            Write(sphere_1ik)
        )
        self.wait(5)
        self.play(
            sphere_1ik.set_fill, RED_E, 0.25,
            sphere_1ik.set_stroke, {"width": 0.0},
            FadeOut(sphere_1ik_words)
        )

        # Start applying quaternion multiplication
        kwargs = {"solid": False, "stroke_width": 0}
        sphere_ijk.add_updater(
            lambda s: s.become(self.get_projected_sphere(0, **kwargs))
        )
        sphere_1jk.add_updater(
            lambda s: s.become(self.get_projected_sphere(1, **kwargs))
        )
        sphere_1ik.add_updater(
            lambda s: s.become(self.get_projected_sphere(2, **kwargs))
        )
        sphere_1ij.add_updater(
            lambda s: s.become(self.get_projected_sphere(3, **kwargs))
        )

        self.set_quat([0, 1, 1, 1])

    #
    def project_quaternion(self, quat):
        return self.axes.coords_to_point(
            *stereo_project_point(quat, axis=0, r=1)[1:]
        )

    def get_dot(self):
        if self.fancy_dot:
            sphere = self.get_sphere()
            sphere.set_width(0.2)
            sphere.set_stroke(width=0)
            sphere.set_fill(PINK)
            return sphere
        else:
            return VGroup(
                Dot(color=PINK),
                Dot(color=PINK).rotate(TAU / 4, RIGHT),
            )

    def get_unit_labels(self):
        c2p = self.axes.coords_to_point
        tex_coords_vects = [
            ("i", [1, 0, 0], IN + RIGHT),
            ("-i", [-1, 0, 0], IN + LEFT),
            ("j", [0, 1, 0], UP + OUT + RIGHT),
            ("-j", [0, -1, 0], RIGHT + DOWN),
            ("k", [0, 0, 1], OUT + RIGHT),
            ("-k", [0, 0, -1], IN + RIGHT),
        ]
        labels = VGroup()
        for tex, coords, vect in tex_coords_vects:
            label = OldTex(tex)
            label.scale(self.unit_labels_scale_factor)
            label.rotate(90 * DEGREES, RIGHT)
            label.next_to(c2p(*coords), vect, SMALL_BUFF)
            labels.add(label)
        labels.set_shade_in_3d(True)
        labels.set_background_stroke(width=0)
        return labels

    def set_quat(self, value, run_time=3, added_anims=None):
        if added_anims is None:
            added_anims = []
        self.play(
            self.q_tracker.set_value, value,
            *added_anims,
            run_time=run_time
        )

    def get_projected_sphere(self, null_axis, quaternion=None, solid=True, **kwargs):
        if quaternion is None:
            quaternion = self.get_multiplier()
        axes_to_color = {
            0: interpolate_color(YELLOW, BLACK, 0.5),
            1: GREEN_E,
            2: RED_D,
            3: BLUE_E,
        }
        color = axes_to_color[null_axis]
        config = dict(self.sphere_config)
        config.update({
            "stroke_color": WHITE,
            "stroke_width": 0.5,
            "stroke_opacity": 0.5,
            "max_r": 24,
        })
        if solid:
            config.update({
                "checkerboard_colors": [
                    color, interpolate_color(color, BLACK, 0.5)
                ],
                "fill_opacity": 1,
            })
        else:
            config.update({
                "checkerboard_colors": [],
                "fill_color": color,
                "fill_opacity": 0.25,
            })
        config.update(kwargs)
        sphere = StereoProjectedSphereFromHypersphere(
            quaternion=quaternion,
            null_axis=null_axis,
            **config
        )
        sphere.set_shade_in_3d(True)
        return sphere

    def get_projected_circle(self, quaternion=None, **kwargs):
        if quaternion is None:
            quaternion = self.get_multiplier()
        return StereoProjectedCircleFromHypersphere(quaternion, **kwargs)

    def get_multiplier(self):
        return self.q_tracker.get_value()

    def specially_color_sphere(self, sphere):
        sphere.set_color_by_gradient(BLUE, GREEN, PINK)
        return sphere
