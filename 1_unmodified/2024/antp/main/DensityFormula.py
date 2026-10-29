# ==============================================================================
# Scene:      DensityFormula
# Source:     videos/_2024/antp/main.py (lines 664-727)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DensityFormula.py DensityFormula -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DensityFormula(InteractiveScene):
    def construct(self):
        # Formula
        t2c = {
            "T": BLUE,
        }
        kw = dict(t2c=t2c, font_size=90)
        lhs = TexText("Prime density near $T$", **kw)
        approx = Tex(R"\approx", **kw)
        approx.rotate(PI / 2)
        rhs = Tex(R"1 / \ln(T)", **kw)
        group = VGroup(lhs, approx, rhs)
        group.arrange(DOWN, buff=0.5)
        group.to_edge(UP)

        example = TexText("(e.g. $T = 1{,}000{,}000$)", font_size=60, t2c=t2c)
        example.next_to(lhs, DOWN, LARGE_BUFF)
        arrow = Arrow(
            lhs["T"].get_bottom(),
            example.get_right(),
            stroke_width=8,
            stroke_color=BLUE,
            path_arc=-PI / 2,
            buff=0.2,
        )

        self.add(lhs, example, arrow)
        self.wait()

        self.remove(example, arrow)
        self.add(approx, rhs)

    def old_mess(self):
        # Formula
        kw = dict(t2c={
            "T": BLUE,
            "1{,}000{,}000": BLUE,
        })
        lhs = TexText("What's the density of primes near $T$", **kw)
        rhs = Tex(R"\approx \frac{1}{\ln(T)}", **kw)
        group = VGroup(lhs, rhs)
        group.arrange(RIGHT)
        group.to_edge(UP)

        q_mark = Text("?")
        q_mark.next_to(lhs, RIGHT, buff=0.1)
        q_mark.align_to(lhs[0], DOWN)
        lhs_note = TexText(
            "(Some big number, e.g. $T = 1{,}000{,}000$)",
            font_size=36,
            **kw
        )
        lhs_note.next_to(lhs, DR, buff=LARGE_BUFF)
        lhs_note.shift_onto_screen()
        arrow = Arrow(lhs_note.get_top(), lhs["T"], buff=0.1)
        arrow.set_color(BLUE)

        self.add(lhs)
        self.add(q_mark, lhs_note, arrow)
        self.wait()

        self.remove(q_mark, lhs_note, arrow)
        self.remove(lhs["What's the"])
        self.add(rhs)
