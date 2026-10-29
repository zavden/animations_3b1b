# ==============================================================================
# Scene:      AbstractVectorSpace
# Source:     videos/_2021/some1.py (lines 942-1042)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AbstractVectorSpace.py AbstractVectorSpace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_h_line():
    line = DashedLine(ORIGIN, FRAME_WIDTH * RIGHT)
    line.center()
    return line


class AbstractVectorSpace(Scene):
    def construct(self):
        self.add(get_h_line())
        top_title = Text("Abstract vector space axioms")
        top_title.to_edge(UP, buff=MED_SMALL_BUFF)
        low_title = Text("Concrete vectors")
        low_title.next_to(ORIGIN, DOWN, buff=MED_SMALL_BUFF)
        self.add(top_title, low_title)

        # Vectors
        kw = {"bracket_h_buff": 0.1}
        columns = VGroup(
            Matrix([["1"], ["1"]], **kw).set_color(BLUE_B),
            OldTex("+"),
            Matrix([["-2"], ["3"]], **kw).set_color(BLUE_D),
            OldTex("="),
            Matrix([["1 - 2"], ["1 + 3"]], **kw).set_color(GREEN),
        )
        columns.arrange(RIGHT, buff=SMALL_BUFF)
        columns.next_to(low_title, DOWN, LARGE_BUFF)
        columns.to_edge(LEFT)

        arrows = VGroup(
            Arrow(ORIGIN, (1, 1), fill_color=BLUE_B, buff=0),
            Arrow((1, 1), (-1, 4), fill_color=BLUE_D, buff=0),
            Arrow(ORIGIN, (-1, 4), fill_color=GREEN, buff=0),
        )
        arrows.match_height(columns)
        arrows.scale(1.5)
        arrows.match_y(columns)
        arrows.match_x(low_title)

        funcs = OldTex(
            "(f + g)(x) = f(x) + g(x)",
            tex_to_color_map={"f": BLUE_B, "g": BLUE_D}
        )
        funcs.next_to(arrows, RIGHT, LARGE_BUFF)

        self.add(columns)
        self.add(arrows)
        self.add(funcs)

        # Axioms
        u_tex = "\\vec{\\textbf{u}}"
        w_tex = "\\vec{\\textbf{w}}"
        v_tex = "\\vec{\\textbf{v}}"
        axioms = VGroup(*it.starmap(Tex, [
            (
                "1. \\,",
                u_tex, "+", "(", v_tex, "+", w_tex, ")=(",
                u_tex, "+", v_tex, ")+", w_tex
            ),
            (
                "2. \\,",
                v_tex, "+", w_tex, "=", w_tex, "+", v_tex
            ),
            (
                "3. \\,",
                "\\textbf{0}+", v_tex,
                "=", v_tex, "\\text{ for all }", v_tex
            ),
            (
                "4. \\,",
                "\\forall", v_tex, "\\;\\exists", w_tex,
                "\\text{ s.t. }", v_tex, "+", w_tex, "=\\textbf{0}"
            ),
            (
                "5. \\,",
                "a", "(", "b", v_tex, ")=(", "a", "b", ")", v_tex
            ),
            (
                "6. \\,",
                "1", v_tex, "=", v_tex
            ),
            (
                "7. \\,",
                "a", "(", v_tex, "+", w_tex, ")", "=",
                "a", v_tex, "+", "a", w_tex
            ),
            (
                "8. \\,",
                "(", "a", "+", "b", ")", v_tex, "=",
                "a", v_tex, "+", "b", v_tex
            ),
        ]))
        for axiom in axioms:
            axiom.set_color_by_tex_to_color_map({
                u_tex: BLUE_B,
                w_tex: BLUE_D,
                v_tex: GREEN,
            })
        axioms[:4].arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        axioms[4:].arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        axioms[4:].next_to(axioms[:4], RIGHT, buff=1.5)
        axioms.set_height(2.5)
        axioms.next_to(top_title, DOWN)

        for axiom in axioms:
            self.play(FadeIn(axiom))

        self.add(axioms)
