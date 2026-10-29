# ==============================================================================
# Scene:      FifthRootsOfOneOverlay
# Source:     videos/_2022/puzzles/subsets.py (lines 4864-4875)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FifthRootsOfOneOverlay.py FifthRootsOfOneOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FifthRootsOfOneOverlay(InteractiveScene):
    def construct(self):
        lines = [
            "z^5 &= 1 ",
            "z &= \\sqrt[5]{1}",
        ]
        tex = OldTex("\\\\ ".join(lines), isolate=lines)

        self.add(tex[0])
        self.wait()
        self.play(TransformMatchingShapes(tex[0].copy(), tex[1]))
        self.wait()
