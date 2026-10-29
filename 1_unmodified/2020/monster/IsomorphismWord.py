# ==============================================================================
# Scene:      IsomorphismWord
# Source:     videos/_2020/monster.py (lines 2775-2781)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IsomorphismWord.py IsomorphismWord -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IsomorphismWord(Scene):
    def construct(self):
        word = OldTexText("``Isomorphism''")
        word.scale(2)
        word.to_edge(UP)
        self.play(FadeIn(word, DOWN))
        self.wait()
