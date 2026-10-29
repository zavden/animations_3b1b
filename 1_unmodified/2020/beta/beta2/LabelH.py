# ==============================================================================
# Scene:      LabelH
# Source:     videos/_2020/beta/beta2.py (lines 426-441)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl LabelH.py LabelH -w -m --fps 15
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


def get_prob_coin_label(symbol="H", color=None, p=0.5, num_decimal_places=2):
    label = OldTex("P", "(", "00", ")", "=",)
    coin = get_coin(symbol, color)
    template = label.get_part_by_tex("00")
    coin.replace(template)
    label.replace_submobject(label.index_of_part(template), coin)
    rhs = DecimalNumber(p, num_decimal_places=num_decimal_places)
    rhs.next_to(label, RIGHT, buff=MED_SMALL_BUFF)
    label.add(rhs)
    return label



# ----- From _2020/beta/beta2.py -----

class LabelH(Scene):
    def construct(self):
        p_label = get_prob_coin_label()
        p_label.scale(1.5)
        brace = Brace(p_label, DOWN)
        h = OldTex("h")
        h.scale(2)
        h.next_to(brace, DOWN)

        self.add(p_label)
        self.play(ShowCreationThenFadeAround(p_label))
        self.play(
            GrowFromCenter(brace),
            FadeIn(h, UP),
        )
        self.wait()
