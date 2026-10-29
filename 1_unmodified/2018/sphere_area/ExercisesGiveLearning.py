# ==============================================================================
# Scene:      ExercisesGiveLearning
# Source:     videos/_2018/sphere_area.py (lines 2680-2729)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExercisesGiveLearning.py ExercisesGiveLearning -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExercisesGiveLearning(MovingCameraScene):
    def construct(self):
        bulb = Lightbulb()
        arrow1 = Arrow(ORIGIN, RIGHT, buff=0)
        lectures = OldTexText("Lectures")
        exercises = OldTexText("Exercises")
        frame = self.camera_frame
        frame.scale(0.7)

        bulb.next_to(arrow1, RIGHT)
        for word in lectures, exercises:
            word.next_to(arrow1, LEFT)

        cross = Cross(lectures)

        # Knock down lectures
        self.add(lectures)
        self.play(GrowArrow(arrow1))
        self.play(LaggedStartMap(DrawBorderThenFill, bulb))
        self.play(ShowCreation(cross))
        self.play(
            VGroup(lectures, cross).shift, DOWN,
            FadeIn(exercises, UP)
        )
        self.wait()

        # Show self
        arrow2 = arrow1.copy()
        arrow2.next_to(lectures, LEFT)
        logo = Logo()
        logo.set_height(1)
        logo.next_to(arrow2, LEFT)
        pupil_copy = logo.pupil.copy()

        self.add(logo, pupil_copy)
        self.play(
            frame.shift, 1.5 * LEFT,
            Write(logo, run_time=1.5)
        )
        self.remove(pupil_copy)
        self.play(
            GrowArrow(arrow2),
            FadeOut(cross)
        )
        self.wait()
        self.play(
            VGroup(logo, arrow2).next_to,
            exercises, LEFT
        )
        self.wait()
