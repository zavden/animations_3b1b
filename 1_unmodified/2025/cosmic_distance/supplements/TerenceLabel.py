# ==============================================================================
# Scene:      TerenceLabel
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 5-31)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TerenceLabel.py TerenceLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TerenceLabel(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Terence Tao", font_size=72)
        title.to_edge(UP)
        title.set_fill(border_width=3)
        title.set_backstroke(BLACK, 5)

        subtitle = VGroup(
            Text("Professor of Mathematics at UCLA", font_size=42),
        )
        subtitle.next_to(title, DOWN, LARGE_BUFF, aligned_edge=LEFT)
        subtitle.set_fill(border_width=1.5)
        subtitle.set_backstroke(BLACK, 3)

        arrow = Arrow(title.get_bottom(), title.get_bottom() + (2.5, -1.0, 0), thickness=5, path_arc=45 * DEG)
        arrow.set_fill(WHITE, 1)
        arrow.set_backstroke(BLACK, 2)

        self.add(title)
        self.wait()
        self.play(FadeIn(subtitle, lag_ratio=0.1, run_time=2))
        self.wait()
        return

        self.play(Write(arrow, run_time=2))
        self.wait()
