# ==============================================================================
# Scene:      FirstFewTermsOfCGF
# Source:     videos/_2023/clt_proof/main.py (lines 1029-1048)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FirstFewTermsOfCGF.py FirstFewTermsOfCGF -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FirstFewTermsOfCGF(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(t2c={
            "t": PINK,
            R"\frac{t^2}{2}": PINK,
            R"\frac{t^3}{3!}": PINK,
            R"\frac{t^4}{4!}": PINK,
        })
        rhs = Tex(R"""
            = \mathds{E}[X]t
            + \text{Var}(X)\frac{t^2}{2}
            + K_3[X]\frac{t^3}{3!}
            + K_4[X]\frac{t^4}{4!}
            + \cdots
            """,
            **kw
        )

        self.add(rhs)
