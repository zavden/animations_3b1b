# ==============================================================================
# Scene:      CompiledSudokuVerifier
# Source:     videos/_2025/grover/clarification.py (lines 275-354)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py, _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl CompiledSudokuVerifier.py CompiledSudokuVerifier -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
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



# ----- From _2025/grover/qc_supplements.py -----

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


class CompiledSudokuVerifier(InteractiveScene):
    def construct(self):
        # Set up
        sudoku = Sudoku(height=5)
        sudoku.to_edge(LEFT)

        machine = get_blackbox_machine(height=3, label_tex=R"\text{Verifier}")
        machine.next_to(sudoku, RIGHT, LARGE_BUFF)
        machine[-1].scale(0.65).set_color(YELLOW)

        self.add(sudoku)
        self.add(machine)

        # Pile logic gates into the machine
        gates = VGroup(
            SVGMobject("and_gate"),
            SVGMobject("or_gate"),
            SVGMobject("not_gate"),
        )
        names = VGroup(Text(text) for text in ["AND", "OR", "NOT"])
        names.scale(0.5)
        names.set_fill(GREY_C)

        gates.set_height(0.65)
        gates.set_fill(GREY_B)
        gates.arrange(RIGHT, buff=MED_LARGE_BUFF)
        gates.next_to(machine, UP, MED_LARGE_BUFF)
        for name, gate in zip(names, gates):
            name.next_to(gate, UP)

        pile_of_gates = VGroup(*it.chain(*(g.replicate(200) for g in gates)))
        pile_of_gates.shuffle()
        pile_of_gates.set_fill(opacity=0.25)
        pile_of_gates.generate_target()
        for gate in pile_of_gates.target:
            gate.scale(0.25)
            shift = np.random.uniform(-1.5, 1.5, 3)
            shift[2] = 0
            gate.move_to(machine.get_center() + shift)
            gate.set_fill(opacity=0.1)

        self.add(gates, names)
        self.play(
            MoveToTarget(pile_of_gates, lag_ratio=3.0 / len(pile_of_gates), run_time=8)
        )

        # Turn sudoku into binary
        all_numbers = VGroup(num for grid in sudoku.numbers for num in grid)
        bit_groups = VGroup(
            BitString(num.get_value()).replace(num, 1).scale(0.35)
            for num in all_numbers
        )

        self.play(
            ReplacementTransform(all_numbers, bit_groups, lag_ratio=1e-3),
            sudoku.big_grid.animate.set_fill(opacity=0.1).set_stroke(opacity=0.25),
            sudoku.little_grids.animate.set_fill(opacity=0.1).set_stroke(opacity=0.25),
        )
        self.wait()

        target_bits = bit_groups.copy()
        target_bits.arrange(DOWN, buff=0.025)
        target_bits.set_height(machine.get_height() * 0.5)
        target_bits.move_to(machine, LEFT)
        target_bits.set_opacity(0.1)
        self.play(TransformFromCopy(bit_groups, target_bits, lag_ratio=1e-3, run_time=2))
        self.wait()

        # Show outputs
        outputs = VGroup(Integer(1), Integer(0))
        outputs.set_height(0.75)
        outputs.next_to(machine, RIGHT, LARGE_BUFF)
        marks = VGroup(Checkmark().set_color(GREEN), Exmark().set_color(RED))
        for mark, output in zip(marks, outputs):
            mark.match_height(output)
            mark.next_to(output, RIGHT)
            self.play(FadeIn(output, RIGHT))
            self.play(Write(mark))
            self.wait()
            self.play(FadeOut(mark), FadeOut(output))
