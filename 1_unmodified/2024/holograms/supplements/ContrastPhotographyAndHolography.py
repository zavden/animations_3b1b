# ==============================================================================
# Scene:      ContrastPhotographyAndHolography
# Source:     videos/_2024/holograms/supplements.py (lines 117-148)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContrastPhotographyAndHolography.py ContrastPhotographyAndHolography -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ContrastPhotographyAndHolography(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Information lost in ordinary photography", font_size=60)
        title.to_edge(UP)
        underline = Underline(title, buff=-0.05)

        points = BulletedList(
            "All but one viewing angle",
            "Phase",
            buff=LARGE_BUFF
        )

        points.scale(1.25)
        points.next_to(underline, DOWN, buff=1.5)
        points.shift(2 * LEFT)
        self.add(*(p[0] for p in points))

        self.play(
            FadeIn(title),
            ShowCreation(underline)
        )

        for point in points:
            self.wait()
            self.play(Write(point[1:]))

        self.play(
            FlashAround(points[1], color=TEAL, time_width=1.5, run_time=2),
            points[1].animate.set_color(TEAL)
        )
        self.wait()
