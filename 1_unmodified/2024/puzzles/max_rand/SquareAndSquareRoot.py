# ==============================================================================
# Scene:      SquareAndSquareRoot
# Source:     videos/_2024/puzzles/max_rand.py (lines 204-219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SquareAndSquareRoot.py SquareAndSquareRoot -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SquareAndSquareRoot(InteractiveScene):
    def construct(self):
        # Test
        lines = VGroup(
            Tex(R"\left(\frac{1}{2}\right)^2 = \frac{1}{4}"),
            Tex(R"\sqrt{\frac{1}{4}} = \frac{1}{2}"),
        )
        lines.scale(1.5)

        self.play(FadeIn(lines[0]))
        self.wait()
        self.play(TransformMatchingStrings(
            *lines,
            matched_pairs=[(lines[0]["2"][1], lines[1][R"\sqrt"][0])],
            path_arc=PI / 2,
        ))
