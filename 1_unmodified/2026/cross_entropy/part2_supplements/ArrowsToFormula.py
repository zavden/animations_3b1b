# ==============================================================================
# Scene:      ArrowsToFormula
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 537-565)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrowsToFormula.py ArrowsToFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ArrowsToFormula(InteractiveScene):
    def construct(self):
        # Test
        formula = Tex(R"\sum_i p_i (-\log q_i)", t2c={"p_i": GREEN, "q_i": PINK})
        formula.scale(1.5).to_edge(RIGHT, LARGE_BUFF)

        screens = ScreenRectangle().get_grid(2, 1, buff=0.5)
        screens.set_height(FRAME_HEIGHT - 1).to_edge(LEFT)
        screens.stretch(0.9, 0, about_edge=LEFT)

        path_arc = 90 * DEG
        arrows = VGroup(
            Arrow(screens[0].get_right() + UP, formula.get_top() + LEFT, path_arc=-path_arc, thickness=5),
            Arrow(screens[1].get_right() + DOWN, formula.get_bottom() + LEFT, path_arc=path_arc, thickness=5),
        )
        arrows.set_fill(WHITE)

        # Animate
        formula.save_state()
        for part in formula:
            part.set_opacity(0).move_to(arrows[1].get_start())
        self.play(
            Write(arrows[1]),
            Restore(formula, lag_ratio=0.01),
            run_time=2
        )
        self.wait()
        self.play(Write(arrows[0]))
        self.wait()
