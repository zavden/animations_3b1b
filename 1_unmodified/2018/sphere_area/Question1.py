# ==============================================================================
# Scene:      Question1
# Source:     videos/_2018/sphere_area.py (lines 3306-3343)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Question1.py Question1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Question1(Scene):
    def construct(self):
        kwargs = {
            "tex_to_color_map": {
                "circumference": RED,
            }
        }
        question = OldTexText(
            """
            \\small
            Question \\#1: What is the circumference of\\\\
            one of these rings (in terms of $R$ and $\\theta$)?\\\\
            """,
            **kwargs
        )
        prompt = OldTexText(
            """
            Multiply this circumference by $R\\,d\\theta$ to \\\\
            get an approximation of the ring's area.
            """,
            **kwargs

        )
        for words in question, prompt:
            words.set_width(FRAME_WIDTH - 1)

        self.play(FadeInFromDown(question))
        self.wait(2)
        for word in question, prompt:
            word.circum = word.get_part_by_tex("circumference")
            word.remove(word.circum)
        self.play(
            FadeOut(question, UP),
            FadeInFromDown(prompt),
            question.circum.replace, prompt.circum,
            run_time=1.5
        )
        self.wait()
