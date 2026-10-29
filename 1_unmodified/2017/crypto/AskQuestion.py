# ==============================================================================
# Scene:      AskQuestion
# Source:     videos/_2017/crypto.py (lines 107-128)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskQuestion.py AskQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskQuestion(Scene):
    CONFIG = {
        "time_per_char" : 0.06,
    }
    def construct(self):
        strings = [
            "What", "does", "it", "mean   ", "to", 
            "have    ", "a", "Bitcoin?"
        ]
        question = OldTexText(*strings)
        question.set_color_by_tex("have", YELLOW)
        self.wait()
        for word, part in zip(strings, question):
            n_chars = len(word.strip())
            n_spaces = len(word) - n_chars
            self.play(
                LaggedStartMap(FadeIn, part),
                run_time = self.time_per_char * len(word),
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )
            self.wait(self.time_per_char*n_spaces)
        self.wait(2)
