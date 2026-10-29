# ==============================================================================
# Scene:      RandyFlipsAndStacks
# Source:     videos/_2018/eop/chapter1/various_intro_visuals.py (lines 8-44)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/coin_flipping_pi_creature.py, _2018/eop/reusables/coin_stacks.py, _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl RandyFlipsAndStacks.py RandyFlipsAndStacks -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
#   - FlatCoin edge rebuilt with GL path calls (arc, line down, shifted arc reversed, line up): the Cairo cubic point-list construction draws loops with GL quadratic curves
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *


# ----- From _2018/eop/reusables/eop_constants.py -----

COIN_RADIUS = 0.18


COIN_THICKNESS = 0.4 * COIN_RADIUS


COIN_FORESHORTENING = 0.5


COIN_NB_RIDGES = 20


COIN_STROKE_WIDTH = 2


GRADE_COLOR_1 = COLOR_HEADS = RED_E


GRADE_COLOR_2 = COLOR_TAILS = BLUE_C


COLOR_HEADS_COIN = RED


COLOR_TAILS_COIN = BLUE_E


TALLY_BACKGROUND_WIDTH = 1.0


TALLY_BACKGROUND_COLOR = BLACK



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


class FlatCoin(UprightCoin):
# For use in coin stacks
    CONFIG = {
        "thickness": COIN_THICKNESS,
        "foreshortening": COIN_FORESHORTENING,
        "nb_ridges": COIN_NB_RIDGES
    }

    def __init__(self, **kwargs):
        UprightCoin.__init__(self, **kwargs)
        self.symbol_mob.rotate(TAU/8)
        self.stretch_in_place(self.foreshortening, 1)
        
        # draw the edge
        # CHANGE: Cairo built the edge with cubic anchors/handles by index; GL curves are quadratic, so the same list of points drew loops.
        # Rebuild it as: front arc (indices 12:25), straight line down, the shifted arc backwards, straight line up.
        arc_points = self.get_points()[12:25]
        shifted_arc_points = self.copy().shift(self.thickness * DOWN).get_points()[12:25]
        edge = VMobject()
        edge.set_points(np.array(arc_points))
        edge.add_line_to(arc_points[-1] + self.thickness * DOWN)
        back_points = shifted_arc_points[::-1]
        for k in range(1, len(back_points) - 1, 2):
            edge.add_quadratic_bezier_curve_to(back_points[k], back_points[k + 1])
        edge.add_line_to(arc_points[0])
        edge.set_fill(
            color = self.fill_color,
            opacity = self.fill_opacity
        )
        edge.set_stroke(width = self.stroke_width)
        self.add(edge)

        # draw the ridges
        PI = TAU/2
        dtheta = PI/self.nb_ridges
        ridge_angles = np.arange(dtheta,PI,dtheta)
        # add a twist onto each coin
        ridge_angles += np.random.rand(1) * dtheta
        # crop the angles that overshoot on either side
        ridge_angles = ridge_angles[(ridge_angles > 0) * (ridge_angles < PI)]
        ridge_positions = 0.5 * 2 * self.radius * np.array([
            np.cos(theta) for theta in ridge_angles
        ])
        ridge_color = interpolate_color(self.stroke_color, self.fill_color, 0.7)
        for x in ridge_positions:
            y = -(1 - (x/self.radius)**2)**0.5 * self.foreshortening * self.radius
            ridge = Line(
                x * RIGHT + y * UP,
                x * RIGHT + y * UP + self.thickness * DOWN,
                stroke_color = ridge_color,
                stroke_width = self.stroke_width
            )
            self.add(ridge)

        # redraw the unfilled edge to cover the ridge ends
        empty_edge = edge.copy()
        empty_edge.set_fill(opacity = 0)
        self.add(empty_edge)


class FlatHeads(FlatCoin):
    CONFIG = {
        "fill_color": COLOR_HEADS_COIN,
        "symbol": "H",
    }


class FlatTails(FlatCoin):
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



# ----- From _2018/eop/reusables/coin_stacks.py -----

