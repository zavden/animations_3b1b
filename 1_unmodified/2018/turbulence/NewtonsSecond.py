# ==============================================================================
# Scene:      NewtonsSecond
# Source:     videos/_2018/turbulence.py (lines 1173-1207)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NewtonsSecond.py NewtonsSecond -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NewtonsSecond(Scene):
    def construct(self):
        square = Square(
            stroke_color=WHITE,
            fill_color=GREY_B,
            fill_opacity=0.5,
            side_length=1
        )
        label = OldTex("m")
        label.scale(1.5)
        label.move_to(square)
        square.add(label)
        square.save_state()
        arrows = VGroup(
            Vector(0.5 * UP).next_to(square, UP, buff=0),
            Vector(RIGHT).next_to(square, RIGHT, buff=0),
        )

        self.play(
            square.shift, 4 * RIGHT + 2 * UP,
            rate_func=lambda t: t**2,
            run_time=2
        )
        self.wait()
        square.restore()
        self.play(
            LaggedStartMap(GrowArrow, arrows)
        )
        square.add(arrows)
        self.play(
            square.shift, 4 * RIGHT + 2 * UP,
            rate_func=lambda t: t**2,
            run_time=2
        )
        self.wait()
