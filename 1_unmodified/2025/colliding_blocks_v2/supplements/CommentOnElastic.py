# ==============================================================================
# Scene:      CommentOnElastic
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 199-219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CommentOnElastic.py CommentOnElastic -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CommentOnElastic(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.play(
            morty.says("Assume perfectly\nelastic collisions"),
            self.change_students("pondering", "erm", "tease", look_at=self.screen)
        )
        self.wait(2)
        self.play(
            stds[2].says(
                "Then there should\nbe no sound",
                mode="sassy",
                bubble_direction=LEFT,
                look_at=morty.eyes
            ),
            morty.debubble("guilty"),
        )
        self.play(self.change_students("erm", "angry", "sassy", look_at=morty.eyes))
        self.wait(3)
