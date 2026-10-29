# ==============================================================================
# Scene:      KeyTakeaways
# Source:     videos/_2020/sir.py (lines 2021-2116)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KeyTakeaways.py KeyTakeaways -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class KeyTakeaways(Scene):
    def construct(self):
        takeaways = VGroup(*[
            OldTexText(
                text,
                alignment="",
            )
            for text in [
                """
                    Changes in how many people slip through the tests\\\\
                    cause disproportionately large changes to the total\\\\
                    number of people infected.
                """,
                """
                    Social distancing slows the spread, but\\\\
                    even small imperfections prolong it.
                """,
                """
                    Reducing transit between communities, late in the game,\\\\
                    has a very limited effect.
                """,
                """
                    Shared central locations dramatically speed up\\\\
                    the spread.
                """,
            ]
        ])
        takeaway = OldTexText(
            "The growth rate is very sensitive to:\\\\",
            "- \\# Daily interactions\\\\",
            "- Probability of infection\\\\",
            "- Duration of illness\\\\",
            alignment="",
        )
        takeaway[1].set_color(GREEN_D)
        takeaway[2].set_color(GREEN_C)
        takeaway[3].set_color(GREEN_B)
        takeaway.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        takeaways.add_to_back(takeaway)

        takeaways.scale(1.25)

        titles = VGroup()
        for i in range(len(takeaways)):
            title = OldTexText("Key takeaway \\#")
            num = Integer(i + 1)
            num.next_to(title, RIGHT, buff=SMALL_BUFF)
            title.add(num)
            titles.add(title)

        titles.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        titles.to_edge(LEFT)
        titles.set_color(GREY_D)

        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH - 1)
        h_line.to_edge(UP, buff=1.5)

        for takeaway in takeaways:
            takeaway.next_to(h_line, DOWN, buff=0.75)
            max_width = FRAME_WIDTH - 2
            if takeaway.get_width() > max_width:
                takeaway.set_width(max_width)

        takeaways[3].shift(0.25 * UP)

        self.add(titles)
        self.wait()

        for title, takeaway in zip(titles, takeaways):
            other_titles = VGroup(*titles)
            other_titles.remove(title)
            self.play(title.set_color, WHITE, run_time=0.5)
            title.save_state()
            temp_h_line = h_line.copy()
            self.play(
                title.scale, 1.5,
                title.to_edge, UP,
                title.set_x, 0,
                title.set_color, YELLOW,
                FadeOut(other_titles),
                ShowCreation(temp_h_line),
            )

            self.play(FadeIn(takeaway, lag_ratio=0.1, run_time=2, rate_func=linear))
            self.wait(2)
            temp_h_line.rotate(PI)
            self.play(
                Restore(title),
                FadeIn(other_titles),
                Uncreate(temp_h_line),
                FadeOut(takeaway, DOWN, lag_ratio=0.25 / len(takeaway.family_members_with_points()))
            )
            self.wait()

        self.embed()
