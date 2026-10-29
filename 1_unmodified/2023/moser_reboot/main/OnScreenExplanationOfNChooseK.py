# ==============================================================================
# Scene:      OnScreenExplanationOfNChooseK
# Source:     videos/_2023/moser_reboot/main.py (lines 1260-1286)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OnScreenExplanationOfNChooseK.py OnScreenExplanationOfNChooseK -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OnScreenExplanationOfNChooseK(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(
            tex_to_color_map={"{n}": BLUE, "{k}": TEAL},
            alignment=""
        )
        explanation = VGroup(
            TexText(R"""
            The claim is that if you look at the ${k}^\text{th}$ element of the
            ${n}^\text{th}$ row in Pascal's triangle, it equals ${n} \choose {k}$. To show this,
            it's enough to show that
                $$ {{n} \choose {k}} = {{n} - 1 \choose {k} - 1} + {{n} - 1 \choose {k}} $$
            Can you see why?
            """, **kw),
            TexText(R"""
                There's a nice counting argument which proves this equation. Imagine
                you have ${n}$ items, and you want to choose ${k}$ of them. On the one hand,
                by definition, there are ${n} \choose {k}$ ways to do this. But on the other
                hand, imagine marking one of the items as special. How many ways can you
                select ${k}$ unmarked items? How may ways can you select ${k}$ items where
                one of them is the marked one? What does this tell you?
            """, **kw)
        )
        explanation.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        explanation.set_width(FRAME_WIDTH - 1)
        self.add(explanation)
