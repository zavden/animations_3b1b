# ==============================================================================
# Scene:      OtherExponentialDerivatives
# Source:     videos/_2025/laplace/prequel_equations.py (lines 230-246)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OtherExponentialDerivatives.py OtherExponentialDerivatives -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OtherExponentialDerivatives(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(t2c={"t": GREY_B})
        derivs = VGroup(
            Tex(R"\frac{d}{dt} 2^t = (0.693...)2^t", **kw),
            Tex(R"\frac{d}{dt} 3^t = (1.098...)3^t", **kw),
            Tex(R"\frac{d}{dt} 4^t = (1.386...)4^t", **kw),
            Tex(R"\frac{d}{dt} 5^t = (1.609...)5^t", **kw),
            Tex(R"\frac{d}{dt} 6^t = (1.791...)6^t", **kw),
        )
        derivs.scale(0.75)
        derivs.arrange(DOWN, buff=0.7)
        derivs.to_corner(UL)

        self.play(LaggedStartMap(FadeIn, derivs, shift=UP, lag_ratio=0.5, run_time=5))
        self.wait()
