# ==============================================================================
# Scene:      OneMoreSideNote
# Source:     videos/_2023/clt/wordy_scenes.py (lines 1066-1082)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneMoreSideNote.py OneMoreSideNote -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OneMoreSideNote(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.change_students("pondering", "pondering", "erm", look_at=self.screen)
        )
        self.wait()
        self.play(
            self.teacher.says(
                "Will you tolerate\none more\nside note?",
                mode="speaking",
            ),
        )
        self.play(
            self.change_students("tired", "pondering", "hesitant")
        )
        self.wait(4)
