# ==============================================================================
# Scene:      IntroduceFormula
# Source:     videos/_2019/bayes/part1.py (lines 447-526)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceFormula.py IntroduceFormula -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Identify the probabilities of get_bayes_formula by LaTeX parts, avoiding Cairo's glyph indices.
#   - Animate the groups prior, likelihood and p_evidence in IntroduceFormula; the original indices exceeded the size of OldTex.
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


class IntroduceFormula(Scene):
    def construct(self):
        # CHANGE: animate the semantic groups instead of the Cairo indices.
        formula = get_bayes_formula()
        formula.save_state()
        formula.set_width(FRAME_WIDTH - 1)

        def get_formula_slice(*indices):
            return VGroup(*[formula[i] for i in indices])

        H_label = formula.get_part_by_tex("{H}")
        E_label = formula.get_part_by_tex("{E}")

        hyp_label = OldTexText("Hypothesis")
        hyp_label.set_color(HYPOTHESIS_COLOR)
        hyp_label.next_to(H_label, UP, LARGE_BUFF)

        evid_label = OldTexText("Evidence")
        evid_label.set_color(EVIDENCE_COLOR1)
        evid_label.next_to(E_label, DOWN, LARGE_BUFF)

        hyp_arrow = Arrow(hyp_label.get_bottom(), H_label.get_top(), buff=SMALL_BUFF)
        evid_arrow = Arrow(evid_label.get_top(), E_label.get_bottom(), buff=SMALL_BUFF)

        self.add(formula[:6])
        # self.add(get_submobject_index_labels(formula))
        # return
        self.play(
            FadeIn(hyp_label, DOWN),
            GrowArrow(hyp_arrow),
            FadeIn(evid_label, UP),
            GrowArrow(evid_arrow),
        )
        self.wait()

        # Prior
        self.play(
            ShowCreation(formula.get_part_by_tex("=")),
            TransformFromCopy(
                get_formula_slice(0, 1, 2, 5),
                formula.prior,
            ),
        )

        # Likelihood
        lhs_copy = formula[:6].copy()
        likelihood = formula.likelihood
        run_time = 1
        self.play(
            lhs_copy.next_to, likelihood, UP,
            run_time=run_time,
        )
        self.play(
            Swap(lhs_copy[2], lhs_copy[4]),
            run_time=run_time,
        )
        self.play(
            lhs_copy.move_to, likelihood,
            run_time=run_time,
        )

        # Evidence
        self.play(
            ShowCreation(formula.get_part_by_tex("\\over")),
            TransformFromCopy(
                get_formula_slice(0, 1, 4, 5),
                formula.p_evidence,
            ),
        )
        self.wait()

        self.clear()
        self.play(
            formula.restore,
            formula.scale, 1.5,
            formula.to_edge, UP,
            FadeOut(VGroup(
                hyp_arrow, hyp_label,
                evid_arrow, evid_label,
            ))
        )
