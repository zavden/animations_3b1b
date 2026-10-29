# ==============================================================================
# Scene:      SampleRateOverlay
# Source:     videos/_2022/piano/fourier_animations.py (lines 778-799)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SampleRateOverlay.py SampleRateOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SampleRateOverlay(Scene):
    def construct(self):
        text = VGroup(
            OldTexText("48,000 samples / sec"),
            OldTex("\\Downarrow"),
            OldTexText("20 ms window", " = 960-dimensional vector")
        )
        text.arrange(DOWN)
        text.to_edge(UP)

        text[2][1].set_color(YELLOW)
        text[2][0].save_state()
        text[2][0].match_x(text)
        self.play(Write(text[0]), run_time=1)
        self.wait()
        self.play(
            GrowFromPoint(text[1], text[0].get_bottom()),
            FadeIn(text[2][0], DOWN)
        )
        self.wait()
        self.play(Restore(text[2][0]), FadeIn(text[2][1]))
        self.wait()
