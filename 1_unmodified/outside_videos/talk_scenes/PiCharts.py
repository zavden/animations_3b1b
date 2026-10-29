# ==============================================================================
# Scene:      PiCharts
# Source:     videos/outside_videos/talk_scenes.py (lines 47-99)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiCharts.py PiCharts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiCharts(Scene):
    def construct(self):
        # Add top lines
        equation = OldTex(
            "\\frac{1}{10}", "+", "\\frac{2}{5}", "=", "\\; ?"
        )
        equation.scale(2)
        equation.to_edge(UP)
        vs = OldTexText("vs.")
        vs.scale(3)
        vs.next_to(equation, DOWN, LARGE_BUFF)
        self.add(equation, vs)

        # Add pi charts
        pi_equation = VGroup(
            self.get_pi_chart(10),
            OldTex("+").scale(2),
            self.get_pi_chart(5),
            OldTex("=").scale(2),
            OldTex("?").scale(2),
        )
        pi_equation[0][0].set_fill(RED)
        pi_equation[2][:2].set_fill(RED)
        pi_equation.arrange(RIGHT)
        pi_equation.next_to(vs, DOWN)
        self.add(pi_equation)

        vs.shift(UL * MED_SMALL_BUFF)

        # Swap
        pi_equation.to_edge(UP)
        arrow = OldTex("\\downarrow").scale(3)
        arrow.next_to(pi_equation[1], DOWN, LARGE_BUFF)
        equation.next_to(arrow, DOWN)
        equation.shift(0.7 * RIGHT)

        self.remove(vs)
        self.add(arrow)

    def get_pi_chart(self, n):
        result = VGroup(*[
            Sector(
                start_angle=TAU / 4 - k * TAU / n,
                angle=-TAU / n,
                stroke_color=WHITE,
                stroke_width=2,
                fill_color=BLUE_E,
                fill_opacity=1,
            )
            for k in range(n)
        ])
        result.scale(1.5)
        return result
