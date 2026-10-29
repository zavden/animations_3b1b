# ==============================================================================
# Scene:      EntropyRate
# Source:     videos/_2026/cross_entropy/supplements.py (lines 1033-1054)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EntropyRate.py EntropyRate -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class EntropyRate(InteractiveScene):
    def construct(self):
        # Test
        name = Text("Entropy Rate: ")
        form = Tex(R"\lim _{n \rightarrow \infty} \frac{1}{n} H\left(X_1, X_2, \ldots X_n\right)", t2c={"H": BLUE})
        group = VGroup(name, form)
        group.arrange(RIGHT)
        group.to_edge(UP)

        pre_form = Tex(R"H(X)", t2c={"H": BLUE})
        pre_form.move_to(form, LEFT)
        pre_name = Text("Entropy:")
        pre_name.move_to(name, RIGHT)

        self.add(pre_name, pre_form)
        self.wait()
        self.play(
            TransformMatchingStrings(pre_name, name),
            TransformMatchingTex(pre_form, form),
            run_time=1
        )
        self.wait()
