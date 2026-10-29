# ==============================================================================
# Scene:      Intro
# Source:     videos/_2025/grover/clarification.py (lines 111-143)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl Intro.py Intro -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The comments folder pointed to Grant's Dropbox (/Users/grant/...): it now uses Path('Comments'), a local folder with placeholder screenshots that data_files copies.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#   - _lib/assets/generated/2025/grover/Comments/comment_1..6.png  (6 placeholder comment screenshots, 900x260, copied to Comments/ next to the scene with data_files)
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

class Intro(InteractiveScene):
    random_seed = 1

    def construct(self):
        # Test
        background = FullScreenRectangle().set_fill(GREY_E)
        background.set_fill(GREY_E, 0.5)
        self.add(background)

        icon = get_quantum_computer_symbol(height=3)
        icon.center()
        self.play(Write(icon, run_time=3, lag_ratio=1e-2, stroke_color=TEAL))
        self.wait()
        self.play(icon.animate.to_edge(LEFT))
        self.wait()

        # Comments
        # CHANGE: local folder with placeholder comment screenshots (the originals are in Grant's Dropbox); it is copied next to the scene via data_files
        folder = Path('Comments')
        comments = Group(
            Group(ImageMobject(folder / name))
            for name in os.listdir(folder)
        )
        for comment in comments:
            comment.add_to_back(SurroundingRectangle(comment, buff=0).set_stroke(WHITE, 1))
            comment.set_width(4)
            comment.move_to(4 * LEFT)
            comment.shift(np.random.uniform(-1, 1) * RIGHT + np.random.uniform(-3, 3) * UP)

        self.play(
            FadeOut(icon, time_span=(0, 2)),
            LaggedStartMap(FadeIn, comments, lag_ratio=0.6, shift=0.25 * UP, run_time=8)
        )
        self.wait()
