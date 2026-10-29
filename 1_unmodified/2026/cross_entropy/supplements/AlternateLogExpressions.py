# ==============================================================================
# Scene:      AlternateLogExpressions
# Source:     videos/_2026/cross_entropy/supplements.py (lines 866-888)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AlternateLogExpressions.py AlternateLogExpressions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AlternateLogExpressions(InteractiveScene):
    def construct(self):
        kw = dict(
            t2c={
                R"-\log_2": BLUE,
                R"\log_2": BLUE,
                R"\log_{1/2}": BLUE,
                "p": TEAL
            }
        )
        terms = VGroup(
            Tex(R"-\log_2(p)", **kw),
            Tex(R"= \log_2(1 / p)", **kw),
            Tex(R"= \log_{1/2}(p)", **kw),
        )
        terms.arrange(RIGHT)

        # Test
        self.add(terms[0])
        self.wait()
        for idx in [0, 1]:
            self.play(TransformMatchingStrings(terms[idx].copy(), terms[idx + 1], run_time=1, path_arc=30 * DEG))
            self.wait()
