# ==============================================================================
# Scene:      NoWhiteLight
# Source:     videos/_2024/holograms/supplements.py (lines 495-521)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NoWhiteLight.py NoWhiteLight -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NoWhiteLight(InteractiveScene):
    def construct(self):
        # Test
        white_label = VGroup(
            Text("White light", font_size=60),
            Text("(many frequencies)").set_color(GREY_B)
        )
        white_label.arrange(DOWN)
        white_label.to_edge(UP).set_x(-3)
        laser_label = VGroup(
            Text("Laser", font_size=60).set_color(GREEN_SCREEN),
            Text("(single frequency)").set_color(GREY_B),
        )
        laser_label.arrange(DOWN)
        laser_label.move_to(white_label, UP)

        cross = Cross(white_label, stroke_width=(0, 7, 7, 7, 0))

        self.add(white_label)
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()
        self.play(
            FadeOut(VGroup(white_label, cross), DR),
            FadeIn(laser_label, DR),
        )
        self.wait()
