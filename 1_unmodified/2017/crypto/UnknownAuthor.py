# ==============================================================================
# Scene:      UnknownAuthor
# Source:     videos/_2017/crypto.py (lines 161-180)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnknownAuthor.py UnknownAuthor -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UnknownAuthor(Scene):
    CONFIG = {
        "camera_config" : {
            "background_image" : "bitcoin_paper"
        }
    }
    def construct(self):
        rect = Rectangle(height = 0.4, width = 2.5)
        rect.shift(2.45*UP)
        question = OldTexText("Who is this?")
        question.next_to(rect, RIGHT, buff = 1.5)
        arrow = Arrow(question, rect, buff = SMALL_BUFF)
        VGroup(question, arrow, rect).set_color(RED_D)

        self.play(ShowCreation(rect))
        self.play(
            Write(question),
            ShowCreation(arrow)
        )
        self.wait()
