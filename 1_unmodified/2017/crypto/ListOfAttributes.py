# ==============================================================================
# Scene:      ListOfAttributes
# Source:     videos/_2017/crypto.py (lines 130-159)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ListOfAttributes.py ListOfAttributes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ListOfAttributes(Scene):
    def construct(self):
        logo = BitcoinLogo()

        digital = OldTexText("Digital")
        government, bank = buildings = [
            SVGMobject(
                file_name = "%s_building"%word,
                height = 2,
                fill_color = GREY_B,
                fill_opacity = 1,
                stroke_width = 0,
            )
            for word in ("government", "bank")
        ]
        attributes = VGroup(digital, *buildings)
        attributes.arrange(RIGHT, buff = LARGE_BUFF)
        for building in buildings:
            building.cross = Cross(building)
            building.cross.set_stroke(width = 12)

        self.play(DrawBorderThenFill(logo))
        self.play(
            logo.to_corner, UP+LEFT,
            Write(digital, run_time = 2)
        )
        for building in buildings:
            self.play(FadeIn(building))
            self.play(ShowCreation(building.cross))
        self.wait()
