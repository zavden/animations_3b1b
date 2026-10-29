# ==============================================================================
# Scene:      CheckOutMathologer
# Source:     videos/_2017/borsuk.py (lines 82-125)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CheckOutMathologer.py CheckOutMathologer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CheckOutMathologer(PiCreatureScene):
    CONFIG = {
        "logo_height" : 1.5,
        "screen_height" : 5,
        "channel_name" : "Mathologer",
        "logo_file" : "mathologer_logo",
        "logo_color" : None,
    }
    def construct(self):
        logo = self.get_logo()
        name = OldTexText(self.channel_name)
        name.next_to(logo, RIGHT)

        rect = Rectangle(height = 9, width = 16)
        rect.set_height(self.screen_height)
        rect.next_to(logo, DOWN)
        rect.to_edge(LEFT)

        self.play(
            self.get_logo_intro_animation(logo),
            self.pi_creature.change_mode, "hooray",
        )
        self.play(
            ShowCreation(rect),
            Write(name)
        )
        self.wait(2)
        self.change_mode("happy")
        self.wait(2)

    def get_logo(self):
        logo = ImageMobject(self.logo_file)
        logo.set_height(self.logo_height)
        logo.to_corner(UP+LEFT)
        if self.logo_color is not None:
            logo.set_color(self.logo_color)
            logo.stroke_width = 1
        return logo

    def get_logo_intro_animation(self, logo):
        logo.save_state()
        logo.shift(DOWN)
        logo.set_color(BLACK)
        return ApplyMethod(logo.restore)
