# ==============================================================================
# Scene:      PrerequisitesWrapper
# Source:     videos/_2021/matrix_exp.py (lines 6246-6277)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrerequisitesWrapper.py PrerequisitesWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PrerequisitesWrapper(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        title = Text("Helpful background knowledge")
        title.to_edge(UP)
        self.add(title)

        screens = VGroup(*(ScreenRectangle() for x in range(2)))
        screens.arrange(RIGHT, buff=LARGE_BUFF)
        screens.set_width(FRAME_WIDTH - 1)
        screens.move_to(DOWN)
        screens.set_fill(BLACK, 1)
        screens.set_stroke(WHITE, 2)

        topics = VGroup(
            OldTexText("Basics of $e^x$"),
            OldTexText("How matrices act\\\\as transformations"),
        )
        for topic, screen in zip(topics, screens):
            topic.next_to(screen, UP)
            topic.set_color(WHITE)

        for topic, screen in zip(topics, screens):
            sc = screen.copy()
            sc.set_fill(opacity=0)
            sc.set_stroke(width=3)
            self.play(
                FadeIn(topic, 0.5 * UP),
                FadeIn(screen),
                VShowPassingFlash(sc, time_width=1.0, run_time=1.5),
            )
            self.wait(2)
