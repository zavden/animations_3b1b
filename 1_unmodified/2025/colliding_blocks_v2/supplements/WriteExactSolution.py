# ==============================================================================
# Scene:      WriteExactSolution
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 985-1013)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteExactSolution.py WriteExactSolution -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteExactSolution(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Answer", font_size=72)
        title.to_edge(UP)
        underline = Underline(title, stretch_factor=1.5)
        VGroup(title, underline).set_color(YELLOW)
        self.play(
            FadeIn(title, lag_ratio=0.1),
            ShowCreation(underline)
        )

        # Answer
        kw = dict(
            t2c={
                R"\theta": YELLOW,
                R"m_1": BLUE,
                R"m_2": BLUE,
            }
        )
        solution = VGroup(
            Tex(R"\#\text{Collisions} = \lceil \pi / \theta - 1 \rceil", **kw),
            Tex(R"\text{Where } \; \theta = \text{arctan}\left(\sqrt{m_2 / m_1}\right)", **kw),
        )
        solution.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        solution.next_to(underline, DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)

        self.play(LaggedStartMap(FadeIn, solution, shift=0.5 * DOWN, lag_ratio=0.5))
        self.wait()
