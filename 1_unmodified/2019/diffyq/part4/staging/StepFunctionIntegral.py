# ==============================================================================
# Scene:      StepFunctionIntegral
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1998-2069)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StepFunctionIntegral.py StepFunctionIntegral -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StepFunctionIntegral(Scene):
    def construct(self):
        light_pink = interpolate_color(PINK, WHITE, 0.25)
        tex_config = {
            "tex_to_color_map": {
                "{t}": light_pink,
                "{dt}": light_pink,
                "{n}": YELLOW,
            }
        }
        cn_expression = OldTex(
            """
            c_{n} =
            \\int_0^1 \\text{step}({t})
            e^{-{n}\\cdot 2\\pi i {t}} {dt}
            """,
            **tex_config
        )
        expansion = OldTex(
            """
            =
            \\int_0^{0.5} 1 \\cdot e^{-{n}\\cdot 2\\pi i {t}} {dt} +
            \\int_{0.5}^1 -1 \\cdot e^{-{n}\\cdot 2\\pi i {t}} {dt}
            """,
            **tex_config
        )
        group = VGroup(cn_expression, expansion)
        group.arrange(RIGHT)
        group.set_width(FRAME_WIDTH - 1)
        group.to_corner(UL)

        words1 = OldTex(
            "\\text{Challenge 1: Show that }"
            "c_{n} = {2 \\over {n} \\pi i}",
            "\\text{ for odd }", "{n}",
            "\\text{ and 0 otherwise}",
            **tex_config,
        )
        words2 = OldTex(
            "\\text{Challenge 2: }",
            "&\\text{Using }",
            "\\sin(x) = (e^{ix} - e^{-ix}) / 2i,",
            "\\text{ show that}\\\\"
            "&\\text{step}({t}) = "
            "\\sum_{n = -\\infty}^{\\infty}",
            "c_{n} e^{{n} \\cdot 2\\pi i {t}}",
            "=",
            "\\sum_{n = 1, 3, 5, \\dots}",
            "{4 \\over {n} \\pi}",
            "\\sin\\left({n} \\cdot 2\\pi {t}\\right)",
            **tex_config,
        )
        words3 = OldTexText(
            "Challenge 3: How can you turn this into an "
            "expansion with \\\\ \\phantom{Challenge 3:} cosines? "
            "(Hint: Draw the sine waves over $[0.25, 0.75]$)",
            # "Challenge 3: By focusing on the range $[0.25, 0.75]$, relate\\\\"
            # "\\quad\\;\\, this to an expansion with cosines."
            alignment="",
        )

        all_words = VGroup(words1, words2, words3)
        all_words.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        all_words.scale(0.8)
        all_words.to_edge(DOWN)

        self.add(cn_expression)
        self.wait()
        self.play(FadeIn(expansion, LEFT))
        for words in all_words:
            self.play(FadeIn(words))
            self.wait()
