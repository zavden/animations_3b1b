# ==============================================================================
# Scene:      GrahamsConstantAlt
# Source:     videos/_2020/chess.py (lines 2939-2989)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GrahamsConstantAlt.py GrahamsConstantAlt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GrahamsConstantAlt(Scene):
    def construct(self):
        # lhs = OldTex("g_{64}", "=")
        # lhs[0][1:].scale(0.7, about_edge=DL)
        lhs = OldTex("")
        lhs.scale(2)

        rhs = VGroup()
        for ndots in [1, 3, 6, 7, 9, 12]:
            row = VGroup(*[
                OldTex("2"),
                OldTex("\\uparrow\\uparrow"),
                VGroup(*[
                    OldTex("\\cdot") for x in range(ndots)
                ]).arrange(RIGHT, buff=0.2),
                OldTex("\\uparrow\\uparrow"),
                OldTex("3"),
            ])
            row.arrange(RIGHT, buff=MED_SMALL_BUFF)
            if ndots == 1:
                rc = row.get_center()
                row[:2].move_to(rc, RIGHT)
                row[2].set_opacity(0)
                row[3:].move_to(rc, LEFT)
            row.add(Brace(row[1:-1], DOWN, buff=SMALL_BUFF))
            rhs.add(row)
        rhs.replace_submobject(0, Integer(12))
        # rhs[0][-1].set_opacity(0)
        rhs.replace_submobject(3, OldTex("\\vdots"))
        rhs.arrange(UP)
        rhs.next_to(lhs, RIGHT)

        rbrace = Brace(rhs[1:], RIGHT)
        rbrace_tex = rbrace.get_text("7 times")

        equation = VGroup(lhs, rhs, rbrace, rbrace_tex)
        equation.center().to_edge(LEFT, buff=LARGE_BUFF)

        self.add(lhs, rhs[0])
        self.play(TransformFromCopy(rhs[0], rhs[1]),)
        self.play(TransformFromCopy(rhs[1], rhs[2]))
        self.play(
            Write(rhs[3]),
            TransformFromCopy(rhs[2], rhs[4]),
        )
        self.play(
            TransformFromCopy(rhs[4], rhs[5]),
            GrowFromCenter(rbrace),
            Write(rbrace_tex)
        )
        self.wait()