class CoinStack(VGroup):
    CONFIG = {
        "coin_thickness": COIN_THICKNESS,
        "size": 5,
        "face": FlatCoin,
    }

    def init_points(self):
        for n in range(self.size):
            coin = self.face(thickness = self.coin_thickness)
            coin.shift(n * self.coin_thickness * UP)
            self.add(coin)
        if self.size == 0:
            point = VectorizedPoint()
            self.add(point)


class HeadsStack(CoinStack):
    CONFIG = {
        "face": FlatHeads
    }


class TailsStack(CoinStack):
    CONFIG = {
        "face": FlatTails
    }


class DecimalTally(TexText):

    def __init__(self, heads, tails, **kwargs):

        TexText.__init__(self, str(heads), "\\textemdash\,", str(tails), **kwargs)
        self[0].set_color(COLOR_HEADS)
        self[-1].set_color(COLOR_TAILS)


class TallyStack(VGroup):
    CONFIG = {
        "coin_thickness": COIN_THICKNESS,
        "show_decimals": True
    }

    def __init__(self, h, t, anchor = ORIGIN, **kwargs):
        self.nb_heads = h
        self.nb_tails = t
        self.anchor = anchor
        VGroup.__init__(self,**kwargs)

    def init_points(self):
        stack1 = HeadsStack(size = self.nb_heads, coin_thickness = self.coin_thickness)
        stack2 = TailsStack(size = self.nb_tails, coin_thickness = self.coin_thickness)
        stack1.next_to(self.anchor, LEFT, buff = 0.5 * SMALL_BUFF)
        stack2.next_to(self.anchor, RIGHT, buff = 0.5 * SMALL_BUFF)
        stack1.align_to(self.anchor, DOWN)
        stack2.align_to(self.anchor, DOWN)
        self.heads_stack = stack1
        self.tails_stack = stack2
        self.add(stack1, stack2)
        self.background_rect = background_rect = RoundedRectangle(
            width = TALLY_BACKGROUND_WIDTH,
            height = TALLY_BACKGROUND_WIDTH,
            corner_radius = 0.1,
            fill_color = TALLY_BACKGROUND_COLOR,
            fill_opacity = 1.0,
            stroke_width = 3
        ).align_to(self.anchor, DOWN).shift(0.1 * DOWN)
        self.add_to_back(background_rect)

        self.decimal_tally = DecimalTally(self.nb_heads, self.nb_tails)
        self.position_decimal_tally(self.decimal_tally)
        if self.show_decimals:
            self.add(self.decimal_tally)

    def position_decimal_tally(self, decimal_tally):
        decimal_tally.match_width(self.background_rect)
        decimal_tally.scale(0.6)
        decimal_tally.next_to(self.background_rect.get_top(), DOWN, buff = 0.15)
        return decimal_tally


    def move_anchor_to(self, new_anchor):
        for submob in self.submobjects:
            submob.shift(new_anchor - self.anchor)

        self.anchor = new_anchor
        self.position_decimal_tally(self.decimal_tally)

        return self



# ----- From _2018/eop/chapter1/various_intro_visuals.py -----

class RandyFlipsAndStacks(Scene):

    def construct(self):

        randy = CoinFlippingPiCreature(color = MAROON_E)
        randy.scale(0.5).to_edge(LEFT + DOWN)

        heads = tails = 0
        tally = TallyStack(heads, tails, anchor = ORIGIN)

        nb_flips = 10

        flips = np.random.randint(2, size = nb_flips)

        for i in range(nb_flips):

            self.play(FlipCoin(randy))
            self.wait(0.5)

            flip = flips[i]
            if flip == 0:
                heads += 1
            elif flip == 1:
                tails += 1
            else:
                raise Exception("That side does not exist on this coin")

            new_tally = TallyStack(heads, tails, anchor = ORIGIN)

            if tally.nb_heads == 0 and new_tally.nb_heads == 1:
                self.play(FadeIn(new_tally.heads_stack))
            elif tally.nb_tails == 0 and new_tally.nb_tails == 1:
                self.play(FadeIn(new_tally.tails_stack))
            else:
                self.play(Transform(tally, new_tally))

            tally = new_tally
