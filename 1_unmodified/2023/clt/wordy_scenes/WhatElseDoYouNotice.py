# ==============================================================================
# Scene:      WhatElseDoYouNotice
# Source:     videos/_2023/clt/wordy_scenes.py (lines 652-662)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatElseDoYouNotice.py WhatElseDoYouNotice -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhatElseDoYouNotice(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        self.remove(self.background)
        self.play(
            morty.says("What else do\nyou notice?"),
            self.change_students("pondering", "erm", "pondering", look_at=self.screen)
        )
        self.wait(2)
        self.play(self.change_students("erm", "pondering", "tease", look_at=self.screen))
        self.wait(2)
