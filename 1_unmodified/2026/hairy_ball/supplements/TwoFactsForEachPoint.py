# ==============================================================================
# Scene:      TwoFactsForEachPoint
# Source:     videos/_2026/hairy_ball/supplements.py (lines 353-370)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoFactsForEachPoint.py TwoFactsForEachPoint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoFactsForEachPoint(InteractiveScene):
    def construct(self):
        # Test
        features = VGroup(
            Tex(R"\text{1)  } p \rightarrow -p", font_size=72),
            Tex(R"\text{2)  } &\text{Motion varies }\\ &\text{continuously with } p", font_size=72),
        )
        features[1][2:].scale(0.8, about_edge=UL)
        features.arrange(DOWN, aligned_edge=LEFT, buff=1.5)
        features.to_edge(LEFT)

        for feature in features:
            self.add(feature[:2])
        self.wait()
        for feature in features:
            self.play(FadeIn(feature[2:], lag_ratio=0.1))
            self.wait()
        self.wait()
