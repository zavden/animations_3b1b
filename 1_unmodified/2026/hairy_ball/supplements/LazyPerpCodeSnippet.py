# ==============================================================================
# Scene:      LazyPerpCodeSnippet
# Source:     videos/_2026/hairy_ball/supplements.py (lines 114-127)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LazyPerpCodeSnippet.py LazyPerpCodeSnippet -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LazyPerpCodeSnippet(InteractiveScene):
    def construct(self):
        # Test
        code = Code("""
            def lazy_perp(heading):
                # Returns the normalized cross product
                # between (0, 0, 1) and heading
                # Note the division by 0 for x=y=0
                x, y, z = heading
                return np.array([-y, x, 0]) / np.sqrt(x * x + y * y)
        """, alignment="LEFT")
        code.to_corner(UL)
        self.play(Write(code))
        self.wait()
