# ==============================================================================
# Scene:      SpoilerAlert
# Source:     videos/_2019/bayes/part1.py (lines 1444-1476)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SpoilerAlert.py SpoilerAlert -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Identify the probabilities of get_bayes_formula by LaTeX parts, avoiding Cairo's glyph indices.
# ==============================================================================

from manim_imports_ext import *

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


class SpoilerAlert(Scene):
    def construct(self):
        sa_words = OldTexText("Spoiler Alert")
        sa_words.scale(2)
        sa_words.to_edge(UP)
        sa_words.set_color(RED)

        alert = Triangle(start_angle=90 * DEGREES)
        alert.set_stroke(RED, 8)
        alert.set_height(sa_words.get_height())
        alert.round_corners(0.1)
        bang = OldTexText("!")
        bang.set_color(RED)
        bang.scale(1.5)
        bang.move_to(alert)
        alert.add(bang)

        alert.next_to(sa_words, LEFT)
        sa_words.add(alert.copy())
        alert.next_to(sa_words, RIGHT)
        sa_words.add(alert)

        formula = get_bayes_formula()
        formula_words = OldTexText("This is secretly ")
        formula_words.scale(1.5)
        formula_group = VGroup(formula_words, formula)
        formula_group.arrange(DOWN, buff=MED_LARGE_BUFF)
        formula_group.next_to(sa_words, DOWN, LARGE_BUFF)

        self.add(sa_words)
        self.wait()
        self.play(FadeIn(formula_group, UP))
        self.wait()
