# ==============================================================================
# Scene:      JustFlippingWithResults
# Source:     videos/_2018/eop/chapter1/just_randy_flipping_coin.py (lines 20-38)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/coin_flipping_pi_creature.py, _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl JustFlippingWithResults.py JustFlippingWithResults -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
#   - import random re-added after `from random import *` (the star import rebinds random to a function)
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *
# CHANGE: `from random import *` rebinds the name random to the function random.random; re-import the module so random.choice works
import random


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



# ----- From _2018/eop/reusables/coin_flipping_pi_creature.py -----

class PiCreatureCoin(VMobject):
    CONFIG = {
        "diameter": 0.8,
        "thickness": 0.2,
        "nb_ridges" : 7,
        "stroke_color": YELLOW,
        "stroke_width": 3,
        "fill_color": YELLOW,
        "fill_opacity": 0.7,
    }

    def init_points(self):
        outer_rect = Rectangle(
            width = self.diameter,
            height = self.thickness,
            fill_color  = self.fill_color,
            fill_opacity = self.fill_opacity,
            stroke_color = self.stroke_color,
            stroke_width = 0, #self.stroke_width
        )
        self.add(outer_rect)
        PI = TAU/2
        ridge_angles = np.arange(PI/self.nb_ridges,PI,PI/self.nb_ridges)
        ridge_positions = 0.5 * self.diameter * np.array([
            np.cos(theta) for theta in ridge_angles
        ])
        ridge_color = interpolate_color(BLACK,self.stroke_color,0.5)
        for x in ridge_positions:
            ridge = Line(
                x * RIGHT + 0.5 * self.thickness * DOWN,
                x * RIGHT + 0.5 * self.thickness * UP,
                stroke_color = ridge_color,
                stroke_width = self.stroke_width
            )
            self.add(ridge)


class CoinFlippingPiCreature(PiCreature):
    CONFIG = {
        "flip_height": 3
    }

    def __init__(self, mode = "coin_flip_1", **kwargs):

        coin = PiCreatureCoin()
        PiCreature.__init__(self, mode = mode, **kwargs)
        self.coin = coin
        self.add(coin)
        right_arm = self.get_arm_copies()[1]
        coin.rotate(-TAU/24)
        coin.next_to(right_arm, RIGHT+UP, buff = 0)
        coin.shift(0.1 * self.get_width() * LEFT)
        coin.shift(0.2 * DOWN)

    def flip_coin_up(self):
        self.change("coin_flip_2")


class FlipUpAndDown(Animation):
    CONFIG = {
        "vector" : UP,
        "height" : 3,
        "nb_turns" : 1
    }

    def update(self,t):
        self.mobject.shift(self.height * 4 * t * (1 - t) * self.vector)
        self.mobject.rotate(t * self.nb_turns * TAU)


class FlipCoin(AnimationGroup):
    CONFIG = {
        "coin_rate_func" : there_and_back,
        "pi_rate_func" : lambda t : there_and_back_with_pause(t, 1./4)
    }
    def __init__(self, pi_creature, **kwargs):
        digest_config(self, kwargs)
        pi_creature_motion = ApplyMethod(
            pi_creature.flip_coin_up,
            rate_func = self.pi_rate_func,
            **kwargs
        )
        coin_motion = Succession(
            EmptyAnimation(run_time = 1.0),
            FlipUpAndDown(
                pi_creature.coin, 
                vector = UP,
                nb_turns = 5,
                height = pi_creature.flip_height * pi_creature.get_height(),
                rate_func = self.coin_rate_func,
                **kwargs
            )
        )
        AnimationGroup.__init__(self,pi_creature_motion, coin_motion)



# ----- From _2018/eop/chapter1/just_randy_flipping_coin.py -----

class JustFlippingWithResults(Scene):

    def construct(self):

        randy = CoinFlippingPiCreature(color = MAROON_E, flip_height = 1).shift(2 * DOWN)
        self.add(randy)

        self.wait(2)

        for i in range(10):
            self.wait()
            self.play(FlipCoin(randy))
            result = random.choice(["H", "T"])
            if result == "H":
                coin = UprightHeads().scale(3)
            else:
                coin = UprightTails().scale(3)
            coin.move_to(2 * UP + 2.5 * LEFT + i * 0.6 * RIGHT)
            self.play(FadeIn(coin))
