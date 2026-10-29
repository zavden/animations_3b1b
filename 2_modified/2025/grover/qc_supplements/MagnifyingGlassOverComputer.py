# ==============================================================================
# Scene:      MagnifyingGlassOverComputer
# Source:     videos/_2025/grover/qc_supplements.py (lines 459-473)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MagnifyingGlassOverComputer.py MagnifyingGlassOverComputer -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#   - _lib/assets/svg_images/magnifying_glass2.svg  (substitute: copy of the repo's magnifying_glass.svg)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *

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


def get_magnifying_glass(height=3.0, color=GREY_D):
    glass = SVGMobject("magnifying_glass2")
    glass.set_fill(GREY_D)
    glass.set_shading(0.35, 0.15, 0.5)
    circle = VMobject().set_points(glass[0].get_subpaths()[1])
    circle.set_fill(GREEN_SCREEN, 1, border_width=3)
    circle.set_stroke(width=0)
    glass.add_to_back(circle)
    glass.set_height(height)
    return glass


class MagnifyingGlassOverComputer(InteractiveScene):
    def construct(self):
        # Test
        comp = get_quantum_computer_symbol(height=2.5)
        comp.center()
        glass = get_magnifying_glass()
        glass.next_to(comp, UL, buff=2).shift_onto_screen()

        self.add(comp, glass)
        self.play(
            glass.animate.shift(-glass[0].get_center()).set_anim_args(path_arc=-60 * DEG),
            rate_func=there_and_back_with_pause,
            run_time=6
        )
        self.wait()
