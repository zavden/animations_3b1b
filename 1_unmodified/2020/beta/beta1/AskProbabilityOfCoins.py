# ==============================================================================
# Scene:      AskProbabilityOfCoins
# Source:     videos/_2020/beta/beta1.py (lines 1898-1943)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl AskProbabilityOfCoins.py AskProbabilityOfCoins -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

COIN_COLOR_MAP = {
    "H": BLUE_E,
    "T": RED_E,
}


# Coins
def get_coin(symbol, color=None):
    if color is None:
        color = COIN_COLOR_MAP.get(symbol, GREY_E)
    coin = VGroup()
    circ = Circle()
    circ.set_fill(color, 1)
    circ.set_stroke(WHITE, 1)
    circ.set_height(1)
    label = OldTexText(symbol)
    label.set_height(0.5 * circ.get_height())
    label.move_to(circ)
    coin.add(circ, label)
    coin.symbol = symbol
    return coin



# ----- From _2020/beta/beta1.py -----

class AskProbabilityOfCoins(Scene):
    def construct(self):
        condition = VGroup(
            OldTexText("If you've seen"),
            Integer(80, color=BLUE_C),
            get_coin("H").set_height(0.5),
            OldTexText("and"),
            Integer(20, color=RED_C),
            get_coin("T").set_height(0.5),
        )
        condition.arrange(RIGHT)
        condition.to_edge(UP)
        self.add(condition)

        question = OldTex(
            "\\text{What is }",
            "P(", "00", ")", "?"
        )
        coin = get_coin("H")
        coin.replace(question.get_part_by_tex("00"))
        question.replace_submobject(
            question.index_of_part_by_tex("00"),
            coin
        )
        question.next_to(condition, DOWN)
        self.add(question)

        values = ["H"] * 80 + ["T"] * 20
        random.shuffle(values)

        coins = VGroup(*[
            get_coin(symbol)
            for symbol in values
        ])
        coins.arrange_in_grid(10, 10, buff=MED_SMALL_BUFF)
        coins.set_width(5)
        coins.next_to(question, DOWN, MED_LARGE_BUFF)

        self.play(
            ShowIncreasingSubsets(coins),
            run_time=8,
            rate_func=bezier([0, 0, 1, 1])
        )
        self.wait()

        self.embed()
