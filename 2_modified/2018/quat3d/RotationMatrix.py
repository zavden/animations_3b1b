# ==============================================================================
# Scene:      RotationMatrix
# Source:     videos/_2018/quat3d.py (lines 537-637)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/quaternions.py
#
# Run from this folder:
#     manimgl RotationMatrix.py RotationMatrix -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - QuaternionTracker rewritten on top of GL ValueTracker.value (4 components); the Cairo version stored the quaternion as a (1, 4) point array, which GL points (3D) reject
# ==============================================================================

from manim_imports_ext import *


# ----- From _2018/quaternions.py -----

# CHANGE: GL ValueTracker holds its value in self.value (not in 3D points), so a 4-component tracker can no longer use set_points
# with a (1, 4) array; rely on ValueTracker's value storage and drop "dim": 4 (it would also override Mobject.dim)
class QuaternionTracker(ValueTracker):
    CONFIG = {
        "force_unit": True,
    }

    def __init__(self, four_vector=None, **kwargs):
        if four_vector is None:
            four_vector = np.array([1, 0, 0, 0])
        ValueTracker.__init__(self, four_vector, **kwargs)
        if self.force_unit:
            self.add_updater(lambda q: q.normalize())

    def normalize(self):
        self.set_value(normalize(
            self.get_value(),
            fall_back=np.array([1, 0, 0, 0])
        ))
        return self



# ----- From _2018/quat3d.py -----

W_COLOR = YELLOW


I_COLOR = GREEN


J_COLOR = RED


K_COLOR = BLUE


class QuaternionLabel(VGroup):
    CONFIG = {
        "decimal_config": {}
    }

    def __init__(self, quat, **kwargs):
        VGroup.__init__(self, **kwargs)
        dkwargs = dict(self.decimal_config)
        decimals = VGroup()
        decimals.add(DecimalNumber(quat[0], color=W_COLOR, **dkwargs))
        dkwargs["include_sign"] = True
        decimals.add(
            DecimalNumber(quat[1], color=I_COLOR, **dkwargs),
            DecimalNumber(quat[2], color=J_COLOR, **dkwargs),
            DecimalNumber(quat[3], color=K_COLOR, **dkwargs),
        )
        self.add(
            decimals[0],
            decimals[1], OldTex("i"),
            decimals[2], OldTex("j"),
            decimals[3], OldTex("k"),
        )
        self.arrange(RIGHT, buff=SMALL_BUFF)

        self.decimals = decimals

    def set_value(self, quat):
        for decimal, coord in zip(self.decimals, quat):
            decimal.set_value(coord)
        return self


class RandyPrism(Cube):
    CONFIG = {
        "height": 0.25,
        "width": 1,
        "depth": 1.2,
        "fill_color": BLUE_D,
        "fill_opacity": 0.9,
        "stroke_color": WHITE,
        "stroke_width": 1,
    }

    def __init__(self, **kwargs):
        Cube.__init__(self, **kwargs)
        self.set_height(1)
        randy = Randolph(mode="pondering")
        randy.set_height(0.8)
        randy.rotate(TAU / 4, RIGHT)
        randy.shift(0.7 * DOWN)
        randy.set_shade_in_3d(True, z_index_as_group=True)
        self.randy = randy
        self.add(randy)
        self.set_height(self.height, stretch=True)
        self.set_width(self.width, stretch=True)
        self.set_depth(self.depth, stretch=True)
        self.center()


