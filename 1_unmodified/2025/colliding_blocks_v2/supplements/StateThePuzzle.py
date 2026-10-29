# ==============================================================================
# Scene:      StateThePuzzle
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 307-316)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StateThePuzzle.py StateThePuzzle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StateThePuzzle(InteractiveScene):
    def construct(self):
        # Test
        question = TexText(
            R"Given $m_1$ and $m_2$, how \\ many collisions take place?",
            t2c={R"$m_1$": BLUE, R"$m_2$": BLUE}
        )
        question.to_edge(UP)
        self.play(Write(question))
        self.wait()
