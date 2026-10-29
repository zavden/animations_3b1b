# ==============================================================================
# Scene:      ThisReallyDoesHappen
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1493-1500)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisReallyDoesHappen.py ThisReallyDoesHappen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThisReallyDoesHappen(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.teacher.says("This really\ndoes happen!", mode="surprised"),
        )
        self.play(self.change_students("sassy", "confused", "pleading", look_at=self.screen))
        self.wait(4)
