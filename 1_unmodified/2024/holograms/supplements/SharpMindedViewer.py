# ==============================================================================
# Scene:      SharpMindedViewer
# Source:     videos/_2024/holograms/supplements.py (lines 1181-1195)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SharpMindedViewer.py SharpMindedViewer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SharpMindedViewer(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle())
        randy = Randolph()
        randy.to_edge(LEFT)
        randy.shift(DOWN)

        self.play(randy.change("sassy", RIGHT))
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change("confused", RIGHT))
        self.wait()
        self.play(Blink(randy))
        self.wait()
