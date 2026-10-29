# ==============================================================================
# Scene:      BinaryChoices
# Source:     videos/_2018/eop/chapter1/various_intro_visuals.py (lines 116-132)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/combinations.py, _2018/eop/reusables/binary_option.py, _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl BinaryChoices.py BinaryChoices -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Xmark (red \times from eop/independence.py) is not defined in this file: built directly with OldTex("\\times").set_color(RED)
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



# ----- From _2018/eop/combinations.py -----

class Male(Tex):
    CONFIG = {
        "height" : 0.4,
        "tex" : "\\male",
        "color" : BLUE,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        Tex.__init__(self, self.tex, **kwargs)
        self.set_height(self.height)
        self.set_color(self.color)


class Female(Male):
    CONFIG = {
        "tex" : "\\female",
        "color" : MAROON_B,
    }



# ----- From _2018/eop/chapter1/various_intro_visuals.py -----

class BinaryChoices(Scene):

    def construct(self):

        example1 = BinaryOption(UprightHeads(), UprightTails())
        example2 = BinaryOption(Male(), Female())
        # CHANGE: Xmark (a red \times from eop/independence.py) is not defined here; build it directly
        example3 = BinaryOption(Checkmark(), OldTex("\\times").set_color(RED))

        example2.next_to(example1, DOWN, buff = MED_LARGE_BUFF)
        example3.next_to(example2, DOWN, buff = MED_LARGE_BUFF)

        all = VGroup(example1, example2, example3)
        all = all.scale(2)

        self.play(
            LaggedStartMap(FadeIn, all)
        )
