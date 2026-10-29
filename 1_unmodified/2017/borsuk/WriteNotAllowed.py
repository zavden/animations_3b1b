# ==============================================================================
# Scene:      WriteNotAllowed
# Source:     videos/_2017/borsuk.py (lines 589-593)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteNotAllowed.py WriteNotAllowed -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteWords(Scene):
    CONFIG = {
        "words" : "",
        "color" : WHITE,
    }
    def construct(self):
        words = OldTexText(self.words)
        words.set_color(self.color)
        words.set_width(FRAME_WIDTH-1)
        words.to_edge(DOWN)
        self.play(Write(words))
        self.wait(2)


class WriteNotAllowed(WriteWords):
    CONFIG = {
        "words" : "Not allowed",
        "color" : RED,
    }
