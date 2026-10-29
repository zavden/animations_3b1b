# ==============================================================================
# Scene:      TypicalComputation
# Source:     videos/_2021/quick_eigen.py (lines 486-683)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TypicalComputation.py TypicalComputation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
# ==============================================================================

from manim_imports_ext import *

class TypicalComputation(Scene):
    def construct(self):
        # Task
        words, mat = task = VGroup(
            Text("Find the eigenvalues of ", t2c={"eigenvalues": TEAL}),
            IntegerMatrix([[3, 1], [4, 1]]).set_height(1),
        )
        task.arrange(RIGHT, buff=MED_LARGE_BUFF)
        task.to_edge(UP)
        self.add(task)

        # Top line of the computation
        det_expression = OldTex("""
            \\text{det}\\left( \\left[ \\begin{array}{cc}
                3 - \\lambda & 1 \\\\
                4 & 1 - \\lambda
            \\end{array} \\right] \\right)
        """)[0]
        lambdas = VGroup(det_expression[7], det_expression[12])
        lambdas.set_color(TEAL)
        t0, t1, t2, t3 = terms = VGroup(
            det_expression[5:8],
            det_expression[8:9],
            det_expression[9:10],
            det_expression[10:13],
        ).copy()
        p_height = terms[0].get_height() * 1.5
        for term in terms:
            parens = OldTex("(", ")")
            parens.set_height(p_height)
            parens[0].next_to(term, LEFT, 0.5 * SMALL_BUFF)
            parens[1].next_to(term, RIGHT, 0.5 * SMALL_BUFF)
            term.parens = parens
            term.parens.set_opacity(0)
            term.add(term.parens)

        eq = OldTex("=")
        eq.next_to(det_expression, RIGHT)
        rhs = VGroup(
            t0.copy(), t3.copy(), OldTex("-"), t1.copy(), t2.copy()
        )
        rhs.arrange(RIGHT)
        rhs.next_to(eq, RIGHT)
        rhs.set_opacity(1)
        VGroup(det_expression, terms, eq, rhs).next_to(task, DOWN, LARGE_BUFF)

        movers = VGroup(det_expression[5], det_expression[10])
        movers.save_state()
        movers[0].move_to(det_expression[6])
        movers[1].move_to(det_expression[11])

        self.play(
            TransformFromCopy(mat.get_brackets(), VGroup(*(det_expression[i] for i in [4, 13]))),
            TransformFromCopy(mat.get_entries(), VGroup(*(det_expression[i] for i in [5, 8, 9, 10]))),
            FadeTransform(
                mat.get_brackets().copy().set_opacity(0),
                VGroup(*(det_expression[i] for i in [0, 1, 2, 3, 14]))
            ),
            run_time=1
        )
        self.play(
            Write(VGroup(*(det_expression[i] for i in [6, 7, 11, 12]))),
            Restore(movers),
        )
        self.wait()
        self.add(det_expression)

        self.play(
            FadeIn(eq),
            TransformFromCopy(VGroup(t0, t3), rhs[:2]),
        )
        self.play(
            FadeIn(rhs[2]),
            TransformFromCopy(VGroup(t1, t2), rhs[3:])
        )
        self.wait()

        # Line 2
        eq2 = eq.copy()
        eq2.shift(DOWN)
        self.add(eq2)
        rhs2 = OldTex("\\left( 3 - 4\\lambda + \\lambda^2 \\right) - 4")[0]
        rhs2.next_to(eq2, RIGHT)
        VGroup(rhs2[4], rhs2[6]).set_color(TEAL)

        top_terms = VGroup(
            VGroup(rhs[0][0], rhs[0][2]),
            VGroup(rhs[1][0], rhs[1][2]),
        )
        alt_mid = OldTex("-3\\lambda", tex_to_color_map={"\\lambda": TEAL})
        alt_mid.move_to(rhs2[2:5], DL)
        bottom_terms = VGroup(rhs2[1], alt_mid, rhs2[2:5], rhs2[5:8])
        for pair, bt in zip(it.product(*top_terms), bottom_terms):
            rects = VGroup(*(SurroundingRectangle(t, buff=SMALL_BUFF) for t in pair))
            self.add(rects)
            self.add(bt)
            self.wait(0.5)
            if bt is alt_mid:
                self.remove(bt)
            self.remove(rects)
        self.play(
            FadeIn(VGroup(rhs2[0], rhs2[8])),
            FadeTransform(rhs[2:].copy(), rhs2[9:])
        )
        self.wait()

        # Line 3
        eq3 = eq2.copy().shift(DOWN)
        rhs3 = OldTex("\\lambda^2 - 4 \\lambda - 1")[0]
        rhs3.next_to(eq3, RIGHT)
        VGroup(rhs3[0], rhs3[4]).set_color(TEAL)

        kw = {"path_arc": 45 * DEGREES}
        self.play(LaggedStart(
            TransformFromCopy(eq2, eq3, **kw),
            Transform(rhs2[1].copy(), rhs3[6].copy(), remover=True, **kw),
            TransformFromCopy(rhs2[9:11], rhs3[5:], **kw),
            TransformFromCopy(rhs2[2:5], rhs3[2:5], **kw),
            TransformFromCopy(rhs2[6:8], rhs3[0:2], **kw),
            run_time=1.5, lag_ratio=0.02,
        ))
        self.wait()

        # Characteristic polynomial
        brace = Brace(rhs3, DOWN)
        char_poly = VGroup(
            Text("Characteristic polynomial of", font_size=30, fill_color=BLUE),
            mat.copy()
        )
        char_poly.arrange(RIGHT)
        char_poly.next_to(brace, DOWN)
        char_poly.shift_onto_screen()

        self.play(
            GrowFromCenter(brace),
            FadeIn(char_poly, DOWN),
        )
        self.wait()

        # Roots
        equals_zero = OldTex("= 0")
        equals_zero.next_to(rhs3, RIGHT)
        root_words = OldTex(
            "\\lambda_1, \\lambda_2 \\,=\\, \\text{roots}",
            tex_to_color_map={
                "\\lambda_1": TEAL_C,
                "\\lambda_2": TEAL_B,
                "=": WHITE,
            }
        )
        new_rhs3 = VGroup(rhs3, equals_zero)
        root_words.next_to(brace, DOWN)
        root_words.match_x(new_rhs3)
        self.play(
            FadeIn(root_words, DOWN),
            FadeOut(char_poly, DOWN),
            brace.animate.become(Brace(new_rhs3)),
            Write(equals_zero),
        )
        self.wait()

        # Quadratic formula
        formula = OldTex("\\frac{4 \\pm \\sqrt{4^2 - 4(1)(-1)}}{2}")
        formula2 = OldTex("=\\frac{4 \\pm \\sqrt{20}}{2}")
        formula3 = OldTex("= 2 \\pm \\sqrt{5}")
        formula.move_to(root_words[-1], LEFT)
        formula.shift(0.5 * DL)

        self.play(
            TransformMatchingShapes(rhs3.copy(), formula),
            FadeOut(root_words[-1]),
            root_words[:-1].animate.shift(0.5 * DL),
        )
        self.wait()
        solution = VGroup(root_words[:-1], formula)
        self.play(
            solution.animate.shift(formula2.get_width() * LEFT),
        )
        formula2.next_to(formula, RIGHT)
        self.play(FadeIn(formula2))
        self.wait()
        solution.add(formula2)
        self.play(
            solution.animate.shift(formula3.get_width() * LEFT),
        )
        formula3.next_to(formula2, RIGHT)
        self.play(FadeIn(formula3))
        self.wait()

        # Straight line
        full_rect = FullScreenFadeRectangle()
        # CHANGE: Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
        arrow = FillArrow(mat, formula3, thickness=0.05)
        arrow.set_fill(YELLOW)

        self.add(full_rect, task, formula3)
        self.play(FadeIn(full_rect))
        self.play(GrowArrow(arrow))
        self.wait()
