# ==============================================================================
# Scene:      TwoInterpretationsWrapper
# Source:     videos/_2022/wordle/scenes.py (lines 3195-3223)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoInterpretationsWrapper.py TwoInterpretationsWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoInterpretationsWrapper(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        screens = ScreenRectangle().get_grid(1, 2, buff=MED_LARGE_BUFF)
        screens.set_fill(BLACK, 1)
        screens.set_stroke(WHITE, 1)
        screens.set_width(FRAME_WIDTH - 1)
        screens.move_to(DOWN)

        title = Text("Two applications of entropy", font_size=60)
        title.to_edge(UP)

        screen_titles = VGroup(
            Text("Expected information from guess"),
            Text("Remaining uncertainty"),
        )
        screen_titles.scale(0.8)
        for screen, word in zip(screens, screen_titles):
            word.next_to(screen, UP)

        screen_titles[0].set_color(BLUE)
        screen_titles[1].set_color(TEAL)

        self.add(title)
        self.add(screens)
        self.wait()
        for word in screen_titles:
            self.play(Write(word, run_time=1))
            self.wait()
