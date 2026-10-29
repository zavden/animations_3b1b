# ==============================================================================
# Scene:      UnderlyingSystemVsUserFacing
# Source:     videos/_2017/crypto.py (lines 640-706)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnderlyingSystemVsUserFacing.py UnderlyingSystemVsUserFacing -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

BITCOIN_COLOR = "#f7931a"


class UnderlyingSystemVsUserFacing(Scene):
    def construct(self):
        underlying = OldTexText("Underlying \\\\ system")
        underlying.shift(DOWN).to_edge(LEFT)
        user_facing = OldTexText("User-facing")
        user_facing.next_to(underlying, UP, LARGE_BUFF, LEFT)

        protocol = OldTexText("Bitcoin protocol")
        protocol.next_to(underlying, RIGHT, MED_LARGE_BUFF)
        protocol.set_color(BITCOIN_COLOR)
        banking = OldTexText("Banking system")
        banking.next_to(protocol, RIGHT, MED_LARGE_BUFF)
        banking.set_color(GREEN)

        phone = SVGMobject(
            file_name = "phone",
            fill_color = WHITE,
            fill_opacity = 1,
            height = 1,
            stroke_width = 0,
        )
        phone.next_to(protocol, UP, LARGE_BUFF)
        card = SVGMobject(
            file_name = "credit_card",
            fill_color = GREY_B,
            fill_opacity = 1,
            stroke_width = 0,
            height = 1
        )
        card.next_to(banking, UP, LARGE_BUFF)

        btc = BitcoinLogo()
        btc.next_to(phone, UP, MED_LARGE_BUFF)
        dollar = OldTex("\\$")
        dollar.set_height(1)
        dollar.set_color(GREEN)
        dollar.next_to(card, UP, MED_LARGE_BUFF)
        card.save_state()
        card.shift(2*RIGHT)
        card.set_fill(opacity = 0)


        h_line = Line(underlying.get_left(), banking.get_right())
        h_line.next_to(underlying, DOWN, MED_SMALL_BUFF, LEFT)
        h_line2 = h_line.copy()
        h_line2.next_to(user_facing, DOWN, MED_LARGE_BUFF, LEFT)
        h_line3 = h_line.copy()
        h_line3.next_to(user_facing, UP, MED_LARGE_BUFF, LEFT)
        v_line = Line(5*UP, ORIGIN)
        v_line.next_to(underlying, RIGHT, MED_SMALL_BUFF)
        v_line.shift(1.7*UP)
        v_line2 = v_line.copy()
        v_line2.next_to(protocol, RIGHT, MED_SMALL_BUFF)
        v_line2.shift(1.7*UP)

        self.add(h_line, h_line2, h_line3, v_line, v_line2)
        self.add(underlying, user_facing, btc)
        self.play(Write(protocol))
        self.wait(2)
        self.play(
            card.restore,
            Write(dollar)
        )
        self.play(Write(banking))
        self.wait(2)
        self.play(DrawBorderThenFill(phone))
        self.wait(2)
