# ==============================================================================
# Scene:      ReferenceFilter
# Source:     videos/_2022/puzzles/subsets.py (lines 4174-4214)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceFilter.py ReferenceFilter -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceFilter(InteractiveScene):
    def construct(self):
        # Grid
        c_grid = Tex("c_{10}").get_grid(10, 10, buff=MED_LARGE_BUFF)
        c_grid.set_height(FRAME_HEIGHT - 1)

        for n, c_mob in zip(it.count(1), c_grid):
            sub = Integer(n)
            sub.match_height(c_mob[1:])
            sub.move_to(c_mob[1:], UL)
            c_mob.remove(*c_mob[1:])
            c_mob.add(sub)

        self.play(FadeIn(c_grid, run_time=2, lag_ratio=0.025))
        c_grid.generate_target()
        c_grid.target.set_opacity(0.25)
        c_grid.target[4::5].set_fill(TEAL, 1)
        self.play(MoveToTarget(c_grid, run_time=2, lag_ratio=0.025))
        self.wait()

        # Name frequency
        c_grid.generate_target()
        c_grid.target.set_height(4.0)
        c_grid.target.set_y(0).to_edge(LEFT)
        freq_label = Text("Frequency question")
        freq_label.next_to(c_grid.target, UP, MED_LARGE_BUFF)

        self.play(
            MoveToTarget(c_grid),
            Write(freq_label),
        )
        self.wait()

        # Roots of unity (to be overlaid)
        uc_label = OldTexText("Values of the form $e^{it}$")
        uc_label.match_y(freq_label, UP)
        uc_label.set_x(-freq_label.get_x())

        arrow = Vector(2.0 * RIGHT).next_to(c_grid, RIGHT)
        self.play(ShowCreation(arrow), Write(uc_label))
        self.wait()
