# ==============================================================================
# Scene:      IntroText
# Source:     videos/_2026/spheres_talk/supplements.py (lines 107-122)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroText.py IntroText -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroText(InteractiveScene):
    def construct(self):
        # Test
        group = VGroup(
            Text("Exploring high-dimensional spheres", font_size=90),
            Text("Delivered at UC Santa Cruz on February 17, 2026"),
        )
        group[1].set_color(GREY_A)
        group.arrange(DOWN, buff=0.5)
        group.set_width(FRAME_WIDTH - 3)
        self.play(LaggedStart(
            Write(group[0], lag_ratio=0.1),
            FadeIn(group[1], 0.25 * DOWN),
            lag_ratio=0.6
        ))
        self.wait()
