# ==============================================================================
# Scene:      DiseaseBayes
# Source:     videos/_2019/bayes/footnote.py (lines 1012-1118)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DiseaseBayes.py DiseaseBayes -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Adjust the prior, likelihood and evidence groups in DiseaseBayes to the actual structure of OldTex.
#   - Replace the letters with characters using replace_submobject so that GL updates the family and the characters move with the formula.
#   - Identify posterior, prior, likelihood and evidence by their LaTeX parts, avoiding indices shifted by the empty parts of legacy OldTex.
#   - Exclude the empty fragments of legacy OldTex from the probabilities to keep the six symbols that Swap uses and to extract P(+) correctly.
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


class DiseaseBayes(Scene):
    def construct(self):
        formula = OldTex(
            "P(D | +) = {P(D) P(+ | D) \\over P(+)}",
            tex_to_color_map={
                "D": YELLOW,
                "+": BLUE,
            },
            isolate=list("P(|)=")
        )
        formula.scale(2.5)

        Ds = formula.get_parts_by_tex("D")
        for D in Ds:
            index = formula.index_of_part(D)
            pi = Randolph()
            pi.change("sick")
            pi.set_color(SICKLY_GREEN)
            pi.replace(D)
            # CHANGE: refresh GL's family so the replacement follows its formula group.
            formula.replace_submobject(index, pi)
            pi.get_tex = lambda: ""

        # CHANGE: locate whole probabilities instead of assuming Cairo glyph offsets.
        starts = [index for index, part in enumerate(formula) if part.get_tex().strip() == "P"]

        def probability(index):
            start = starts[index]
            end = start + 1
            while end < len(formula) and ")" not in formula[end].get_tex():
                end += 1
            # CHANGE: exclude empty legacy fragments from the symbol indices below.
            return VGroup(*[
                part for part in formula[start:end + 1]
                if part.family_members_with_points()
            ])

        lhs = probability(0)
        prior = probability(1)
        likelihood_part = probability(2)
        evidence = probability(3)
        lhs.save_state()
        lhs.center()

        sicky = lhs[2]

        sick_words = OldTexText(
            "You are sick",
            tex_to_color_map={
                "sick": SICKLY_GREEN,
            },
        )
        sick_words.scale(1.5)
        sick_words.next_to(sicky, UP, 2 * LARGE_BUFF)
        positive_words = OldTexText("Positive test result")
        positive_words.scale(1.5)
        positive_words.set_color(BLUE)
        positive_words.next_to(lhs[4], DOWN, 2 * LARGE_BUFF)

        sick_arrow = Arrow(sicky.get_top(), sick_words.get_bottom())
        positive_arrow = Arrow(lhs[4].get_bottom(), positive_words.get_top())

        arrow_groups = VGroup(
            sick_words, sick_arrow,
            positive_words, positive_arrow,
        )

        sicky.save_state()
        sicky.change("happy")
        sicky.set_color(BLUE)

        self.play(FadeInFromDown(lhs))
        self.play(
            Restore(sicky),
            GrowArrow(sick_arrow),
            FadeInFromDown(sick_words),
        )
        self.play(
            GrowArrow(positive_arrow),
            FadeIn(positive_words, UP),
        )
        self.wait(2)
        self.play(
            Restore(lhs),
            MaintainPositionRelativeTo(arrow_groups, lhs),
            FadeIn(formula.get_part_by_tex("=")),
        )

        # Prior
        def get_formula_slice(*indices):
            return VGroup(*[formula[i] for i in indices])

        self.play(
            TransformFromCopy(
                VGroup(lhs[0], lhs[1], lhs[2], lhs[-1]),
                prior,
            ),
        )

        # Likelihood
        lhs_copy = lhs.copy()
        likelihood = likelihood_part
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
                VGroup(likelihood_part[0], likelihood_part[1], likelihood_part[2], likelihood_part[5]),
                evidence,
            ),
        )
        self.wait()
