# ==============================================================================
# Scene:      FinalComment
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 264-269)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FinalComment.py FinalComment -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FinalComment(Scene):
    def construct(self):
        self.add(OldTexText(
            "Thoughts on what ending should go here?\\\\"
            "See the Patreon post."
        ))
