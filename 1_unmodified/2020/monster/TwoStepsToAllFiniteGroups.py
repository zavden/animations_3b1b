# ==============================================================================
# Scene:      TwoStepsToAllFiniteGroups
# Source:     videos/_2020/monster.py (lines 3555-3719)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoStepsToAllFiniteGroups.py TwoStepsToAllFiniteGroups -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoStepsToAllFiniteGroups(Scene):
    def construct(self):
        # List
        title = OldTexText("How to categorize all finite groups")
        title.scale(1.5)
        title.add(Underline(title))
        title.to_edge(UP)

        steps = VGroup(
            OldTexText("1. ", "Find all the ", "simple groups", "."),
            OldTexText("2. ", "Find all the ", "ways to\\\\", "combine ", "simple groups", "."),
        )
        steps[1][3:].next_to(steps[1][1], DOWN, SMALL_BUFF, aligned_edge=LEFT)
        steps.arrange(DOWN, aligned_edge=LEFT, buff=2)
        steps.set_y(-0.5)
        steps.to_edge(LEFT)
        for step in steps:
            step.set_color_by_tex("simple groups", TEAL)

        self.add(title)
        self.wait()
        self.play(LaggedStartMap(
            FadeIn, VGroup(steps[0][0], steps[1][0]),
            lambda m: (m, RIGHT),
            lag_ratio=0.4,
        ))
        self.wait()
        self.play(FadeIn(steps[0][1:], lag_ratio=0.1))
        self.wait()
        self.play(
            TransformFromCopy(steps[0][1], steps[1][1]),
            TransformFromCopy(steps[0][2], steps[1][4]),
            FadeIn(VGroup(*[steps[1][i] for i in (2, 3, 5)])),
        )
        self.wait()

        # Periodic table
        table = VGroup(*[
            VGroup(*[
                Square() for x in range(n)
            ]).arrange(DOWN, buff=0)
            for n in [7, 6, *[4] * 10, *[6] * 5, 7]
        ])
        table.arrange(RIGHT, buff=0, aligned_edge=DOWN)
        table.set_width(4)
        table.to_edge(RIGHT)
        table.match_y(steps[0])
        table.set_stroke(GREY_A, 2)

        table_arrow = Arrow(
            steps[0].get_right(), table.get_left(),
            buff=0.5,
        )

        self.play(
            GrowArrow(table_arrow),
            FadeIn(table, lag_ratio=0.1, run_time=3),
        )
        self.wait()

        # Chemistry
        chem_words = OldTexText("All of chemistry")
        chem_words.match_y(steps[1])
        chem_words.match_x(table)
        chem_words.set_color(RED)
        chem_arrow = Arrow(
            steps[1].get_right(), chem_words.get_left(),
            buff=0.5
        )
        self.play(
            GrowArrow(chem_arrow),
            Write(chem_words),
        )
        self.wait()

        # Found all simples
        top_group = VGroup(steps[0], table_arrow, table)
        bottom_group = VGroup(steps[1], chem_arrow, chem_words)
        frame = self.camera.frame

        top_rect = SurroundingRectangle(top_group, buff=MED_LARGE_BUFF)
        top_rect.set_stroke(GREEN, 4)
        check = Checkmark()
        check.set_height(0.7)
        check.next_to(top_rect, UP, aligned_edge=LEFT)
        check.shift(RIGHT)

        self.play(
            frame.scale, 1.1,
            bottom_group.shift, 0.5 * DOWN,
            bottom_group.set_opacity, 0.5,
            ShowCreation(top_rect),
            FadeOut(title, UP),
        )
        self.play(Write(check))
        self.wait()

        proof_words = OldTexText("(prove you have them all.)")
        proof_words.next_to(steps[0], DOWN)
        proof_words.set_color(GREY_A)
        self.play(Write(proof_words, run_time=2))
        self.wait()

        # What was involved
        stats = VGroup(
            OldTexText("1955-2004"),
            OldTexText("$10{,}000+$ pages"),
            OldTexText("100's of mathematicians"),
            OldTexText("Plenty of computation"),
        )
        stats.arrange_in_grid(buff=1.5, aligned_edge=LEFT)
        stats.next_to(top_rect, DOWN, buff=LARGE_BUFF)
        for stat in stats:
            dot = Dot()
            dot.next_to(stat, LEFT)
            stat.add(dot)

        turn_animation_into_updater(ApplyMethod(frame.shift, DOWN, run_time=3))
        self.add(frame)
        for stat in stats:
            self.play(FadeIn(stat), bottom_group.set_opacity, 0)
            self.wait(0.5)
        self.remove(bottom_group)

        # 2004 paper mention
        stats.generate_target()
        stats.target.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        stats.target.move_to(stats, UL)

        last_paper = OldTexText(
            "The Classification of Quasithin Groups\\\\",
            "Aschbacher and Smith (2004)\\\\",
            "(12{,}000 pages!)",
        )
        last_paper.scale(0.7)
        last_paper[:-1].set_color(YELLOW)
        last_paper.move_to(stats, RIGHT)
        last_paper.shift(RIGHT)

        self.play(
            FadeIn(last_paper, DOWN),
            MoveToTarget(stats),
        )
        self.wait()

        # Quote
        quote = OldTexText(
            """
            ``...undoubtedly one of the most\\\\
            extraordinary theorems that pure\\\\
            mathematics has ever seen.''\\\\
            """,
            "-Richard Elwes",
            alignment="",
        )
        quote.scale(0.9)
        quote[0].set_color(YELLOW)
        quote[-1].shift(MED_SMALL_BUFF * DR)
        quote.move_to(last_paper, LEFT)

        self.play(
            FadeIn(quote),
            FadeOut(last_paper),
        )
        self.wait()
