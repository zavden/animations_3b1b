# ==============================================================================
# Scene:      CrossEntropyKLDivergenceTitles
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 4-27)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CrossEntropyKLDivergenceTitles.py CrossEntropyKLDivergenceTitles -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CrossEntropyKLDivergenceTitles(InteractiveScene):
    def construct(self):
        # Test
        titles = VGroup(
            Text("Cross-Entropy", font_size=60),
            Text("KL Divergence", font_size=60),
        )
        titles.to_edge(UP)
        kw = dict(t2c={"p_i": GREEN, "q_i": PINK})
        formulas = VGroup(
            Tex(R"\sum_i p_i \big(-\log(q_i)\big)", **kw),
            Tex(R"\sum_i p_i \log\left({p_i / q_i}\right)", **kw),
        )

        for x, title, formula in zip([-1, 1], titles, formulas):
            title.set_x(x * FRAME_WIDTH / 4)
            formula.next_to(title, DOWN)

            self.play(LaggedStart(
                Write(title),
                FadeIn(formula, 0.5 * DOWN),
                lag_ratio=0.25
            ))
            self.wait()
