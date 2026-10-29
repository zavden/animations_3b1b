# ==============================================================================
# Scene:      SimpleSolutionSummary
# Source:     videos/_2025/laplace/shm.py (lines 1106-1129)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleSolutionSummary.py SimpleSolutionSummary -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleSolutionSummary(InteractiveScene):
    def construct(self):
        # Summary of the "strategy" up top
        t2c = {"m": RED, "k": TEAL, "{s}": YELLOW, R"\omega": PINK}
        kw = dict(t2c=t2c, font_size=36)
        arrow = Vector(1.5 * RIGHT)
        top_eq = VGroup(
            Tex(R"m x''(t) + k x(t) = 0", **kw),
            arrow,
            Tex(R"e^{{s}t}\left(m{s}^2 + k\right) = 0", **kw),
            Tex(R"\Longrightarrow", **kw),
            Tex(R"{s} = \pm i \underbrace{\sqrt{k / m}}_{\omega}", **kw),
        )
        top_eq.arrange(RIGHT)
        top_eq[-1].align_to(top_eq[2], UP)
        guess = Tex(R"\text{Guess } e^{{s}t}", **kw)
        guess.scale(0.75)
        guess.next_to(arrow, UP, buff=0)
        arrow.add(guess)

        top_eq.set_width(FRAME_WIDTH - 1)

        top_eq.center().to_edge(UP)
        self.add(top_eq)
