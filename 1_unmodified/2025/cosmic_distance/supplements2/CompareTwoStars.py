# ==============================================================================
# Scene:      CompareTwoStars
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 608-643)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareTwoStars.py CompareTwoStars -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareTwoStars(InteractiveScene):
    def construct(self):
        # Set up two stars
        frame = self.frame
        stars = Group(
            GlowDot(UR, color=WHITE, radius=0.2),
            GlowDot(DR, color=WHITE, radius=0.8),
        )
        randy = Randolph(mode="pondering", height=1)
        randy.shift(4 * LEFT - randy.eyes[1].get_center())
        randy.look_at(stars[0])

        frame.reorient(-88, 87, 0, (-4.0, -0.0, 0.0), 0.19)
        self.add(stars)
        self.wait()
        self.play(
            frame.animate.to_default_state(),
            FadeIn(randy, time_span=(1, 2)),
            run_time=3,
        )

        # Show observation lines
        lines = always_redraw(lambda: VGroup(
            DashedLine(randy.eyes[1].get_right(), stars[0].get_center()),
            DashedLine(randy.eyes[1].get_right(), stars[1].get_center()),
        ).set_stroke(WHITE, 1))

        self.play(*map(ShowCreation, lines))
        self.add(lines)
        self.wait()
        self.play(
            stars[0].animate.shift(lines[0].get_vector()).scale(4),
            run_time=2
        )
        self.play(Blink(randy))
        self.wait()
