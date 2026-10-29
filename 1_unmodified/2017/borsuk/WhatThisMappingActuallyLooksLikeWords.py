# ==============================================================================
# Scene:      WhatThisMappingActuallyLooksLikeWords
# Source:     videos/_2017/borsuk.py (lines 2405-2412)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatThisMappingActuallyLooksLikeWords.py WhatThisMappingActuallyLooksLikeWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatThisMappingActuallyLooksLikeWords(Scene):
    def construct(self):
        words = OldTexText("What this mapping actually looks like")
        words.set_width(FRAME_WIDTH-1)
        words.to_edge(DOWN)

        self.play(Write(words))
        self.wait()
