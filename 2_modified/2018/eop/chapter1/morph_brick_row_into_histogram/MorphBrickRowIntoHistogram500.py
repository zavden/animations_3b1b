# ==============================================================================
# Scene:      MorphBrickRowIntoHistogram500
# Source:     videos/_2018/eop/chapter1/morph_brick_row_into_histogram.py (lines 294-299)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/brick_row.py, _2018/eop/reusables/coin_stacks.py, _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/eop_helpers.py, _2018/eop/reusables/histograms.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl MorphBrickRowIntoHistogram500.py MorphBrickRowIntoHistogram500 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
#   - tallies initialised before the show_tallies check (the original used it unbound when show_tallies is False)
#   - FlatCoin edge rebuilt with GL path calls (arc, line down, shifted arc reversed, line up): the Cairo cubic point-list construction draws loops with GL quadratic curves
#   - choose(level, level//2): integer division (Python 2 / gave a float)
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


COIN_SEQUENCE_SPACING = 0.1


GRADE_COLOR_1 = COLOR_HEADS = RED_E


GRADE_COLOR_2 = COLOR_TAILS = BLUE_C


COLOR_HEADS_COIN = RED


COLOR_TAILS_COIN = BLUE_E


TALLY_BACKGROUND_WIDTH = 1.0


TALLY_BACKGROUND_COLOR = BLACK


OUTCOME_COLOR = WHITE


OUTCOME_OPACITY = 0.5



# ----- From _2018/eop/reusables/eop_helpers.py -----

def graded_color(n,k):
    if n != 0:
        alpha = float(k)/n
    else:
        alpha = 0.5
    color = interpolate_color(GRADE_COLOR_1, GRADE_COLOR_2, alpha)
    return color



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


