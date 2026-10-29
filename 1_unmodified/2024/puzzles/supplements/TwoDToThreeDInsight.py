# ==============================================================================
# Scene:      TwoDToThreeDInsight
# Source:     videos/_2024/puzzles/supplements.py (lines 151-191)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoDToThreeDInsight.py TwoDToThreeDInsight -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoDToThreeDInsight(InteractiveScene):
    def construct(self):
        # 2D -> 3D
        self.add(FullScreenRectangle())
        rects = Rectangle(4, 3).replicate(2)
        rects.set_width(FRAME_WIDTH // 2 - 1)
        rects.move_to(0.5 * DOWN)
        rects.arrange(RIGHT, buff=1)
        rects.set_fill(BLACK, 1)
        rects.set_stroke(WHITE, 2)

        titles = VGroup(Text("2D Puzzle"), Text("3D Insight"))
        for title, rect in zip(titles, rects):
            title.next_to(rect, UP)

        arrow = Arrow(titles[0].get_corner(UR), titles[1].get_corner(UL), path_arc=-45 * DEGREES)

        self.add(rects)
        self.add(titles)
        self.wait()
        self.play(GrowArrow(arrow, path_arc=-22 * DEGREES))
        self.wait()

        # Ask about four dimension
        new_titles = VGroup(Text("3D Puzzle"), Text("4D Insight"))
        for title, rect in zip(new_titles, rects):
            title.next_to(rect, UP)

        new_arrow = arrow.copy()

        left_shift = 8 * LEFT
        self.play(
            FadeOut(titles[0], left_shift),
            FadeOut(arrow, left_shift),
            TransformMatchingStrings(titles[1], new_titles[0])
        )
        self.play(
            GrowArrow(new_arrow, path_arc=-22 * DEGREES),
            FadeIn(new_titles[1], 4 * RIGHT)
        )
        self.wait()
