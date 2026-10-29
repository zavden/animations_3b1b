# ==============================================================================
# Scene:      SomethingSomethingLimits
# Source:     videos/_2022/visual_proofs/lies.py (lines 398-404)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SomethingSomethingLimits.py SomethingSomethingLimits -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SomethingSomethingLimits(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("Something,\nsomething\nlimits!", mode="shruggie"),
            self.change_students("hesitant", "angry", "erm")
        )
        self.wait()
