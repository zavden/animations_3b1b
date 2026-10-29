# ==============================================================================
# Scene:      TwoByTwoGrid
# Source:     videos/_2025/grover/clarification.py (lines 468-645)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py, _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl TwoByTwoGrid.py TwoByTwoGrid -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#   - _lib/assets/svg_images/and_gate.svg  (generated placeholder: ANSI AND gate with terminals)
#   - _lib/assets/svg_images/or_gate.svg  (generated placeholder: ANSI OR gate with terminals)
#   - _lib/assets/svg_images/not_gate.svg  (generated placeholder: ANSI NOT gate with terminals)
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


def get_blackbox_machine(height=2, color=GREY_D, label_tex="f(n)", label_height_ratio=0.25):
    square = Square(height)
    in_tri = ArrowTip().set_height(0.5 * height)
    out_tri = in_tri.copy().rotate(PI)
    in_tri.move_to(square.get_left())
    out_tri.move_to(square.get_right())
    machine = Union(square, in_tri, out_tri)
    machine.set_fill(color, 1)
    machine.set_stroke(WHITE, 2)

    label = Tex(label_tex)
    label.set_height(label_height_ratio * height)
    label.move_to(machine)
    machine.add(label)

    machine.output_group = VGroup()

    return machine



# ----- From _2025/grover/clarification.py -----

default_sudoku_values = [  # TODO
    [7, 4, 3, 6, 5, 1, 9, 8, 2],
    [1, 8, 9, 2, 3, 4, 7, 6, 5],
    [6, 2, 5, 9, 8, 7, 4, 3, 1],
    [3, 2, 5, 8, 6, 9, 4, 1, 7],
    [9, 7, 6, 3, 4, 1, 5, 2, 8],
    [1, 4, 8, 7, 5, 2, 3, 6, 9],
    [2, 3, 8, 5, 7, 6, 1, 9, 4],
    [4, 1, 7, 8, 9, 3, 6, 5, 2],
    [5, 9, 6, 2, 1, 4, 8, 7, 3],
]


default_sudoku_locked_cells = [
    [3, 7, 8],
    [1, 6, 7, 8],
    [3, 5],
    [1, 3, 6, 8],
    [5],
    [1, 3, 4, 8],
    [5, 6],
    [5],
    [4, 9],
]


class Sudoku(VGroup):
    def __init__(
        self,
        values=default_sudoku_values,
        locked_cells=default_sudoku_locked_cells,
        height=4,
        big_square_stroke_width=3,
        little_square_stroke_width=0.5,
        locked_number_color=BLUE_B,
        num_to_square_height_ratio=0.5
    ):
        self.big_grid = self.get_square_grid(height, big_square_stroke_width)
        self.little_grids = VGroup(
            self.get_square_grid(height / 3, little_square_stroke_width).move_to(square)
            for square in self.big_grid
        )
        self.numbers = VGroup(
            VGroup(
                Integer(num).replace(square, 1).scale(num_to_square_height_ratio)
                for square, num in zip(grid, arr)
            )
            for grid, arr in zip(self.little_grids, values)
        )
        self.locked_cells = locked_cells
        self.locked_numbers = VGroup()
        self.unlocked_numbers = VGroup()

        for coords, group in zip(locked_cells, self.numbers):
            for x, num in enumerate(group):
                if x in coords:
                    self.locked_numbers.add(num)
                else:
                    self.unlocked_numbers.add(num)
        self.locked_numbers.set_fill(locked_number_color, border_width=2)

        super().__init__(self.big_grid, self.little_grids, self.numbers)

    def get_rows(self):
        grids = self.numbers
        slices = [slice(0, 3), slice(3, 6), slice(6, 9)]
        rows = VGroup()
        for slc1 in slices:
            for slc2 in slices:
                row = VGroup()
                for grid in grids[slc1]:
                    for num in grid[slc2]:
                        row.add(num)
                rows.add(row)
        return rows

    def get_columns(self):
        grids = self.numbers
        slices = [slice(0, 9, 3), slice(1, 9, 3), slice(2, 9, 3)]
        cols = VGroup()
        for slc1 in slices:
            for slc2 in slices:
                col = VGroup()
                for grid in grids[slc1]:
                    for num in grid[slc2]:
                        col.add(num)
                cols.add(col)
        return cols

    def get_number_squares(self):
        return self.numbers

    def get_square_grid(
        self,
        height,
        stroke_width,
        stroke_color=WHITE,
        fill_color=GREY_E,
    ):
        square = Square()
        square.set_fill(fill_color, 1)
        square.set_stroke(stroke_color, stroke_width)
        grid = square.get_grid(3, 3, buff=0)
        grid.set_height(height)
        return grid


