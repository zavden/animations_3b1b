# ==============================================================================
# Scene:      ContactTracingWords
# Source:     videos/_2020/ctracing.py (lines 237-252)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContactTracingWords.py ContactTracingWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ContactTracingWords(Scene):
    def construct(self):
        words = OldTexText("Contact\\\\", "Tracing")
        words.set_height(4)
        for word in words:
            self.add(word)
            self.wait()
        self.wait()
        return
        self.play(ShowIncreasingSubsets(words))
        self.wait()
        self.play(
            words.set_height, 1,
            words.to_corner, UL,
        )
        self.wait()
