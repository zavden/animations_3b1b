# ==============================================================================
# Scene:      RemovedConnectionBetweenLedgerAndCash
# Source:     videos/_2017/crypto.py (lines 1765-1802)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RemovedConnectionBetweenLedgerAndCash.py RemovedConnectionBetweenLedgerAndCash -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RemovedConnectionBetweenLedgerAndCash(TeacherStudentsScene):
    def construct(self):
        ledger = Rectangle(
            height = 2, width = 1.5,
            color = WHITE
        )
        ledger_name = OldTexText("Ledger")
        ledger_name.set_width(ledger.get_width() - MED_SMALL_BUFF)
        ledger_name.next_to(ledger.get_top(), DOWN)
        ledger.add(ledger_name)

        arrow = OldTex("\\leftrightarrow")
        cash = OldTex("\\$\\$\\$")
        cash.set_color(GREEN)
        arrow.next_to(ledger, RIGHT)
        cash.next_to(arrow, RIGHT)
        group = VGroup(ledger, arrow, cash)
        group.next_to(self.teacher, UP+LEFT)

        self.add(group)
        self.play(
            Animation(group),
            self.teacher.change, "raise_right_hand"
        )
        self.play(
            arrow.shift, 2*UP,
            arrow.set_fill, None, 0
        )
        self.play(
            ledger.shift, LEFT, 
            cash.shift, RIGHT
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = ledger,
            added_anims = [self.teacher.change, "happy"]
        )
        self.wait(3)
