# ==============================================================================
# Scene:      VonNeumannPhrase2
# Source:     videos/_2022/wordle/scenes.py (lines 2404-2405)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VonNeumannPhrase2.py VonNeumannPhrase2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VonNeumannPhrase(Scene):
    text = "You should call \n it entropy!"

    def construct(self):
        label = Text(self.text)
        label.set_backstroke(width=8)
        for word in self.text.split():
            self.add(label.get_part_by_text(word))
            self.wait(0.1)
        self.wait()


class VonNeumannPhrase2(VonNeumannPhrase):
    text = "Nobody knows what \n entropy really is."
