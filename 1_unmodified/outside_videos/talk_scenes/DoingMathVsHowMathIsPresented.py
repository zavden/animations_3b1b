# ==============================================================================
# Scene:      DoingMathVsHowMathIsPresented
# Source:     videos/outside_videos/talk_scenes.py (lines 4-44)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DoingMathVsHowMathIsPresented.py DoingMathVsHowMathIsPresented -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DoingMathVsHowMathIsPresented(Scene):
    def construct(self):
        titles = VGroup(
            OldTexText("How math is presented"),
            OldTexText("Actually doing math"),
        )
        for title, vect in zip(titles, [LEFT, RIGHT]):
            title.scale(1.2)
            title.to_edge(UP)
            title.shift(vect * FRAME_WIDTH / 4)

        blocks = VGroup(
            self.get_block(0.98),
            self.get_block(0.1),
        )

        self.add(titles)
        v_line = DashedLine(FRAME_WIDTH * UP / 2, FRAME_WIDTH * DOWN / 2)
        self.add(v_line)
        for block, title in zip(blocks, titles):
            block.next_to(title, DOWN)
            self.play(LaggedStartMap(FadeInFromLarge, block))
            self.wait(2)

    def get_block(self, prob):
        block = VGroup(*[
            self.get_mark(prob)
            for x in range(100)
        ])
        block.arrange_in_grid()
        block.set_width(5)
        return block

    def get_mark(self, prob):
        if random.random() < prob:
            mark = OldTex("\\checkmark").set_color(GREEN)
        else:
            mark = OldTex("\\times").set_color(RED)
        mark.set_height(1)
        mark.set_width(1, stretch=True)
        return mark
