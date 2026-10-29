# ==============================================================================
# Scene:      PatYourselfOnTheBack
# Source:     videos/_2018/lost_lecture.py (lines 4182-4223)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PatYourselfOnTheBack.py PatYourselfOnTheBack -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PatYourselfOnTheBack(TeacherStudentsScene):
    CONFIG = {
        "camera_config": {"background_opacity": 1},
    }

    def construct(self):
        self.teacher_says(
            "Pat yourself \\\\ on the back!",
            target_mode="hooray"
        )
        self.play_all_student_changes("happy")
        self.wait(3)
        self.play(
            RemovePiCreatureBubble(
                self.teacher,
                target_mode="raise_right_hand"
            ),
            self.change_students(
                *3 * ["pondering"],
                look_at=self.screen
            )
        )
        self.look_at(UP)
        self.wait(8)
        self.play_student_changes(*3 * ["thinking"])
        self.look_at(UP)
        self.wait(12)
        self.teacher_says("I just love this!")

        feynman = ImageMobject("Feynman", height=4)
        feynman.to_corner(UL)
        chess = ImageMobject("ChessGameOfTheCentury")
        chess.set_height(4)
        chess.next_to(feynman)

        self.play(FadeInFromDown(feynman))
        self.wait()
        self.play(
            RemovePiCreatureBubble(self.teacher, target_mode="happy"),
            FadeInFromDown(chess)
        )
        self.wait(2)
