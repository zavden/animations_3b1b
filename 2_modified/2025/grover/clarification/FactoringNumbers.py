# ==============================================================================
# Scene:      FactoringNumbers
# Source:     videos/_2025/grover/clarification.py (lines 1430-1459)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl FactoringNumbers.py FactoringNumbers -w -m --fps 15
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

class FactoringNumbers(InteractiveScene):
    def construct(self):
        # Show factoring number
        factor_values = [314159265359, 1618033988749]
        icon = get_quantum_computer_symbol(height=2).move_to(RIGHT)
        factors = VGroup(Integer(value) for value in factor_values)
        factors.arrange(RIGHT, buff=LARGE_BUFF)
        product_value = int(factor_values[0] * factor_values[1])
        product = Tex("{:,d}".format(product_value).replace(",", "{,}"))
        product.next_to(icon, LEFT)

        product.set_color(TEAL)
        factors.set_submobject_colors_by_gradient(BLUE, GREEN)

        times = Tex(R"\times")
        times.move_to(factors)

        factor_group = VGroup(factors[0], times, factors[1])
        factor_group.arrange(DOWN, SMALL_BUFF)
        factor_group.next_to(icon, RIGHT, MED_LARGE_BUFF)

        self.add(icon)
        self.play(FadeIn(product, lag_ratio=0.1))
        self.wait()
        self.play(LaggedStart(
            FadeOutToPoint(product.copy(), icon.get_center(), lag_ratio=0.02, path_arc=45 * DEG),
            FadeInFromPoint(factor_group, icon.get_center(), lag_ratio=0.02, path_arc=45 * DEG),
            lag_ratio=0.3
        ))
        self.wait()
