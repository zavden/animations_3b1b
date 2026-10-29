# ==============================================================================
# Scene:      ShowKeyFormulas
# Source:     videos/_2026/cross_entropy/supplements.py (lines 974-1030)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowKeyFormulas.py ShowKeyFormulas -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ShowKeyFormulas(InteractiveScene):
    def construct(self):
        # Add formulas
        kw = dict(
            font_size=36,
            t2c={"p": TEAL, "q": BLUE, "p_i": TEAL, "q_i": BLUE}
        )
        formulas = VGroup(
            Tex(R"I = -\log_2(p)", **kw),
            Tex(R"H(p) = \sum_i p_i\big(-\log_2(p_i)\big)", **kw),
            Tex(R"H(p, q) = \sum_i p_i\big(-\log_2(q_i)\big)", **kw),
            Tex(R"D_{\text{KL}}(p || q) = \sum_i p_i\big(\log_2(p_i / q_i)\big)", **kw),
        )
        formulas.arrange(DOWN, buff=LARGE_BUFF)
        formulas.to_edge(RIGHT)

        self.play(LaggedStartMap(Write, formulas, lag_ratio=0.25, run_time=3))
        self.wait()

        # Move to corners
        rects = FullScreenFadeRectangle().get_grid(2, 2, buff=0)
        rects.set_height(FRAME_HEIGHT).move_to(ORIGIN)
        div_lines = VGroup(Line(UP, DOWN), Line(LEFT, RIGHT))
        div_lines.replace(rects, stretch=True)
        div_lines.set_stroke(WHITE, 2)

        for formula, rect in zip(formulas, rects):
            formula.target = formula.generate_target()
            formula.target.next_to(rect.get_top(), DOWN)

        self.play(MoveToTarget(formulas[0]))
        self.reveal_name(formulas[0], "Information")
        self.wait()
        self.play(
            LaggedStartMap(MoveToTarget, formulas[1:], lag_ratio=0.25, run_time=3),
            Write(div_lines),
        )
        self.wait()
        names = ["Entropy", "Cross-entropy", "KL Divergence"]
        for formula, name in zip(formulas[1:], names):
            self.reveal_name(formula, name)
        self.wait()

    def reveal_name(self, formula, name):
        lhs_str, rhs_str = formula.get_string().split("=")
        lhs = formula[lhs_str][0]
        rhs = formula["=" + rhs_str][0]
        rhs.target = rhs.generate_target()

        name_mob = Text(name, font_size=formula.font_size)
        name_mob.move_to(lhs, RIGHT)

        VGroup(name_mob, rhs.target).move_to(formula)
        self.play(
            FadeTransformPieces(lhs, name_mob),
            MoveToTarget(rhs)
        )
