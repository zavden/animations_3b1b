# ==============================================================================
# Scene:      BobName
# Source:     videos/_2021/shadows.py (lines 350-352)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BobName.py BobName -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleWriting(Scene):
    text = ""
    font = "Better Grade"
    color = WHITE
    font_size = 48

    def construct(self):
        words = Text(self.text, font=self.font, font_size=self.font_size)
        words.set_color(self.color)
        self.play(Write(words))
        self.wait()


class BobName(SimpleWriting):
    text = "Bob"
    font = "Kalam"
