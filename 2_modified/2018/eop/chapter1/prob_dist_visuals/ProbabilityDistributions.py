# ==============================================================================
# Scene:      ProbabilityDistributions
# Source:     videos/_2018/eop/chapter1/prob_dist_visuals.py (lines 5-307)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/brick_row.py, _2018/eop/reusables/coin_stacks.py, _2018/eop/reusables/dice.py, _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/eop_helpers.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl ProbabilityDistributions.py ProbabilityDistributions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
#   - removed self.ensure_valid_file() (GL SVGMobject has no such method; it resolves file_name itself)
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



# ----- From _2018/eop/reusables/dice.py -----

class DieFace(SVGMobject):
    
    def __init__(self, value, **kwargs):

        self.value = value
        self.file_name = "Dice-" + str(value)
        # CHANGE: ensure_valid_file() does not exist in GL (SVGMobject finds the file by name)
        SVGMobject.__init__(self, file_name = self.file_name)


class RowOfDice(VGroup):
    CONFIG = {
        "values" : list(range(1,7)),
        "direction": RIGHT,
    }

    def init_points(self):
        for value in self.values:
            new_die = DieFace(value)
            new_die.submobjects[0].set_fill(opacity = 0)
            new_die.submobjects[0].set_stroke(width = 7)
            new_die.next_to(self, self.direction)
            self.add(new_die)
        self.move_to(ORIGIN)


class TwoDiceTable(VMobject):
    CONFIG = {
        "cell_size" : 1,
        "label_scale": 0.7
    }

    def __init__(self, **kwargs):

        VMobject.__init__(self, **kwargs)
        colors = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 13)

        self.cells = VGroup()
        self.labels = VGroup()
        for i in range(1,7):
            for j in range(1,7):
                cell = Square(side_length = self.cell_size)
                cell.set_fill(color = colors[i+j], opacity = 0.8)
                cell.move_to(i*self.cell_size*DOWN + j*self.cell_size*RIGHT)
                self.cells.add(cell)
                label = Integer(i+j).scale(self.label_scale)
                label.move_to(cell)
                self.labels.add(label)


        self.add(self.cells, self.labels)
        row1 = RowOfDice().match_width(self)
        row2 = row1.copy().rotate(-TAU/4)
        row1.next_to(self, UP)
        row2.next_to(self, LEFT)
        self.rows = VGroup(row1, row2)
        self.add(self.rows)
        self.center()



# ----- From _2018/eop/chapter1/prob_dist_visuals.py -----

class ProbabilityDistributions(PiCreatureScene):

    CONFIG = {
        "default_pi_creature_kwargs": {
        "color": MAROON_E,
        "flip_at_start": False,
        },
    }

    def construct(self):

        lag_ratio = 0.2
        run_time = 3
        

