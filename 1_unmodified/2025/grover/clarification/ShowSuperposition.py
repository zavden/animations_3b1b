# ==============================================================================
# Scene:      ShowSuperposition
# Source:     videos/_2025/grover/clarification.py (lines 745-845)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl ShowSuperposition.py ShowSuperposition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/state_vectors.py -----

class BitString(VGroup):
    def __init__(self, value, length=4, buff=SMALL_BUFF):
        self.length = length
        bit_mob = Integer(0)
        super().__init__(bit_mob.copy() for n in range(length))
        self.arrange(RIGHT, buff=buff)
        self.set_value(value)

    def set_value(self, value):
        bits = bin(value)[2:].zfill(self.length)
        for mob, bit in zip(self, bits):
            mob.set_value(int(bit))


class Ket(Tex):
    def __init__(self, mobject, height_scale_factor=1.25, buff=SMALL_BUFF):
        super().__init__(R"| \rangle")
        self.set_height(height_scale_factor * mobject.get_height())
        self[0].next_to(mobject, LEFT, buff)
        self[1].next_to(mobject, RIGHT, buff)


class KetGroup(VGroup):
    def __init__(self, mobject, **kwargs):
        ket = Ket(mobject, **kwargs)
        super().__init__(ket, mobject)



# ----- From _2025/grover/clarification.py -----

class ShowSuperposition(InteractiveScene):
    def construct(self):
        # Axes
        frame = self.frame
        x_range = y_range = z_range = (-2, 2, 1)
        axes = ThreeDAxes(x_range, y_range, z_range)
        unit_size = 3
        axes.set_height(2 * unit_size)

        basis_vectors = VGroup(
            Vector(unit_size * vect, thickness=5)
            for vect in np.identity(3)
        )
        basis_vectors.set_submobject_colors_by_gradient(BLUE_D, BLUE_B)
        for n, vect in enumerate(basis_vectors):
            if n < 2:
                vect.always.set_perpendicular_to_camera(frame)
            else:
                vect.rotate(90 * DEG, OUT)

        frame.reorient(-33, 74, 0)
        frame.clear_updaters()
        frame.add_ambient_rotation(0.5 * DEG)
        self.add(axes)
        self.add(basis_vectors)

        # Label bases
        basis_labels = VGroup(
            KetGroup(BitString(n, length=2)).set_height(0.35)
            for n in range(3)
        )
        basis_labels.rotate(90 * DEG, RIGHT)
        for label, vect, direction in zip(basis_labels, basis_vectors, [RIGHT, UP + OUT, RIGHT]):
            label.next_to(vect.get_end(), direction, MED_SMALL_BUFF)
            label.set_fill(vect.get_color(), 1)

        self.add(basis_labels, basis_vectors)
        self.wait(4)

        # Show a general vector
        vect_coords = normalize([np.sqrt(2) / 2, 0.5, 0.5])
        vector = Vector(unit_size * vect_coords, thickness=5, fill_color=TEAL)
        vector.set_perpendicular_to_camera(frame)
        dec_kw = dict(include_sign=True, font_size=36)
        vect_label = VGroup(
            DecimalNumber(vect_coords[0], **dec_kw),
            KetGroup(BitString(0, 2)),
            DecimalNumber(vect_coords[1], **dec_kw),
            KetGroup(BitString(1, 2)),
            DecimalNumber(vect_coords[2], **dec_kw),
            KetGroup(BitString(2, 2)),
            DecimalNumber(0, **dec_kw),
            KetGroup(BitString(3, 2)),
        )
        vect_label[1::2].set_submobject_colors_by_gradient(BLUE, BLUE_E)
        vect_label.arrange(RIGHT, buff=SMALL_BUFF)
        vect_label.rotate(90 * DEG, RIGHT)
        vect_label.next_to(vector.get_end(), RIGHT)

        self.play(
            GrowArrow(vector),
            frame.animate.set_x(1),
        )
        self.play(FadeIn(vect_label))
        self.wait(5)

        # Show column vector
        col = DecimalMatrix(np.array([*vect_coords, 0]).reshape(-1, 1), decimal_config=dec_kw)
        col.scale(0.75)
        col.rotate(90 * DEG, RIGHT)
        col.next_to(vector.get_end(), RIGHT)
        eq = Tex("=")
        eq.rotate(90 * DEG, RIGHT)
        eq.next_to(col, RIGHT, SMALL_BUFF)

        self.play(
            FadeIn(col.get_brackets()),
            TransformFromCopy(vect_label[0::2], col.get_entries(), run_time=2),
            FadeIn(eq),
            vect_label.animate.next_to(eq, RIGHT, SMALL_BUFF)
        )

        # Surrounding rectangles
        rects = VGroup(
            SurroundingRectangle(mob.copy().rotate(90 * DEG, LEFT)).rotate(90 * DEG, RIGHT)
            for mob in [col, vect_label]
        )
        rects.set_stroke(YELLOW, 2)
        self.play(ShowCreation(rects[0]))
        self.wait(5)
        self.play(Transform(*rects))
        self.wait(7)

        # Write superposition
        word = TexText("``Superposition''", font_size=72)
        word.rotate(90 * DEG, RIGHT)
        word.set_color(YELLOW)
        word.next_to(rects[0], OUT)

        self.play(Write(word), frame.animate.set_x(2), run_time=3)
        self.wait(8)
