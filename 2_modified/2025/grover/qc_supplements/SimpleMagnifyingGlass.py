# ==============================================================================
# Scene:      SimpleMagnifyingGlass
# Source:     videos/_2025/grover/qc_supplements.py (lines 844-860)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SimpleMagnifyingGlass.py SimpleMagnifyingGlass -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/magnifying_glass2.svg  (substitute: copy of the repo's magnifying_glass.svg)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *

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


class SimpleMagnifyingGlass(InteractiveScene):
    def construct(self):
        # Test
        glass = get_magnifying_glass(height=3)
        glass.to_corner(UL)
        glass.target = glass.generate_target()
        glass.target.scale(1.75)
        glass.target.shift(1.5 * LEFT - glass.target[0].get_center())

        self.add(glass)
        self.wait()
        self.play(
            MoveToTarget(glass, path_arc=-45 * DEG),
            run_time=6,
            rate_func=there_and_back_with_pause,
        )
        self.wait()
