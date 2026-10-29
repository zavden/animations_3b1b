# ==============================================================================
# Scene:      TakeOver
# Source:     videos/_2018/lost_lecture.py (lines 123-151)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TakeOver.py TakeOver -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - pi_creature_says(content) took the primary creature in Cairo; GL's version needs the creature first, so use say(content)
# ==============================================================================

from manim_imports_ext import *

class TakeOver(PiCreatureScene):
    CONFIG = {
        "default_pi_creature_kwargs": {
            "color": GREY_BROWN,
            "flip_at_start": True,
        },
        "default_pi_creature_start_corner": DR,
    }

    def construct(self):
        gradient = ImageMobject("white_black_gradient")
        gradient.set_height(FRAME_HEIGHT)
        self.add(gradient)

        morty = self.pi_creatures
        henry = ImageMobject("Henry_As_Stick")
        henry.set_height(4)
        henry.to_edge(LEFT)
        henry.to_edge(DOWN)

        self.add(morty, henry)
        # CHANGE: pi_creature_says(content) took the primary creature in Cairo; GL's version needs the creature first, so use say(content)
        self.say(
            "Muahaha!  All \\\\ mine now.",
            bubble_config={"fill_opacity": 0.5},
            bubble_creation_class=FadeIn,
            target_mode="conniving",
            added_anims=[henry.rotate, 5 * DEGREES]
        )
        self.wait(2)
