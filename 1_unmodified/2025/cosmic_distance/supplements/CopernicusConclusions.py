# ==============================================================================
# Scene:      CopernicusConclusions
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 1078-1142)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CopernicusConclusions.py CopernicusConclusions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CopernicusConclusions(InteractiveScene):
    def construct(self):
        # Add title
        title = TexText("Copernicus", font_size=48)
        underline = Underline(title, buff=-0.05)
        title.add(underline)
        title.to_corner(UL)
        title.set_color(YELLOW)

        self.add(title)

        # Facts
        facts = BulletedList(
            R"proposed the planets\\go around the Sun",
            R"assumed orbits\\were circular",
            R"calculated all the\\orbital periods",
            buff=0.75,
            font_size=36
        )
        facts.next_to(title, DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        facts.shift(MED_SMALL_BUFF * RIGHT)

        for fact in facts:
            self.play(FadeIn(fact, RIGHT))
            self.wait()

        # Test
        self.play(
            self.frame.animate.reorient(0, 0, 0, (0.78, -0.58, 0.0), 9.00),
            facts[:2].animate.scale(0.75, about_edge=UL).set_opacity(0.5),
            facts[2].animate.scale(1.25, about_edge=UL).shift(0.5 * UP)
        )
        self.wait()

        # Show orbital periods
        periods = VGroup(
            Text("Mercury: 88 days"),
            Text("Venus: 225 days"),
            Text("Earth: 365 days"),
            Text("Mars: 687 days"),
            Text("Jupiter: 4,333 days"),
            Text("Saturn: 10,755 days"),
        )
        periods.scale(0.75)
        periods.arrange(DOWN, aligned_edge=LEFT)
        periods.next_to(facts, DOWN, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
        periods.shift(RIGHT)

        self.play(
            LaggedStartMap(FadeIn, periods, shift=0.35 * RIGHT, lag_ratio=0.15)
        )
        self.add(periods)

        # Highlight a few periods
        arrow = Vector(LEFT)
        arrow.set_fill(WHITE, 0)
        arrow.next_to(periods[0], RIGHT)
        for i, color in zip(range(2, 5), [BLUE, RED, ORANGE]):
            self.play(
                periods[:i].animate.set_fill(WHITE, 0.5),
                periods[i + 1:].animate.set_fill(WHITE, 0.5),
                periods[i].animate.set_fill(color, 1),
                arrow.animate.set_fill(color, 1).next_to(periods[i], RIGHT, SMALL_BUFF)
            )
            self.wait()
