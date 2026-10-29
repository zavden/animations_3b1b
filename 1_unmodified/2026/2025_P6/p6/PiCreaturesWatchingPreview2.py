# ==============================================================================
# Scene:      PiCreaturesWatchingPreview2
# Source:     videos/_2026/2025_P6/p6.py (lines 4629-4648)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiCreaturesWatchingPreview2.py PiCreaturesWatchingPreview2 -w -m --fps 15
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)


class PiCreaturesWatchingPreview2(TeacherStudentsScene):
    def construct(self):
        # Students watch the preview
        self.play(self.get_teacher().change("raise_right_hand", look_at=UP * 2 + LEFT * 4))
        self.play(
            self.get_students()[0].change("happy", look_at=UP * 2 + LEFT * 4),
            self.get_students()[1].change("pondering", look_at=UP * 2 + LEFT * 4),
            self.get_students()[2].change("well", look_at=UP * 2 + LEFT * 4)
        )
        self.wait(3)

        # Teacher reminds students to be patient
        self.teacher_says(Text("You'll need to\nbe patient", font_size=40))
        self.play(
            self.get_students()[0].change("pondering", look_at=DOWN * 2),
            self.get_students()[1].change("thinking", look_at=DOWN * 2),
            self.get_students()[2].change("pondering", look_at=DOWN * 2)
        )

        self.wait(7)
