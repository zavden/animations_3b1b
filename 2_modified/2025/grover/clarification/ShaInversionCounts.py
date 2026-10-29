# ==============================================================================
# Scene:      ShaInversionCounts
# Source:     videos/_2025/grover/clarification.py (lines 1380-1400)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl ShaInversionCounts.py ShaInversionCounts -w -m --fps 15
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


def get_classical_computer_symbol(height=2, color=GREY_B, symbol_tex=R"\mathcal{C}", symbol_color=YELLOW):
    return get_quantum_computer_symbol(height, color, symbol_tex, symbol_color)



# ----- From _2025/grover/clarification.py -----

class ShaInversionCounts(InteractiveScene):
    def construct(self):
        # Test
        classical = VGroup(
            get_classical_computer_symbol(height=1),
            TexText("$2^{256}$ Steps"),
        )
        quantum = VGroup(
            get_quantum_computer_symbol(height=1),
            TexText(R"$\displaystyle \left\lceil \frac{\pi}{4} 2^{128} \right\rceil$ Steps"),
        )
        group = VGroup(classical, quantum)
        for elem in group:
            elem.arrange(RIGHT)
        group.arrange(DOWN, buff=2.0, aligned_edge=LEFT)
        group.to_corner(UR)

        self.play(FadeIn(classical, UP))
        self.wait()
        self.play(FadeTransformPieces(classical.copy(), quantum, lag_ratio=1e-4))
        self.wait()
