# ==============================================================================
# Scene:      ShowLinearityExample
# Source:     videos/_2025/grover/clarification.py (lines 978-1043)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py, _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl ShowLinearityExample.py ShowLinearityExample -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
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



# ----- From _2025/grover/qc_supplements.py -----

def get_quantum_computer_symbol(height=2, color=GREY_B, symbol_tex=R"|Q\rangle", symbol_color=TEAL):
    chip = SVGMobject("computer_chip")
    chip.set_height(height)
    chip.to_edge(RIGHT)
    chip.set_fill(GREY_C)
    chip.set_shading(0.7, 0, 0)
    symbol = Tex(symbol_tex)
    symbol.set_fill(symbol_color)
    symbol.set_stroke(symbol_color, 1)
    symbol.set_height(0.4 * chip.get_height())
    symbol.move_to(chip)

    result = VGroup(chip, symbol)
    return result


def get_blackbox_machine(height=2, color=GREY_D, label_tex="f(n)", label_height_ratio=0.25):
    square = Square(height)
    in_tri = ArrowTip().set_height(0.5 * height)
    out_tri = in_tri.copy().rotate(PI)
    in_tri.move_to(square.get_left())
    out_tri.move_to(square.get_right())
    machine = Union(square, in_tri, out_tri)
    machine.set_fill(color, 1)
    machine.set_stroke(WHITE, 2)

    label = Tex(label_tex)
    label.set_height(label_height_ratio * height)
    label.move_to(machine)
    machine.add(label)

    machine.output_group = VGroup()

    return machine



# ----- From _2025/grover/clarification.py -----

class ShowLinearityExample(InteractiveScene):
    def construct(self):
        # Add machine
        machine = get_blackbox_machine()
        machine[-1].set_color(TEAL)
        icon = get_quantum_computer_symbol(height=1)
        icon.next_to(machine, DOWN)

        self.add(machine, icon)
        self.wait()

        # Show a weighted sum
        kets = VGroup(
            KetGroup(BitString(n, 2))
            for n in range(4)
        )
        kets.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        kets.set_submobject_colors_by_gradient(BLUE, BLUE_E)
        kets.next_to(machine, LEFT, MED_LARGE_BUFF)

        components = VGroup(
            DecimalNumber(n, include_sign=True, font_size=42)
            for n in normalize([1, -2, 3, -4])
        )
        for component, ket in zip(components, kets):
            component.next_to(ket, LEFT, SMALL_BUFF)

        in_group = VGroup(components, kets)
        self.play(FadeIn(in_group, RIGHT))
        self.wait()
        self.play(
            FadeOutToPoint(in_group.copy(), machine.get_left() + RIGHT, lag_ratio=0.01, run_time=2)
        )

        # Show output
        out_kets = VGroup()
        for ket in kets:
            f_group = Tex(R"f()", font_size=60)
            f_group.set_color(TEAL)
            f_group[:2].next_to(ket, LEFT, SMALL_BUFF)
            f_group[2].next_to(ket, RIGHT, SMALL_BUFF)
            out_ket = VGroup(f_group, ket.copy())
            out_kets.add(out_ket)

        out_components = components.copy()
        out_kets.next_to(machine, RIGHT, buff=1.5)
        for out_ket, component in zip(out_kets, out_components):
            component.next_to(out_ket, LEFT, SMALL_BUFF)

        out_group = VGroup(out_components, out_kets)

        self.play(
            FadeInFromPoint(out_group, machine.get_right() + LEFT, lag_ratio=0.01, run_time=2)
        )
        self.wait()

        # Highlight components
        in_rects = VGroup(map(SurroundingRectangle, components))
        out_rects = VGroup(map(SurroundingRectangle, out_components))

        self.play(
            LaggedStartMap(VFadeInThenOut, in_rects, lag_ratio=0.5),
            LaggedStartMap(VFadeInThenOut, out_rects, lag_ratio=0.5),
            run_time=5,
        )
        self.wait()
