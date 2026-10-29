# ==============================================================================
# Scene:      TryUnitSquareVisual
# Source:     videos/_2018/eop/bayes_footnote.py (lines 452-530)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TryUnitSquareVisual.py TryUnitSquareVisual -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TryUnitSquareVisual(SampleSpaceScene):
    def construct(self):
        sample_space = self.get_sample_space()
        self.add_prior_division()
        self.add(sample_space)
        self.add_conditional_divisions()
        prior_label = sample_space.horizontal_parts.labels[0]
        final_labels = self.final_labels

        hard_to_see = OldTexText("Hard to see")
        hard_to_see.scale(0.7)
        hard_to_see.next_to(prior_label, UP)
        hard_to_see.to_edge(UP)
        hard_to_see.set_color(YELLOW)
        arrow = Arrow(hard_to_see, prior_label)

        self.wait()
        anims = self.get_division_change_animations(
            sample_space, sample_space.horizontal_parts,
            0.001, new_label_kwargs = {"labels" : final_labels}
        )
        self.play(*anims, run_time = 2)
        self.wait()
        self.play(
            Write(hard_to_see, run_time = 2),
            ShowCreation(arrow)
        )
        self.wait(2)

    def add_prior_division(self):
        sample_space = self.sample_space
        sample_space.divide_horizontally(0.1)
        initial_labels, final_labels = [
            VGroup(
                OldTex("P(\\text{Disease})", s1),
                OldTex("P(\\text{Not disease})", s2),
            ).scale(0.7)
            for s1, s2 in (("", ""), ("= 0.001", "= 0.999"))
        ]
        sample_space.get_side_braces_and_labels(initial_labels)
        sample_space.add_braces_and_labels()

        self.final_labels = final_labels

    def add_conditional_divisions(self):
        sample_space = self.sample_space
        top_part, bottom_part = sample_space.horizontal_parts

        top_brace = Brace(top_part, UP)
        top_label = OldTex(
            "P(", "+", "|", "\\text{Disease}", ")", "=", "1"
        )
        top_label.scale(0.7)
        top_label.next_to(top_brace, UP)
        top_label.set_color_by_tex("+", GREEN)

        self.play(GrowFromCenter(top_brace))
        self.play(FadeIn(top_label))
        self.wait()

        bottom_part.divide_vertically(
            0.95, colors = [BLUE_E, YELLOW_E]
        )
        bottom_label = OldTex(
            "P(", "+", "|", "\\text{Not disease}", ")", "=", "1"
        )
        bottom_label.scale(0.7)
        bottom_label.set_color_by_tex("+", GREEN)
        braces, labels = bottom_part.get_bottom_braces_and_labels(
            [bottom_label]
        )
        bottom_brace = braces[0]

        self.play(
            FadeIn(bottom_part.vertical_parts),
            GrowFromCenter(bottom_brace),
        )
        self.play(FadeIn(bottom_label))
        self.wait()
