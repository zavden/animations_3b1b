# ==============================================================================
# Scene:      WhatWouldBeNice
# Source:     videos/_2023/gauss_int/supplements.py (lines 826-832)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatWouldBeNice.py WhatWouldBeNice -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhatWouldBeNice(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("You know what\nwould be nice?"),
            self.change_students("pondering", "happy", "tease", look_at=self.screen)
        )
        self.wait(4)
