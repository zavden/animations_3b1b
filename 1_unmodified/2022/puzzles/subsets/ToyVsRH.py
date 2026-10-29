# ==============================================================================
# Scene:      ToyVsRH
# Source:     videos/_2022/puzzles/subsets.py (lines 419-470)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ToyVsRH.py ToyVsRH -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ToyVsRH(InteractiveScene):
    def construct(self):
        # Screens
        self.add(FullScreenRectangle().set_fill(GREY_E, 1))
        screens = ScreenRectangle().replicate(2)
        screens.set_stroke(WHITE, 1)
        screens.set_fill(BLACK, 1)
        screens.set_height(3.5)
        screens[0].to_corner(UL, buff=SMALL_BUFF)
        screens[1].to_corner(DR, buff=SMALL_BUFF)

        titles = VGroup(
            Text("Our puzzle"),
            Text("Riemann Hypothesis"),
        )
        for title, screen, vect in zip(titles, screens, [RIGHT, LEFT]):
            title.next_to(screen, vect, buff=MED_LARGE_BUFF)
        titles[0].shift(UP)
        titles[1].shift(DOWN)
        toy = Text("(toy problem)")
        toy.set_fill(GREY_B)
        toy.next_to(titles[0], RIGHT)

        self.add(screens)
        self.add(titles)

        # Distance
        arrow = CubicBezier(
            screens[0].get_right() + SMALL_BUFF * RIGHT,
            screens[0].get_right() + 5 * RIGHT,
            screens[1].get_left() + 5 * LEFT,
            screens[1].get_left() + MED_SMALL_BUFF * LEFT,
        )
        arrow.add(ArrowTip().scale(0.5).move_to(arrow.get_end()))
        arrow.set_color(TEAL)

        arrow_label = Text("Long long\ndistance", font_size=36)
        arrow_label.next_to(arrow.pfp(0.25), RIGHT)
        arrow_label.set_color(TEAL)
        or_is_it = Text("or is it?", font_size=36)
        or_is_it.next_to(arrow_label, DOWN, MED_LARGE_BUFF)
        or_is_it.set_color(YELLOW)

        self.play(ShowCreation(arrow))
        self.play(Write(arrow_label, run_time=1))
        self.wait()
        self.play(
            FadeIn(toy, 0.5 * RIGHT)
        )
        self.wait()
        self.play(FadeIn(or_is_it, 0.5 * DOWN))
        self.wait()
