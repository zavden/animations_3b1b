# ==============================================================================
# Scene:      AliceWords
# Source:     videos/_2021/shadows.py (lines 373-377)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AliceWords.py AliceWords -w -m --fps 15
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


class BobWords(SimpleWriting):
    font = "Kalam"
    font_size = 24
    words1 = "Embraces calculations"
    words2 = "Loves specifics"

    def construct(self):
        words = VGroup(*(
            Text(text, font=self.font, font_size=self.font_size)
            for text in (self.words1, self.words2)
        ))
        words.arrange(DOWN)

        for word in words:
            self.play(Write(word))
            self.wait()


class AliceWords(BobWords):
    font = "Better Grade"
    words1 = "Procrastinates calculations"
    words2 = "Seeks generality"
    font_size = 48
