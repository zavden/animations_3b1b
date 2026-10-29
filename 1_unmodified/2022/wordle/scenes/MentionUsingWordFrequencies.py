# ==============================================================================
# Scene:      MentionUsingWordFrequencies
# Source:     videos/_2022/wordle/scenes.py (lines 2541-2549)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionUsingWordFrequencies.py MentionUsingWordFrequencies -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MentionUsingWordFrequencies(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText("Next step: Integrate\\\\word frequency data"),
            added_anims=[self.change_students("hooray", "happy", "tease")]
        )
        self.wait()
        self.play(self.students[1].change("pondering"))
        self.wait(2)
