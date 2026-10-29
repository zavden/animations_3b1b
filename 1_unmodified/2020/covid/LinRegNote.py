# ==============================================================================
# Scene:      LinRegNote
# Source:     videos/_2020/covid.py (lines 1204-1208)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LinRegNote.py LinRegNote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LinRegNote(Scene):
    def construct(self):
        text = OldTexText("(Starting from when\\\\there were 100 cases)")
        text.set_stroke(BLACK, 8, background=True)
        self.add(text)
