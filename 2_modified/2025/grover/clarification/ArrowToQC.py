# ==============================================================================
# Scene:      ArrowToQC
# Source:     videos/_2025/grover/clarification.py (lines 260-272)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl ArrowToQC.py ArrowToQC -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *


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

class ArrowToQC(InteractiveScene):
    def construct(self):
        # Test
        icon = get_quantum_computer_symbol(height=2.5)
        icon.center().to_edge(DOWN)
        arrow = Vector(1.5 * DOWN, thickness=6)
        arrow.next_to(icon, UP)

        self.play(
            GrowArrow(arrow),
            FadeIn(icon, DOWN)
        )
        self.wait()
