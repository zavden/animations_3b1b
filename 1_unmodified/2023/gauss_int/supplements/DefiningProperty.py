# ==============================================================================
# Scene:      DefiningProperty
# Source:     videos/_2023/gauss_int/supplements.py (lines 946-992)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefiningProperty.py DefiningProperty -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DefiningProperty(InteractiveScene):
    def construct(self):
        # Setup
        prop = VGroup(
            Text("1. Radial symmetry", font_size=36),
            Text("2. Independence of\neach coordinate", font_size=36),
        )
        prop.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        implies = Tex(R"\Downarrow", font_size=72)
        form = Tex(R"e^{-c r^2}", t2c={"c": RED}, font_size=72)

        derivation = VGroup(prop, implies, form)
        derivation.arrange(DOWN, buff=MED_LARGE_BUFF)
        form.shift(0.25 * UP)
        derivation.to_edge(LEFT, buff=1.0).shift(0.5 * DOWN)
        derivation_box = SurroundingRectangle(derivation, buff=0.5)
        derivation_box.set_stroke(YELLOW, 2)
        derivation_box.set_fill(YELLOW, 0.05)

        title = Text("Herschel-Maxwell\nDerivation")
        title.next_to(derivation_box, UP, MED_LARGE_BUFF)

        self.add(derivation_box)
        self.add(derivation)
        self.add(title)
        self.wait()

        # If we view this
        words = Text(
            "Suppose we take this\nto define a Gaussian...",
            t2s={"define": ITALIC},
            t2c={"define": TEAL},
            alignment="LEFT"
        )
        words.match_width(derivation_box)
        words.next_to(derivation_box, UP)

        self.play(LaggedStart(
            FadeIn(words, 0.5 * UP),
            FadeOut(title, UP),
            lag_ratio=0.2,
        ))
        self.wait()
        self.play(
            FlashAround(prop[0], color=TEAL, time_width=1, run_time=2)
        )
        self.wait()
