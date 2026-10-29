# ==============================================================================
# Scene:      QuixoteReference
# Source:     videos/_2019/windmill.py (lines 3782-3813)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuixoteReference.py QuixoteReference -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuixoteReference(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle()
        rect.set_fill([GREY_D, GREY])

        windmill = SVGMobject("windmill")
        windmill.set_fill([GREY_BROWN, WHITE], 1)
        windmill.set_stroke(width=0)
        windmill.set_height(6)
        windmill.to_edge(RIGHT)
        # windmill.to_edge(DOWN, buff=0)

        quixote = SVGMobject("quixote")
        quixote.flip()
        quixote.set_height(4)
        quixote.to_edge(LEFT)
        quixote.set_stroke(BLACK, width=0)
        quixote.set_fill(BLACK, 1)
        quixote.align_to(windmill, DOWN)

        self.add(rect)
        # self.add(windmill)
        self.play(LaggedStart(
            DrawBorderThenFill(windmill),
            DrawBorderThenFill(
                quixote,
                stroke_width=1,
            ),
            lag_ratio=0.4,
            run_time=3
        ))
        self.wait()
