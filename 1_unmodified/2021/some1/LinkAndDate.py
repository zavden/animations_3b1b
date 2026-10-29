# ==============================================================================
# Scene:      LinkAndDate
# Source:     videos/_2021/some1.py (lines 87-113)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LinkAndDate.py LinkAndDate -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_tripple_underline(mobject, buff=0.1):
    ul1 = Underline(mobject, buff=buff).set_stroke(BLUE_C, 3)
    ul2 = Underline(ul1).scale(0.9).set_stroke(BLUE_D, 2)
    ul3 = Underline(ul2).scale(0.9).set_stroke(BLUE_E, 1)
    return VGroup(ul1, ul2, ul3)


class LinkAndDate(Scene):
    def construct(self):
        words = link, date = VGroup(
            Text("https://3b1b.co/SoME1", font="CMU Serif"),
            Text("August 22nd", font="CMU Serif")
        )
        words.set_width(10)
        words.arrange(DOWN, buff=0.5)
        words.set_stroke(BLACK, 5, background=True)

        lines = get_tripple_underline(date)

        details = Text("(Full details here)")
        details.to_corner(UR)
        arrow = Arrow(details, link, buff=0.5)

        self.play(Write(link), run_time=1)
        self.wait()
        self.add(lines, words)
        self.play(
            FadeIn(date, scale=1.2, rate_func=squish_rate_func(smooth, 0.3, 0.7)),
            ShowCreation(lines, lag_ratio=0.25)
        )
        self.wait()

        self.play(FadeIn(details), GrowArrow(arrow))
        self.wait()