# WEATHER FORECAST

    
        unit_rect = Rectangle(
            height = 3, width = 3
        ).shift(DOWN)

        p_rain = 0.23
        p_sun = 1 - p_rain
        opacity = 0.7

        rain_rect = unit_rect.copy().stretch(p_rain, 0)
        rain_rect.align_to(unit_rect, LEFT)
        rain_rect.set_fill(color = BLUE, opacity = opacity)
        rain_rect.set_stroke(width = 0)

        sun_rect = unit_rect.copy().stretch(p_sun, 0)
        sun_rect.next_to(rain_rect, RIGHT, buff = 0)
        sun_rect.set_fill(color = YELLOW, opacity = opacity)
        sun_rect.set_stroke(width = 0)

        self.add(unit_rect, rain_rect, sun_rect)

        rain = SVGMobject(file_name = "rain").scale(0.25)
        sun = SVGMobject(file_name = "sun").scale(0.35)

        rain.flip().move_to(rain_rect)
        sun.move_to(sun_rect)

        self.add(rain, sun)


        text_scale =  0.7

        brace_rain = Brace(rain_rect, UP)
        p_rain_label = OldTexText("$P($rain$)=$").scale(text_scale)
        p_rain_decimal = DecimalNumber(p_rain).scale(text_scale)
        p_rain_decimal.next_to(p_rain_label)
        p_rain_whole_label = VGroup(p_rain_label, p_rain_decimal)
        p_rain_whole_label.next_to(brace_rain, UP)

        brace_sun = Brace(sun_rect, DOWN)
        p_sun_label = OldTexText("$P($sunshine$)=$").scale(text_scale)
        p_sun_decimal = DecimalNumber(p_sun).scale(text_scale)
        p_sun_decimal.next_to(p_sun_label)
        p_sun_whole_label = VGroup(p_sun_label, p_sun_decimal)
        p_sun_whole_label.next_to(brace_sun, DOWN)

        self.add(brace_rain, p_rain_whole_label, brace_sun, p_sun_whole_label)

        self.wait(6)



        # new_p_rain = 0.68
        # new_p_sun = 1 - new_p_rain

        # new_rain_rect = unit_rect.copy().stretch(new_p_rain, 0)
        # new_rain_rect.align_to(unit_rect, LEFT)
        # new_rain_rect.set_fill(color = BLUE, opacity = opacity)
        # new_rain_rect.set_stroke(width = 0)

        # new_sun_rect = unit_rect.copy().stretch(new_p_sun, 0)
        # new_sun_rect.next_to(new_rain_rect, RIGHT, buff = 0)
        # new_sun_rect.set_fill(color = YELLOW, opacity = opacity)
        # new_sun_rect.set_stroke(width = 0)

        # new_rain = SVGMobject(file_name = "rain").scale(0.35)
        # new_sun = SVGMobject(file_name = "sun").scale(0.35)

        # new_rain.flip().move_to(new_rain_rect)
        # new_sun.move_to(new_sun_rect)

        # new_brace_rain = Brace(new_rain_rect, UP)
        # new_p_rain_label = OldTexText("$P($rain$)=$").scale(text_scale)
        # new_p_rain_decimal = DecimalNumber(new_p_rain).scale(text_scale)
        # new_p_rain_decimal.next_to(new_p_rain_label)
        # new_p_rain_whole_label = VGroup(new_p_rain_label, new_p_rain_decimal)
        # new_p_rain_whole_label.next_to(new_brace_rain, UP)

        
        # new_brace_sun = Brace(new_sun_rect, DOWN)
        # new_p_sun_label = OldTexText("$P($sunshine$)=$").scale(text_scale)
        # new_p_sun_decimal = DecimalNumber(new_p_sun).scale(text_scale)
        # new_p_sun_decimal.next_to(new_p_sun_label)
        # new_p_sun_whole_label = VGroup(new_p_sun_label, new_p_sun_decimal)
        # new_p_sun_whole_label.next_to(new_brace_sun, DOWN)

        # def rain_update_func(alpha):
        #     return alpha * new_p_rain + (1 - alpha) * p_rain

        # def sun_update_func(alpha):
        #     return 1 - rain_update_func(alpha)

        # update_p_rain = ChangingDecimal(
        #     p_rain_decimal, rain_update_func,
        #     tracked_mobject = p_rain_label,
        #     run_time = run_time
        # )
        # update_p_sun = ChangingDecimal(
        #     p_sun_decimal, sun_update_func,
        #     tracked_mobject = p_sun_label,
        #     run_time = run_time
        # )

        # self.play(
        #     Transform(rain_rect, new_rain_rect, run_time = run_time),
        #     Transform(sun_rect, new_sun_rect, run_time = run_time),
        #     Transform(rain, new_rain, run_time = run_time),
        #     Transform(sun, new_sun, run_time = run_time),
        #     Transform(brace_rain, new_brace_rain, run_time = run_time),
        #     Transform(brace_sun, new_brace_sun, run_time = run_time),
        #     Transform(p_rain_label, new_p_rain_label, run_time = run_time),
        #     Transform(p_sun_label, new_p_sun_label, run_time = run_time),
        #     update_p_rain,
        #     update_p_sun
        # )



        # move the forecast into a corner

        forecast = VGroup(
            rain_rect, sun_rect, rain, sun, brace_rain, brace_sun,
            p_rain_whole_label, p_sun_whole_label, unit_rect
        )

        forecast.target = forecast.copy().scale(0.5)
        forecast.target.to_corner(UL)

        self.play(MoveToTarget(forecast))

        self.play(
            FadeOut(brace_rain),
            FadeOut(brace_sun),
            FadeOut(p_rain_whole_label),
            FadeOut(p_sun_whole_label),
        )

        self.wait(3)


