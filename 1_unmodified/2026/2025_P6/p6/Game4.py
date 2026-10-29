# ==============================================================================
# Scene:      Game4
# Source:     videos/_2026/2025_P6/p6.py (lines 4408-4529)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Game4.py Game4 -w -m --fps 15
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)


class Game4(InteractiveScene):
    def construct(self):
        # Add the board
        BOARD_N = 19
        board_extent = 6.2
        spacing = board_extent / (BOARD_N - 1)
        board_center = np.array([0.0, 0.0, 0.0])

        def grid_point(col, row):
            return board_center + np.array([
                -board_extent / 2 + col * spacing,
                -board_extent / 2 + row * spacing,
                0.0,
            ])

        board_bg = Square(side_length=board_extent + spacing * 1.4)
        board_bg.set_fill(color=TEAL_D, opacity=1)
        board_bg.set_stroke(width=0)
        board_bg.move_to(board_center)

        grid_lines = VGroup(*[
            Line(grid_point(i, 0), grid_point(i, BOARD_N - 1),
                 stroke_color=GREY_D, stroke_width=3)
            for i in range(BOARD_N)
        ], *[
            Line(grid_point(0, i), grid_point(BOARD_N - 1, i),
                 stroke_color=GREY_D, stroke_width=3)
            for i in range(BOARD_N)
        ])
        hoshi = VGroup(*[
            Dot(grid_point(c, r), radius=0.045, color=BLACK)
            for c in (3, 9, 15) for r in (3, 9, 15)
        ])
        self.add(board_bg, grid_lines)

        # Moves data
        LETTERS = "ABCDEFGHJKLMNOPQRST"
        COORDS = [
            "Q16", "D4", "C16", "R4", "P4", "P3", "O3", "Q3", "C6", "F3", "N4", "Q5",
            "J3", "E17", "H16", "C13", "E16", "C10", "D17", "B4", "O17", "R11", "E4",
            "E5", "D9", "F4", "C9", "D10", "E10", "E11", "F11", "E12", "F12", "B10",
            "F9", "F13", "G13", "F14", "G14", "N17", "N16", "M17", "O18", "J16",
            "H17", "K13", "Q10", "Q11", "P10", "P11", "O11", "O12", "N12", "O13",
            "N13", "N11", "O10", "N14", "M11", "O15", "O16", "N10", "M14", "N9",
            "N15", "O14", "M12", "R10", "L9", "J9", "K11", "G12", "H10", "G15",
            "H15", "F16", "F17",
            "L11",
            "K10", "M10", "L12", "K12", "N8", "O9", "P8", "P9", "Q9", "Q8", "R9",
            "O8", "L10", "J11", "S9", "P7", "Q13", "R8", "C4", "C5", "P15",
            "S8", "T9", "S10", "H13", "J10", "L7", "G11", "F10", "K8", "L8", "G8",
            "F8", "G7", "C12", "E15", "E18", "B13", "D13", "E13", "E6", "F5", "D14",
            "D12", "J7", "H9", "B6", "J14", "G16", "F15", "H14", "J12", "B12", "C11",
            "H5", "G5", "P2", "S13", "D6", "C3", "Q2", "R2", "S14", "R13", "R14",
            "K17", "G2", "T14", "T15", "T13", "S16", "B8", "B9", "A9", "C8", "H6",
            "J6", "H4", "F2", "E2", "E1", "D1", "A12", "A11", "L16", "J15", "L17",
            "L18", "G9", "J18", "R12", "S12", "R1", "S1", "P12", "T8", "P14", "T10",
            "P5", "K4",
        ]
        NUMBERS = list(range(1, 177)) + [179, 180]
        assert len(COORDS) == len(NUMBERS) == 178

        board = {}

        def neighbors(p):
            c, r = p
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nc, nr = c + dc, r + dr
                if 0 <= nc < BOARD_N and 0 <= nr < BOARD_N:
                    yield (nc, nr)

        def group_and_liberties(start):
            color = board[start]
            stack, seen, group, libs = [start], set(), set(), set()
            while stack:
                p = stack.pop()
                if p in seen:
                    continue
                seen.add(p)
                group.add(p)
                for np_ in neighbors(p):
                    c = board.get(np_)
                    if c is None:
                        libs.add(np_)
                    elif c == color and np_ not in seen:
                        stack.append(np_)
            return group, libs

        stone_radius = spacing * 0.47
        stone_mobs = {}

        # Play the sequence of moves
        for n, coord_s in zip(NUMBERS, COORDS):
            color = "B" if n % 2 == 1 else "W"
            col = LETTERS.index(coord_s[0])
            row = int(coord_s[1:]) - 1
            pos = (col, row)

            board[pos] = color
            opp = "W" if color == "B" else "B"
            captured = []
            for np_ in neighbors(pos):
                if board.get(np_) == opp:
                    group, libs = group_and_liberties(np_)
                    if not libs:
                        captured.extend(group)
            captured = sorted(set(captured))
            for cp in captured:
                del board[cp]

            stone = Circle(radius=stone_radius)
            stone.set_fill(BLACK if color == "B" else WHITE, opacity=1)
            stone.set_stroke(width=0)
            stone.move_to(grid_point(*pos))

            fade_outs = [FadeOut(stone_mobs[cp]) for cp in captured if cp in stone_mobs]
            self.play(FadeIn(stone), *fade_outs, run_time=0.12)

            stone_mobs[pos] = stone
            for cp in captured:
                stone_mobs.pop(cp, None)

        self.wait(2)
