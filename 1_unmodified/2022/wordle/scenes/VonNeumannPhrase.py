# ==============================================================================
# Scene:      VonNeumannPhrase
# Source:     videos/_2022/wordle/scenes.py (lines 2392-2401)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VonNeumannPhrase.py VonNeumannPhrase -w -m --fps 15
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
