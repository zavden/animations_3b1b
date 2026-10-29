# ==============================================================================
# Scene:      ShowProbsInBrickRow3
# Source:     videos/_2018/eop/chapter1/brick_row_scene.py (lines 951-985)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/brick_row.py, _2018/eop/reusables/coin_flipping_pi_creature.py, _2018/eop/reusables/coin_stacks.py, _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/eop_helpers.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl ShowProbsInBrickRow3.py ShowProbsInBrickRow3 -w -m --fps 15
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


class SplitRectsInBrickWall(AnimationGroup):

    def __init__(self, mobject, **kwargs):

        #print mobject.height, mobject.get_height()
        r = self.subdiv_level = mobject.subdiv_level + 1
        
        subdivs = VGroup()
        x = -0.5 * mobject.get_width()

        anims = []
        for k in range(0, r):
            proportion = float(choose(r,k)) / 2**r
            x += proportion * mobject.get_width()
            subdiv = DashedLine(
                mobject.get_top() + x * RIGHT,
                mobject.get_bottom() + x * RIGHT,
                dash_length = 0.05
            )
            subdivs.add(subdiv)
            anims.append(ShowCreation(subdiv))

        mobject.add(subdivs)
        AnimationGroup.__init__(self, *anims, **kwargs)



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



# ----- From _2018/eop/chapter1/brick_row_scene.py -----