class TwoByTwoGrid(InteractiveScene):
    random_seed = 1

    def construct(self):
        # Set up
        rects = ScreenRectangle().set_height(FRAME_HEIGHT / 2).get_grid(2, 2, buff=0)
        h_line = Line(LEFT, RIGHT).replace(rects, 0)
        v_line = Line(UP, DOWN).replace(rects, 1)
        lines = VGroup(h_line, v_line)
        lines.set_stroke(WHITE, 2)

        self.add(lines)

        # Add classical verifiers
        verifiers = get_blackbox_machine(label_tex="").replicate(4)
        for n, verifier, rect in zip(it.count(), verifiers, rects):
            verifier.set_height(1.0)
            verifier.move_to(rect)
            if n < 2:
                label = Text("Verifier", font_size=24)
                label.set_color(YELLOW)
            else:
                verifier.rotate(90 * DEG)
                label = get_quantum_computer_symbol(height=0.75)

            label.move_to(verifier)
            verifier.add(label)

        verifiers[:2].shift(0.75 * RIGHT)

        good_sudoku, bad_sudoku = sudokus = VGroup(
            Sudoku(big_square_stroke_width=2, little_square_stroke_width=0.25)
            for x in range(2)
        )
        sudokus.set_height(2.5)

        for number in bad_sudoku.unlocked_numbers:
            number.set_value(random.randint(1, 9))

        classical_outputs = VGroup(Integer(1), Integer(0))
        marks = VGroup(Checkmark().set_color(GREEN), Exmark().set_color(RED))

        for sudoku, verifier, output, mark in zip(sudokus, verifiers, classical_outputs, marks):
            sudoku.next_to(verifier, LEFT, MED_LARGE_BUFF)
            output.next_to(verifier, RIGHT, MED_LARGE_BUFF)
            mark.match_height(output)
            mark.next_to(output, RIGHT, SMALL_BUFF)

        self.add(verifiers[:2])
        self.add(sudokus)

        for sudoku, verifier, output, mark in zip(sudokus, verifiers, classical_outputs, marks):
            self.play(LaggedStart(
                FadeOutToPoint(sudoku.numbers.copy(), verifier.get_center(), lag_ratio=1e-3),
                FadeInFromPoint(output, verifier.get_center()),
                lag_ratio=0.5,
                run_time=2
            ))
            self.play(Write(mark))

        self.wait()

        # Map to quantum verifiers
        self.play(TransformFromCopy(verifiers[:2], verifiers[2:], run_time=2))
        self.wait()

        # Translate True behavior
        good_input = self.turn_into_bits(good_sudoku)
        good_ket = KetGroup(good_input.copy(), height_scale_factor=1.5)
        good_ket.next_to(verifiers[2], UP)
        good_ket_out = good_ket.copy()
        neg = Tex("-", font_size=24)
        neg.set_fill(GREEN, border_width=3)
        neg.next_to(good_ket_out, LEFT, SMALL_BUFF)
        good_ket_out.add_to_back(neg)
        good_ket_out.next_to(verifiers[2], DOWN, buff=0.2)

        mult_neg_1_words = TexText(R"Multiply\\by $-1$", font_size=36)
        mult_neg_1_words.set_fill(TEAL_A)
        mult_neg_1_words.next_to(verifiers[2], RIGHT, MED_LARGE_BUFF)

        self.play(FadeTransform(good_input.copy(), good_ket))
        self.wait()
        self.play(
            LaggedStart(
                FadeOutToPoint(good_ket.copy(), verifiers[2].get_center(), lag_ratio=0.01),
                FadeInFromPoint(good_ket_out, verifiers[2].get_center(), lag_ratio=0.01),
                lag_ratio=0.5
            ),
            FadeIn(mult_neg_1_words, RIGHT),
        )
        self.wait()

        # Translate False behavior (a lot of coying, but I'm in a rush)
        bad_input = self.turn_into_bits(bad_sudoku)
        bad_ket = KetGroup(bad_input.copy(), height_scale_factor=1.5)
        bad_ket.next_to(verifiers[3], UP)
        bad_ket_out = bad_ket.copy()
        bad_ket_out.next_to(verifiers[3], DOWN)

        mult_pos_1_words = TexText(R"Multiply\\by $+1$", font_size=36)
        mult_pos_1_words.set_fill(TEAL_A)
        mult_pos_1_words.next_to(verifiers[3], RIGHT, MED_LARGE_BUFF)

        self.play(FadeTransform(bad_input.copy(), bad_ket))
        self.wait()
        self.play(
            LaggedStart(
                FadeOutToPoint(bad_ket.copy(), verifiers[3].get_center(), lag_ratio=0.01),
                FadeInFromPoint(bad_ket_out, verifiers[3].get_center(), lag_ratio=0.01),
                lag_ratio=0.5
            ),
            FadeIn(mult_pos_1_words, RIGHT),
        )
        self.wait()

        # Show logic gates
        gate_groups = VGroup(
            SVGMobject("and_gate").replicate(2),
            SVGMobject("not_gate").replicate(2),
            SVGMobject("or_gate").replicate(2),
        )
        for group in gate_groups:
            group.set_fill(BLUE)
            group.target = group.generate_target()
            for mob, box in zip(group, verifiers):
                mob.match_height(box)
                mob.scale(0.8)
                mob.next_to(box, UP)
            for mob, box in zip(group.target, verifiers[2:]):
                mob.match_width(box)
                mob.scale(0.7)
                mob.move_to(box)
                mob.set_fill(TEAL, 0.5)

        for group in gate_groups:
            self.play(LaggedStartMap(FadeIn, group, shift=UP, lag_ratio=0.5))
            self.wait()
            self.play(TransformFromCopy(group, group.target))
            self.play(FadeOut(group.target))
            self.play(FadeOut(group))

    def turn_into_bits(self, sudoku):
        # Test
        bits = VGroup(
            BitString(num.get_value()).replace(num, 1).scale(0.35)
            for grid in sudoku.numbers for num in grid
        )
        sudoku.save_state()

        in_group = VGroup(
            bits[0].copy().set_width(0.25),
            Tex(R"\cdots", font_size=20),
            bits[-1].copy().set_width(0.25),
        )
        for piece in in_group:
            piece.space_out_submobjects(0.85)
        in_group[1].scale(0.7)
        in_group.arrange(RIGHT, buff=0.025)
        in_group.replace(sudoku, 0)
        in_group.set_fill(GREY_A)

        sudoku.saved_state.scale(0.5)
        sudoku.saved_state.fade(0.5)
        sudoku.saved_state.to_edge(UP, buff=MED_SMALL_BUFF)

        self.play(
            sudoku.animate.fade(0.9),
            FadeIn(bits, lag_ratio=1e-3)
        )
        self.play(LaggedStart(
            ReplacementTransform(bits[0], in_group[0]),
            *(ReplacementTransform(bs, in_group[1]) for bs in bits[1:-1]),
            ReplacementTransform(bits[-1], in_group[-1]),
            Restore(sudoku),
            lag_ratio=1e-2,
        ))
        return in_group
