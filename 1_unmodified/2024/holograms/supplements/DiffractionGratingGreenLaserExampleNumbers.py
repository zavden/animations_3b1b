# ==============================================================================
# Scene:      DiffractionGratingGreenLaserExampleNumbers
# Source:     videos/_2024/holograms/supplements.py (lines 806-823)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiffractionGratingGreenLaserExampleNumbers.py DiffractionGratingGreenLaserExampleNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DiffractionGratingGreenLaserExampleNumbers(InteractiveScene):
    def construct(self):
        # Test
        lines = VGroup(
            VGroup(
                Text("Grating: 500 lines / mm"),
                Tex(R"\Rightarrow d = 2 \times 10^{-6} \text{m}"),
            ).arrange(RIGHT),
            VGroup(
                Text("Green light wavelength: 500 nm "),
                Tex(R"\Rightarrow \lambda = 5 \times 10^{-7} \text{m}"),
            ).arrange(RIGHT),
            Tex(R"\theta = \sin^{-1}(\lambda / d) = \sin^{-1}\left(5 \times 10^{-7} / 2 \times 10^{-6} \right) \approx 14.5^\circ")
        )
        lines.arrange(DOWN, aligned_edge=LEFT, buff=LARGE_BUFF)
        lines.to_edge(LEFT)
        lines[0][1].align_to(lines[1][1], LEFT)
        self.add(lines)
