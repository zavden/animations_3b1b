# ==============================================================================
# Scene:      LandscapeOfTools
# Source:     videos/_2019/bayes/footnote.py (lines 562-672)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/bayes/part1.py
#
# Run from this folder:
#     manimgl LandscapeOfTools.py LandscapeOfTools -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Identify the probabilities of get_bayes_formula by LaTeX parts, avoiding Cairo's glyph indices.
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/bayes/part1.py -----

HYPOTHESIS_COLOR = YELLOW


NOT_HYPOTHESIS_COLOR = GREY


EVIDENCE_COLOR1 = BLUE_C


def get_bayes_formula(expand_denominator=False):
    t2c = {
        "{H}": HYPOTHESIS_COLOR,
        "{\\neg H}": NOT_HYPOTHESIS_COLOR,
        "{E}": EVIDENCE_COLOR1,
    }
    isolate = ["P", "\\over", "=", "\\cdot", "+"]

    tex = "P({H} | {E}) = {P({H}) P({E} | {H}) \\over "
    if expand_denominator:
        tex += "P({H}) P({E} | {H}) + P({\\neg H}) \\cdot P({E} | {\\neg H})}"
    else:
        tex += "P({E})}"

    formula = OldTex(
        tex,
        tex_to_color_map=t2c,
        isolate=isolate,
    )

    # CHANGE: identify the probabilities by their LaTeX parts, without Cairo glyph indices that do
    # not match the OldTex groups of GL.
    starts = [i for i, part in enumerate(formula) if part.get_tex().strip() == "P"]

    def probability(index):
        start = starts[index]
        end = start + 1
        while end < len(formula) and ")" not in formula[end].get_tex():
            end += 1
        return formula[start:end + 1]

    formula.posterior = probability(0)
    formula.prior = probability(1)
    formula.likelihood = probability(2)
    if expand_denominator:
        formula.denom_prior = probability(3)
        formula.denom_likelihood = probability(4)
        formula.denom_anti_prior = probability(5)
        formula.denom_anti_likelihood = probability(6)
    else:
        formula.p_evidence = probability(3)

    return formula



# ----- From _2019/bayes/footnote.py -----

def get_bayes_formula():
    return OldTex(
        "P(A|B) = {P(A)P(B|A) \\over P(B)}",
        tex_to_color_map={
            "A": YELLOW,
            "B": BLUE,
        },
        isolate=list("P(|)")
    )


class LandscapeOfTools(TeacherStudentsScene):
    def construct(self):
        group = self.get_formulas()
        bayes = group[0].copy()

        self.play(
            self.teacher.change, "raise_right_hand",
            self.change_students(
                *3 * ["confused"],
                look_at=group,
            ),
            FadeInFromDown(bayes),
        )
        self.remove(bayes)
        self.play(
            ShowSubmobjectsOneByOne(group, remover=True),
            run_time=5
        )
        self.add(bayes)
        self.wait(2)

        bubble = self.students[0].get_bubble()
        self.add(bubble, bayes)
        self.play(
            bayes.move_to, bubble.get_bubble_center(),
            DrawBorderThenFill(bubble),
            self.teacher.change, "happy",
            self.change_students(
                "pondering", "erm", "erm",
                look_at=bubble,
            )
        )
        self.play_all_student_changes(
            "thinking", look_at=bayes,
        )
        self.wait()
        self.play(
            FadeOut(bayes),
            bubble.set_fill, BLACK, 0.2,
            bubble.set_stroke, WHITE, 1,
            self.change_students(
                "pleading", "guilty", "guilty",
            ),
            self.teacher.change, "hesitant"
        )
        self.wait(2)

    def get_formulas(self):
        group = VGroup(
            get_bayes_formula(),
            OldTex(
                "P(X = k) = {\\lambda^k \\over k!}", "e^{-\\lambda}",
                tex_to_color_map={
                    "k": YELLOW,
                    "\\lambda": GREEN,
                }
            ),
            OldTex(
                "{1 \\over \\sigma\\sqrt{2\\pi}}",
                "e^{\\frac{1}{2}\\left({(x - \\mu) \\over \\sigma}\\right)^2}",
                tex_to_color_map={
                    "\\sigma": GREEN,
                    "\\mu": BLUE,
                }
            ),
            OldTex(
                "P(X = k) =", "\\left({n \\over k}\\right)", "p^k(1-p)^{n-k}",
                tex_to_color_map={
                    "\\over": BLACK,
                    "p": WHITE,
                    "k": YELLOW,
                    "n": BLUE,
                    "k": GREEN
                }
            ),
            OldTex(
                "E[X + Y] = E[x] + E[y]"
            ),
            OldTex(
                "\\text{Var}(X + Y) = \\text{Var}(x) + \\text{Var}(y) + 2\\text{Cov}(X, Y)"
            ),
            OldTex(
                "H = \\sum_{i} -p_i \\log", "(p_i)",
                tex_to_color_map={
                    "p_i": YELLOW,
                }
            ),
            OldTex(
                "{n \\choose k}",
                "{B(k + \\alpha, n -k + \\beta) \\over B(\\alpha, \\beta)}",
                tex_to_color_map={
                    "\\alpha": BLUE,
                    "\\beta": YELLOW,
                }
            ),
            OldTex(
                "P(d) = \\log_{10}\\left(1 + {1 \\over d}\\right)",
                tex_to_color_map={"d": BLUE},
            ),
            OldTex(
                "\\text{Cov}(X, Y) = \\sum_{i, j} p({x}_i, {y}_j)({x}_i - \\mu_{x})({y}_j - \\mu_{y})",
                tex_to_color_map={
                    "{x}": BLUE,
                    "{y}": RED,
                }
            ),
        )

        group.move_to(self.hold_up_spot, DOWN)
        group.shift_onto_screen()
        return group