class ShowSeveralQuaternionRotations(SpecialThreeDScene):
    CONFIG = {
        "quaternions": [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 1, 0],
            [1, 1, 1, -1],
            [0, -1, 2, 1],
            [1, 0, 0, -1],
            [1, -1, 0, 0],
            [1, -1, 1, 0],
            [1, -1, 1, -1],
            [1, 0, 0, 0],
        ],
        "start_phi": 70 * DEGREES,
        "start_theta": -140 * DEGREES,
        "ambient_rotation_rate": 0.01,
    }

    def construct(self):
        self.add_q_tracker()
        self.setup_labels()
        self.setup_camera_position()
        self.add_prism()
        self.add_axes()
        self.apply_quaternions()

    def add_q_tracker(self):
        self.q_tracker = QuaternionTracker()
        self.q_tracker.add_updater(lambda m: m.normalize())
        self.add(self.q_tracker)

    def setup_labels(self):
        left_q_label = QuaternionLabel([1, 0, 0, 0])
        right_q_label = QuaternionLabel([1, 0, 0, 0])
        for label in left_q_label, right_q_label:
            lp, rp = OldTex("()")
            lp.next_to(label, LEFT, SMALL_BUFF)
            rp.next_to(label, RIGHT, SMALL_BUFF)
            label.add(lp, rp)
        point_label = OldTex(
            *"(xi+yj+zk)",
            tex_to_color_map={
                "i": I_COLOR,
                "j": J_COLOR,
                "k": K_COLOR,
            }
        )
        left_q_label.next_to(point_label, LEFT)
        right_q_label.next_to(point_label, RIGHT)
        group = VGroup(left_q_label, point_label, right_q_label)
        group.arrange(RIGHT)
        group.set_width(FRAME_WIDTH - 1)
        group.to_edge(UP)
        self.add_fixed_in_frame_mobjects(BackgroundRectangle(group))

        for label, text in zip(group, ["$q$", "Some 3d point", "$q^{-1}$"]):
            brace = Brace(label, DOWN)
            text_mob = OldTexText(text)
            if text_mob.get_width() > brace.get_width():
                text_mob.match_width(brace)
            text_mob.next_to(brace, DOWN, buff=SMALL_BUFF)
            text_mob.add_background_rectangle()
            label.add(brace, text_mob)

        self.add_fixed_in_frame_mobjects(*group)

        left_q_label.add_updater(
            lambda m: m.set_value(self.q_tracker.get_value())
        )
        left_q_label.add_updater(lambda m: self.add_fixed_in_frame_mobjects(m))
        right_q_label.add_updater(
            lambda m: m.set_value(quaternion_conjugate(
                self.q_tracker.get_value()
            ))
        )
        right_q_label.add_updater(lambda m: self.add_fixed_in_frame_mobjects(m))

    def setup_camera_position(self):
        self.set_camera_orientation(
            phi=self.start_phi,
            theta=self.start_theta,
        )
        self.begin_ambient_camera_rotation(self.ambient_rotation_rate)

    def add_prism(self):
        prism = self.prism = self.get_prism()
        prism.add_updater(
            lambda p: p.become(self.get_prism(
                self.q_tracker.get_value()
            ))
        )
        self.add(prism)

    def add_axes(self):
        axes = self.axes = always_redraw(self.get_axes)
        self.add(axes)

    def apply_quaternions(self):
        for quat in self.quaternions:
            self.change_q(quat)
            self.wait(2)

    #
    def get_unrotated_prism(self):
        return RandyPrism().scale(2)

    def get_prism(self, quaternion=[1, 0, 0, 0]):
        prism = self.get_unrotated_prism()
        angle, axis = angle_axis_from_quaternion(quaternion)
        prism.rotate(angle=angle, axis=axis, about_point=ORIGIN)
        return prism

    def get_axes(self):
        prism = self.prism
        centers = [sm.get_center() for sm in prism[:6]]
        axes = VGroup()
        for i in range(3):
            for u in [-1, 1]:
                vect = np.zeros(3)
                vect[i] = u
                dots = [np.dot(normalize(c), vect) for c in centers]
                max_i = np.argmax(dots)
                ec = centers[max_i]
                prism.get_edge_center(vect)
                p1 = np.zeros(3)
                p1[i] = ec[i]
                p1 *= dots[max_i]
                p2 = 10 * vect
                axes.add(Line(p1, p2))
        axes.set_stroke(GREY_B, 1)
        axes.set_shade_in_3d(True)
        return axes

    def change_q(self, value, run_time=3, added_anims=None, **kwargs):
        if added_anims is None:
            added_anims = []
        self.play(
            self.q_tracker.set_value, value,
            *added_anims,
            run_time=run_time,
            **kwargs
        )


class RotationMatrix(ShowSeveralQuaternionRotations):
    CONFIG = {
        "start_phi": 60 * DEGREES,
        "start_theta": -60 * DEGREES,
    }

    def construct(self):
        self.add_q_tracker()
        self.setup_camera_position()
        self.add_prism()
        self.add_basis_vector_labels()
        self.add_axes()

        title = OldTexText("Rotation matrix")
        title.scale(1.5)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        angle = 75 * DEGREES
        axis = [0.3, 1, 0.3]
        matrix = rotation_matrix(angle=angle, axis=axis)
        matrix_mob = DecimalMatrix(matrix, h_buff=1.6)
        matrix_mob.next_to(title, DOWN)
        matrix_mob.to_edge(LEFT)
        title.next_to(matrix_mob, UP)
        self.add_fixed_in_frame_mobjects(matrix_mob)

        colors = [I_COLOR, J_COLOR, K_COLOR]
        matrix_mob.set_column_colors(*colors)

        columns = matrix_mob.get_columns()
        column_rects = VGroup(*[
            SurroundingRectangle(c).match_color(c[0])
            for c in columns
        ])
        labels = VGroup(*[
            OldTexText(
                "Where", tex, "goes",
                tex_to_color_map={tex: rect.get_color()}
            ).next_to(rect, DOWN)
            for letter, rect in zip(["\\i", "\\j", "k"], column_rects)
            for tex in ["$\\hat{\\textbf{%s}}$" % (letter)]
        ])
        labels.space_out_submobjects(0.8)

        quaternion = quaternion_from_angle_axis(angle, axis)

        self.play(Write(matrix_mob))
        self.change_q(quaternion)
        self.wait()
        last_label = VectorizedPoint(matrix_mob.get_bottom())
        last_rect = VMobject()
        for label, rect in zip(labels, column_rects):
            self.add_fixed_in_frame_mobjects(rect, label)
            self.play(
                FadeIn(label),
                FadeOut(last_label),
                ShowCreation(rect),
                FadeOut(last_rect)
            )
            self.wait()
            last_label = label
            last_rect = rect
        self.play(FadeOut(last_label), FadeOut(last_rect))
        self.wait(5)

    def get_unrotated_prism(self):
        prism = RandyPrism()
        prism.scale(1.5)
        arrows = VGroup()
        for i, color in enumerate([I_COLOR, J_COLOR, K_COLOR]):
            vect = np.zeros(3)
            vect[i] = 1
            arrow = Arrow(
                prism.get_edge_center(vect), 2 * vect,
                preserve_tip_size_when_scaling=False,
                color=color,
                buff=0,
            )
            arrows.add(arrow)
        arrows.set_shade_in_3d(True)
        prism.arrows = arrows
        prism.add(arrows)
        return prism

    def add_basis_vector_labels(self):
        labels = VGroup(
            OldTex("\\hat{\\textbf{\\i}}"),
            OldTex("\\hat{\\textbf{\\j}}"),
            OldTex("\\hat{\\textbf{k}}"),
        )

        def generate_updater(arrow):
            return lambda m: m.move_to(
                arrow.get_end() + 0.2 * normalize(arrow.get_vector()),
            )

        for arrow, label in zip(self.prism.arrows, labels):
            label.match_color(arrow)
            label.add_updater(generate_updater(arrow))
            self.add_fixed_orientation_mobjects(label)
