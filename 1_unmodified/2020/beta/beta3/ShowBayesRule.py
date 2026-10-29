# ==============================================================================
# Scene:      ShowBayesRule
# Source:     videos/_2020/beta/beta3.py (lines 753-843)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl ShowBayesRule.py ShowBayesRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

CMARK_TEX = "\\text{\\ding{51}}"


XMARK_TEX = "\\text{\\ding{55}}"



# ----- From _2020/beta/beta3.py -----

class ShowBayesRule(Scene):
    def construct(self):
        hyp = "\\text{Hypothesis}"
        data = "\\text{Data}"
        bayes = OldTex(
            f"P({hyp} \\,|\\, {data})", "=", "{",
            f"P({data} \\,|\\, {hyp})", f"P({hyp})",
            "\\over", f"P({data})",
            tex_to_color_map={
                hyp: YELLOW,
                data: GREEN,
            }
        )

        title = OldTexText("Bayes' rule")
        title.scale(2)
        title.to_edge(UP)

        self.add(title)
        self.add(*bayes[:5])
        self.wait()
        self.play(
            *[
                TransformFromCopy(bayes[i], bayes[j], path_arc=30 * DEGREES)
                for i, j in [
                    (0, 7),
                    (1, 10),
                    (2, 9),
                    (3, 8),
                    (4, 11),
                ]
            ],
            FadeIn(bayes[5]),
            run_time=1.5
        )
        self.wait()
        self.play(
            *[
                TransformFromCopy(bayes[i], bayes[j], path_arc=30 * DEGREES)
                for i, j in [
                    (0, 12),
                    (1, 13),
                    (4, 14),
                    (0, 16),
                    (3, 17),
                    (4, 18),
                ]
            ],
            FadeIn(bayes[15]),
            run_time=1.5
        )
        self.add(bayes)
        self.wait()

        hyp_word = bayes.get_part_by_tex(hyp)
        example_hyp = OldTexText(
            "For example,\\\\",
            "$0.9 < s < 0.99$",
        )
        example_hyp[1].set_color(YELLOW)
        example_hyp.next_to(hyp_word, DOWN, buff=1.5)

        data_word = bayes.get_part_by_tex(data)
        example_data = OldTex(
            "48\\,", CMARK_TEX,
            "\\,2\\,", XMARK_TEX,
        )
        example_data.set_color_by_tex(CMARK_TEX, GREEN)
        example_data.set_color_by_tex(XMARK_TEX, RED)
        example_data.scale(1.5)
        example_data.next_to(example_hyp, RIGHT, buff=1.5)

        hyp_arrow = Arrow(
            hyp_word.get_bottom(),
            example_hyp.get_top(),
        )
        data_arrow = Arrow(
            data_word.get_bottom(),
            example_data.get_top(),
        )

        self.play(
            GrowArrow(hyp_arrow),
            FadeInFromPoint(example_hyp, hyp_word.get_center()),
        )
        self.wait()
        self.play(
            GrowArrow(data_arrow),
            FadeInFromPoint(example_data, data_word.get_center()),
        )
        self.wait()
