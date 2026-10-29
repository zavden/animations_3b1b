# ==============================================================================
# Scene:      SudokuCheckingCode
# Source:     videos/_2025/grover/clarification.py (lines 215-257)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SudokuCheckingCode.py SudokuCheckingCode -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SudokuCheckingCode(InteractiveScene):
    def construct(self):
        # Thanks Claude!
        code = Code("""
            def is_valid_sudoku(board):
                \"\"\"
                Check if a completed Sudoku board is valid.

                Args:
                    board: A 9x9 list of lists where each
                    cell contains an integer from 1 to 9

                Returns:
                    bool: True if the solution is valid, False otherwise
                \"\"\"
                # Check rows
                for row in board:
                    if set(row) != set(range(1, 10)):
                        return False

                # Check columns
                for col in range(9):
                    column = [board[row][col] for row in range(9)]
                    if set(column) != set(range(1, 10)):
                        return False

                # Check 3x3 sub-boxes
                for box_row in range(0, 9, 3):
                    for box_col in range(0, 9, 3):
                        # Get all numbers in the current 3x3 box
                        box = []
                        for i in range(3):
                            for j in range(3):
                                box.append(board[box_row + i][box_col + j])
                        if set(box) != set(range(1, 10)):
                            return False

                # If all checks pass, the solution is valid
                return True
        """, alignment="LEFT")
        code.set_height(7)
        self.play(ShowIncreasingSubsets(code, run_time=8, rate_func=linear))
        self.wait()
