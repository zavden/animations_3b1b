# ==============================================================================
# Scene:      ExamplePlease
# Source:     videos/_2018/alt_calc.py (lines 1478-1482)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExamplePlease.py ExamplePlease -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class ExamplePlease(TeacherStudentsScene):
    def construct(self):
        self.student_says("Example?", index=0)
        self.teacher_holds_up(OldTex("f(x) = x^2").scale(1.5))
        self.wait(2)
