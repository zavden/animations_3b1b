# ==============================================================================
# Scene:      ThreeAssumptions
# Source:     videos/_2023/clt/wordy_scenes.py (lines 1085-1189)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeAssumptions.py ThreeAssumptions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThreeAssumptions(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Three assumptions", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.set_color(RED)
        underline = Underline(title, stretch_factor=1.5)
        underline.match_color(title)
        underline.shift(0.15 * UP)


        # Points
        points = [
            TexText(R"1. All $X_i$'s are independent \\ from each other."),
            TexText(R"2. Each $X_i$ is drawn from \\ the same distribution."),
            TexText(R"3. $0 < \text{Var}(X_i) < \infty$"),
        ]
        points[0]["from each other."].align_to(points[0]["All"], LEFT)
        points[1]["the same distribution."].align_to(points[1]["Each"], LEFT)
        VGroup(*points).arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT).to_edge(LEFT)
        for point in points:
            point["X_i"].set_color(BLUE)

        rects = VGroup(*(SurroundingRectangle(point[2:]) for point in points))
        rects.set_stroke(width=0)
        rects.set_fill(interpolate_color(RED_E, BLACK, 0.9), 1.0)

        # Add title and numbers
        self.add(title)
        self.play(ShowCreation(underline, run_time=2))
        self.play(
            LaggedStart(*(
                Write(point[:2])
                for point in points
            ), lag_ratio=0.7),
            LaggedStartMap(FadeIn, rects, lag_ratio=0.7)
        )
        self.add(*points, rects)
        self.wait()

        # Add first two points
        self.play(rects[0].animate.stretch(0, 0, about_edge=RIGHT))
        self.remove(rects[0])
        self.wait()

        word = points[0]["independent"]
        self.play(
            FlashUnder(word, color=TEAL),
            word.animate.set_color(TEAL),
        )
        self.wait()

        self.play(rects[1].animate.stretch(0, 0, about_edge=RIGHT))
        self.remove(rects[1])
        self.wait()
        word = points[1]["same distribution"]
        self.play(
            FlashUnder(word, color=YELLOW),
            word.animate.set_color(YELLOW),
        )
        self.wait()

        # Mention iid
        box = SurroundingRectangle(VGroup(*points[:2]))
        box.set_stroke(GREY_C, 2)
        iid_words = TexText(R"i.i.d. $\rightarrow$ independent and identically distributed")
        iid_words.next_to(box, UP, MED_LARGE_BUFF, aligned_edge=LEFT)

        title.add(underline)

        self.play(
            FadeOut(title),
            ShowCreation(box),
        )
        self.play(Write(iid_words))
        self.wait(2)
        self.play(
            FadeOut(box),
            FadeOut(iid_words),
            FadeIn(title)
        )
        self.wait()

        # Mention generalizations
        gen_words = TexText(R"These can be relaxed (see Lindeberg CLT, $\alpha$-mixing, etc.)")
        gen_words.scale(0.7)
        gen_words.set_color(GREY_A, 1)
        gen_words.next_to(box, UP, aligned_edge=LEFT)
        self.play(
            FadeOut(title),
            FadeIn(gen_words),
            FadeIn(box)
        )
        self.wait(2)
        self.play(
            FadeOut(box),
            FadeOut(gen_words),
            FadeIn(title),
        )
        self.wait()

        # Add last point
        self.play(rects[2].animate.stretch(0, 0, about_edge=RIGHT))
        self.remove(rects[2])
        self.wait(2)
