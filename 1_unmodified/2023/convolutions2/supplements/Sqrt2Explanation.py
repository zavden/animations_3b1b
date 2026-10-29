# ==============================================================================
# Scene:      Sqrt2Explanation
# Source:     videos/_2023/convolutions2/supplements.py (lines 620-660)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Sqrt2Explanation.py Sqrt2Explanation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Sqrt2Explanation(InteractiveScene):
    def construct(self):
        # Test
        tex_kw = dict(font_size=30, alignment="")
        explanation = VGroup(
            TexText(R"""
                Think about what a Riemann sum approximating the area of \\
                the slice below would look like, where the slice is taken over \\
                the line $x + y = s$. If you have some samples of $x$, spaced \\
                apart by $\Delta x$, the sum of the areas of the rectangles \\
                below looks like\\

                $$
                \displaystyle \sum_{x \in \text{samples}}
                \overbrace{f(x) g(s - x)}^{\text{Rect. height}}
                \underbrace{\sqrt{2} \cdot \Delta x}_{\text{Rect. width}}
                $$\\
            """, **tex_kw),
            TexText(R"""
                This is \emph{almost} a Riemann approximation of the\\
                integral we care about \\

                $$\displaystyle [f * g](s) = \int_{-\infty}^\infty f(x)g(s - x)dx.$$\\

                The only difference is that factor of $\sqrt{2}$. That factor \\
                persists in the limit as $\Delta x \to 0$, so the area of the \\
                slice below is exactly $\sqrt{2} \cdot [f * g](s)$.\\
            """, **tex_kw),
        )
        explanation[0][196:].scale(1.25, about_edge=UP).match_x(explanation[0][:196])
        explanation[1][57:83].scale(1.25, about_edge=UP).match_x(explanation[1][:57])
        explanation.arrange(RIGHT, buff=LARGE_BUFF, aligned_edge=UP)
        explanation.set_width(FRAME_WIDTH - 1)
        h_line = Line(UP, DOWN).match_height(explanation)
        h_line.move_to(explanation)
        h_line.shift(0.5 * RIGHT)
        h_line.set_stroke(GREY_B, 1)
        explanation.add(h_line)
        explanation.to_edge(UP)

        self.add(explanation)
