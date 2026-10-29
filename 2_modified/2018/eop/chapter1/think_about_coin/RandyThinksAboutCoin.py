# ==============================================================================
# Scene:      RandyThinksAboutCoin
# Source:     videos/_2018/eop/chapter1/think_about_coin.py (lines 5-31)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/binary_option.py, _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl RandyThinksAboutCoin.py RandyThinksAboutCoin -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *


# ----- From _2018/eop/reusables/binary_option.py -----

class BinaryOption(VMobject):
    CONFIG = {
    "text_scale" : 0.5
    }

    def __init__(self, mob1, mob2, **kwargs):

        VMobject.__init__(self, **kwargs)
        text = OldTexText("or").scale(self.text_scale)
        mob1.next_to(text, LEFT)
        mob2.next_to(text, RIGHT)
        self.add(mob1, text, mob2)



# ----- From _2018/eop/reusables/eop_constants.py -----

COIN_RADIUS = 0.18


COIN_STROKE_WIDTH = 2


COLOR_HEADS_COIN = RED


COLOR_TAILS_COIN = BLUE_E



# ----- From _2018/eop/reusables/upright_coins.py -----

class UprightCoin(Circle):
# For use in coin sequences
    CONFIG = {
        "radius": COIN_RADIUS,
        "stroke_width": COIN_STROKE_WIDTH,
        "stroke_color": WHITE,
        "fill_opacity": 1,
        "symbol": "\euro"
    }

    def __init__(self, **kwargs):
        Circle.__init__(self,**kwargs)
        self.symbol_mob = OldTexText(self.symbol, stroke_color = self.stroke_color)
        self.symbol_mob.set_height(0.5*self.get_height()).move_to(self)
        self.add(self.symbol_mob)


class UprightHeads(UprightCoin):
    CONFIG = {
        "fill_color": COLOR_HEADS_COIN,
        "symbol": "H",
    }


class UprightTails(UprightCoin):
    CONFIG = {
        "fill_color": COLOR_TAILS_COIN,
        "symbol": "T",
    }



# ----- From _2018/eop/chapter1/think_about_coin.py -----

class RandyThinksAboutCoin(PiCreatureScene):

    def construct(self):

        randy = self.get_primary_pi_creature()
        randy.center()
        self.add(randy)
        self.wait()
        h_or_t = BinaryOption(UprightHeads().scale(3), UprightTails().scale(3),
            text_scale = 1.5)
        self.think(h_or_t, direction = LEFT)

        v = 0.3
        self.play(
            h_or_t[0].shift,v*UP,
            h_or_t[2].shift,v*DOWN,
        )
        self.play(
            h_or_t[0].shift,2*v*DOWN,
            h_or_t[2].shift,2*v*UP,
        )
        self.play(
            h_or_t[0].shift,v*UP,
            h_or_t[2].shift,v*DOWN,
        )

        self.wait()
