# ==============================================================================
# Scene:      LorenzTransform
# Source:     videos/_2019/windmill.py (lines 3590-3626)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LorenzTransform.py LorenzTransform -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LorenzTransform(Scene):
    def construct(self):
        grid = NumberPlane(
            # faded_line_ratio=0,
            # y_axis_config={
            #     "y_min": -10,
            #     "y_max": 10,
            # }
        )
        grid.scale(2)
        back_grid = grid.copy()
        back_grid.set_stroke(GREY, 0.5)
        # back_grid.set_opacity(0.5)

        c_lines = VGroup(Line(DL, UR), Line(DR, UL))
        c_lines.scale(FRAME_HEIGHT)
        c_lines.set_stroke(YELLOW, 3)

        equation = OldTex(
            "d\\tau^2 = dt^2 - dx^2"
        )
        equation.scale(1.7)
        equation.to_corner(UL, buff=MED_SMALL_BUFF)
        equation.shift(2.75 * DOWN)
        equation.set_stroke(BLACK, 5, background=True)

        self.add(back_grid, grid, c_lines)
        self.add(equation)
        beta = 0.4
        self.play(
            grid.apply_matrix, np.array([
                [1, beta],
                [beta, 1],
            ]) / (1 - beta**2),
            run_time=2
        )
        self.wait()
