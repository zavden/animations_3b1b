# ==============================================================================
# Scene:      TransitionWrapper
# Source:     videos/_2021/matrix_exp.py (lines 5599-5629)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TransitionWrapper.py TransitionWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TransitionWrapper(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        screens = VGroup(*(ScreenRectangle() for x in range(2)))
        screens.set_width(0.4 * FRAME_WIDTH)
        screens[0].to_edge(LEFT)
        screens[1].to_edge(RIGHT)
        screens.set_fill(BLACK, 1)
        screens[0].set_stroke(BLUE, 2)
        screens[1].set_stroke(GREY_BROWN, 2)
        self.add(screens)

        arrow = Arrow(*screens)
        exp = OldTex("e^{Mt}")
        exp.next_to(arrow, UP)
        titles = VGroup(
            OldTexText("Time: $0$"),
            OldTexText("Time: $t$"),
        )
        for screen, title in zip(screens, titles):
            title.next_to(screen, UP)
            screen.add(title)

        vf_words = OldTexText("Vector field defined by $\\vec{\\textbf{v} } \\rightarrow M\\vec{\\textbf{v} }$")
        vf_words.match_width(screens[0])
        vf_words.next_to(screens[0], DOWN)
        self.add(vf_words)

        self.play(ShowCreation(arrow))
        self.play(Write(exp))
        self.wait()
