# ==============================================================================
# Scene:      MillionFlips
# Source:     videos/_2018/eop/chapter1/million_flips.py (lines 5-96)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl MillionFlips.py MillionFlips -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
#   - import random re-added after `from random import *` (the star import rebinds random to a function)
#   - FlatCoin edge rebuilt with GL path calls (arc, line down, shifted arc reversed, line up): the Cairo cubic point-list construction draws loops with GL quadratic curves
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *
# CHANGE: `from random import *` rebinds the name random to the function random.random; re-import the module so random.random() works
import random


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



# ----- From _2018/eop/chapter1/million_flips.py -----

class MillionFlips(Scene):
    def construct(self):
        title = OldTexText("1{,}000{,}000 flips")
        title.to_edge(UP)
        self.add(title)

        small_wait_time = 1.0 / 15  # Um...

        n_flips_label = OldTexText("\\# Flips: ")
        n_heads_label = OldTexText("\\# Heads: ")
        n_flips_count = Integer(0)
        n_heads_count = Integer(0)
        n_heads_label.to_edge(RIGHT, buff=2 * LARGE_BUFF)
        n_flips_label.next_to(n_heads_label, DOWN, aligned_edge=LEFT)
        n_flips_count.next_to(n_flips_label[-1], RIGHT)
        n_heads_count.next_to(n_heads_label[-1], RIGHT)
        VGroup(n_flips_count, n_heads_count).shift(0.5 * SMALL_BUFF * UP)
        self.add(n_flips_label, n_heads_label, n_flips_count, n_heads_count)

        coins = VGroup(*[
            FlatHeads() if random.random() < 0.5 else FlatTails()
            for x in range(100)
        ])
        self.organize_group(coins)

        proportions = np.random.normal(0.5, 0.5 * 0.1, 100)
        hundred_boxes = VGroup(*[
            Square(
                stroke_width=1,
                stroke_color=WHITE,
                fill_opacity=1,
                fill_color=interpolate_color(COLOR_HEADS, COLOR_TAILS, prop)
            )
            for prop in proportions
        ])
        self.organize_group(hundred_boxes)

        ten_k_proportions = np.random.normal(0.5, 0.5 * 0.01, 100)
        ten_k_boxes = VGroup(*[
            Square(
                stroke_width=1,
                stroke_color=WHITE,
                fill_opacity=1,
                fill_color=interpolate_color(COLOR_HEADS, COLOR_TAILS, prop)
            )
            for prop in ten_k_proportions
        ])
        self.organize_group(ten_k_boxes)

        # Animations
        for coin in coins:
            self.add(coin)
            self.increment(n_flips_count)
            if isinstance(coin, FlatHeads):
                self.increment(n_heads_count)
            self.wait(small_wait_time)

        self.play(
            FadeIn(hundred_boxes[0]),
            coins.set_stroke, {"width": 0},
            coins.replace, hundred_boxes[0]
        )
        hundred_boxes[0].add(coins)
        for box, prop in list(zip(hundred_boxes, proportions))[1:]:
            self.add(box)
            self.increment(n_flips_count, 100)
            self.increment(n_heads_count, int(np.round(prop * 100)))
            self.wait(small_wait_time)

        self.play(
            FadeIn(ten_k_boxes[0]),
            hundred_boxes.set_stroke, {"width": 0},
            hundred_boxes.replace, ten_k_boxes[0]
        )
        ten_k_boxes[0].add(hundred_boxes)
        for box, prop in list(zip(ten_k_boxes, ten_k_proportions))[1:]:
            self.add(box)
            self.increment(n_flips_count, 10000)
            self.increment(n_heads_count, int(np.round(prop * 10000)))
            self.wait(small_wait_time)
        self.wait()

    def organize_group(self, group):
        group.arrange_in_grid(10)
        group.set_height(5)
        group.shift(DOWN + 2 * LEFT)

    def increment(self, integer_mob, value=1):
        new_int = Integer(integer_mob.number + value)
        new_int.move_to(integer_mob, DL)
        integer_mob.number += value
        integer_mob.submobjects = new_int.submobjects
