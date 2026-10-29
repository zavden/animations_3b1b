# ==============================================================================
# Scene:      ContentAdvice
# Source:     videos/_2021/some1.py (lines 316-356)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContentAdvice.py ContentAdvice -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_tripple_underline(mobject, buff=0.1):
    ul1 = Underline(mobject, buff=buff).set_stroke(BLUE_C, 3)
    ul2 = Underline(ul1).scale(0.9).set_stroke(BLUE_D, 2)
    ul3 = Underline(ul2).scale(0.9).set_stroke(BLUE_E, 1)
    return VGroup(ul1, ul2, ul3)


class ContentAdvice(Scene):
    def construct(self):
        title = Text("Advice for structuring math explanations")
        title.set_width(10)
        title.to_edge(UP)
        underline = Underline(title).scale(1.2).set_stroke(GREY_B, 2)

        self.play(FadeIn(title, UP))
        self.play(ShowCreation(underline))

        points = VGroup(
            Text("1) Concrete before abstract"),
            Text("2) Topic choice > production quality"),
            Text("3) Be niche"),
            Text("4) Know your genre"),
            Text("5) Definitions are not the beginning"),
        )
        points.arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        points.next_to(title, DOWN, buff=1.0)

        self.play(LaggedStartMap(
            FadeIn,
            VGroup(*(point[:2] for point in points)),
            shift=0.25 * RIGHT
        ))
        self.wait()

        for point in points:
            self.play(Write(point[2:]))

        self.wait()
        gt0 = OldTex("> 0")
        gt0.next_to(points[1], RIGHT)
        self.play(
            VGroup(points[0], *points[2:]).animate.set_opacity(0.25)
        )
        self.play(Write(gt0))
        self.play(ShowCreation(get_tripple_underline(
            VGroup(points[1].get_part_by_text("production quality"), gt0)
        )))
        self.wait()
