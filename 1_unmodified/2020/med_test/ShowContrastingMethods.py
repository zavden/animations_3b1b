# ==============================================================================
# Scene:      ShowContrastingMethods
# Source:     videos/_2020/med_test.py (lines 5363-5481)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowContrastingMethods.py ShowContrastingMethods -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowContrastingMethods(Scene):
    def construct(self):
        # Prepare stats
        stats = VGroup(
            OldTexText("Prior: ", "2\\%"),
            OldTexText("Sensitivity: ", "90\\%"),
            OldTexText("Specificity: ", "99\\%"),
        )
        stats.arrange(DOWN, aligned_edge=LEFT)
        colors = [YELLOW, GREEN, BLUE]
        for stat, color in zip(stats, colors):
            stat[0].set_color(color)
            stat[1].align_to(stats[-1][1], LEFT)

        stat_rect = SurroundingRectangle(stats, buff=0.2)
        stat_rect.set_fill(GREY_E, 1)
        stat_rect.set_stroke(WHITE, 2)
        stats.add_to_back(stat_rect)
        stats.set_height(1.5)

        # Setup division
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH)
        h_line.set_stroke(GREY, 2)

        titles = VGroup(
            OldTexText("Using odds"),
            OldTexText("Using probability"),
        )
        titles.set_fill(GREY_A)
        titles[0].to_edge(UP)
        titles[1].next_to(ORIGIN, DOWN, MED_SMALL_BUFF)
        for title in titles:
            line = Underline(title)
            line.shift(0.1 * UP)
            line.set_stroke(GREY_B, 2)
            title.add(line)

        stats_pair = VGroup(stats, stats.copy())
        anims = []
        for sp, u in zip(stats_pair, [1, -1]):
            y = u * FRAME_HEIGHT / 4
            sp.set_y(y)
            sp.shift(0.5 * DOWN)
            sp.to_edge(LEFT)
            anims.append(FadeIn(sp, shift=y * UP))

        self.play(
            ShowCreation(h_line),
            FadeIn(titles),
            *anims
        )

        # Bayes factor method
        prior_odds = OldTexText("Prior odds = ", "2:99")
        bf_eq = VGroup(
            OldTexText("Bayes\\\\Factor"),
            OldTex(
                "= {90\\% \\over 1\\%} = 90",
                tex_to_color_map={"90\\%": GREEN, "1\\%": BLUE}
            ),
        )
        bf_eq.arrange(RIGHT, buff=SMALL_BUFF)

        steps = VGroup(prior_odds, bf_eq)
        steps.scale(0.9)
        steps.arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        steps.next_to(stats, RIGHT, buff=1.0)

        p_rect = SurroundingRectangle(stats[1][1], buff=0.05)
        ss_rect = SurroundingRectangle(VGroup(stats[2][1], stats[3][1]), buff=0.05)
        ss_rect.set_stroke(GREEN)
        p_rect.match_width(ss_rect, stretch=True, about_edge=LEFT)

        p_arrow = Arrow(p_rect.get_right(), prior_odds.get_left(), buff=0.1)
        p_arrow.match_color(p_rect)
        ss_arrow = Arrow(ss_rect.get_right(), bf_eq.get_left(), buff=0.1)
        ss_arrow.match_color(ss_rect)

        ans = OldTex("\\text{180:99} \\approx 2:1 \\rightarrow {2 \\over 3}")
        ans.scale(0.9)
        ans.next_to(steps, RIGHT, buff=1.0)
        globals()['ans'] = ans
        ans_arrows = VGroup(*(
            Arrow(step.get_right(), ans.get_left(), buff=0.1)
            for step in steps
        ))

        # PPV formula
        ppv_formula = OldTex(
            """
            \\text{PPV} = 
            {(0.02)(0.9) \\over (0.02)(0.9) + (1 - 0.02)(0.01)}
            \\approx 0.647
            """,
            tex_to_color_map={
                "0.02": YELLOW,
                "0.9": GREEN,
                "0.01": BLUE,
            }
        )
        ppv_formula.scale(0.9)
        ppv_formula.next_to(stats_pair[1], RIGHT, LARGE_BUFF)

        self.play(
            FadeIn(steps, RIGHT),
            ShowCreation(p_rect),
            ShowCreation(ss_rect),
            GrowArrow(p_arrow),
            GrowArrow(ss_arrow),
        )
        self.play(
            FadeIn(ppv_formula, RIGHT)
        )
        self.play(
            *map(GrowArrow, ans_arrows),
            FadeIn(ans, RIGHT)
        )
        self.wait()
