# ==============================================================================
# Scene:      WaysToMeasureProbabilityDistributionDifferences
# Source:     videos/_2026/cross_entropy/robot.py (lines 8720-8761)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WaysToMeasureProbabilityDistributionDifferences.py WaysToMeasureProbabilityDistributionDifferences -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FancyCircumscribe(VShowPassingFlash):
    def __init__(self, mobject, time_width=1.5, run_time=3, **kwargs):
        rect = SurroundingRectangle(mobject).set_stroke(YELLOW, 3)
        rect.add_line_to(rect.get_corner(UL))
        rect.insert_n_curves(100)
        super().__init__(rect, time_width=time_width, run_time=run_time, **kwargs)


class WaysToMeasureProbabilityDistributionDifferences(InteractiveScene):
    def construct(self):
        # Pi creature is confused thinking about many different possible formulas for measuring sorts of "distance" between distributions
        randy = Randolph(flip_at_start=True).to_edge(RIGHT, buff=1).look(LEFT)
        self.add(randy)
        self.wait(1)

        # Add the list of formulas
        formulas = BulletedList(
            R"L1: $\sum_i |p_i - q_i|$",
            R"L2: $\sum_i (p_i - q_i)^2$",
            R"Bhattacharyya: $-\ln \sum_i \sqrt{p_i q_i}$",
            R"Hellinger: $\frac{1}{2} \sum_i \left(\sqrt{p_i} - \sqrt{q_i}\right)^2$",
            R"Cross Entropy: $\sum_i p_i (-\log_2 q_i)$",
            R"KL Divergence: $\sum_i p_i \left(\log_2\frac{p_i}{q_i}\right)$",
            font_size=45,
            tex_to_color_map={"p_i": GREEN, "q_i": PINK}
        ).to_edge(LEFT, buff=1)
        self.play(
            AnimationGroup(
                AnimationGroup(*[FadeIn(formula, shift=DOWN * 0.4) for formula in formulas], lag_ratio=0.2, run_time=2.5),
                randy.change("confused"), lag_ratio=0.2)
        )
        self.wait(1)
        self.play(Blink(randy))
        self.wait(1)

        self.play(randy.change("pondering", formulas[-2:]), FancyCircumscribe(formulas[-2:], run_time=5))

        # Focus on Cross Entropy and KL Divergence
        self.play(
            AnimationGroup(
                AnimationGroup(*[
                    FadeOut(formula, shift=UP)
                    for formula in formulas[:-2]
                ], lag_ratio=0.1),
                AnimationGroup(
                    formulas[-2:].animate.scale(1.1).set_y(0).to_edge(LEFT, buff=1),
                    randy.change("thinking", LEFT)
                ), lag_ratio=0.32), run_time=2)
        self.play(Blink(randy))
        self.wait(2)
