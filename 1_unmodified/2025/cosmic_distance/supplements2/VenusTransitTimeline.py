# ==============================================================================
# Scene:      VenusTransitTimeline
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 220-277)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VenusTransitTimeline.py VenusTransitTimeline -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VenusTransitTimeline(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        timeline = NumberLine(
            (1500, 2000, 10),
            tick_size=0.05,
            longer_tick_multiple=2,
            big_tick_spacing=100,
            unit_size=1 / 25
        )
        numbers =timeline.add_numbers(
            range(1500, 2050, 50),
            group_with_commas=False,
            font_size=20,
            buff=0.15
        )

        self.add(timeline)

        # Show 1761
        years = [1761, 1769, 1874]
        dots = Group(
            GlowDot(timeline.n2p(year)).set_color(YELLOW)
            for year in years
        )
        arrow = Vector(0.65 * UP, thickness=2)
        arrow.set_color(YELLOW)
        arrow.next_to(dots[0], DOWN, buff=-SMALL_BUFF)
        year_label = Text(str(years[0]), font_size=24)
        year_label.set_color(YELLOW)
        year_label.next_to(arrow, DOWN, SMALL_BUFF)

        self.play(
            GrowArrow(arrow),
            Write(year_label),
            FadeIn(dots[0], UP),
            frame.animate.set_height(6).move_to(dots[0].get_center() + 0.5 * UP).set_anim_args(run_time=2)
        )
        self.wait()

        # Next
        next_arrows = VGroup(
            Arrow(d1.get_center(), d2.get_center(), path_arc=angle, buff=0.05)
            for d1, d2, angle in zip(dots, dots[1:], [-PI, -90 * DEG])
        )
        next_labels = VGroup(
            Text(f"+{n} years", font_size=16).next_to(na, UP, SMALL_BUFF)
            for na, n in zip(next_arrows, [8, 105])
        )

        for na, label, d1, d2 in zip(next_arrows, next_labels, dots, dots[1:]):
            self.play(
                FadeIn(na),
                FadeIn(label, lag_ratio=0.1),
                TransformFromCopy(d1, d2, path_arc=-90 * DEG),
            )
            self.wait()
