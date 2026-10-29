# ==============================================================================
# Scene:      BigVolumeRatio
# Source:     videos/_2026/spheres_talk/supplements.py (lines 458-493)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BigVolumeRatio.py BigVolumeRatio -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BigVolumeRatio(InteractiveScene):
    def construct(self):
        # Test
        fraction = Tex(R"\text{Vol}\Big(\text{100D Unit Ball}\Big) \over 2^{100}")
        fraction["2^{100}"].scale(1.5, about_edge=UP).shift(SMALL_BUFF * DOWN)

        numerator = fraction[R"\text{Vol}\Big(\text{100D Unit Ball}\Big)"]
        numerator_rect = SurroundingRectangle(numerator, buff=0)
        numerator_rect.set_stroke(BLUE, 3)
        randy = Randolph(height=2)
        randy.next_to(fraction, LEFT, MED_LARGE_BUFF)
        randy.shift(0.5 * DOWN)

        self.wait(0.1)
        self.play(FadeIn(fraction))
        self.wait(3)
        self.play(
            VFadeIn(randy),
            randy.change("confused"),
            ShowCreation(numerator_rect)
        )
        self.play(Blink(randy))
        self.wait()

        # Reveal answer
        new_numerator = Tex(R"\pi^{50} / 50!", font_size=72)
        new_numerator.move_to(numerator, DOWN)

        self.play(
            FadeOut(numerator_rect),
            fraction[R"\over"].animate.match_width(new_numerator, stretch=True),
            FadeTransform(numerator, new_numerator),
            randy.change("tease"),
        )
        self.play(Blink(randy))
        self.wait()
