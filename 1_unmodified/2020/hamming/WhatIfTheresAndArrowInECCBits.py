# ==============================================================================
# Scene:      WhatIfTheresAndArrowInECCBits
# Source:     videos/_2020/hamming.py (lines 3452-3466)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatIfTheresAndArrowInECCBits.py WhatIfTheresAndArrowInECCBits -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatIfTheresAndArrowInECCBits(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What if an\\\\error-correction bit\\\\needs to be corrected?",
            bubble_config={'width': 5, 'height': 4, "direction": LEFT},
            added_anims=[self.teacher.change, "happy"]
        )
        self.play_student_changes("confused", "confused")
        self.look_at(self.screen)
        self.wait(2)
        self.teacher_says("Try it!", target_mode="hooray")
        self.play_student_changes(*3 * ["pondering"], look_at=self.screen)
        self.wait(2)
        self.play_student_changes(*3 * ["thinking"], look_at=self.screen)
        self.wait(8)
