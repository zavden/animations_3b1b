# ==============================================================================
# Scene:      CircleAtaphogy
# Source:     videos/outside_videos/gifs.py (lines 20-25)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CircleAtaphogy.py CircleAtaphogy -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Mobject.repeat no longer exists in manimgl; the points are repeated by hand
# ==============================================================================

from manim_imports_ext import *

class CircleAtaphogy(Scene):
    def construct(self):
        circle = Circle(radius=3)
        target = circle.copy()
        # CHANGE: Mobject.repeat no longer exists in manimgl; the points are repeated by hand
        pts = circle.get_points()
        target.set_points(np.concatenate([np.tile(pts[:-1], (7, 1)), pts[-1:]]))
        self.play(
            Transform(circle, target),
            run_time=3.0
        )
