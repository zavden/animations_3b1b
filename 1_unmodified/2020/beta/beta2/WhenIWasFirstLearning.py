# ==============================================================================
# Scene:      WhenIWasFirstLearning
# Source:     videos/_2020/beta/beta2.py (lines 1933-1970)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhenIWasFirstLearning.py WhenIWasFirstLearning -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhenIWasFirstLearning(TeacherStudentsScene):
    def construct(self):
        self.teacher.change_mode("raise_right_hand")
        self.play(
            self.change_students("pondering", "thinking", "tease"),
            self.teacher.change, "thinking",
        )

        younger = BabyPiCreature(color=GREY_BROWN)
        younger.set_height(2)
        younger.move_to(self.students, DL)

        self.look_at(self.screen)
        self.wait()
        self.play(
            ReplacementTransform(self.teacher, younger),
            LaggedStartMap(
                FadeOutAndShift, self.students,
                lambda m: (m, DOWN),
            )
        )

        # Bubble
        bubble = ThoughtBubble()
        bubble[-1].set_fill(GREEN_SCREEN, 1)
        bubble.move_to(younger.get_corner(UR), DL)

        self.play(
            Write(bubble),
            younger.change, "maybe", bubble.get_bubble_center(),
        )
        self.play(Blink(younger))
        for mode in ["confused", "angry", "pondering", "maybe"]:
            self.play(younger.change, mode)
            for x in range(2):
                self.wait()
                if random.random() < 0.5:
                    self.play(Blink(younger))
