# ==============================================================================
# Scene:      ShowMeasurementBook
# Source:     videos/_2018/dandelin.py (lines 851-878)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowMeasurementBook.py ShowMeasurementBook -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowMeasurementBook(TeacherStudentsScene):
    CONFIG = {"camera_config": {"background_opacity": 1}}

    def construct(self):
        measurement = ImageMobject("MeasurementCover")
        measurement.set_height(3.5)
        measurement.move_to(self.hold_up_spot, DOWN)

        words = OldTexText("Highly recommended")
        arrow = Vector(RIGHT, color=WHITE)
        arrow.next_to(measurement, LEFT)
        words.next_to(arrow, LEFT)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeInFromDown(measurement)
        )
        self.play_all_student_changes("hooray")
        self.wait()
        self.play(
            GrowArrow(arrow),
            FadeIn(words, RIGHT),
            self.change_students(
                "thinking", "happy", "pondering",
                look_at=arrow
            )
        )
        self.wait(3)
