# ==============================================================================
# Scene:      TalkFrame
# Source:     videos/_2026/spheres_talk/supplements.py (lines 4-25)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TalkFrame.py TalkFrame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TalkFrame(InteractiveScene):
    def construct(self):
        # Test
        background = FullScreenRectangle()
        background.set_fill(interpolate_color(BLUE_E, BLACK, 0.9), 1)
        background.set_shading(0.1, 0.1, 0)

        slides = ScreenRectangle()
        slides.set_fill(BLACK, 1)
        slides.set_stroke(WHITE, 1)
        slides.set_height(6)
        slides.to_edge(LEFT, buff=0.1)

        speaker = ScreenRectangle()
        speaker.set_width(3)
        speaker.set_fill(BLACK, 1)
        speaker.set_stroke(WHITE, 1)
        speaker.next_to(slides, RIGHT, aligned_edge=UP)

        self.add(background)
        self.add(slides)
        self.add(speaker)
