# ==============================================================================
# Scene:      FourBitAdder
# Source:     videos/_2025/grover/clarification.py (lines 1462-1472)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FourBitAdder.py FourBitAdder -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/Four_bit_adder_with_carry_lookahead.svg  (generated placeholder: diagram of a 4-bit carry-lookahead adder, 158 strokes)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *

class FourBitAdder(InteractiveScene):
    def construct(self):
        # Test
        circuit = SVGMobject("Four_bit_adder_with_carry_lookahead")
        circuit.set_height(7.0)
        circuit.set_stroke(WHITE, 1)
        circuit.set_fill(BLACK, 0)
        circuit.sort(lambda p: np.dot(p, DR))

        self.play(Write(circuit, lag_ratio=1e-2, run_time=3))
        self.wait()
