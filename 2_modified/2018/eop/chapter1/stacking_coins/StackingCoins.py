# ==============================================================================
# Scene:      StackingCoins
# Source:     videos/_2018/eop/chapter1/stacking_coins.py (lines 5-29)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/coin_stacks.py, _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl StackingCoins.py StackingCoins -w -m --fps 15
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



# ----- From _2018/eop/chapter1/stacking_coins.py -----

class StackingCoins(Scene):

    def construct(self):

        h = t = 0
        heads_stack = HeadsStack(size = h)
        heads_stack.next_to(0.5*LEFT + 3*DOWN, UP)
        tails_stack = TailsStack(size = t)
        tails_stack.next_to(0.5*RIGHT + 3*DOWN, UP)
        self.add(heads_stack, tails_stack)

        for i in range(120):
            flip = np.random.choice(["H", "T"])
            if flip == "H":
                h += 1
                new_heads_stack = HeadsStack(size = h)
                new_heads_stack.next_to(0.5*LEFT + 3*DOWN, UP)
                self.play(Transform(heads_stack, new_heads_stack,
                    run_time = 0.2))
            elif flip == "T":
                t += 1
                new_tails_stack = TailsStack(size = t)
                new_tails_stack.next_to(0.5*RIGHT + 3*DOWN, UP)
                self.play(Transform(tails_stack, new_tails_stack,
                    run_time = 0.2))
