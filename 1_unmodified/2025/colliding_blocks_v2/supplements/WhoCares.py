# ==============================================================================
# Scene:      WhoCares
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 1094-1119)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhoCares.py WhoCares -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhoCares(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.play(
            stds[2].says("Question...", mode="dance_3"),
            self.change_students("pondering", "pondering", look_at=stds[2].eyes),
            morty.change('tease'),
        )
        self.wait()
        old_bubble = stds[2].bubble
        bubble = stds[2].get_bubble("Who cares?", bubble_type=SpeechBubble)
        self.play(LaggedStart(
            FadeTransformPieces(old_bubble, bubble),
            stds[2].change("angry"),
            self.change_students("guilty", "hesitant"),
            morty.change("hesitant"),
            lag_ratio=0.25
        ))
        self.play(LaggedStart(
            stds[1].animate.look_at(stds[0].eyes),
            stds[0].change("maybe")
        ))
        self.play(Blink(stds[0]))
        self.wait(5)
