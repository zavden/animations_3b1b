# ==============================================================================
# Scene:      ConceptAndNotationFrames
# Source:     videos/_2022/borwein/supplements.py (lines 365-396)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConceptAndNotationFrames.py ConceptAndNotationFrames -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConceptAndNotationFrames(InteractiveScene):
    def construct(self):
        # Screens
        self.add(FullScreenRectangle())
        screens = Rectangle(height=3, width=4).replicate(2)
        screens.arrange(RIGHT, buff=0.25)
        screens.set_width(FRAME_WIDTH - 0.5)
        screens.set_stroke(WHITE, 1)
        screens.set_fill(BLACK, 1)
        screens.move_to(0.5 * DOWN)
        self.add(screens)

        # Titles
        titles = VGroup(
            Text("Moving average fact"),
            Text("In our new notation"),
            Text("How does this..."),
            Text("...relate to this"),
            # Text("These computations..."),
            # Text("...are (in a sense)\nthe same as these"),
        )
        for i, title in enumerate(titles):
            title.next_to(screens[i % 2], UP)
        titles[1].align_to(titles[0], UP)

        # Animations
        for i in range(2):
            self.play(FadeIn(titles[i]))
            self.wait()
        for i in range(2, 4):
            self.play(FadeIn(titles[i], 0.5 * UP), FadeOut(titles[i - 2], 0.5 * UP))
            self.wait()
