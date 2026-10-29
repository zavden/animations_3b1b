# ==============================================================================
# Scene:      TryToDefineExp
# Source:     videos/_2021/matrix_exp.py (lines 3722-3741)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TryToDefineExp.py TryToDefineExp -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - OldTex/OldTexText with {{ }}: manimgl removed that convention (Apr 2021) and no longer splits the text into parts; the double braces are removed and isolate=[...] is passed with the same pieces.
# ==============================================================================

from manim_imports_ext import *

class TryToDefineExp(TeacherStudentsScene):
    CONFIG = {
        "background_color": BLACK,
    }

    def construct(self):
        # CHANGE: OldTex no longer splits on {{ }} (convention removed from manimgl in Apr 2021); they are removed and isolate=[...] is used with the same pieces
        words = OldTexText(
            "Try to define $e^{M}$ to\\\\make sure this is true!",
            isolate=["$e^{M}$"],
        )
        words[1][1].set_color(TEAL)

        self.play(
            PiCreatureSays(self.teacher, words, target_mode="surprised"),
            self.change_students("pondering", "thinking", "pondering"),
        )
        for pi in self.students:
            for eye in pi.eyes:
                eye.refresh_bounding_box()
        self.look_at(4 * UP + 2 * RIGHT)
        self.wait(6)
