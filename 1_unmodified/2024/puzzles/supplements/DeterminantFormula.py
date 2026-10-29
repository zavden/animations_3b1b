# ==============================================================================
# Scene:      DeterminantFormula
# Source:     videos/_2024/puzzles/supplements.py (lines 467-518)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DeterminantFormula.py DeterminantFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DeterminantFormula(InteractiveScene):
    def construct(self):
        # Test
        det_expr = Tex(R"""
            \text{det}\left(\left[
            \begin{array}{ccc}
            a & b & c \\
            d & e & f \\
            g & h & i \\
            \end{array}
            \right]\right)
        """)
        det_expr.scale(1.25)
        det_expr.next_to(ORIGIN, LEFT).set_y(2)
        cols = VGroup(det_expr[k:16:3] for k in range(7, 10))
        col_syms = ["adg", "beh", "cfi"]

        equals = Tex(R"=", font_size=60)
        equals.next_to(det_expr, RIGHT)

        n = 3
        rhs_terms = VGroup()
        perms = list(it.permutations(range(n)))
        for perm in perms:
            parity = sum(int(j < i) for (i, j) in it.combinations(perm, 2))
            sgn = "+" if (parity % 2 == 0) else "-"
            term = Tex(sgn + "".join([col_syms[i][j] for i, j in enumerate(perm)]))
            rhs_terms.add(term)

        rhs_terms.scale(1.25)
        rhs_terms.arrange(DOWN)
        rhs_terms.next_to(equals, RIGHT, aligned_edge=UP)
        rhs_terms.shift(0.2 * UP)

        self.add(det_expr)
        self.add(equals)
        last_highlight = VGroup()
        for perm, term, sgn in zip(perms, rhs_terms, it.cycle([1, -1])):
            highlight = VGroup(cols[i][j] for i, j in enumerate(perm)).copy()
            highlight.set_fill(BLUE if sgn > 0 else RED, 1, border_width=2)
            self.play(
                FadeIn(highlight),
                FadeOut(last_highlight),
                cols.animate.set_opacity(0.5)
            )
            self.play(
                FadeIn(term[0]),
                TransformFromCopy(highlight, term[1:]),
            )

            last_highlight = highlight
        self.play(FadeOut(last_highlight), cols.animate.set_opacity(1))
