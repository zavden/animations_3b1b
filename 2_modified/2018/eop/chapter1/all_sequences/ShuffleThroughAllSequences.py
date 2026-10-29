# ==============================================================================
# Scene:      ShuffleThroughAllSequences
# Source:     videos/_2018/eop/chapter1/all_sequences.py (lines 5-59)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/reusables/eop_constants.py, _2018/eop/reusables/eop_helpers.py, _2018/eop/reusables/upright_coins.py
#
# Run from this folder:
#     manimgl ShuffleThroughAllSequences.py ShuffleThroughAllSequences -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
#   - fps fixed to 15 (PRODUCTION_QUALITY_FRAME_DURATION removed) and the manual update_frame/add_frames per sequence replaced by self.wait(1/fps)
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *


# ----- From _2018/eop/reusables/eop_constants.py -----

COIN_RADIUS = 0.18


COIN_STROKE_WIDTH = 2


COIN_SEQUENCE_SPACING = 0.1


COLOR_HEADS_COIN = RED


COLOR_TAILS_COIN = BLUE_E



# ----- From _2018/eop/reusables/eop_helpers.py -----

def binary(i):
    # returns an array of 0s and 1s
    if i == 0:
        return []
    j = i
    binary_array = []
    while j > 0:
        jj = j/2
        if jj > 0:
            binary_array.append(j % 2)
        else:
            binary_array.append(1)
        j = jj
    return binary_array[::-1]



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



# ----- From _2018/eop/chapter1/all_sequences.py -----

class ShuffleThroughAllSequences(Scene):
    CONFIG = {
        "nb_coins" : 20,
        "run_time" : 5,
        # CHANGE: PRODUCTION_QUALITY_FRAME_DURATION no longer exists; use the render frame rate (15 fps) so one wait per coin sequence is one video frame
        "fps" : 15,
        "coin_size" : 0.5,
        "coin_spacing" : 0.65
    }


    def construct(self):

        nb_frames = self.run_time * self.fps
        nb_relevant_coins = int(np.log2(nb_frames)) + 1
        print("relevant coins:", nb_relevant_coins)
        nb_idle_coins = self.nb_coins - nb_relevant_coins

        idle_heads = CoinSequence(nb_idle_coins * ["H"],
            radius = self.coin_size * 0.5,
            spacing = self.coin_spacing)
        idle_tails = CoinSequence(nb_idle_coins * ["T"],
            radius = self.coin_size * 0.5,
            spacing = self.coin_spacing)
        idle_tails.fade(0.5)

        idle_part = VGroup(idle_heads, idle_tails)
        left_idle_part = CoinSequence(6 * ["H"],
            radius = self.coin_size * 0.5,
            spacing = self.coin_spacing)

        #self.add(idle_part, left_idle_part)
        self.add(left_idle_part)
        last_coin_seq = VGroup()

        for i in range(2**nb_relevant_coins):
            binary_seq = binary(i)
            # pad to the left with 0s
            nb_leading_zeroes = nb_relevant_coins - len(binary_seq)
            for j in range(nb_leading_zeroes):
                binary_seq.insert(0, 0)
            seq2 = ["H" if x == 0 else "T" for x in binary_seq]
            coin_seq = CoinSequence(seq2,
                radius = self.coin_size * 0.5,
                spacing = self.coin_spacing)
            coin_seq.next_to(idle_part, LEFT, buff = self.coin_spacing - self.coin_size)
            left_idle_part.next_to(coin_seq, LEFT, buff = self.coin_spacing - self.coin_size)
            all_coins = VGroup(left_idle_part, coin_seq) #, idle_part)
            all_coins.center()
            self.remove(last_coin_seq)
            self.add(coin_seq)
            # CHANGE: Cairo add_frames(get_frame()) does not exist in GL; one wait of 1/fps adds the frame
            self.wait(1.0/self.fps)
            last_coin_seq = coin_seq
            print(float(i)/2**nb_relevant_coins)
