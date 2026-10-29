# ==============================================================================
# Scene:      OperationsOnQC
# Source:     videos/_2025/grover/clarification.py (lines 436-465)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py, _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl OperationsOnQC.py OperationsOnQC -w -m --fps 15
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



# ----- From _2025/grover/clarification.py -----

class OperationsOnQC(InteractiveScene):
    def construct(self):
        # Bad output
        icon = get_quantum_computer_symbol(height=3)
        icon.center()
        in_ket = KetGroup(BitString(12).scale(2))
        in_ket.next_to(icon, LEFT)
        arrows = Vector(RIGHT, thickness=4).replicate(2)
        arrows[0].next_to(icon, LEFT)
        arrows[1].next_to(icon, RIGHT)
        in_ket.next_to(arrows, LEFT)

        bad_output = VGroup(Text("True"), Text("or"), Text("False"))
        bad_output.scale(1.5)
        bad_output.arrange(DOWN)
        bad_output.next_to(arrows, RIGHT)
        big_cross = Cross(bad_output)
        big_cross.scale(1.25)
        big_cross.set_stroke(RED, [0, 12, 12, 12, 0])

        self.add(icon, arrows, in_ket)
        self.play(LaggedStart(
            FadeOut(in_ket.copy(), shift=2 * RIGHT, scale=0.5),
            FadeIn(bad_output, shift=2 * RIGHT, scale=2),
            lag_ratio=0.5
        ))
        self.play(ShowCreation(big_cross))
        self.wait()
        self.play(FadeOut(in_ket), FadeOut(bad_output), FadeOut(big_cross))
        self.wait()
