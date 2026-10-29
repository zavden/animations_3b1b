# ==============================================================================
# Scene:      PlaneCrashProbability
# Source:     videos/_2018/eop/bayes_footnote.py (lines 1173-1197)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PlaneCrashProbability.py PlaneCrashProbability -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PlaneCrashProbability(Scene):
    def construct(self):
        plane_prob = OldTex(
            "P(\\text{Dying in a }", "\\text{plane}", "\\text{ crash})", 
            "\\approx", "1/", "11{,}000{,}000"
        )
        plane_prob.set_color_by_tex("plane", BLUE)
        car_prob = OldTex(
            "P(\\text{Dying in a }", "\\text{car}", "\\text{ crash})", 
            "\\approx", "1/", "5{,}000"
        )
        car_prob.set_color_by_tex("car", YELLOW)
        plane_prob.shift(UP)
        car_prob.shift(
            plane_prob.get_part_by_tex("approx").get_center() -\
            car_prob.get_part_by_tex("approx").get_center() +\
            DOWN
        )

        self.play(Write(plane_prob))
        self.wait(2)
        self.play(ReplacementTransform(
            plane_prob.copy(), car_prob
        ))
        self.wait(2)
