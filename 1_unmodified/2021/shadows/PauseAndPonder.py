# ==============================================================================
# Scene:      PauseAndPonder
# Source:     videos/_2021/shadows.py (lines 925-964)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PauseAndPonder.py PauseAndPonder -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PauseAndPonder(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)

        self.teacher_says(
            OldTexText("The goal is\\\\not speed."),
            added_anims=[self.change_students(
                "tease", "well", "pondering",
                look_at=self.screen
            )]
        )
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(self.teacher, target_mode="tease"),
            PiCreatureBubbleIntroduction(
                self.students[2],
                Lightbulb(),
                bubble_type=ThoughtBubble,
                bubble_creation_class=lambda m: FadeIn(m, lag_ratio=0.1),
                bubble_config=dict(
                    height=3,
                    width=3,
                    direction=LEFT,
                ),
                target_mode="thinking",
                look_at=self.screen,
            )
        )
        self.wait(3)
        self.teacher_says(
            "Pause and ponder!",
            target_mode="well",
            added_anims=[self.change_students(
                "pondering", "tease", "thinking"
            )],
            run_time=1
        )
        self.wait(5)

        self.embed()
