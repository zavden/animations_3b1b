# ==============================================================================
# Scene:      SudokuChecker
# Source:     videos/_2025/grover/clarification.py (lines 164-212)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SudokuChecker.py SudokuChecker -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class SudokuChecker(InteractiveScene):
    def construct(self):
        # Introduce, and add solution
        sudoku = Sudoku(height=6)
        sudoku.unlocked_numbers.set_opacity(0)

        self.play(Write(sudoku, run_time=3, lag_ratio=1e-2))
        sudoku.unlocked_numbers.shuffle()
        self.play(sudoku.unlocked_numbers.animate.set_opacity(1).set_anim_args(lag_ratio=0.1), run_time=3)
        self.wait()

        # Check rows, columns, squares
        row_rects, col_rects, square_rects = rect_groups = VGroup(
            VGroup(
                VGroup(SurroundingRectangle(num) for num in sg)
                for sg in group
            )
            for group in [sudoku.get_rows(), sudoku.get_columns(), sudoku.get_number_squares()]
        )
        rect_groups.set_stroke(YELLOW, 3)

        for group in rect_groups:
            self.play(
                LaggedStart(*(
                    VFadeInThenOut(sg, lag_ratio=0.025)
                    for sg in group
                ), lag_ratio=0.5, run_time=5)
            )

        # Replace with question marks
        unlocked_numbers = sudoku.unlocked_numbers
        q_marks = VGroup(
            Text("?").replace(num, 1)
            for num in sudoku.unlocked_numbers
        )
        q_marks.set_color(RED)
        unlocked_numbers.save_state()
        self.play(
            Transform(unlocked_numbers, q_marks, lag_ratio=1e-2, run_time=2)
        )
        self.wait()
        self.play(Restore(unlocked_numbers))

        # Show randomization
        def randomize_numbers(numbers):
            for number in numbers:
                number.set_value(random.uniform(1, 9))

        self.play(UpdateFromFunc(sudoku.unlocked_numbers, randomize_numbers, run_time=10))
