# ==============================================================================
# Scene:      ComplainAboutParityCheckWeakness
# Source:     videos/_2020/hamming.py (lines 2421-2462)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplainAboutParityCheckWeakness.py ComplainAboutParityCheckWeakness -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplainAboutParityCheckWeakness(TeacherStudentsScene):
    def construct(self):
        self.embed()

        self.screen.set_fill(BLACK, 1)
        self.add(self.screen)

        self.play(
            PiCreatureSays(
                self.students[1],
                "Wait, it fails\\\\for two flips?",
                target_mode="sassy",
                bubble_config={
                    "height": 3,
                    "width": 3,
                }
            ),
            self.teacher.change, "guilty",
        )
        self.wait()
        self.play(
            PiCreatureSays(
                self.students[2], "Weak!",
                target_mode="angry",
                bubble_config={"direction": LEFT}
            ),
            self.students[0].change, "hesitant"
        )
        self.wait()
        self.play(self.teacher.change, "tease")
        self.wait()
        self.play_student_changes(
            "thinking", "pondering", "pondering",
            look_at=self.screen,
            added_anims=[
                FadeOut(self.students[1].bubble),
                FadeOut(self.students[1].bubble.content),
                FadeOut(self.students[2].bubble),
                FadeOut(self.students[2].bubble.content),
            ]
        )
        self.wait()