class BrickRowScene(PiCreatureScene):


    def split_tallies(self, row, direction = DOWN):
        # Split all tally symbols at once and move the copies
        # either horizontally on top of the brick row
        # or diagonally into the bricks

        self.tallies_copy = self.tallies.copy()
        self.add_foreground_mobject(self.tallies_copy)

        tally_targets_left = [
            rect.get_center() + 0.25 * rect.get_width() * LEFT 
            for rect in row.rects
        ]

        tally_targets_right = [
            rect.get_center() + 0.25 * rect.get_width() * RIGHT 
            for rect in row.rects
        ]

        if np.all(direction == LEFT) or np.all(direction == RIGHT):

            tally_y_pos = self.tallies[0].anchor[1]
            for target in tally_targets_left:
                target[1] = tally_y_pos
            for target in tally_targets_right:
                target[1] = tally_y_pos

        for (i, tally) in enumerate(self.tallies):

            target_left = tally_targets_left[i]
            new_tally_left = TallyStack(tally.nb_heads + 1, tally.nb_tails)
            new_tally_left.move_anchor_to(target_left)
            v = target_left - tally.anchor
            
            self.play(
                tally.move_anchor_to, target_left,
            )
            tally.anchor = target_left
            self.play(Transform(tally, new_tally_left))
            
            tally_copy = self.tallies_copy[i]

            target_right = tally_targets_right[i]
            new_tally_right = TallyStack(tally.nb_heads, tally.nb_tails + 1)
            new_tally_right.move_anchor_to(target_right)
            v = target_right - tally_copy.anchor
            
            self.play(tally_copy.move_anchor_to, target_right)
            tally_copy.anchor = target_right
            self.play(Transform(tally_copy, new_tally_right))

            tally_copy.nb_heads = new_tally_right.nb_heads
            tally_copy.nb_tails = new_tally_right.nb_tails
            tally.nb_heads = new_tally_left.nb_heads
            tally.nb_tails = new_tally_left.nb_tails




    def tally_split_animations(self, row, direction = DOWN):
        # Just creates the animations and returns them
        # Execution can be timed afterwards
        # Returns two lists: first all those going left, then those to the right

        self.tallies_copy = self.tallies.copy()
        self.add_foreground_mobject(self.tallies_copy)

        tally_targets_left = [
            rect.get_center() + 0.25 * rect.get_width() * LEFT 
            for rect in row.rects
        ]

        tally_targets_right = [
            rect.get_center() + 0.25 * rect.get_width() * RIGHT 
            for rect in row.rects
        ]

        if np.all(direction == LEFT) or np.all(direction == RIGHT):

            tally_y_pos = self.tallies[0].anchor[1]
            for target in tally_targets_left:
                target[1] = tally_y_pos
            for target in tally_targets_right:
                target[1] = tally_y_pos


        anims1 = []

        for (i, tally) in enumerate(self.tallies):

            new_tally_left = TallyStack(tally.nb_heads + 1, tally.nb_tails)
            target_left = tally_targets_left[i]
            new_tally_left.move_to(target_left)

            anims1.append(Transform(tally, new_tally_left))
            
            tally.anchor = target_left
            tally.nb_heads = new_tally_left.nb_heads
            tally.nb_tails = new_tally_left.nb_tails
            

        anims2 = []

        for (i, tally) in enumerate(self.tallies_copy):

            new_tally_right = TallyStack(tally.nb_heads, tally.nb_tails + 1)
            target_right = tally_targets_right[i]
            new_tally_right.move_to(target_right)
            
            anims2.append(Transform(tally, new_tally_right))

            tally.anchor = target_right
            tally.nb_heads = new_tally_right.nb_heads
            tally.nb_tails = new_tally_right.nb_tails

        return anims1, anims2



    def split_tallies_at_once(self, row, direction = DOWN):
        anims1, anims2 = self.tally_split_animations(row, direction = direction)
        self.play(*(anims1 + anims2))

    def split_tallies_in_two_steps(self, row, direction = DOWN):
        # First all those to the left, then those to the right
        anims1, anims2 = self.tally_split_animations(row, direction = direction)
        self.play(*anims1)
        self.wait(0.3)
        self.play(*anims2)




    def merge_rects_by_subdiv(self, row):

        half_merged_row = row.copy()
        half_merged_row.subdiv_level += 1
        half_merged_row.init_points()
        half_merged_row.move_to(row)

        self.play(FadeIn(half_merged_row))
        self.remove(row)
        return half_merged_row




    def merge_tallies(self, row, target_pos = UP):
        
        r = row.subdiv_level
        
        if np.all(target_pos == DOWN):
            tally_targets = [
                rect.get_center()
                for rect in row.get_rects_for_level(r)
            ]
        elif np.all(target_pos == UP):
            y_pos = row.get_center()[1] + 1.2 * 0.5 * row.get_height()
            for target in tally_targets:
                target[1] = y_pos
        else:
            raise Exception("Invalid target position (either UP or DOWN)")

        anims = []
        for (tally, target) in zip(self.tallies[1:], tally_targets[1:-1]):
            anims.append(tally.move_anchor_to)
            anims.append(target)

        for (tally, target) in zip(self.tallies_copy[:-1], tally_targets[1:-1]):
            anims.append(tally.move_anchor_to)
            anims.append(target)

        self.play(*anims)
        # update anchors
        for (tally, target) in zip(self.tallies[1:], tally_targets[1:-1]):
            tally.anchor = target
        for (tally, target) in zip(self.tallies_copy[:-1], tally_targets[1:-1]):
            tally.anchor = target

        self.remove(self.tallies_copy)
        self.tallies.add(self.tallies_copy[-1])


    def merge_rects_by_coloring(self, row):

        merged_row = row.copy()
        merged_row.coloring_level += 1
        merged_row.init_points()
        merged_row.move_to(row)

        self.play(FadeIn(merged_row))
        self.remove(row)
        return merged_row



    def move_tallies_on_top(self, row):
        self.play(
            self.tallies.shift, 1.2 * 0.5 * row.height * UP
        )
        for tally in self.tallies:
            tally.anchor += 1.2 * 0.5 * row.height * UP

    def create_pi_creature(self):
        randy = CoinFlippingPiCreature(color = MAROON_E)
        return randy





        

    def construct(self):
        self.force_skipping()
        
        randy = self.get_primary_pi_creature()
        randy = randy.scale(0.5).move_to(3*DOWN + 6*LEFT)
        #self.add(randy)
        self.row = BrickRow(0, height = 2, width = 10)
        self.wait()

        self.play(FadeIn(self.row))

        self.wait()


        # move in all kinds of sequences
        coin_seqs = VGroup()
        for i in range(20):
            n = np.random.randint(1,10)
            seq = [np.random.choice(["H", "T"]) for j in range(n)]
            coin_seq = CoinSequence(seq).scale(1.5)
            loc = np.random.uniform(low = -10, high = 10) * RIGHT
            loc += np.random.uniform(low = -6, high = 6) * UP
            coin_seq.move_to(loc)
            
            coin_seq.target = coin_seq.copy().scale(0.3).move_to(0.4 * loc)
            coin_seq.target.fade(1)
            coin_seqs.add(coin_seq)

        self.play(
            LaggedStartMap(
                Succession, coin_seqs, lambda m: (FadeIn(m, run_time = 0.1), MoveToTarget(m)),
                run_time = 5,
                lag_ratio = 0.5
            )
        )
        
        # # # # # # # #
        # FIRST  FLIP #
        # # # # # # # #


        self.play(FlipCoin(randy))

        self.play(SplitRectsInBrickWall(self.row))
        self.row = self.merge_rects_by_subdiv(self.row)
        self.row = self.merge_rects_by_coloring(self.row)
        #
        # put tallies on top

        single_flip_labels = VGroup(UprightHeads(), UprightTails())
        for (label, rect) in zip(single_flip_labels, self.row.rects):
            label.next_to(rect, UP)
            self.play(FadeIn(label))
            self.wait()

        self.wait()


        # # # # # # # #
        # SECOND FLIP #
        # # # # # # # #

        self.play(FlipCoin(randy))
        self.wait()

        self.play(
            SplitRectsInBrickWall(self.row)
        )
        self.wait()


        # split sequences
        single_flip_labels_copy = single_flip_labels.copy()
        self.add(single_flip_labels_copy)

        
        v = self.row.get_outcome_centers_for_level(2)[0] - single_flip_labels[0].get_center()
        self.play(
            single_flip_labels.shift, v
        )
        new_heads = VGroup(UprightHeads(), UprightHeads())
        for i in range(2):
            new_heads[i].move_to(single_flip_labels[i])
            new_heads[i].shift(COIN_SEQUENCE_SPACING * DOWN)
        self.play(FadeIn(new_heads))

        v = self.row.get_outcome_centers_for_level(2)[-1] - single_flip_labels_copy[-1].get_center()
        self.play(
            single_flip_labels_copy.shift, v
        )
        new_tails = VGroup(UprightTails(), UprightTails())
        for i in range(2):
            new_tails[i].move_to(single_flip_labels_copy[i])
            new_tails[i].shift(COIN_SEQUENCE_SPACING * DOWN)
        self.play(FadeIn(new_tails))

        self.add_foreground_mobject(single_flip_labels)
        self.add_foreground_mobject(new_heads)
        self.add_foreground_mobject(single_flip_labels_copy)
        self.add_foreground_mobject(new_tails)

        # get individual outcomes
        outcomes = self.row.get_outcome_rects_for_level(2, with_labels = False,
            inset = True)
        grouped_outcomes = VGroup(outcomes[0], outcomes[1:3], outcomes[3])

        decimal_tallies = VGroup()
        # introduce notion of tallies
        rects = self.row.get_rects_for_level(2)

        rect = rects[0]
        tally = DecimalTally(2,0)
        tally.next_to(rect, UP)
        decimal_tallies.add(tally)
        self.play(
            FadeIn(tally),
            FadeIn(grouped_outcomes[0])
        )
        self.wait()

        rect = rects[1]
        tally = DecimalTally(1,1)
        tally.next_to(rect, UP)
        decimal_tallies.add(tally)
        self.play(
            FadeIn(tally),
            FadeOut(grouped_outcomes[0]),
            FadeIn(grouped_outcomes[1])
        )
        self.wait()

        rect = rects[2]
        tally = DecimalTally(0,2)
        tally.next_to(rect, UP)
        decimal_tallies.add(tally)
        self.play(
            FadeIn(tally),
            FadeOut(grouped_outcomes[1]),
            FadeIn(grouped_outcomes[2])
        )
        self.wait()

        self.play(
            FadeOut(grouped_outcomes[2])
        )
        self.wait()

        self.wait()
        self.play(
            FadeOut(single_flip_labels),
            FadeOut(new_heads),
            FadeOut(single_flip_labels_copy),
            FadeOut(new_tails)
        )
        self.wait()

        self.tallies = VGroup()
        for (i, rect) in enumerate(self.row.get_rects_for_level(2)):
            tally = TallyStack(2-i, i, show_decimals = False)
            tally.move_to(rect)
            self.tallies.add(tally)


        self.play(FadeIn(self.tallies))
        self.wait()


        anims = []
        for (decimal_tally, tally_stack) in zip(decimal_tallies, self.tallies):
            anims.append(ApplyFunction(
                tally_stack.position_decimal_tally, decimal_tally
            ))
        
        self.play(*anims)
        self.wait()


        # replace the original decimal tallies with
        # the ones that belong to the TallyStacks
        for (decimal_tally, tally_stack) in zip(decimal_tallies, self.tallies):
            self.remove(decimal_tally)
            tally_stack.position_decimal_tally(tally_stack.decimal_tally)
            tally_stack.add(tally_stack.decimal_tally)
        
        self.add_foreground_mobject(self.tallies)
        self.row = self.merge_rects_by_subdiv(self.row)
        self.wait()
        self.row = self.merge_rects_by_coloring(self.row)
        self.wait()
        

        # # # # # # # # # # # # #
        # CALLBACK TO SEQUENCES #
        # # # # # # # # # # # # #

        outcomes = self.row.get_outcome_rects_for_level(2, with_labels = True,
            inset = True)
        subdivs = self.row.get_sequence_subdivs_for_level(2)
        self.play(
            FadeIn(outcomes),
            FadeIn(subdivs),
            FadeOut(self.tallies)
        )

        self.wait()

        rect_to_dice = self.row.get_outcome_rects_for_level(2, with_labels = False,
            inset = False)[1]
        N = 10
        dice_width = rect_to_dice.get_width()/N
        dice_height = rect_to_dice.get_height()/N
        prototype_dice = Rectangle(
            width = dice_width,
            height = dice_height,
            stroke_width = 2,
            stroke_color = WHITE,
            fill_color = WHITE,
            fill_opacity = 0
        )
        prototype_dice.align_to(rect_to_dice, direction = UP)
        prototype_dice.align_to(rect_to_dice, direction = LEFT)
        all_dice = VGroup()
        for i in range(N):
            for j in range(N):
                dice_copy = prototype_dice.copy()
                dice_copy.shift(j * dice_width * RIGHT + i * dice_height * DOWN)
                all_dice.add(dice_copy)

        self.play(
            LaggedStartMap(FadeIn, all_dice),
            FadeOut(outcomes[1])
        )
        self.wait()

        table = Ellipse(width = 1.5, height = 1)
        table.set_fill(color = GREEN_E, opacity = 1)
        table.next_to(rect_to_dice, UP)
        self.add(table)
        coin1 = UprightHeads(radius = 0.1)
        coin2 = UprightTails(radius = 0.1)

        def get_random_point_in_ellipse(ellipse):
            width = ellipse.get_width()
            height = ellipse.get_height()
            x = y = 1
            while x**2 + y**2 > 0.9:
                x = np.random.uniform(-1,1)
                y = np.random.uniform(-1,1)            
            x *= width/2
            y *= height/2
            return ellipse.get_center() + x * RIGHT + y * UP


        for dice in all_dice:
            p1 = get_random_point_in_ellipse(table)
            p2 = get_random_point_in_ellipse(table)
            coin1.move_to(p1)
            coin2.move_to(p2)
            self.add(coin1, coin2)
            self.play(
                ApplyMethod(dice.set_fill, {"opacity" : 0.5},
                    rate_func = there_and_back,
                    run_time = 0.05)
            )

        self.wait()

        self.play(
            FadeOut(outcomes),
            FadeOut(subdivs),
            FadeOut(all_dice),
            FadeOut(table),
            FadeOut(coin1),
            FadeOut(coin2),
            FadeIn(self.tallies)
        )

        self.wait()

        # # # # # # # #
        # THIRD  FLIP #
        # # # # # # # #

        # move row up, leave a copy without tallies below
        new_row = self.row.copy()
        self.clear()
        self.add(randy, self.row, self.tallies)
        self.bring_to_back(new_row)
        self.play(
            self.row.shift, 2.5 * UP,
            self.tallies.shift, 2.5 * UP,
        )

        old_row = self.row
        self.row = new_row

        self.play(FlipCoin(randy))

        self.wait()

        self.play(
            SplitRectsInBrickWall(self.row)
        )
        self.wait()

        self.split_tallies_in_two_steps(self.row)
        self.wait()

        self.add_foreground_mobject(self.tallies)
        self.add_foreground_mobject(self.tallies_copy)


        

        self.remove(new_row)
        new_row = self.row



        self.clear()
        self.add(randy, self.row, old_row)
        self.add_foreground_mobject(self.tallies)
        self.add_foreground_mobject(self.tallies_copy)
        

        self.play(
            self.row.fade, 0.7,
            old_row.fade, 0.7,
            FadeOut(self.tallies),
            FadeOut(self.tallies_copy),
        )

        
        # # # # # # # # # # # # # # # # #
        # SHOW SPLITTING  WITH OUTCOMES #
        # # # # # # # # # # # # # # # # #

        # # show individual outcomes
        # old_outcomes = old_row.get_outcome_rects_for_level(2, with_labels = True)
        # old_outcomes_copy = old_outcomes.copy()
        # new_outcomes = self.row.get_outcome_rects_for_level(3, with_labels = True)
        
        # self.play(
        #     FadeIn(old_outcomes[0]),
        #     FadeIn(old_outcomes_copy[0]),
        # )

        # self.wait()

        # self.play(
        #     Transform(old_outcomes_copy[0], new_outcomes[1])
        # )

        # self.wait()

        # self.play(
        #     FadeIn(old_outcomes[1:3]),
        #     FadeIn(old_outcomes_copy[1:3]),
        # )

        # self.wait()

        # self.play(
        #     Transform(old_outcomes_copy[1:3], new_outcomes[2:4])
        # )

        # self.wait()

        # self.row = self.merge_rects_by_subdiv(self.row)
        # self.wait()

        # self.play(
        #     FadeOut(old_row),
        #     FadeOut(old_outcomes[0:3]),
        #     FadeOut(new_outcomes[1:4]),
        #     self.row.fade,0,
        #     FadeIn(self.tallies[1]),
        #     FadeIn(self.tallies_copy[0]),
        # )

        # # rest of the new row
        # self.play(
        #     FadeIn(self.tallies[:1]),
        #     FadeIn(self.tallies[2:]),
        #     FadeIn(self.tallies_copy[1:])
        # )

        # self.wait()

        # self.merge_tallies(self.row, target_pos = DOWN)
        # self.add_foreground_mobject(self.tallies)
        # self.row = self.merge_rects_by_coloring(self.row)
        # self.wait()


        # # # # # # # # # # # # # # # #
        # SHOW SPLITTING WITH TALLIES #
        # # # # # # # # # # # # # # # #

        tally_left = TallyStack(2,0)
        tally_left.move_to(old_row.rects[0])
        tally_right = TallyStack(1,1)
        tally_right.move_to(old_row.rects[1])

        rect_left = old_row.rects[0].copy()
        rect_right = old_row.rects[1].copy()

        self.play(
            FadeIn(rect_left),
            FadeIn(rect_right),
            FadeIn(tally_left),
            FadeIn(tally_right)
        )

        rect_left.target = rect_left.copy()
        rect_left.target.stretch(0.5,0)
        left_target_pos = self.row.get_outcome_centers_for_level(3)[1]
        left_v = left_target_pos - rect_left.get_center()
        rect_left.target.move_to(left_target_pos)

        rect_right.target = rect_right.copy()
        rect_right.target.stretch(0.5,0)
        right_target_pos = 0.5 * (self.row.get_outcome_centers_for_level(3)[2] + self.row.get_outcome_centers_for_level(3)[3])
        right_v = right_target_pos - rect_right.get_center()
        rect_right.target.move_to(right_target_pos)

        self.play(
            MoveToTarget(rect_left),
            tally_left.move_to, left_target_pos
        )
        #tally_left.anchor += left_v
        
        self.wait()

        new_tally_left = TallyStack(2,1)
        #new_tally_left.move_anchor_to(tally_left.anchor)
        new_tally_left.move_to(tally_left)
        
        self.play(
            Transform(tally_left, new_tally_left)
        )

        self.play(
            MoveToTarget(rect_right),
            tally_right.move_to, right_target_pos
        )
        #tally_right.anchor += right_v
        
        self.wait()
        new_tally_right = TallyStack(2,1)
        #new_tally_right.move_anchor_to(tally_right.anchor)
        new_tally_right.move_to(tally_right)

        self.play(
            Transform(tally_right, new_tally_right)
        )

        self.wait()

        self.row = self.merge_rects_by_subdiv(self.row)
        self.wait()

        self.play(
            FadeOut(old_row),
            self.row.fade,0,
            FadeOut(new_tally_left),
            FadeOut(new_tally_right),
            FadeIn(self.tallies[1]),
            FadeIn(self.tallies_copy[0]),
        )

        # rest of the new row
        self.play(
            FadeIn(self.tallies[:1]),
            FadeIn(self.tallies[2:]),
            FadeIn(self.tallies_copy[1:])
        )

        self.wait()

        self.merge_tallies(self.row, target_pos = DOWN)
        self.add_foreground_mobject(self.tallies)
        self.row = self.merge_rects_by_coloring(self.row)
        self.wait()

        
        # show the 8 individual outcomes
        outcomes = self.row.get_outcome_rects_for_level(3,
            with_labels = True,
            inset = True)
        self.play(FadeOut(self.tallies))
        self.wait()
        self.play(LaggedStartMap(
            FadeIn, outcomes,
            #rate_func = there_and_back_with_pause,
            run_time = 5))
        self.wait()

        braces = VGroup(*[Brace(rect, UP) for rect in self.row.rects])
        counts = [choose(3, i) for i in range(4)]
        probs = VGroup(*[Tex("{" + str(k) + "\over 8}") for k in counts])
        for (brace, prob) in zip(braces, probs):
            prob.next_to(brace, UP)


        self.play(
            LaggedStartMap(ShowCreation, braces),
            LaggedStartMap(Write, probs)
        )
        self.wait()
        self.play(LaggedStartMap(
            FadeOut, outcomes,
            #rate_func = there_and_back_with_pause,
            run_time = 5),
        )
        self.play(
            FadeIn(self.tallies)
        )
        self.wait()

        self.play(
            FadeOut(braces),
            FadeOut(probs)
        )
        self.wait()
 

        # put visuals for other probability distribtuions here

        # back to three coin flips, show all 8 outcomes
        run_time = 5
        self.play(
            LaggedStartMap(FadeIn, outcomes,
                #rate_func = there_and_back_with_pause,
                run_time = run_time),
            FadeOut(self.tallies,
                run_time = run_time)
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, outcomes,
                #rate_func = there_and_back_with_pause,
                run_time = 5),
            FadeIn(self.tallies,
                run_time = run_time)
        )




        # # # # # # # #
        # FOURTH FLIP #
        # # # # # # # #



        
        previous_row = self.row.copy()
        self.add(previous_row)

        v = 1.25 * self.row.height * UP
        self.play(
            previous_row.shift, v,
            self.tallies.shift, v,
        )
        self.add_foreground_mobject(self.tallies)

        self.play(
            SplitRectsInBrickWall(self.row)
        )
        self.wait()

        self.row = self.merge_rects_by_subdiv(self.row)
        

        self.revert_to_original_skipping_status()

        self.wait()

        n = 3 # level to split
        k = 1 # tally to split

        # show individual outcomes
        outcomes = previous_row.get_outcome_rects_for_level(n,
            with_labels = False,
            inset = True
        )
        grouped_outcomes = VGroup()
        index = 0
        for i in range(n + 1):
            size = choose(n,i)
            grouped_outcomes.add(VGroup(outcomes[index:index + size]))
            index += size


        grouped_outcomes_copy = grouped_outcomes.copy()

        original_grouped_outcomes = grouped_outcomes.copy()
        # for later reference

        self.play(
            LaggedStartMap(FadeIn, grouped_outcomes),
            LaggedStartMap(FadeIn, grouped_outcomes_copy),
        )
        self.wait()

        # show how the outcomes in one tally split into two copies
        # going into the neighboring tallies

        #self.revert_to_original_skipping_status()

        target_outcomes = self.row.get_outcome_rects_for_level(n + 1,
            with_labels = False,
            inset = True
        )
        grouped_target_outcomes = VGroup()
        index = 0
        old_tally_sizes = [choose(n,i) for i in range(n + 1)]
        new_tally_sizes = [choose(n + 1,i) for i in range(n + 2)]
                
        for i in range(n + 2):
            size = new_tally_sizes[i]
            grouped_target_outcomes.add(VGroup(target_outcomes[index:index + size]))
            index += size

        old_tally_sizes.append(0) # makes the edge cases work properly
        
        # split all tallies
        for i in range(n + 1):
            self.play(
                Transform(grouped_outcomes[i][0],
                    grouped_target_outcomes[i][0][old_tally_sizes[i - 1]:]
                ),
                Transform(grouped_outcomes_copy[i][0],
                    grouped_target_outcomes[i + 1][0][:old_tally_sizes[i]]
                )
            )
        return
        
        self.wait()

        # fade in new tallies
        new_rects = self.row.get_rects_for_level(4)
        new_tallies = VGroup(*[
            TallyStack(n + 1 - i, i).move_to(rect) for (i, rect) in enumerate(new_rects)
        ])
        self.play(FadeIn(new_tallies))
        self.add_foreground_mobject(new_tallies[1])
        # remove outcomes and sizes except for one tally
        anims = []
        for i in range(n + 1):
            if i != k - 1:
                anims.append(FadeOut(grouped_outcomes_copy[i]))
            if i != k:
                anims.append(FadeOut(grouped_outcomes[i]))
                anims.append(FadeOut(new_tallies[i]))

        #anims.append(FadeOut(self.tallies[0]))
        #anims.append(FadeOut(self.tallies[2:]))
        anims.append(FadeOut(new_tallies[-1]))

        self.play(*anims)

        self.wait()

        self.play(
            Transform(grouped_outcomes_copy[k - 1], original_grouped_outcomes[k - 1])
        )

        self.play(
            Transform(grouped_outcomes[k], original_grouped_outcomes[k])
        )

        new_rects = self.row.get_rects_for_level(n + 1)

        self.play(
            Transform(grouped_outcomes[k][0],grouped_target_outcomes[k][0][old_tally_sizes[k - 1]:]),
            Transform(grouped_outcomes_copy[k - 1][0],grouped_target_outcomes[k][0][:old_tally_sizes[k - 1]]),
        )

        self.play(
            FadeOut(previous_row),
            FadeOut(self.tallies),
        )

        self.row = self.merge_rects_by_coloring(self.row)

        self.play(
            FadeIn(new_tallies[0]),
            FadeIn(new_tallies[2:]),
        )




        # # # # # # # # # #
        # EVEN MORE FLIPS #
        # # # # # # # # # #

        self.play(FadeOut(new_tallies))
        self.clear()
        self.row = BrickRow(3)
        self.add(randy, self.row)       
        

        for i in range(3):

            self.play(FlipCoin(randy))

            self.wait()

            previous_row = self.row.copy()

            self.play(previous_row.shift, 1.25 * self.row.height * UP)

            self.play(
                SplitRectsInBrickWall(self.row)
            )
            self.wait()
            self.row = self.merge_rects_by_subdiv(self.row)
            self.wait()
            self.row = self.merge_rects_by_coloring(self.row)
            self.wait()

            self.play(FadeOut(previous_row))


class ShowProbsInBrickRow3(BrickRowScene):

    def construct(self):

        randy = self.get_primary_pi_creature()
        randy = randy.scale(0.5).move_to(3*DOWN + 6*LEFT)
        #self.add(randy)
        self.row = BrickRow(3, height = 2, width = 10)
        self.wait()

        self.add(self.row)

        tallies = VGroup()
        for (i, rect) in enumerate(self.row.get_rects_for_level(3)):
            tally = TallyStack(3-i, i, show_decimals = False)
            tally.move_to(rect)
            tallies.add(tally)

        self.add(tallies)
        self.wait(6)

        braces = VGroup(*[Brace(rect, UP) for rect in self.row.rects])
        counts = [choose(3, i) for i in range(4)]
        probs = VGroup(*[Tex("{" + str(k) + "\over 8}") for k in counts])
        for (brace, prob) in zip(braces, probs):
            prob.next_to(brace, UP)

        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, braces, run_time = 3),
            LaggedStartMap(Write, probs, run_time = 3)
        )
        self.wait()

        self.play(FadeOut(braces),FadeOut(probs))
