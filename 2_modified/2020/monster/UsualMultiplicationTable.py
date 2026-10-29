# ==============================================================================
# Scene:      UsualMultiplicationTable
# Source:     videos/_2020/monster.py (lines 2219-2335)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl UsualMultiplicationTable.py UsualMultiplicationTable -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ls_copies / ts_copies were not defined in the original; left_syms and top_syms are used
# ==============================================================================

from manim_imports_ext import *

class UsualMultiplicationTable(Scene):
    def construct(self):
        # Setup grid
        grid = VGroup(*[
            VGroup(*[Square() for x in range(4)]).arrange(RIGHT, buff=0)
            for y in range(4)
        ]).arrange(DOWN, buff=0)
        grid.set_height(6)
        grid.to_edge(DOWN, buff=0.5)
        grid.set_fill(GREY_E, 1)
        dots = VGroup(
            *[Tex("\\dots").scale(2).next_to(row, RIGHT) for row in grid[:-1]],
            *[Tex("\\vdots").scale(2).next_to(square, DOWN) for square in grid[-1][:-1]],
            OldTex("\\ddots").scale(2).next_to(grid[-1][-1], DR),
        )

        self.add(grid)

        # Setup abstract dots
        table_dots = VGroup()
        for i, row in zip(it.count(1), grid):
            for j, square in zip(it.count(1), row):
                dots = VGroup(*[Dot() for x in range(i * j)])
                dots.arrange_in_grid(i, j, buff=SMALL_BUFF)
                dots.scale(0.9)
                dots.move_to(square)
                table_dots.add(dots)

        left_dots = table_dots[0::4].copy()
        left_dots.shift(grid[0][0].get_width() * LEFT)
        left_dots.set_color(BLUE)

        top_dots = table_dots[0:4].copy()
        top_dots.shift(grid[0][0].get_height() * UP)
        top_dots.set_color(RED)

        dot_groups = VGroup(left_dots, top_dots, table_dots)

        # Numerals
        sym_groups = VGroup()
        for dot_group in dot_groups:
            sym_group = VGroup()
            for dots in dot_group:
                numeral = Integer(len(dots))
                numeral.set_height(0.6)
                numeral.move_to(dots)
                numeral.match_color(dots)
                sym_group.add(numeral)
            sym_groups.add(sym_group)

        left_syms, top_syms, table_syms = sym_groups

        # Add symbols

        self.add(left_syms, top_syms)
        self.play(LaggedStart(*[
            AnimationGroup(
                # CHANGE: ls_copies / ts_copies were not defined in the original; left_syms and top_syms are used
                Transform(left_syms[i].copy(), table_syms[4 * i + j].copy(), remover=True),
                Transform(top_syms[j].copy(), table_syms[4 * i + j].copy(), remover=True),
            )
            for i, j in it.product(range(4), range(4))
        ], lag_ratio=0.3))
        self.add(table_syms)
        self.wait()

        # To dots
        self.play(
            FadeOut(sym_groups),
            FadeIn(dot_groups),
        )
        self.wait()

        # Show a few products
        last_rects = VGroup()
        ns = random.sample(range(16), 5)
        for n in ns:
            i = n // 4
            j = n % 4
            rects = VGroup(
                SurroundingRectangle(left_dots[i]),
                SurroundingRectangle(top_dots[j]),
                grid[i][j].copy().set_fill(YELLOW, 0.5),
            )
            rects.set_stroke(YELLOW, 4)
            self.play(FadeIn(rects), FadeOut(last_rects), run_time=0.5)
            self.wait()
            last_rects = rects
        self.play(FadeOut(last_rects))

        # Back to syms
        self.play(
            dot_groups.fade, 0.8,
            FadeIn(sym_groups),
        )
        self.wait()

        # Benefits
        frame = self.camera.frame
        frame.generate_target()
        frame.target.set_x(grid.get_right()[0])
        frame.target.scale(1.1)

        benefit = VGroup(
            OldTexText("Abstraction").scale(1.5),
            Vector(DOWN),
            OldTexText("Less cumbersome").scale(1.5),
        )
        benefit.arrange(DOWN)
        benefit.next_to(grid, RIGHT, buff=LARGE_BUFF)

        turn_animation_into_updater(MoveToTarget(frame, run_time=3))
        self.add(frame)

        self.play(Write(benefit[0]))
        self.play(GrowArrow(benefit[1]))
        self.play(FadeIn(benefit[2], UP))
        self.wait()
