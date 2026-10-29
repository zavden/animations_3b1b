# ==============================================================================
# Scene:      PiCreaturesWatchingPreview
# Source:     videos/_2026/2025_P6/p6.py (lines 4617-4626)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiCreaturesWatchingPreview.py PiCreaturesWatchingPreview -w -m --fps 15
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)


class PiCreaturesWatchingPreview(TeacherStudentsScene):
    def construct(self):
        # Students watch the preview
        self.play(self.get_teacher().change("raise_right_hand", look_at=UP * 2))
        self.play(
            self.get_students()[0].change("happy", look_at=UP * 2),
            self.get_students()[1].change("pondering", look_at=UP * 2),
            self.get_students()[2].change("well", look_at=UP * 2)
        )
        self.wait(20)
