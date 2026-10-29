# ==============================================================================
# Scene:      ManyCousinsOfFourierThings
# Source:     videos/_2019/diffyq/part3/staging.py (lines 203-230)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyCousinsOfFourierThings.py ManyCousinsOfFourierThings -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ManyCousinsOfFourierThings(Scene):
    def construct(self):
        series_variants = VGroup(
            OldTexText("Complex", "Fourier Series"),
            OldTexText("Discrete", "Fourier Series"),
        )
        transform_variants = VGroup(
            OldTexText("Discrete", "Fourier Transform"),
            OldTexText("Fast", "Fourier Transform"),
            OldTexText("Quantum", "Fourier Transform"),
        )
        groups = VGroup(series_variants, transform_variants)
        for group, vect in zip(groups, [LEFT, RIGHT]):
            group.scale(0.7)
            group.arrange(DOWN, aligned_edge=LEFT)
            group.move_to(
                vect * FRAME_WIDTH / 4
            )
            group.set_color(YELLOW)

        self.play(*[
            LaggedStartMap(FadeIn, group)
            for group in groups
        ])
        self.play(*[
            LaggedStartMap(FadeOut, group)
            for group in groups
        ])
