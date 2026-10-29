# ==============================================================================
# Scene:      ThetaChart
# Source:     videos/_2019/clacks/solution1.py (lines 2256-2386)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThetaChart.py ThetaChart -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThetaChart(Scene):
    def construct(self):
        self.create_columns()
        self.populate_columns()
        self.show_values()
        self.highlight_example(2)
        self.highlight_example(3)

    def create_columns(self):
        titles = VGroup(*[
            OldTexText("Mass ratio"),
            OldTexText("$\\theta$ formula"),
            OldTexText("$\\theta$ value"),
        ])
        titles.scale(1.5)
        titles.arrange(RIGHT, buff=1.5)
        titles[1].shift(MED_SMALL_BUFF * LEFT)
        titles[2].shift(MED_SMALL_BUFF * RIGHT)
        titles.to_corner(UL)

        lines = VGroup()
        for t1, t2 in zip(titles, titles[1:]):
            line = Line(TOP, BOTTOM)
            x = np.mean([t1.get_center()[0], t2.get_center()[0]])
            line.shift(x * RIGHT)
            lines.add(line)

        h_line = Line(LEFT_SIDE, RIGHT_SIDE)
        h_line.next_to(titles, DOWN)
        h_line.to_edge(LEFT, buff=0)
        lines.add(h_line)
        lines.set_stroke(WHITE, 1)

        self.play(
            LaggedStartMap(FadeInFromDown, titles),
            LaggedStartMap(ShowCreation, lines, lag_ratio=0.8),
        )

        self.h_line = h_line
        self.titles = titles

    def populate_columns(self):
        top_h_line = self.h_line
        x_vals = [t.get_center()[0] for t in self.titles]

        entries = [
            (
                "$m_1$ : $m_2$",
                "$\\arctan(\\sqrt{m_2} / \\sqrt{m_1})$",
                ""
            )
        ] + [
            (
                "{:,} : 1".format(10**(2 * exp)),
                "$\\arctan(1 / {:,})$".format(10**exp),
                self.get_theta_decimal(exp),
            )
            for exp in [1, 2, 3, 4, 5]
        ]

        h_lines = VGroup(top_h_line)
        entry_mobs = VGroup()
        for entry in entries:
            mobs = VGroup(*map(TexText, entry))
            for mob, x in zip(mobs, x_vals):
                mob.shift(x * RIGHT)
            delta_y = (mobs.get_height() / 2) + MED_SMALL_BUFF
            y = h_lines[-1].get_center()[1] - delta_y
            mobs.shift(y * UP)
            mobs[0].set_color(BLUE)
            mobs[2].set_color(YELLOW)
            entry_mobs.add(mobs)

            h_line = DashedLine(LEFT_SIDE, RIGHT_SIDE)
            h_line.shift((y - delta_y) * UP)
            h_lines.add(h_line)

        self.play(
            LaggedStartMap(
                FadeInFromDown,
                VGroup(*[em[:2] for em in entry_mobs]),
            ),
            LaggedStartMap(ShowCreation, h_lines[1:]),
            lag_ratio=0.1,
            run_time=5,
        )

        self.entry_mobs = entry_mobs
        self.h_lines = h_lines

    def show_values(self):
        values = VGroup(*[em[2] for em in self.entry_mobs])
        for value in values:
            self.play(LaggedStartMap(
                FadeIn, value,
                lag_ratio=0.1,
                run_time=0.5
            ))
            self.wait(0.5)

    def highlight_example(self, exp):
        entry_mobs = self.entry_mobs
        example = entry_mobs[exp]
        other_entries = VGroup(*entry_mobs[:exp], *entry_mobs[exp + 1:])

        value = example[-1]
        rhs = OldTex("\\approx {:}".format(10**(-exp)))
        rhs.next_to(value, RIGHT)
        rhs.to_edge(RIGHT, buff=MED_SMALL_BUFF)
        value.generate_target()
        value.target.set_fill(opacity=1)
        value.target.scale(0.9)
        value.target.next_to(rhs, LEFT, SMALL_BUFF)

        self.play(
            other_entries.set_fill, {"opacity": 0.25},
            example.set_fill, {"opacity": 1},
            ShowCreationThenFadeAround(example)
        )
        self.wait()
        self.play(
            MoveToTarget(value),
            Write(rhs),
        )
        self.wait()
        value.add(rhs)

    def get_theta_decimal(self, exp):
        theta = np.arctan(10**(-exp))
        rounded_theta = np.floor(1e10 * theta) / 1e10
        return "{:0.10f}\\dots".format(rounded_theta)
