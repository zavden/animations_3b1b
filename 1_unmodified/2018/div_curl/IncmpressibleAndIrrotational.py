# ==============================================================================
# Scene:      IncmpressibleAndIrrotational
# Source:     videos/_2018/div_curl.py (lines 4073-4117)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IncmpressibleAndIrrotational.py IncmpressibleAndIrrotational -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IncmpressibleAndIrrotational(Scene):
    def construct(self):
        div_0 = OldTexText("div$\\textbf{F} = 0$")
        curl_0 = OldTexText("curl$\\textbf{F}$ = 0")
        incompressible = OldTexText("Incompressible")
        irrotational = OldTexText("Irrotational")

        for text in [div_0, curl_0, incompressible, irrotational]:
            self.stylize_word_for_background(text)

        div_0.to_edge(UP)
        curl_0.next_to(div_0, DOWN, MED_LARGE_BUFF)

        for op, word in (div_0, incompressible), (curl_0, irrotational):
            op.generate_target()
            group = VGroup(op.target, word)
            group.arrange(RIGHT, buff=MED_LARGE_BUFF)
            group.move_to(op)

        self.play(FadeInFromDown(div_0))
        self.play(FadeInFromDown(curl_0))
        self.wait()
        self.play(
            MoveToTarget(div_0),
            FadeInFromDown(incompressible),
        )
        self.wait()
        self.play(
            MoveToTarget(curl_0),
            FadeInFromDown(irrotational),
        )
        self.wait()

        rect = SurroundingRectangle(VGroup(curl_0, irrotational))
        question = OldTexText("Does this actually happen?")
        question.next_to(rect, DOWN)
        question.match_color(rect)
        self.stylize_word_for_background(question)

        self.play(ShowCreation(rect))
        self.play(Write(question))
        self.wait()

    def stylize_word_for_background(self, word):
        word.add_background_rectangle()
