# ==============================================================================
# Scene:      EnergyAndMomentumLaws
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 319-339)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EnergyAndMomentumLaws.py EnergyAndMomentumLaws -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EnergyAndMomentumLaws(InteractiveScene):
    def construct(self):
        # Test
        laws = VGroup(
            Text("Conservation of Energy"),
            Text("Conservation of Momentum"),
        )
        laws.arrange(DOWN, buff=0.75)
        laws.move_to(3 * UP, UP)

        self.play(FadeIn(laws[0], UP))
        self.wait()
        self.play(
            TransformMatchingStrings(
                *laws,
                key_map={"Energy": "Momentum"},
                mismatch_animation=FadeTransform,
                run_time=1
            )
        )
        self.wait()