# DOUBLE DICE THROW

        cell_size = 0.5
        dice_table = TwoDiceTable(cell_size = cell_size, label_scale = 0.7)
        dice_table.shift(0.8 * DOWN)
        dice_unit_rect = SurroundingRectangle(
            dice_table.cells, buff = 0,
            stroke_color=WHITE
        )

        dice_table_grouped_cells = VGroup()

        for i in range(6):
            dice_table_grouped_cells.add(VGroup(*[
                VGroup(
                    dice_table.cells[6 * i - 5 * k],
                    dice_table.labels[6 * i - 5 * k],
                )
                for k in range(i + 1)
            ]))

        for i in range(5):
            dice_table_grouped_cells.add(VGroup(*[
                VGroup(
                    dice_table.cells[31 + i - 5 * k],
                    dice_table.labels[31 + i - 5 * k],
                )
                for k in range(5 - i)
            ]))

        # self.play(
        #     FadeIn(dice_unit_rect),
        #     FadeIn(dice_table.rows)
        # )

        # for (cell, label) in zip(dice_table.cells, dice_table.labels):
        #     cell.add(label)

        # self.play(
        #     LaggedStartMap(FadeIn, dice_table_grouped_cells,
        #         lag_ratio = lag_ratio, run_time = run_time)
        # )
        self.play(
            FadeIn(dice_table_grouped_cells),
            FadeIn(dice_unit_rect),
            FadeIn(dice_table.rows)
        )

        self.wait(3)


        self.play(
            dice_table_grouped_cells.space_out_submobjects, {"factor" : 1.5},
            rate_func=there_and_back_with_pause,
            run_time=run_time
        )

        dice_table.add(dice_unit_rect)
        dice_table_target = dice_table.deepcopy()
        dice_table_target.scale(0.5)
        dice_table_target.to_corner(UR, buff=LARGE_BUFF)
        dice_table_target.shift(0.4 * UP)

        self.play(Transform(dice_table, dice_table_target))

        self.play(
            FadeOut(dice_table.rows),
            FadeOut(dice_unit_rect),
        )

        self.wait(3)

# TITLE

        text = OldTexText("Probability distributions")
        text.to_edge(UP)
        text_rect = SurroundingRectangle(text, buff=MED_SMALL_BUFF)
        text_rect.match_color(text)

        self.play(
            FadeIn(text),
            ShowCreation(text_rect)
        )

        self.wait(3)


# COIN FLIP


        brick_row = BrickRow(3, height = 2, width = 10)
        coin_flip_rect = VGroup(brick_row)

        tallies = VGroup()
        for (i, brick) in enumerate(brick_row.rects):
            tally = TallyStack(3 - i, i)
            tally.move_to(brick)
            tallies.add(tally)
        coin_flip_rect.add(tallies)

        coin_flip_rect.scale(0.65).shift(RIGHT)
        self.play(FadeIn(coin_flip_rect))

        counts = [1, 3, 3, 1]
        braces = VGroup()
        labels = VGroup()
        for (rect, count) in zip(brick_row.rects, counts):
            label = OldTex("{" + str(count) + "\\over 8}").scale(0.5)
            brace = Brace(rect, DOWN)
            label.next_to(brace, DOWN)
            braces.add(brace)
            labels.add(label)

        self.play(
            FadeIn(braces),
            FadeIn(labels)
        )

        coin_flip_rect.add(braces, labels)


        self.wait(6)

        outcomes = brick_row.get_outcome_rects_for_level(3, with_labels = True,
            inset = True)
        outcomes.scale(0.65)
        outcomes.move_to(brick_row.get_center())
        outcome_braces = VGroup(*[
            Brace(outcome, DOWN) for outcome in outcomes
        ])
        outcome_labels = VGroup(*[
            OldTex("{1\over 8}").scale(0.5).next_to(brace, DOWN)
            for brace in outcome_braces
        ])

        self.play(
            FadeOut(tallies),
            FadeIn(outcomes),
            FadeOut(braces),
            FadeOut(labels),
            FadeIn(outcome_braces),
            FadeIn(outcome_labels)
        )


        self.wait(10)
