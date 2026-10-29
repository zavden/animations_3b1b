# ==============================================================================
# Scene:      FromRowsToColumns
# Source:     videos/_2021/shadows.py (lines 5176-5219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FromRowsToColumns.py FromRowsToColumns -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FromRowsToColumns(Scene):
    def construct(self):
        n = 5
        grid = Dot().get_grid(n, n, buff=MED_LARGE_BUFF)

        grids = grid.get_grid(1, 2, buff=3)

        buff = 0.2
        row_rects = VGroup(*(
            SurroundingRectangle(grids[0][k:k + n], buff=buff)
            for k in range(0, n * n, n)
        ))
        col_rects = VGroup(*(
            SurroundingRectangle(grids[1][k::n], buff=buff)
            for k in range(n)
        ))
        rects = VGroup(row_rects, col_rects)
        rects.set_fill(opacity=0.25)
        rects.set_stroke(width=2)
        row_rects.set_color(BLUE)
        col_rects.set_color(YELLOW)

        # plus_template = OldTex("+")
        # plus_template.match_height(grids[0][0])
        # for grid in grids:
        #     plusses = VGroup()
        #     for k, dot in enumerate(grid):
        #         if k % n != n - 1:
        #             pc = plus_template.copy()
        #             pc.move_to(midpoint(dot.get_center(), grid[k + 1].get_center()))
        #             plusses.add(pc)
        #     grid.add(plusses)

        arrow = Arrow(grids[0], grids[1], buff=0.5)

        self.add(grids[0])
        self.play(FadeIn(row_rects, lag_ratio=0.2))
        self.wait()
        self.play(
            TransformFromCopy(grids[0], grids[1]),
            ShowCreation(arrow)
        )
        self.play(FadeIn(col_rects, lag_ratio=0.2))
        self.wait()
