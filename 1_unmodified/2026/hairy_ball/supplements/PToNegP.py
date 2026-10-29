# ==============================================================================
# Scene:      PToNegP
# Source:     videos/_2026/hairy_ball/supplements.py (lines 532-549)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PToNegP.py PToNegP -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PToNegP(InteractiveScene):
    def construct(self):
        # Test
        p, to, neg_p = expression = VGroup(
            Tex(R"p"), Tex(R"\longrightarrow"), Tex(R"-p")
        )
        expression.arrange(RIGHT, buff=0.75)
        expression.scale(2.5)
        expression.to_edge(UP)

        to.save_state()
        to.stretch(0, 0, about_edge=LEFT)
        to.stretch(0.5, 1)

        self.play(Write(p))
        self.play(Restore(to))
        self.play(FadeTransformPieces(p.copy(), neg_p))
        self.wait()
