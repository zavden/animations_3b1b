# ==============================================================================
# Scene:      SpoilerAlert
# Source:     videos/_2024/puzzles/supplements.py (lines 421-440)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SpoilerAlert.py SpoilerAlert -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SpoilerAlert(InteractiveScene):
    def construct(self):
        # Test
        tri = RegularPolygon(3)
        tri.set_height(3)
        tri.round_corners(radius=0.25)
        tri.set_stroke(RED, 20)
        tri.move_to(UP)

        bang = Tex("!", font_size=240)
        bang.move_to(interpolate(tri.get_bottom(), tri.get_top(), 0.45))
        bang.match_color(tri)

        words = Text("Spoiler", font_size=120)
        words.next_to(tri, DOWN, buff=0.5)
        words.set_color(RED)

        self.add(tri)
        self.play(FadeIn(words, scale=1.25), Write(bang), run_time=1)
        self.wait()
