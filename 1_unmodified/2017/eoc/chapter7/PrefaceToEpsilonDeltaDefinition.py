# ==============================================================================
# Scene:      PrefaceToEpsilonDeltaDefinition
# Source:     videos/_2017/eoc/chapter7.py (lines 1387-1429)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrefaceToEpsilonDeltaDefinition.py PrefaceToEpsilonDeltaDefinition -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class PrefaceToEpsilonDeltaDefinition(TeacherStudentsScene):
    def construct(self):
        title = OldTex("(\\epsilon, \\delta) \\text{ definition}")
        title.next_to(self.get_teacher().get_corner(UP+LEFT), UP)
        title.save_state()
        title.shift(DOWN)
        title.set_fill(opacity = 0)

        self.play(
            title.restore,
            self.get_teacher().change_mode, "raise_right_hand",
        )
        self.play_student_changes(*["confused"]*3)
        self.wait()
        self.student_says(
            "Isn't that pretty \\\\ technical?",
            target_mode = "guilty",
            added_anims = [
                title.to_edge, UP,
                self.get_teacher().change_mode, "plain",
                self.get_teacher().look_at, self.get_students()[1].eyes
            ]
        )
        self.look_at(self.get_teacher().eyes, self.get_students())
        self.wait()
        self.teacher_says("", bubble_config = {"stroke_width" : 0})
        self.play_student_changes(
            *["pondering"]*3,
            look_at = UP+LEFT,
            added_anims = [self.get_teacher().look_at, UP+LEFT]
        )
        self.wait(3)
        words = OldTexText(
            "It's a glimpse of\\\\",
            "real analysis"
        )
        words.set_color_by_tex("real", YELLOW)
        self.teacher_says(
            words, 
            bubble_config = {"height" : 3, "width" : 6}
        )
        self.play_student_changes(*["happy"]*3)
        self.wait(6)
