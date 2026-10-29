# ==============================================================================
# Scene:      BetweenNothingAndQuarantineWrapper
# Source:     videos/_2020/sir.py (lines 2331-2367)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BetweenNothingAndQuarantineWrapper.py BetweenNothingAndQuarantineWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BetweenNothingAndQuarantineWrapper(Scene):
    def construct(self):
        self.add(FullScreenFadeRectangle(
            fill_color=GREY_E,
            fill_opacity=1,
        ))
        rects = VGroup(*[
            ScreenRectangle()
            for x in range(3)
        ])
        rects.arrange(RIGHT)
        rects.set_width(FRAME_WIDTH - 1)
        self.add(rects)

        rects.set_fill(BLACK, 1)
        rects.set_stroke(WHITE, 2)

        titles = VGroup(
            OldTexText("Do nothing"),
            OldTexText("Quarantine\\\\", "80$\\%$ of cases"),
            OldTexText("Quarantine\\\\", "all cases"),
        )
        for title, rect in zip(titles, rects):
            title.next_to(rect, UP)

        q_marks = OldTex("???")
        q_marks.scale(2)
        q_marks.move_to(rects[1])

        self.add(rects)
        self.play(LaggedStartMap(
            FadeInFromDown,
            VGroup(titles[0], titles[2], titles[1]),
            lag_ratio=0.3,
        ))
        self.play(Write(q_marks))
        self.wait()
