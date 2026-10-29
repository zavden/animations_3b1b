# ==============================================================================
# Scene:      CompareThreeIntegrals
# Source:     videos/_2023/gauss_int/supplements.py (lines 598-672)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareThreeIntegrals.py CompareThreeIntegrals -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CompareThreeIntegrals(InteractiveScene):
    def construct(self):
        # Frames
        self.add(FullScreenRectangle().set_fill(GREY_E, 0.5))
        buff = MED_LARGE_BUFF
        rects = Rectangle(height=5.0, width=(FRAME_WIDTH - 4 * buff) / 3).replicate(3)
        rects.arrange(RIGHT, buff=buff)
        rects.to_edge(DOWN, buff=1.0)
        rects.set_fill(BLACK, 1)
        rects.set_stroke(TEAL, 1)

        # Titles
        kw = dict(
            font_size=48,
            t2c={"C": PINK, "{x}": BLUE, "{y}": YELLOW, "{r}": RED}
        )
        titles = VGroup(
            TexText("Area = $C$", **kw),
            TexText("Volume = $C^2$", **kw),
            TexText(R"Volume = $\pi$", **kw),
        )
        titles[2][R"\pi"].scale(1.5, about_edge=DL)
        integrals = VGroup(
            Tex(R"\int_{-\infty}^\infty e^{-{x}^2}\,d{x} = C", **kw),
            Tex(R"\int_{-\infty}^\infty \int_{-\infty}^\infty e^{-{y}^2} e^{-{x}^2}\,d{x}\,d{y} = C^2", **kw),
            Tex(R"\int_0^\infty 2\pi r \cdot e^{-{r}^2} \,d{r} = \pi", **kw),
        )
        integrals.scale(0.5)

        for title, integral, rect in zip(titles, integrals, rects):
            title.next_to(rect, UP, buff=MED_LARGE_BUFF)
            integral.next_to(rect.get_top(), DOWN)

        # Show first two
        self.add(*rects[:2])
        self.wait()

        for title, integral in zip(titles[:2], integrals[:2]):
            self.play(
                FadeIn(title, 0.5 * UP),
                FadeIn(integral, 0.5 * DOWN)
            )
        self.wait(2)

        # Show third
        self.play(
            FadeIn(rects[2]),
            FadeIn(titles[2], 0.5 * UP),
            FadeIn(integrals[2], 0.5 * DOWN)
        )
        self.wait()

        # Equations
        eq_pi = titles[2][R"= $\pi$"][0].copy()
        eq_pi.generate_target()
        eq_sqrt_pi = Tex(R"= \sqrt{\pi}", **kw)
        for title, rhs in zip(titles[:2], (eq_sqrt_pi, eq_pi.target)):
            title.generate_target()
            rhs.next_to(title, RIGHT)
            rhs.shift((title["="].get_y() - rhs[0].get_y()) * UP)
            VGroup(title.target, rhs).match_x(title)

        self.play(LaggedStart(
            MoveToTarget(eq_pi),
            MoveToTarget(titles[1]),
            lag_ratio=0.35,
        ))
        self.play(LaggedStart(
            TransformMatchingShapes(eq_pi.copy(), eq_sqrt_pi, run_time=1),
            MoveToTarget(titles[0]),
            lag_ratio=0.35,
        ))
        self.wait()
        self.play(FlashAround(eq_sqrt_pi[1:], run_time=2, time_width=1))
        self.wait()
