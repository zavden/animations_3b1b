# ==============================================================================
# Scene:      ThreeMainObservations
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 5-66)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThreeMainObservations.py ThreeMainObservations -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

class ThreeMainObservations(Scene):
    def construct(self):
        fourier = ImageMobject("Joseph Fourier")
        name = OldTexText("Joseph Fourier")
        name.match_width(fourier)
        name.next_to(fourier, DOWN, SMALL_BUFF)
        fourier.add(name)
        fourier.set_height(5)
        fourier.to_corner(DR)
        fourier.shift(LEFT)
        bubble = ThoughtBubble(
            direction=RIGHT,
            height=3,
            width=4,
        )
        bubble.move_tip_to(fourier.get_corner(UL) + 0.5 * DR)

        observations = VGroup(
            OldTexText(
                "1)",
                "Sine = Nice",
            ),
            OldTexText(
                "2)",
                "Linearity"
            ),
            OldTexText(
                "3)",
                "Fourier series"
            ),
        )
        # heart = SuitSymbol("hearts")
        # heart.replace(observations[0][2])
        # observations[0][2].become(heart)
        # observations[0][1].add(happiness)
        # observations[2][2].align_to(
        #     observations[2][1], LEFT,
        # )

        observations.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=2 * LARGE_BUFF,
        )
        observations.set_height(FRAME_HEIGHT - 2)
        observations.to_corner(UL, buff=LARGE_BUFF)

        self.add(fourier)
        self.play(ShowCreation(bubble))
        self.wait()
        self.play(LaggedStart(*[
            TransformFromCopy(bubble, observation[0])
            for observation in observations
        ], lag_ratio=0.2))
        self.play(
            FadeOut(fourier),
            FadeOut(bubble),
        )
        self.wait()
        for obs in observations:
            self.play(FadeIn(obs[1], LEFT))
            self.wait()
