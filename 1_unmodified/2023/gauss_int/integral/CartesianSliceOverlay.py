# ==============================================================================
# Scene:      CartesianSliceOverlay
# Source:     videos/_2023/gauss_int/integral.py (lines 1212-1305)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CartesianSliceOverlay.py CartesianSliceOverlay -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CartesianSliceOverlay(InteractiveScene):
    def construct(self):
        # Show integral
        kw = dict(
            t2c={"{x}": BLUE, "{y}": YELLOW, "C": RED},
            font_size=48,
        )
        integral1 = Tex(R"\int_{-\infty}^\infty C \cdot e^{-{y}^2} d{y}", **kw)
        integral2 = Tex(R"= C \int_{-\infty}^\infty e^{-{y}^2}d{y}", **kw)
        rhs = Tex(R"= C^2", **kw)
        top_eq = VGroup(integral1, integral2, rhs)
        top_eq.arrange(RIGHT, buff=MED_SMALL_BUFF)
        top_eq.to_corner(UL)
        for part in top_eq:
            part.shift((integral1[0].get_y() - part[0].get_y()) * UP)

        self.play(FadeIn(integral1))
        self.wait()

        # Spell out meanings of each part
        area_part = integral1[R"C \cdot e^{-{y}^2}"]
        volume_part = integral1[R"C \cdot e^{-{y}^2} d{y}"]
        area_rect = SurroundingRectangle(area_part, buff=0.05)
        volume_rect = SurroundingRectangle(volume_part, buff=0.05)
        rects = VGroup(area_rect, volume_rect)
        rects.set_stroke(TEAL, 1)
        rects.set_fill(TEAL, 0.25)

        area_word = Text("Area of a slice")
        volume_word = Text("Volume of a slice")
        words = VGroup(area_word, volume_word)
        arrows = VGroup()
        for word, rect in zip(words, rects):
            word.next_to(rect, DOWN, LARGE_BUFF, LEFT)
            arrows.add(Arrow(rect, word))

        self.add(area_rect, integral1)
        self.play(
            FadeIn(area_rect),
            GrowArrow(arrows[0]),
            FadeIn(area_word)
        )
        self.wait()
        self.play(
            Transform(*rects),
            Transform(*arrows),
            TransformMatchingStrings(area_word, volume_word, run_time=1),
        )
        self.wait()
        self.play(*map(FadeOut, [area_rect, arrows[0], volume_word]))
        self.wait()

        # Show meaning of C
        sub_int = Tex(R"C = \int_{-\infty}^\infty e^{-{x}^2} d{x}", **kw)
        sub_int.next_to(top_eq, DOWN, LARGE_BUFF, aligned_edge=LEFT)
        box = SurroundingRectangle(sub_int)
        box.set_stroke(RED, 2)

        arrow = Arrow(integral1["C"], box, stroke_color=RED)

        for mob in box, sub_int:
            mob.save_state()
            mob.replace(integral1["C"], stretch=True)
            mob.set_opacity(0)

        self.play(
            ShowCreation(arrow),
            Restore(box),
            Restore(sub_int),
        )
        self.wait()
        self.play(TransformMatchingTex(integral1.copy(), integral2, path_arc=30 * DEGREES))
        self.wait()

        # Expand
        box2 = SurroundingRectangle(integral2[2:], buff=SMALL_BUFF)
        box2.set_stroke(RED, 1)
        self.play(TransformFromCopy(box, box2))
        self.wait()
        self.play(
            FadeOut(box2),
            Write(rhs)
        )
        self.wait()

        # Emphasize C^2
        C2 = rhs["C^2"]
        everything = VGroup(integral1, integral2, sub_int)
        self.play(C2.animate.scale(2, about_point=C2.get_left() + 0.1 * LEFT))
        self.play(
            FlashAround(C2, time_width=1.5, run_time=3),
            everything.animate.set_opacity(0.7),
        )
        self.wait()
