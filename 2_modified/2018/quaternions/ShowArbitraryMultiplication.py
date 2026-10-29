# ==============================================================================
# Scene:      ShowArbitraryMultiplication
# Source:     videos/_2018/quaternions.py (lines 5773-5864)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowArbitraryMultiplication.py ShowArbitraryMultiplication -w -m --fps 15
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


class Hand(SVGMobject):
    CONFIG = {
        "file_name": "pinch_hand",
        "height": 0.5,
        "sheen": 0.2,
        "fill_color": ORANGE,
    }

    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        # self.rotate(30 * DEGREES)
        self.add(VectorizedPoint().next_to(self, UP, buff=0.17))


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


class RuleOfQuaternionMultiplication(HypersphereStereographicProjection):
    CONFIG = {
        "fancy_dot": True,
        "initial_quaternion_sample_values": [],
    }

    def construct(self):
        self.setup_all_trackers()
        self.show_multiplication_by_i_on_circle_1i()
        self.show_multiplication_by_i_on_circle_jk()
        self.show_multiplication_by_i_on_ijk_sphere()

    def setup_all_trackers(self):
        self.setup_multiplier_tracker()
        self.force_skipping()
        self.setup_axes()
        self.introduce_quaternion_label()
        self.add_unit_labels()
        self.revert_to_original_skipping_status()

    def setup_multiplier_tracker(self):
        self.multiplier_tracker = QuaternionTracker([1, 0, 0, 0])
        self.multiplier_tracker.add_updater(
            lambda m: m.set_value(normalize(
                m.get_value(),
                fall_back=[1, 0, 0, 0]
            ))
        )
        self.add(self.multiplier_tracker)

    def add_unit_labels(self):
        labels = self.unit_labels = self.get_unit_labels()
        one_label = OldTex("1")
        one_label.scale(self.unit_labels_scale_factor)
        one_label.set_shade_in_3d(True)
        one_label.rotate(90 * DEGREES, RIGHT)
        one_label.next_to(ORIGIN, IN + RIGHT, SMALL_BUFF)
        labels.add(one_label)
        self.add(labels)

    def show_multiplication_by_i_on_circle_1i(self):
        m_tracker = self.multiplier_tracker

        def get_circle_1i():
            return self.get_projected_circle(
                basis_vectors=[
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                ],
                colors=[GREEN, YELLOW],
                quaternion=m_tracker.get_value(),
            )
        circle = get_circle_1i()
        arrows = self.get_i_circle_arrows()

        def set_to_q_value(mt):
            mt.set_value(self.q_tracker.get_value())

        self.play(ShowCreation(circle, run_time=2))
        self.play(LaggedStartMap(ShowCreation, arrows, lag_ratio=0.25))
        self.wait()
        circle.add_updater(lambda c: c.become(get_circle_1i()))
        m_tracker.add_updater(set_to_q_value)
        self.add(m_tracker)
        self.set_quat([0, 1, 0, 0])
        self.wait()
        self.set_quat([-1, 0.001, 0, 0])
        self.wait()
        self.q_tracker.set_value([-1, -0.001, 0, 0])
        self.set_quat([0, -1, 0, 0])
        self.wait()
        self.set_quat([1, 0, 0, 0])
        self.wait(3)
        self.play(FadeOut(arrows))

        m_tracker.remove_updater(set_to_q_value)
        self.circle_1i = circle

    def show_multiplication_by_i_on_circle_jk(self):
        def get_circle_jk():
            return self.get_projected_circle(
                basis_vectors=[
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                colors=[RED, BLUE_E]
            )
        circle = get_circle_jk()
        arrows = self.get_jk_circle_arrows()
        m_tracker = self.multiplier_tracker
        q_tracker = self.q_tracker

        def set_q_to_mj(qt):
            qt.set_value(q_mult(
                m_tracker.get_value(), [0, 0, 1, 0]
            ))

        self.move_camera(theta=-50 * DEGREES)
        self.play(ShowCreation(circle, run_time=2))
        circle.add_updater(lambda c: c.become(get_circle_jk()))
        self.wait(10)
        self.stop_ambient_camera_rotation()
        self.begin_ambient_camera_rotation(rate=-0.01)
        self.play(*map(ShowCreation, arrows))
        self.wait()
        self.set_quat([0, 0, 1, 0], run_time=1)
        q_tracker.insert_updater(set_q_to_mj, index=0)
        self.add(self.circle_1i)
        self.play(
            m_tracker.set_value, [0, 1, 0, 0],
            run_time=3
        )
        self.wait()
        self.play(
            m_tracker.set_value, [-1, 0.001, 0, 0],
            run_time=3
        )
        self.wait()
        m_tracker.set_value([-1, 0.001, 0, 0])
        self.play(
            m_tracker.set_value, [0, -1, 0, 0],
            run_time=3
        )
        self.wait()
        self.play(
            m_tracker.set_value, [1, 0, 0, 0],
            run_time=3
        )
        self.wait()
        q_tracker.remove_updater(set_q_to_mj)
        self.play(
            FadeOut(arrows),
            q_tracker.set_value, [1, 0, 0, 0],
        )
        self.wait(10)

        self.circle_jk = circle

    def show_multiplication_by_i_on_ijk_sphere(self):
        m_tracker = self.multiplier_tracker
        q_tracker = self.q_tracker
        m_tracker.add_updater(lambda m: m.set_value(q_tracker.get_value()))

        def get_sphere():
            result = self.get_projected_sphere(null_axis=0, solid=False)
            self.specially_color_sphere(result)
            return result

        sphere = get_sphere()

        self.play(Write(sphere))
        sphere.add_updater(lambda s: s.become(get_sphere()))

        self.set_quat([0, 1, 0, 0])
        self.wait()
        self.set_quat([-1, 0.001, 0, 0])
        self.wait()
        self.q_tracker.set_value([-1, -0.001, 0, 0])
        self.set_quat([0, -1, 0, 0])
        self.wait()
        self.set_quat([1, 0, 0, 0])
        self.wait(3)

    #
    def get_multiplier(self):
        return self.multiplier_tracker.get_value()

    def get_i_circle_arrows(self):
        c2p = self.axes.coords_to_point
        i_arrow = Arrow(
            ORIGIN, 2 * RIGHT, path_arc=-120 * DEGREES,
            buff=SMALL_BUFF,
        )
        neg_one_arrow = Arrow(
            ORIGIN, 5.5 * RIGHT + UP,
            path_arc=-30 * DEGREES,
            buff=SMALL_BUFF,
        )
        neg_i_arrow = Arrow(
            4.5 * LEFT + 1.5 * UP, ORIGIN,
            path_arc=-30 * DEGREES,
            buff=SMALL_BUFF,
        )
        one_arrow = i_arrow.copy()
        result = VGroup(i_arrow, neg_one_arrow, neg_i_arrow, one_arrow)
        for arrow in result:
            arrow.set_color(GREY_B)
            arrow.set_stroke(width=3)
            arrow.rotate(90 * DEGREES, RIGHT)
        i_arrow.next_to(c2p(0, 0, 0), OUT + RIGHT, SMALL_BUFF)
        neg_one_arrow.next_to(c2p(1, 0, 0), OUT + RIGHT, SMALL_BUFF)
        neg_i_arrow.next_to(c2p(-1, 0, 0), OUT + LEFT, SMALL_BUFF)
        one_arrow.next_to(c2p(0, 0, 0), OUT + LEFT, SMALL_BUFF)
        return result

    def get_jk_circle_arrows(self):
        arrow = Arrow(
            1.5 * RIGHT, 1.5 * UP,
            path_arc=90 * DEGREES,
            buff=SMALL_BUFF,
            use_rectangular_stem=False
        )
        arrow.set_color(GREY_B)
        arrow.set_stroke(width=3)
        arrows = VGroup(*[
            arrow.copy().rotate(angle, about_point=ORIGIN)
            for angle in np.arange(0, TAU, TAU / 4)
        ])
        arrows.rotate(90 * DEGREES, RIGHT)
        arrows.rotate(90 * DEGREES, OUT)
        return arrows


class ShowMultiplicationBy135Example(RuleOfQuaternionMultiplication):
    CONFIG = {
        "fancy_dot": True,
    }

    def construct(self):
        self.setup_all_trackers()
        self.add_circles()
        self.add_ijk_sphere()
        self.show_multiplication()

    def add_circles(self):
        self.circle_1i = self.add_auto_updating_circle(
            basis_vectors=[
                [1, 0, 0, 0],
                [0, 1, 0, 0],
            ],
            colors=[YELLOW, GREEN_E]
        )
        self.circle_jk = self.add_auto_updating_circle(
            basis_vectors=[
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            colors=[RED, BLUE_E]

        )

    def add_auto_updating_circle(self, **circle_config):
        circle = self.get_projected_circle(**circle_config)
        circle.add_updater(
            lambda c: c.become(self.get_projected_circle(**circle_config))
        )
        self.add(circle)
        return circle

    def add_ijk_sphere(self):
        def get_sphere():
            result = self.get_projected_sphere(
                null_axis=0,
                solid=False,
                stroke_width=0.5,
                stroke_opacity=0.2,
                fill_opacity=0.2,
            )
            self.specially_color_sphere(result)
            return result
        sphere = get_sphere()
        sphere.add_updater(lambda s: s.become(get_sphere()))
        self.add(sphere)
        self.sphere = sphere

    def show_multiplication(self):
        m_tracker = self.multiplier_tracker

        quat = normalize(np.array([-1, 1, 0, 0]))
        point = self.project_quaternion(quat)
        arrow = Vector(DR)
        arrow.next_to(point, UL, MED_SMALL_BUFF)
        arrow.set_color(PINK)
        label = OldTex(
            "-{\\sqrt{2} \\over 2}", "+",
            "{\\sqrt{2} \\over 2}", "i",
        )
        label.next_to(arrow.get_start(), UP)
        label.set_background_stroke(width=0)

        def get_one_point():
            return self.circle_1i[0].get_points()[0]

        def get_j_point():
            return self.circle_jk[0].get_points()[0]

        one_point = VectorizedPoint()
        one_point.add_updater(lambda v: v.set_location(get_one_point()))
        self.add(one_point)

        hand = Hand()
        hand.rotate(45 * DEGREES, RIGHT)
        hand.add_updater(
            lambda h: h.move_to(get_one_point(), LEFT)
        )

        j_line = Line(ORIGIN, get_j_point())
        moving_j_line = j_line.deepcopy()
        moving_j_line.add_updater(
            lambda m: m.put_start_and_end_on(ORIGIN, get_j_point())
        )

        self.add(j_line, moving_j_line)
        self.set_camera_orientation(
            phi=60 * DEGREES, theta=-70 * DEGREES
        )
        self.play(
            FadeInFromLarge(label, 3),
            GrowArrow(arrow)
        )
        self.set_quat(quat)
        self.wait(5)
        self.play(FadeInFromLarge(hand))
        self.add(m_tracker)
        for q in [quat, [1, 0, 0, 0], quat]:
            self.play(
                m_tracker.set_value, q,
                UpdateFromFunc(
                    m_tracker,
                    lambda m: m.set_value(normalize(m.get_value()))
                ),
                run_time=5
            )
            self.wait()


class ShowArbitraryMultiplication(ShowMultiplicationBy135Example):
    CONFIG = {
        "fancy_dot": True,
        "run_time_per_rotation": 4,
        "special_quaternion": [-0.5, 0.5, 0.5, 0.5],
    }

    def construct(self):
        self.setup_all_trackers()
        self.add_circles()
        self.add_ijk_sphere()
        self.show_multiplication()

    def add_circles(self):
        self.circle1 = self.add_auto_updating_circle(
            basis_vectors=[
                [1, 0, 0, 0],
                [0, 1, 1, 1],
            ],
            colors=[YELLOW_E, YELLOW]
        )
        bv1 = normalize([0, -1, -1, 2])
        bv2 = [0] + list(normalize(np.cross([1, 1, 1], bv1[1:])))
        self.circle2 = self.add_auto_updating_circle(
            basis_vectors=[bv1, bv2],
            colors=[WHITE, GREY]
        )

    def show_multiplication(self):
        q_tracker = self.q_tracker
        m_tracker = self.multiplier_tracker
        run_time = self.run_time_per_rotation

        def normalize_tracker(t):
            t.set_value(normalize(t.get_value()))

        # for tracker in q_tracker, m_tracker:
        #     self.add(Mobject.add_updater(tracker, normalize_tracker))
        updates = [
            UpdateFromFunc(tracker, normalize_tracker)
            for tracker in (q_tracker, m_tracker)
        ]

        special_q = self.special_quaternion
        pq_point = self.project_quaternion(special_q)
        label = OldTexText("Some unit quaternion")
        label.set_color(PINK)
        label.rotate(90 * DEGREES, RIGHT)
        label.next_to(pq_point, IN + RIGHT, SMALL_BUFF)

        circle1, circle2 = self.circle1, self.circle2
        for circle in [circle1, circle2]:
            circle.tucked_away_updaters = circle.updaters
            circle.clear_updaters()
            self.remove(circle)

        hand = Hand()
        hand.rotate(90 * DEGREES, RIGHT)
        hand.move_to(ORIGIN, LEFT)
        hand.set_shade_in_3d(True)
        one_dot = self.get_dot()
        one_dot.set_color(YELLOW_E)
        one_dot.move_to(ORIGIN)
        one_dot.add_updater(
            lambda m: m.move_to(circle1[0].get_points()[0])
        )
        self.add(one_dot)

        self.stop_ambient_camera_rotation()
        self.begin_ambient_camera_rotation(rate=0.02)
        self.set_quat(special_q)
        self.play(FadeIn(label, IN))
        self.wait(3)
        for circle in [circle1, circle2]:
            self.play(ShowCreation(circle, run_time=3))
            circle.updaters = circle.tucked_away_updaters
            self.wait(2)
        self.play(
            FadeIn(hand, 2 * IN + 2 * RIGHT),
            run_time=2
        )
        hand.add_updater(
            lambda h: h.move_to(circle1[0].get_points()[0], LEFT)
        )

        for quat in [special_q, [1, 0, 0, 0], special_q]:
            self.play(
                m_tracker.set_value, special_q,
                *updates,
                run_time=run_time,
            )
            self.wait()
