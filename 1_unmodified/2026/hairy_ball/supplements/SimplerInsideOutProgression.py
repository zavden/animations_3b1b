# ==============================================================================
# Scene:      SimplerInsideOutProgression
# Source:     videos/_2026/hairy_ball/supplements.py (lines 552-573)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimplerInsideOutProgression.py SimplerInsideOutProgression -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimplerInsideOutProgression(InteractiveScene):
    def construct(self):
        # Test
        parts = VGroup(
            Tex(R"(x, y, z)"),
            Vector(0.75 * DOWN),
            Tex(R"(-x, -y, z)"),
            Vector(0.75 * DOWN),
            Tex(R"(-x, -y, -z)"),
        )
        parts.arrange(DOWN, buff=MED_SMALL_BUFF)
        self.add(parts[0])
        self.wait()

        for i in [0, 2]:
            src, arrow, trg = parts[i:i + 3]
            self.play(
                TransformMatchingStrings(src.copy(), trg),
                GrowArrow(arrow),
                run_time=1
            )
            self.wait()
