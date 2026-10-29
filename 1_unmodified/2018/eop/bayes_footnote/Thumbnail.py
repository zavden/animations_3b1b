# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2018/eop/bayes_footnote.py (lines 1486-1504)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/eop/bayes.py
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2018/eop/bayes.py -----

class Thumbnail(SampleSpaceScene):
    def construct(self):
        title = OldTexText("Bayes' rule")
        title.scale(2)
        title.to_edge(UP)
        self.add(title)

        prior_label = OldTex("P(", "H", ")")
        post_label = OldTex("P(", "H", "|", "D", ")")
        for label in prior_label, post_label:
            label.set_color_by_tex("H", YELLOW)
            label.set_color_by_tex("D", GREEN)
            label.scale(1.5)

        sample_space = self.get_sample_space()
        sample_space.set_height(4.5)
        sample_space.divide_horizontally(0.3)
        sample_space[0].divide_vertically(0.8, colors = [GREEN, BLUE])
        sample_space[1].divide_vertically(0.3, colors = [GREEN_E, BLUE_E])
        sample_space.get_side_braces_and_labels([prior_label])
        sample_space.add_braces_and_labels()
        post_rects = self.get_posterior_rectangles()
        group = self.get_posterior_rectangle_braces_and_labels(
            post_rects, [post_label]
        )
        post_rects.add(group)

        VGroup(sample_space, post_rects).next_to(title, DOWN, LARGE_BUFF)
        self.add(sample_space, post_rects)



# ----- From _2018/eop/bayes_footnote.py -----

SICKLY_GREEN = "#9BBD37"


class Thumbnail(Scene):
    def construct(self):
        title = OldTexText("Why is this \\\\ counterintuitive?")
        title.scale(2)
        title.to_edge(UP)

        randy = Randolph(mode = "sick",  color = SICKLY_GREEN)
        # randy.look_at(title)
        randy.scale(1.5)
        randy.shift(3*LEFT)
        randy.to_edge(DOWN)

        prob = OldTex("P(", "\\text{Sick}", "|", "\\text{Test+}", ")")
        prob.scale(2)
        prob.set_color_by_tex("Sick", YELLOW)
        prob.set_color_by_tex("Test", GREEN)
        prob.next_to(randy, RIGHT)

        self.add(title, randy, prob)