class CoinSequence(VGroup):
    CONFIG = {
        "sequence": [],
        "radius" : COIN_RADIUS,
        "spacing": COIN_SEQUENCE_SPACING,
        "direction": RIGHT
    }

    def __init__(self, sequence, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.sequence = sequence
        offset = 0
        for symbol in self.sequence:
            if symbol == "H":
                new_coin = UprightHeads(radius = self.radius)
            elif symbol == "T":
                new_coin = UprightTails(radius = self.radius)
            else:
                new_coin = UprightCoin(symbol = symbol, radius = self.radius)
            new_coin.shift(offset * self.direction)
            self.add(new_coin)
            offset += self.spacing


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



# ----- From _2018/eop/reusables/brick_row.py -----

class BrickRow(VMobject):

    CONFIG = {
        "left_color" : COLOR_HEADS,
        "right_color" : COLOR_TAILS,
        "height" : 1.0,
        "width" : 8.0,
        "outcome_shrinkage_factor_x" : 0.95,
        "outcome_shrinkage_factor_y" : 0.94
    }

    def __init__(self, n, **kwargs):
        self.subdiv_level = n
        self.coloring_level = n
        VMobject.__init__(self, **kwargs)


    def init_points(self):

        self.submobjects = []
        self.rects = self.get_rects_for_level(self.coloring_level)
        self.add(self.rects)
        self.subdivs = self.get_subdivs_for_level(self.subdiv_level)
        self.add(self.subdivs)

        self.border = SurroundingRectangle(self,
            buff = 0, color = WHITE)
        self.add(self.border)



    def get_rects_for_level(self,r):
        rects = VGroup()
        for k in range(r + 1):
            proportion = float(choose(r,k)) / 2**r
            new_rect = Rectangle(
                width = proportion * self.width, 
                height = self.height,
                fill_color = graded_color(r,k),
                fill_opacity = 1,
                stroke_width = 0
            )
            if len(rects.submobjects) > 0:
                new_rect.next_to(rects,RIGHT,buff = 0)
            else:
                new_rect.next_to(self.get_center() + 0.5 * self.width * LEFT, RIGHT, buff = 0)
            rects.add(new_rect)
        return rects


    def get_subdivs_for_level(self,r):
        subdivs = VGroup()
        x = - 0.5 * self.width
        for k in range(0, r):
            proportion = float(choose(r,k)) / 2**r
            x += proportion * self.width
            subdiv = Line(
                x * RIGHT + 0.5 * self.height * UP,
                x * RIGHT + 0.5 * self.height * DOWN,
            )
            subdivs.add(subdiv)
        subdivs.move_to(self.get_center())
        return subdivs


    def get_sequence_subdivs_for_level(self,r):
        subdivs = VGroup()
        x = - 0.5 * self.width
        dx = 1.0 / 2**r
        for k in range(1, 2 ** r):
            proportion = dx
            x += proportion * self.width
            subdiv = DashedLine(
                x * RIGHT + 0.5 * self.height * UP,
                x * RIGHT + 0.5 * self.height * DOWN,
            )
            subdivs.add(subdiv)
        subdivs.move_to(self.get_center())
        return subdivs


    def get_outcome_centers_for_level(self,r):
        
        dpos = float(self.width) / (2 ** r) * RIGHT
        pos = 0.5 * self.width * LEFT + 0.5 * dpos
        centers = []
        for k in range(0, 2 ** r):
            centers.append(self.get_center() + pos + k * dpos)

        return centers

    def get_outcome_rects_for_level(self, r, inset = False, with_labels = False):

        centers = self.get_outcome_centers_for_level(r)
        if inset == True:
            outcome_width = self.outcome_shrinkage_factor_x * float(self.width) / (2 ** r)
            outcome_height = self.outcome_shrinkage_factor_y * self.height
        else:
            outcome_width = float(self.width) / (2 ** r)
            outcome_height = self.height
        
        corner_radius = 0.1 # max(0.1, 0.3 * min(outcome_width, outcome_height))
        # this scales down the corner radius for very narrow rects
        rect = RoundedRectangle(
            width = outcome_width,
            height = outcome_height,
            corner_radius = corner_radius,
            fill_color = OUTCOME_COLOR,
            fill_opacity = OUTCOME_OPACITY,
            stroke_width = 0
        )
        rects = VGroup()
        for center in centers:
            rects.add(rect.copy().move_to(center))

        rects.move_to(self.get_center())


        if with_labels == False:
            return rects

        # else
        sequences = self.get_coin_sequences_for_level(r)
        labels = VGroup()
        for (seq, rect) in zip(sequences, rects):
            coin_seq = CoinSequence(seq, direction = DOWN)
            coin_seq.shift(rect.get_center() - coin_seq.get_center())
            # not simply move_to bc coin_seq is not centered
            rect.add(coin_seq)
            rect.label = coin_seq

        return rects

    def get_coin_sequences_for_level(self,r):
        # array of arrays of characters
        if r < 0 or int(r) != r:
            raise Exception("Level must be a positive integer")
        if r == 0:
            return []
        if r == 1:
            return [["H"], ["T"]]

        previous_seq_array = self.get_coin_sequences_for_level(r - 1)
        subdiv_lengths = [choose(r - 1, k) for k in range(r)]

        seq_array = []
        index = 0
        for length in subdiv_lengths:
            
            for seq in previous_seq_array[index:index + length]:
                seq_copy = copy.copy(seq)
                seq_copy.append("H")
                seq_array.append(seq_copy)

            for seq in previous_seq_array[index:index + length]:
                seq_copy = copy.copy(seq)
                seq_copy.append("T")
                seq_array.append(seq_copy)
            index += length

        return seq_array


    def get_outcome_width_for_level(self,r):
        return self.width / (2**r)

    def get_rect_widths_for_level(self, r):
        ret_arr = []
        for k in range(0, r):
            proportion = float(choose(r,k)) / 2**r
            ret_arr.append(proportion * self.width)
        return ret_arr



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



# ----- From _2018/eop/reusables/histograms.py -----

class OutlineableBars(VGroup):

    # A group of bars (rectangles), together with
    # a method that draws an outline around them,
    # assuming the bars are arranged in a histogram
    # (aligned at the bottom without gaps).

    # We use this to morph a row of bricks into a histogram.

    CONFIG = {
        "outline_stroke_width" : 3,
        "stroke_color" : WHITE
    }
    def create_outline(self, animated = False, **kwargs):

        outline_points = []

        for (i, bar) in enumerate(self.submobjects):
            
            if i == 0:
                # start with the lower left
                outline_points.append(bar.get_corner(DOWN + LEFT))

            # upper two points of each bar
            outline_points.append(bar.get_corner(UP + LEFT))
            outline_points.append(bar.get_corner(UP + RIGHT))

            previous_bar = bar
        # close the outline
            # lower right
        outline_points.append(previous_bar.get_corner(DOWN + RIGHT))
            # lower left
        outline_points.append(outline_points[0])

        self.outline = Polygon(*outline_points,
            stroke_width = self.outline_stroke_width,
            stroke_color = self.stroke_color)

        if animated:
            self.play(FadeIn(self.outline, **kwargs))
        return self.outline



# ----- From _2018/eop/chapter1/morph_brick_row_into_histogram.py -----

class GenericMorphBrickRowIntoHistogram(Scene):

    CONFIG = {
        "level" : 3,
        "bar_width" : 2.0,
        "bar_anchor_height" : -3.0,
        "show_tallies" : False,
        "show_nb_flips" : True
    }

    def construct(self):

        self.row = BrickRow(self.level, height = self.bar_width, width = 10)
        self.bars = OutlineableBars(*[self.row.rects[i] for i in range(self.level + 1)])
        self.bar_anchors = [self.bar_anchor_height * UP + self.row.height * (i - 0.5 * self.level) * RIGHT for i in range(self.level + 1)]

        self.add(self.row)

        # CHANGE: tallies was only defined when show_tallies is True but always passed to FadeOut (bug of the original, UnboundLocalError)
        tallies = VMobject()
        if self.show_tallies:


            for (i,brick) in enumerate(self.row.rects):
                tally = TallyStack(self.level - i, i)
                tally.move_to(brick)
                self.add(tally)
                tallies.add(tally)
                brick.set_stroke(width = 3)

        if self.show_nb_flips:
            nb_flips_text = OldTexText("\# of flips: " + str(self.level))
            nb_flips_text.to_corner(UR)
            self.add(nb_flips_text)

        self.remove(self.row.subdivs, self.row.border)

        for rect in self.row.rects:
            rect.set_stroke(color = WHITE, width = 3)

        self.wait()
        self.play(
            self.row.rects.space_out_submobjects, {"factor" : 1.3},
            FadeOut(tallies)
        )
        self.wait()
        anims = []
        for brick in self.row.rects:
            anims.append(brick.rotate)
            anims.append(TAU/4)
        
        self.play(*anims)

        self.wait()

        anims = []
        for (i,brick) in enumerate(self.row.rects):
            anims.append(brick.next_to)
            anims.append(self.bar_anchors[i])
            anims.append({"direction" : UP, "buff" : 0})
        self.play(*anims)
        self.wait()

        self.bars.create_outline()
        anims = [
            ApplyMethod(rect.set_stroke, {"width" : 0})
                for rect in self.bars
        ]
        anims.append(FadeIn(self.bars.outline))
        self.play(*anims)

        self.wait()


class MorphBrickRowIntoHistogram20(GenericMorphBrickRowIntoHistogram):
    CONFIG = {
        "level" : 20,
        "prob_ticks" : 0.05,
        "bar_width" : 0.5,
        "bar_anchor_height" : -3.0,
        "x_ticks": 5
    }

    def construct(self):

        super(MorphBrickRowIntoHistogram20, self).construct()

        x_axis = Line(ORIGIN, 10 * RIGHT, color = WHITE, buff = 0)
        x_axis.next_to(self.bars, DOWN, buff = 0)
        #x_labels = VMobject(*[Tex(str(i)) for i in range(4)])
        x_labels = VMobject()
        for (i, bar) in enumerate(self.bars):
            if i % self.x_ticks != 0:
                continue
            label = Integer(i)
            label.next_to(self.bar_anchors[i], DOWN)
            x_labels.add(label)

        nb_tails_label = OldTexText("\# of tails")
        nb_tails_label.move_to(5 * RIGHT + 2.5 * DOWN)
        self.wait()

        self.play(
            FadeIn(x_axis),
            FadeIn(x_labels),
            FadeIn(nb_tails_label)
        )
        self.wait()

        # draw y-guides

        # CHANGE: Python 2 integer division: level//2 as the second argument of choose
        max_prob = float(choose(self.level, self.level//2)) / 2 ** self.level

        y_guides = VMobject()
        y_guide_heights = []
        prob_grid = np.arange(self.prob_ticks, 1.3 * max_prob, self.prob_ticks)
        for i in prob_grid:
            y_guide = Line(5 * LEFT, 5 * RIGHT, stroke_color = GREY)
            y_guide_height = self.bar_anchor_height + i * float(self.row.width)
            y_guide_heights.append(y_guide_height)
            y_guide.move_to(y_guide_height * UP)
            y_guide_label = DecimalNumber(i, num_decimal_places = 2, color = GREY)
            y_guide_label.scale(0.7)
            y_guide_label.next_to(y_guide, LEFT)
            y_guide.add(y_guide_label)
            y_guides.add(y_guide)

        self.bring_to_back(y_guides)
        self.play(FadeIn(y_guides), Animation(self.bars))
        self.wait()

        histogram_width = self.bars.get_width()
        histogram_height = self.bars.get_height()

        # scale to fit screen
        self.scale_x = 10.0/((len(self.bars) - 1) * self.bar_width)
        self.scale_y = 6.0/histogram_height


        anims = []
        for (bar, x_label) in zip(self.bars, x_labels):
            v = (self.scale_x - 1) * x_label.get_center()[0] * RIGHT
            anims.append(x_label.shift)
            anims.append(v)


        anims.append(self.bars.stretch_about_point)
        anims.append(self.scale_x)
        anims.append(0)
        anims.append(ORIGIN)
        anims.append(self.bars.outline.stretch_about_point)
        anims.append(self.scale_x)
        anims.append(0)
        anims.append(ORIGIN)

        self.play(*anims)
        self.wait()

        anims = []
        for (guide, i, h) in zip(y_guides, prob_grid, y_guide_heights):
            new_y_guide_height = self.bar_anchor_height + i * self.scale_y * float(self.row.width)
            v = (new_y_guide_height - h) * UP
            anims.append(guide.shift)
            anims.append(v)

        anims.append(self.bars.stretch_about_point)
        anims.append(self.scale_y)
        anims.append(1)
        anims.append(self.bars.get_bottom())
        anims.append(self.bars.outline.stretch_about_point)
        anims.append(self.scale_y)
        anims.append(1)
        anims.append(self.bars.get_bottom())

        self.play(*anims)
        self.wait()


class MorphBrickRowIntoHistogram500(MorphBrickRowIntoHistogram20):
    CONFIG = {
        "level" : 500,
        "x_ticks": 100,
        "prob_ticks": 0.01
    }
