# ==============================================================================
# Scene:      ContrastRandomShufflingWithClustersAndTravel
# Source:     videos/_2020/covid.py (lines 1832-1859)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContrastRandomShufflingWithClustersAndTravel.py ContrastRandomShufflingWithClustersAndTravel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ContrastRandomShufflingWithClustersAndTravel(Scene):
    def construct(self):
        background = FullScreenFadeRectangle()
        background.set_fill(GREY_E)
        self.add(background)

        squares = VGroup(*[Square() for x in range(2)])
        squares.set_width(FRAME_WIDTH / 2 - 1)
        squares.arrange(RIGHT, buff=0.75)
        squares.to_edge(DOWN)
        squares.set_fill(BLACK, 1)
        squares.stretch(0.8, 1)
        self.add(squares)

        titles = VGroup(
            OldTexText("Random shuffling"),
            OldTexText("Clusters with travel"),
        )
        for title, square in zip(titles, squares):
            title.scale(1.4)
            title.next_to(square, UP)
        titles[1].align_to(titles[0], UP)

        self.play(LaggedStartMap(
            FadeInFrom, titles,
            lambda m: (m, 0.25 * DOWN),
        ))
        self.wait()
