# ==============================================================================
# Scene:      StrangeTurnsFraming
# Source:     videos/_2022/puzzles/subsets.py (lines 4553-4575)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StrangeTurnsFraming.py StrangeTurnsFraming -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StrangeTurnsFraming(InteractiveScene):
    def construct(self):
        # Title
        self.add(FullScreenRectangle())

        screens = Square().replicate(2)
        screens.set_stroke(WHITE, 1)
        screens.set_fill(BLACK, 1)
        screens.set_height(5.5)
        screens.arrange_to_fit_width(FRAME_WIDTH - 2)
        screens.to_edge(DOWN, buff=LARGE_BUFF)

        titles = VGroup(*(
            Text(f"Strange turn {n}", font_size=48)
            for n in [1, 2]
        ))
        for title, screen in zip(titles, screens):
            title.next_to(screen, UP)

        self.add(screens)
        for title in reversed(titles):
            self.play(FadeIn(title, 0.5 * UP))
        self.wait()
