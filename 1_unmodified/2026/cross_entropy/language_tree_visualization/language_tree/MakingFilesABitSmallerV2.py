# ==============================================================================
# Scene:      MakingFilesABitSmallerV2
# Source:     videos/_2026/cross_entropy/language_tree_visualization/language_tree.py (lines 1011-1029)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MakingFilesABitSmallerV2.py MakingFilesABitSmallerV2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MakingFilesABitSmallerV2(InteractiveScene):
    def construct(self):
        # Draw an arrow to the document
        arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, thickness=7).set_color(YELLOW)
        document = VGroup(*[
            Rectangle(
                width=5,
                height=1,
                fill_opacity=1,
                fill_color=interpolate_color(TEAL_B, TEAL_E, random.random()),
                stroke_width=1,
                stroke_color=WHITE
            ).scale(0.22)
            for _ in range(8)
        ]).arrange(DOWN, buff=0).set_width(3).set_x(0.5 * (arrow.get_right()[0] + FRAME_WIDTH * 0.5))
        self.play(AnimationGroup(GrowArrow(arrow), GrowFromCenter(document), lag_ratio=0.3))

        # Make the file smaller
        self.play(document.animate.scale(1.2).stretch(0.3, 1), run_time=2)
