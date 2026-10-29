# ==============================================================================
# Scene:      FinalWordsOnRule
# Source:     videos/_2018/eop/bayes.py (lines 2070-2153)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FinalWordsOnRule.py FinalWordsOnRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FinalWordsOnRule(SampleSpaceScene):
    def construct(self):
        self.add_sample_space()
        self.add_uses()
        self.tweak_values()

    def add_sample_space(self):
        sample_space = self.sample_space = SampleSpace()
        prior = 0.2
        top_conditional = 0.8
        bottom_condional = 0.3
        sample_space.divide_horizontally(prior)
        sample_space[0].divide_vertically(
            top_conditional, colors = [GREEN, RED]
        )
        sample_space[1].divide_vertically(
            bottom_condional, colors = [GREEN_E, RED_E]
        )
        B = "\\text{Belief}"
        D = "\\text{Data}"
        P_B = OldTex("P(", B, ")")
        P_D_given_B = OldTex("P(", D, "|", B, ")")
        P_D_given_not_B = OldTex(
            "P(", D, "|", "\\text{not }", B, ")"
        )
        P_B_given_D = OldTex("P(", B, "|", D, ")")
        labels = VGroup(P_B, P_D_given_B, P_D_given_not_B, P_B_given_D)
        for label in labels:
            label.scale(0.7)
            label.set_color_by_tex(B, BLUE)
            label.set_color_by_tex(D, GREEN)

        prior_rects = self.get_prior_rectangles()
        post_rects = self.get_posterior_rectangles()
        for i in range(2):
            sample_space[i][1].fade(0.7)

        braces = VGroup()
        bs, ls = sample_space.get_side_braces_and_labels([P_B])
        braces.add(*bs)
        bs, ls = sample_space[0].get_top_braces_and_labels([P_D_given_B])
        braces.add(*bs)
        bs, ls = sample_space[1].get_bottom_braces_and_labels([P_D_given_not_B])
        braces.add(*bs)
        bs, ls = self.get_posterior_rectangle_braces_and_labels(
            post_rects, [P_B_given_D]
        )
        braces.add(*bs)

        group = VGroup(sample_space, braces, labels, post_rects)
        group.to_corner(DOWN + LEFT)
        self.add(group)

        self.post_rects = post_rects

    def add_uses(self):
        uses = OldTexText(
            "Machine learning, ", 
            "scientific inference, $\\dots$",
        )
        uses.to_edge(UP)
        for use in uses:
            self.play(Write(use, run_time = 2))
        self.wait()

    def tweak_values(self):
        post_rects = self.post_rects
        new_value_lists = [
            (0.85, 0.1, 0.11),
            (0.3, 0.9, 0.4),
            (0.97, 0.3, 1./22),
        ]
        for new_values in new_value_lists:
            for i, value in zip(list(range(2)), new_values):
                self.play(*self.get_conditional_change_anims(
                    i, value, post_rects
                ))
                self.wait()
            self.play(*it.chain(
                self.get_horizontal_division_change_animations(new_values[-1]),
                self.get_posterior_rectangle_change_anims(post_rects)
            ))
            self.wait()
        self.wait(2)
