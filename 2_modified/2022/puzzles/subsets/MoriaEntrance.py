# ==============================================================================
# Scene:      MoriaEntrance
# Source:     videos/_2022/puzzles/subsets.py (lines 4780-4798)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MoriaEntrance.py MoriaEntrance -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - mines-of-moria-entrance.svg (placeholder arched door, svg_images/; make_puzzles_assets.py)
# ==============================================================================

from manim_imports_ext import *

class MoriaEntrance(InteractiveScene):
    def construct(self):
        # Show
        path = SVGMobject("mines-of-moria-entrance")
        path.set_height(FRAME_HEIGHT - 1)
        outline = path.copy()
        outline.set_stroke(WHITE, 2)
        outline.set_fill(opacity=0)
        outline.insert_n_curves(20)
        self.play(
            LaggedStartMap(
                VShowPassingFlash,
                VGroup(*outline.family_members_with_points()),
                lag_ratio=0.001,
                time_width=1.5,
            ),
            FadeIn(path),
            run_time=5,
        )
