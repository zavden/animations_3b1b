# ==============================================================================
# Scene:      StateVectorsAsABasis
# Source:     videos/_2025/grover/clarification.py (lines 357-433)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl StateVectorsAsABasis.py StateVectorsAsABasis -w -m --fps 15
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

class StateVectorsAsABasis(InteractiveScene):
    def construct(self):
        # Axes
        frame = self.frame
        x_range = y_range = z_range = (-2, 2, 1)
        axes = ThreeDAxes(x_range, y_range, z_range)
        axes.set_height(4)

        basis_vectors = VGroup(
            Vector(2 * vect, thickness=4)
            for vect in np.identity(3)
        )
        basis_vectors.set_submobject_colors_by_gradient(BLUE_D, BLUE_B)
        for vect in basis_vectors:
            vect.rotate(90 * DEG, axis=vect.get_vector())

        frame.reorient(-23, 81, 0, (-1.0, 0, 0.5), 4)
        frame.add_ambient_rotation()
        self.add(axes)

        # Bit strings
        two_qubits = VGroup(
            KetGroup(BitString(n, length=2))
            for n in range(4)
        )
        four_qubits = VGroup(
            KetGroup(BitString(n, length=4))
            for n in range(16)
        )
        for group in [two_qubits, four_qubits]:
            group.fix_in_frame()
            group.arrange(DOWN)
            group.set_max_height(7)
            group.to_edge(LEFT, buff=LARGE_BUFF)
        two_qubits.scale(1.5, about_edge=LEFT).space_out_submobjects(1.25)

        basis_labels = VGroup(
            two_qubits[0].copy().scale(0.3).rotate(90 * DEG, RIGHT).next_to(basis_vectors[0].get_end(), OUT, SMALL_BUFF),
            two_qubits[1].copy().scale(0.3).rotate(90 * DEG, RIGHT).next_to(basis_vectors[1].get_end(), OUT, SMALL_BUFF),
            two_qubits[2].copy().scale(0.3).rotate(90 * DEG, RIGHT).next_to(basis_vectors[2].get_end(), RIGHT, SMALL_BUFF),
        )
        basis_labels.unfix_from_frame()

        self.play(LaggedStartMap(FadeIn, two_qubits, shift=0.5 * UP, lag_ratio=0.5))

        for src, trg, vect in zip(two_qubits, basis_labels, basis_vectors):
            self.play(
                TransformFromCopy(src, trg),
                GrowArrow(vect)
            )
        self.wait(2)

        # Name basis vectors
        basis_name = TexText(R"``Basis vectors''")
        basis_name.fix_in_frame()
        basis_name.set_color(BLUE)
        basis_name.to_corner(UR, buff=MED_SMALL_BUFF)
        self.play(Write(basis_name))
        self.wait(10)
        self.play(FadeOut(basis_name))

        # Replace with larger vectors
        new_basis_labels = VGroup(
            four_qubits[0].copy().scale(0.3).rotate(90 * DEG, RIGHT).next_to(basis_vectors[0].get_end(), OUT, SMALL_BUFF),
            four_qubits[1].copy().scale(0.3).rotate(90 * DEG, RIGHT).next_to(basis_vectors[1].get_end(), OUT, SMALL_BUFF),
            four_qubits[2].copy().scale(0.3).rotate(90 * DEG, RIGHT).next_to(basis_vectors[2].get_end(), RIGHT, SMALL_BUFF),
        )
        new_basis_labels.unfix_from_frame()
        self.play(
            FadeOut(two_qubits),
            FadeOut(basis_labels),
            LaggedStartMap(FadeIn, four_qubits, lag_ratio=0.25)
        )

        for src, trg in zip(four_qubits, new_basis_labels):
            self.play(TransformFromCopy(src, trg))
        self.wait(20)
