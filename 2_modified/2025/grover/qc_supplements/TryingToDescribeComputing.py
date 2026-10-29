# ==============================================================================
# Scene:      TryingToDescribeComputing
# Source:     videos/_2025/grover/qc_supplements.py (lines 900-1010)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TryingToDescribeComputing.py TryingToDescribeComputing -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#   - _lib/assets/svg_images/Four_bit_adder_with_carry_lookahead.svg  (generated placeholder: diagram of a 4-bit carry-lookahead adder, 158 strokes)
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


def get_classical_computer_symbol(height=2, color=GREY_B, symbol_tex=R"\mathcal{C}", symbol_color=YELLOW):
    return get_quantum_computer_symbol(height, color, symbol_tex, symbol_color)


class TryingToDescribeComputing(InteractiveScene):
    def construct(self):
        # Characters
        randy = Randolph()
        randy.move_to(2 * DOWN + 3 * LEFT)
        buddy = PiCreature(color=MAROON_E).flip()
        buddy.next_to(randy, RIGHT, buff=3)
        randy.make_eye_contact(buddy)

        for pi in [randy, buddy]:
            pi.body.insert_n_curves(100)

        self.add(randy, buddy)

        # Objects
        laptop = Laptop()
        laptop.scale(0.75)
        laptop.rotate(70 * DEG, LEFT)
        laptop.rotate(45 * DEG, UP)
        laptop.move_to(UP + 0.5 * LEFT)

        chip = get_classical_computer_symbol(height=1)
        chip.next_to(randy, UR, MED_LARGE_BUFF)

        # Show objects
        self.play(LaggedStart(
            randy.change("raise_right_hand", laptop),
            FadeIn(laptop, UP),
            buddy.change("erm", laptop),
            lag_ratio=0.5,
        ))
        self.play(Blink(buddy))
        self.wait()
        self.play(LaggedStart(
            randy.change("well", buddy.eyes),
            FadeIn(chip, UP),
            laptop.animate.shift(1.5 * UP),
            buddy.change("confused"),
            lag_ratio=0.25
        ))
        self.play(Blink(randy))

        # Show factoring numbers
        factors = Tex(R"91 = 7 \times 13")
        factors.next_to(randy, UL, MED_LARGE_BUFF)
        factors.shift_onto_screen(buff=LARGE_BUFF)
        self.play(
            randy.change("raise_left_hand", factors),
            FadeInFromPoint(factors, chip.get_center(), lag_ratio=0.05),
        )
        self.play(Blink(buddy))
        self.wait(2)

        # Put numbers in chip
        c_label = chip[1]
        chip.remove(c_label)

        seven = factors["7"][0].copy()
        product = factors[R"7 \times 13"][0].copy()

        self.play(
            randy.change('raise_right_hand', chip),
            chip.animate.scale(2, about_edge=DOWN),
            FadeOut(c_label, 0.5 * UP),
            FadeOut(laptop, UP),
            buddy.change("pondering", chip),
        )
        self.play(
            seven.animate.move_to(chip).scale(1.5),
        )
        self.play(Blink(buddy))
        self.wait()

        product.move_to(chip)
        self.play(
            ReplacementTransform(seven, product[0]),
            Write(product[1:]),
            buddy.change('hesitant', chip),
        )
        result = Tex(R"91")
        result.scale(1.5)
        result.move_to(chip)
        self.play(
            TransformFromCopy(product, result, lag_ratio=0.2),
            product.animate.set_opacity(0.25),
        )
        self.play(Blink(randy))
        self.wait()

        # Logic gates
        gates = SVGMobject("Four_bit_adder_with_carry_lookahead")
        gates.set_height(4)
        gates.to_edge(UP, MED_SMALL_BUFF)
        gates.to_edge(LEFT)
        gates.set_fill(opacity=0)
        gates.set_stroke(WHITE, 1)

        self.play(
            randy.change("dance_3", gates),
            Write(gates, run_time=2),
            FadeOut(factors, DOWN),
            buddy.change("awe", gates)
        )
        self.play(Blink(buddy))
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change("tease"),
            FadeOut(gates, 3 * LEFT, rate_func=running_start, path_arc=30 * DEG)
        )
        self.wait()
