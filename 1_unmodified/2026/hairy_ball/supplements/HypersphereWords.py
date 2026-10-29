# ==============================================================================
# Scene:      HypersphereWords
# Source:     videos/_2026/hairy_ball/supplements.py (lines 946-960)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HypersphereWords.py HypersphereWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HypersphereWords(InteractiveScene):
    def construct(self):
        # Test
        words = VGroup(
            Text("Hairs on a neatly-combed 4d hypersphere", font_size=60),
            Text("Represented via streographic projection into 3d space", font_size=48).set_color(GREY_A)
        )
        words.set_backstroke(BLACK, 10)
        words.arrange(DOWN)
        words.to_corner(UL)

        self.add(words[0])
        self.wait()
        self.play(FadeIn(words[1], lag_ratio=0.1, run_time=2))
        self.wait()
