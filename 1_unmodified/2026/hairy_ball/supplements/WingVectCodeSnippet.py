# ==============================================================================
# Scene:      WingVectCodeSnippet
# Source:     videos/_2026/hairy_ball/supplements.py (lines 99-111)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WingVectCodeSnippet.py WingVectCodeSnippet -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WingVectCodeSnippet(InteractiveScene):
    def construct(self):
        # Test
        code = Code("""
            def wing_vect(heading_vect):
                \"\"\"
                Return 3d vector perpendicular
                to heading_vect
                \"\"\"
                ...
        """, alignment="LEFT")
        self.play(ShowIncreasingSubsets(code, run_time=2, rate_func=linear))
        self.wait()
