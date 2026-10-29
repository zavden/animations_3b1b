# ==============================================================================
# Scene:      VolumeRatio
# Source:     videos/_2026/spheres_talk/supplements.py (lines 657-676)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VolumeRatio.py VolumeRatio -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VolumeRatio(InteractiveScene):
    def construct(self):
        # 3D
        group = VGroup(
            Tex(R"{8  \cdot \big({4 \over 3} \pi \big) \over 2 \times 2 \times 2}"),
            Tex(R"="),
            Tex(R"{4 \over 3} \pi")
        )
        group.arrange(RIGHT, buff=0.25)
        self.add(group)

        # 100D
        self.clear()
        group = VGroup(
            Tex(R"{2^{100}  \cdot \big(\pi^{50} / 50! \big) \over 2^{100}}"),
            Tex(R"="),
            Tex(R"{\pi^{50} \over 50!}"),
        )
        group.arrange(RIGHT, buff=0.5)
        self.add(group)
