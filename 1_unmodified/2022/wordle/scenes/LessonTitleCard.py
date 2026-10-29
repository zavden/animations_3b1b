# ==============================================================================
# Scene:      LessonTitleCard
# Source:     videos/_2022/wordle/scenes.py (lines 1007-1024)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LessonTitleCard.py LessonTitleCard -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LessonTitleCard(Scene):
    def construct(self):
        title = VGroup(
            Text("Lesson today:", font_size=40),
            Text("Information theory", color=TEAL),
        )
        title.arrange(DOWN)
        title.scale(1.5)
        title.center()
        title[1].add(
            Underline(title[1], buff=-0.05).set_stroke(GREY, 2)
        )

        self.add(title[0])
        self.play(Write(title[1], run_time=1))
        self.wait()
        self.play(title.animate.scale(1 / 1.5).to_edge(UP))
        self.wait()
