# ==============================================================================
# Scene:      FinalExercise
# Source:     videos/_2023/gauss_int/supplements.py (lines 1238-1333)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FinalExercise.py FinalExercise -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FinalExercise(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(
            t2c={
                "I_n": YELLOW,
                "I_1": YELLOW,
                "I_2": YELLOW,
                "I_{n - 2}": YELLOW,
                "C_2": TEAL,
                "C_3": TEAL,
                "C_4": TEAL,
                "C_5": TEAL,
                "C_6": TEAL,
                "C_n": TEAL,
                "C_{n - 2}": TEAL,
                "{r}": BLUE,
            },
            font_size=30,
            alignment=""
        )
        parts = VGroup(
            TexText(R"""
                \textbf{Part 1} \\

                Define $I_n$ to be the integral below. For example, we showed in this \\
                video that $I_1 = \sqrt{\pi}$ and $I_2 = \pi$.
                $$
                I_n =
                \underbrace{\int_{-\infty}^\infty \cdots \int_{-\infty}^\infty}_{n \text{ times}}
                e^{-(x_1^2 + \cdots + x_n^2)} dx_1 \cdots dx_n
                $$
                Explain why $I_n = \pi^{n / 2}$. Specifically, factor the expression then integrate \\
                along each of the $n$ coordinate axes.
            """, **kw),
            TexText(R"""
                \textbf{Part 2} \\

                We all learn that the circumference of a circle is $2\pi {r}$, and the surface area \\
                of a sphere is $4\pi {r}^2$. In general, the boundary of an $n$-dimensional ball has \\
                an $(n-1)$-dimensional volume of $C_n {r}^{n - 1}$ for some constant $C_n$. For\\
                example, $C_2 = 2\pi$ and $C_3 = 4 \pi$. Our goal is to figure out this value $C_n$ \\
                for each dimension $n$.\\

                Explain why the integral from the previous problem can also be \\
                interpreted as
                $$
                I_n = \int_0^\infty C_n {r}^{n - 1} e^{-{r}^2} dr
                $$
            """, **kw),
            TexText(R"""
                \textbf{Part 3} \\

                Using integration by parts, show that
                \begin{align*}
                I_n = \int_0^\infty C_n {r}^{n - 1} e^{-{r}^2} dr 
                &=\frac{n - 2}{2} C_n \int_0^\infty {r}^{n - 3} e^{-{r}^2} dr \\
                &= \frac{n - 2}{2} C_n \cdot { I_{n - 2} \over C_{n - 2}}
                \end{align*}
                \quad \\
                (Hint, let $u = {r}^{n - 2}$ and $dv = {r} e^{-{r}^2} dr$)
            """, **kw),
            TexText(R"""
                \textbf{Part 4} \\

                Combine parts 1 and 3 to deduce $C_n = \frac{2\pi}{n - 2} C_{n - 2}$ for $n > 2$. Use this \\
                to write the values of $C_3$, $C_4$, $C_5$, and as many more as you'd like. \\

                Considering the recurrence relation above, together with the assumption \\
                that $(-1/2)! = \sqrt{\pi}$ (a story for another day), can you explain why \\
                the formula below for the $(n-1)$-dimensional boundary of a $n$-dimensional \\
                ball makes sense? \\
                $$ n {\pi^{n/2} \over (n/2)!} {r}^{n - 1}$$
            """, **kw),
        )

        rects = ScreenRectangle().get_grid(2, 2, buff=0)
        rects.set_height(7)
        rects.set_width(FRAME_WIDTH, stretch=True)
        rects.to_edge(DOWN, buff=0)
        rects.set_stroke(WHITE, 2)
        self.add(rects)

        title = Text("Challenge for the ambitious viewer", font_size=60)
        title.set_color(RED)
        title.to_edge(UP, MED_SMALL_BUFF)
        self.add(title)

        parts.scale(0.7)
        for part, rect in zip(parts, rects):
            part.move_to(rect, UL).shift(DR * SMALL_BUFF)

        self.add(parts)

        self.play(LaggedStartMap(FadeIn, parts, lag_ratio=0.7))
        self.wait()
