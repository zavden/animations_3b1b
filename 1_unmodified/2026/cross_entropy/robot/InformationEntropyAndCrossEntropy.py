# ==============================================================================
# Scene:      InformationEntropyAndCrossEntropy
# Source:     videos/_2026/cross_entropy/robot.py (lines 7419-7450)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InformationEntropyAndCrossEntropy.py InformationEntropyAndCrossEntropy -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class InformationEntropyAndCrossEntropy(InteractiveScene):
    def construct(self):
        # Write the definitions of information, entropy, cross entropy, and KL divergence
        definitions = VGroup(
            Tex(
                R"\text{Information}(\text{event}) = -\log_2(p_\text{event})",
                font_size=60, tex_to_color_map={"event": YELLOW, R"p_\text{event}": YELLOW}
            ),
            Tex(
                R"\text{Entropy}(P) = \displaystyle\sum_i p_i \cdot -\log_2 p_i",
                font_size=60, tex_to_color_map={"P": GREEN, "p_i": GREEN}
            ),
            Tex(
                R"\text{Cross Entropy}(Q, P) = \displaystyle\sum_i p_i \cdot -\log_2 q_i",
                font_size=60, tex_to_color_map={"P": GREEN, "Q": PINK, "p_i": GREEN, "q_i": PINK}
            )
        ).arrange_in_grid(n_cols=1, buff=0.7)
        for definition in definitions:
            definition.shift(LEFT * (definition["="].get_x() - definitions[0]["="].get_x()))
        definitions.center()
        part1 = definitions[:2]
        part1.save_state()
        part1[1].shift(DOWN * 0.5)
        part1.set_y(0)
        self.play(FadeIn(definitions[0]))
        self.wait(1)
        self.play(FadeIn(definitions[1]))
        self.wait(2)

        self.play(
            part1.animate.restore(),
            FadeIn(definitions[2], shift=UP * 0.6), run_time=2)
