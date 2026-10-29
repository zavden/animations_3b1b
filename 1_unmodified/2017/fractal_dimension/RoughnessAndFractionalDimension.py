# ==============================================================================
# Scene:      RoughnessAndFractionalDimension
# Source:     videos/_2017/fractal_dimension.py (lines 2324-2365)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RoughnessAndFractionalDimension.py RoughnessAndFractionalDimension -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RoughnessAndFractionalDimension(Scene):
    def construct(self):
        title = OldTexText(
            "Non-integer dimension $\\Leftrightarrow$ Roughness"
        )
        title.to_edge(UP)
        self.add(title)

        randy = Randolph().scale(2)
        randy.to_corner(DOWN+RIGHT)
        self.add(randy)

        target = randy.copy()
        target.change_mode("hooray")
        ponder_target = randy.copy()
        ponder_target.change_mode("pondering")
        for mob in target, ponder_target:
            fractalify(mob, order = 2)

        dimension_label = OldTexText("Boundary dimension = ", "1")
        dimension_label.to_edge(LEFT)
        one = dimension_label[1]
        one.set_color(BLUE)
        new_dim = OldTex("1.2")
        new_dim.move_to(one, DOWN+LEFT)
        new_dim.set_color(one.get_color())
        self.add(dimension_label)

        self.play(Blink(randy))
        self.play(
            Transform(randy, target, run_time = 2),
            Transform(one, new_dim)
        )
        self.wait()
        self.play(Blink(randy))
        self.play(randy.look, DOWN+RIGHT)
        self.wait()
        self.play(randy.look, DOWN+LEFT)
        self.play(Blink(randy))
        self.wait()
        self.play(Transform(randy, ponder_target))
        self.wait()
