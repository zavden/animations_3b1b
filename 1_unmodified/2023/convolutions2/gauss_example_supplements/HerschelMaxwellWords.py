# ==============================================================================
# Scene:      HerschelMaxwellWords
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 1115-1142)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HerschelMaxwellWords.py HerschelMaxwellWords -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HerschelMaxwellWords(InteractiveScene):
    def construct(self):
        # Test
        ideas = VGroup(
            VGroup(
                Text("Herschel-Maxwell derivation", font_size=60),
                TexText(
                    R"Rotational symmetry of $f({x})f({y}) \Rightarrow f({x}) = Ae^{-cx^2}$",
                    t2c={"{x}": BLUE, "{y}": YELLOW},
                    font_size=36,
                ),
            ).arrange(DOWN),
            TexText(
                R"Why $\pi$ is in this formula",
                font_size=60,
                t2c={R"\pi": YELLOW}
            )
        )
        for idea in ideas:
            idea.move_to(3.15 * UP)

        self.play(FadeIn(ideas[0], 0.5 * UP))
        self.wait()
        self.play(
            FadeIn(ideas[1], 0.5 * UP),
            FadeOut(ideas[0], 0.5 * UP),
        )
        self.wait()
