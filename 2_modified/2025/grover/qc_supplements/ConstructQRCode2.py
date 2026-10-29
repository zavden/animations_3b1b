# ==============================================================================
# Scene:      ConstructQRCode2
# Source:     videos/_2025/grover/qc_supplements.py (lines 1443-1526)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ConstructQRCode2.py ConstructQRCode2 -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/channel_support_QR_code.svg  (generated: real QR of '3b1b.co/support' with one square per module and 6 position-eye pieces)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *

class ConstructQRCode2(InteractiveScene):
    def construct(self):
        # Test
        code = SVGMobject("channel_support_QR_code")
        code.set_fill(BLACK, 1)
        code.set_height(4)
        background = SurroundingRectangle(code, buff=0.25)
        background.set_fill(GREY_A, 1)
        background.set_stroke(width=0)
        background.set_z_index(-1)

        squares = code[:-6]
        corner_pieces = code[-6:]

        squares.shuffle()
        squares.sort(get_norm)
        squares.set_fill(interpolate_color(BLUE_E, BLACK, 0.5), 1)

        union = Union(*squares.copy().space_out_submobjects(0.99)).scale(1 / 0.99)
        union.set_stroke(WHITE, 2)
        union_pieces = VGroup(
            VMobject().set_points(path)
            for path in union.get_subpaths()
        )
        union_pieces.submobjects.sort(key=lambda m: -len(m.get_points()))
        union_pieces.note_changed_family()
        union_pieces.set_stroke(WHITE, 1)
        union_pieces.set_anti_alias_width(3)

        # New
        frame = self.frame
        frame.set_height(3)
        self.add(background, union_pieces, squares, corner_pieces)
        self.play(
            frame.animate.to_default_state(),
            ShowCreation(
                union_pieces,
                lag_ratio=0,
            ),
            # Write(squares, lag_ratio=0.1, time_span=(10, 20)),
            FadeIn(background, time_span=(20, 25)),
            Write(squares, stroke_color=BLUE, stroke_width=1, time_span=(12, 25)),
            Write(corner_pieces, time_span=(20, 25)),
            run_time=25,
        )
        self.play(
            FadeOut(union_pieces),
            squares.animate.set_fill(BLACK, 1),
        )
        squares.shuffle()
        self.play(LaggedStart(
            *(
                Rotate(square, 90 * DEG)
                for square in squares
            ),
            lag_ratio=0.02,
            run_time=10
        ))

        # Old
        return

        squares.save_state()
        squares.arrange_in_grid(buff=0)
        squares.move_to(background)
        squares.shuffle()
        for square in squares:
            dot = Dot()
            dot.set_fill(BLACK)
            dot.replace(square)
            square.set_points(dot.get_points())
        squares.set_stroke(WHITE, 1)
        squares.set_fill(opacity=0)

        background.save_state()
        background.set_fill(GREY_D)
        background.match_height(squares.saved_state)

        self.play(
            Restore(background),
            Restore(squares, lag_ratio=0.1),
            Write(corner_pieces, time_span=(18, 23), lag_ratio=0.25),
            run_time=35,
        )
