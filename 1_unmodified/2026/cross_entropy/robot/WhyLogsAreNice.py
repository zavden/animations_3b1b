# ==============================================================================
# Scene:      WhyLogsAreNice
# Source:     videos/_2026/cross_entropy/robot.py (lines 7747-7778)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyLogsAreNice.py WhyLogsAreNice -w -m --fps 15
# ==============================================================================

from __future__ import annotations
import math
from manim_imports_ext import *

class WhyLogsAreNice(InteractiveScene):
    def construct(self):
        # Write some rules of logs
        equation = Tex(
            R"-\log_2(p_1 \cdot p_2) = -(\log_2 p_1 + \log_2 p_2)",
            font_size=62,
            tex_to_color_map={"p_1": BLUE, "p_2": GREEN}
        )
        self.play(Write(equation), run_time=5)
        self.wait(3)
        self.play(FadeOut(equation))

        p = 0.000000001
        log_p = round(-math.log2(p), 2)
        small_prob = Tex(
            F"p = {p:.9f}", tex_to_color_map={"p": BLUE}, font_size=70
        )
        small_prob_log = Tex(
            R"-\log_2 p \approx " + str(log_p), tex_to_color_map={"p": BLUE}, font_size=70
        ).match_height(small_prob).move_to(small_prob).shift(DOWN)
        self.play(FadeIn(small_prob))
        self.wait(2)
        small_prob.generate_target()
        small_prob.target.shift(UP * 0.5)
        arrow = CurvedArrow(small_prob.target.get_left() + LEFT * 0.3 + DOWN * 0.2, small_prob_log.get_left() + LEFT * 0.3).set_color(YELLOW)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    MoveToTarget(small_prob),
                    FadeIn(small_prob_log, shift=UP), run_time=2),
                FadeIn(arrow, run_time=1.5), lag_ratio=0.7)
        )
