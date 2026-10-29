# ==============================================================================
# Scene:      WhatStaysConstantWrapper
# Source:     videos/_2019/windmill.py (lines 3518-3545)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatStaysConstantWrapper.py WhatStaysConstantWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatStaysConstantWrapper(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": GREY_E
        }
    }

    def construct(self):
        rect = ScreenRectangle()
        rect.set_height(6)
        rect.set_stroke(WHITE, 2)
        rect.set_fill(BLACK, 1)
        title1 = OldTexText("What stays constant?")
        title2 = OldTexText("Find an ", "``invariant''")
        title2[1].set_color(YELLOW)
        for title in [title1, title2]:
            title.scale(2)
            title.to_edge(UP)
        rect.next_to(title1, DOWN)

        self.add(rect)
        self.play(FadeInFromDown(title1))
        self.wait()
        self.play(
            FadeOut(title1, UP),
            FadeInFromDown(title2),
        )
        self.wait()
