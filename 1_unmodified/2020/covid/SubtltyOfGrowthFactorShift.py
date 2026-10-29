# ==============================================================================
# Scene:      SubtltyOfGrowthFactorShift
# Source:     videos/_2020/covid.py (lines 1687-1829)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SubtltyOfGrowthFactorShift.py SubtltyOfGrowthFactorShift -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

CASE_DATA = [
    9,
    15,
    30,
    40,
    56,
    66,
    84,
    102,
    131,
    159,
    173,
    186,
    190,
    221,
    248,
    278,
    330,
    354,
    382,
    461,
    481,
    526,
    587,
    608,
    697,
    781,
    896,
    999,
    1124,
    1212,
    1385,
    1715,
    2055,
    2429,
    2764,
    3323,
    4288,
    5364,
    6780,
    8555,
    10288,
    12742,
    14901,
    17865,
    21395,
    # 25404,
    # 29256,
    # 33627,
    # 38170,
    # 45421,
    # 53873,
]


class SubtltyOfGrowthFactorShift(Scene):
    def construct(self):
        # Set up totals
        total_title = OldTexText("Totals")
        total_title.add(Underline(total_title))
        total_title.to_edge(UP)
        total_title.scale(1.25)
        total_title.shift(LEFT)
        total_title.set_color(YELLOW)
        total_title.shift(LEFT)

        data = CASE_DATA[-4:]
        data.append(int(data[-1] + 1.15 * (data[-1] - data[-2])))
        totals = VGroup(*[Integer(value) for value in data])
        totals.scale(1.25)
        totals.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        totals.next_to(total_title, DOWN, buff=0.6)
        totals[-1].set_color(BLUE)

        # Set up dates
        dates = VGroup(
            OldTexText("March 3, 2020"),
            OldTexText("March 4, 2020"),
            OldTexText("March 5, 2020"),
            OldTexText("March 6, 2020"),
        )
        for date, total in zip(dates, totals):
            date.scale(0.75)
            date.set_color(GREY_B)
            date.next_to(total, LEFT, buff=0.75, aligned_edge=DOWN)

        # Set up changes
        change_arrows = VGroup()
        change_labels = VGroup()
        for t1, t2 in zip(totals, totals[1:]):
            arrow = Arrow(
                t1.get_right(),
                t2.get_right(),
                path_arc=-150 * DEGREES,
                buff=0.1,
                max_tip_length_to_length_ratio=0.15,
            )
            arrow.shift(MED_SMALL_BUFF * RIGHT)
            arrow.set_stroke(width=3)
            change_arrows.add(arrow)

            diff = t2.get_value() - t1.get_value()
            label = Integer(diff, include_sign=True)
            label.set_color(GREEN)
            label.next_to(arrow, RIGHT)
            change_labels.add(label)

        change_labels[-1].set_color(BLUE)

        change_title = OldTexText("Changes")
        change_title.add(Underline(change_title).shift(0.128 * UP))
        change_title.scale(1.25)
        change_title.set_color(GREEN)
        change_title.move_to(change_labels)
        change_title.align_to(total_title, UP)

        # Set up growth factors
        gf_labels = VGroup()
        gf_arrows = VGroup()
        for c1, c2 in zip(change_labels, change_labels[1:]):
            arrow = Arrow(
                c1.get_right(),
                c2.get_right(),
                path_arc=-150 * DEGREES,
                buff=0.1,
                max_tip_length_to_length_ratio=0.15,
            )
            arrow.set_stroke(width=1)
            gf_arrows.add(arrow)

            line = Line(LEFT, RIGHT)
            line.match_width(c2)
            line.set_stroke(WHITE, 2)
            numer = c2.deepcopy()
            denom = c1.deepcopy()
            frac = VGroup(numer, line, denom)
            frac.arrange(DOWN, buff=SMALL_BUFF)
            frac.scale(0.7)
            frac.next_to(arrow, RIGHT)
            eq = OldTex("=")
            eq.next_to(frac, RIGHT)
            gf = DecimalNumber(c2.get_value() / c1.get_value())
            gf.next_to(eq, RIGHT)
            gf_labels.add(VGroup(frac, eq, gf))

        gf_title = OldTexText("Growth factors")
        gf_title.add(Underline(gf_title))
        gf_title.scale(1.25)
        gf_title.move_to(gf_labels[0][-1])
        gf_title.align_to(total_title, DOWN)

        # Add things
        self.add(dates, total_title)
        self.play(
            LaggedStartMap(
                FadeInFrom, totals[:-1],
                lambda m: (m, UP),
            )
        )
        self.wait()
        self.play(
            ShowCreation(change_arrows[:-1]),
            LaggedStartMap(
                FadeInFrom, change_labels[:-1],
                lambda m: (m, LEFT),
            ),
            FadeIn(change_title),
        )
        self.wait()
        self.play(
            ShowCreation(gf_arrows[:-1]),
            LaggedStartMap(FadeIn, gf_labels[:-1]),
            FadeIn(gf_title),
        )
        self.wait()

        # Show hypothetical new value
        self.play(LaggedStart(
            FadeIn(gf_labels[-1]),
            FadeIn(gf_arrows[-1]),
            FadeIn(change_labels[-1]),
            FadeIn(change_arrows[-1]),
            FadeIn(totals[-1]),
        ))
        self.wait()

        # Change it
        alt_change = data[-2] - data[-3]
        alt_total = data[-2] + alt_change
        alt_gf = 1

        self.play(
            ChangeDecimalToValue(gf_labels[-1][-1], alt_gf),
            ChangeDecimalToValue(gf_labels[-1][0][0], alt_change),
            ChangeDecimalToValue(change_labels[-1], alt_change),
            ChangeDecimalToValue(totals[-1], alt_total),
        )
        self.wait()
