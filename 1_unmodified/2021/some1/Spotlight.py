# ==============================================================================
# Scene:      Spotlight
# Source:     videos/_2021/some1.py (lines 1151-1161)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Spotlight.py Spotlight -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Spotlight(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        screen = ScreenRectangle()
        screen.set_height(6.0)
        screen.set_stroke(WHITE, 2)
        screen.set_fill(BLACK, 1)
        screen.to_edge(DOWN)
        animated_screen = AnimatedBoundary(screen)
        self.add(screen, animated_screen)
        self.wait(16)
