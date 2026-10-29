# ==============================================================================
# Scene:      QuickEstimatesAndMisconceptions
# Source:     videos/_2020/med_test.py (lines 2117-2200)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuickEstimatesAndMisconceptions.py QuickEstimatesAndMisconceptions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuickEstimatesAndMisconceptions(Scene):
    def construct(self):
        titles = VGroup(
            OldTexText("Quick\\\\estimations"),
            OldTexText("Combating\\\\misconceptions"),
        )
        for title, u in zip(titles, [-1, 1]):
            title.set_x(u * FRAME_WIDTH / 4)
        titles.to_edge(UP, buff=MED_SMALL_BUFF)

        circles = VGroup(
            Circle(color=BLUE),
            Circle(color=RED),
        )
        circles[1].flip()
        circles.set_height(4)
        circles.set_stroke(width=3)
        circles.set_fill(opacity=0.5)

        for circle, title, u in zip(circles, titles, [-1, 1]):
            circle.set_x(u)
            title.set_color(
                interpolate_color(circle.get_color(), WHITE, 0.5)
            )
            title.next_to(circle, UP)
            title.shift(u * RIGHT)

        self.play(
            LaggedStartMap(FadeIn, titles, shift=0.2 * UP),
            LaggedStartMap(DrawBorderThenFill, circles),
            run_time=1.5,
        )
        self.wait()

        arrow = OldTex("\\leftrightarrow", font_size=72)
        arrow.move_to(circles)
        self.play(
            circles[0].next_to, arrow, LEFT,
            circles[1].next_to, arrow, RIGHT,
            titles[0].shift, 0.7 * LEFT,
            titles[1].shift, 0.7 * RIGHT,
            GrowFromCenter(arrow),
        )
        self.wait(2)
        self.play(
            FadeOut(arrow, DOWN),
            circles[0].shift, 2.0 * RIGHT,
            circles[1].shift, 2.0 * LEFT,
            titles[0].shift, 1.0 * RIGHT,
            titles[1].shift, 1.0 * LEFT,
        )
        self.wait()

        titles[1].save_state()
        self.play(
            FadeOut(titles[0]),
            FadeOut(circles[0]),
            titles[1].match_x, circles[1]
        )
        self.wait()

        circles[0].save_state()
        titles[0].save_state()
        circles[0].next_to(circles[1], LEFT, MED_LARGE_BUFF)
        titles[0].next_to(circles[0], UP)

        self.play(
            FadeIn(titles[0]),
            FadeIn(circles[0]),
        )
        self.wait()

        bayes_factor = OldTexText("Bayes\\\\factor", font_size=72)
        bayes_factor.move_to(circles[0])

        self.play(Write(bayes_factor))
        self.wait()
        restoration_group = VGroup(circles[0], titles[0], titles[1])
        self.add(restoration_group, bayes_factor)
        self.play(
            bayes_factor.move_to, VGroup(circles[0].saved_state, circles[1]),
            LaggedStartMap(Restore, restoration_group)
        )
        self.wait()
