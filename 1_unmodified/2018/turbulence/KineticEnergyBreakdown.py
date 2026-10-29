# ==============================================================================
# Scene:      KineticEnergyBreakdown
# Source:     videos/_2018/turbulence.py (lines 1265-1296)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KineticEnergyBreakdown.py KineticEnergyBreakdown -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class KineticEnergyBreakdown(Scene):
    def construct(self):
        title = OldTexText("Kinetic energy breakdown")
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.next_to(title, DOWN)
        v_line = Line(h_line.get_center(), FRAME_HEIGHT * DOWN / 2)
        lc_title = OldTexText("Simpler physics")
        lc_title.set_color(YELLOW)
        rc_title = OldTexText("Turbulence physics")
        rc_title.set_color(GREEN)
        for word, vect in (lc_title, LEFT), (rc_title, RIGHT):
            word.next_to(h_line, DOWN)
            word.shift(FRAME_WIDTH * vect / 4)

        left_items = VGroup(
            OldTexText("- Big moving things"),
            OldTexText("- Heat"),
        )
        left_items.arrange(DOWN, aligned_edge=LEFT)
        left_items.next_to(lc_title, DOWN, MED_LARGE_BUFF)
        left_items.to_edge(LEFT)

        self.play(
            Write(VGroup(*it.chain(
                title, h_line, v_line, lc_title, rc_title
            )))
        )
        self.wait()
        for item in left_items:
            self.play(FadeIn(item))
            self.wait()
