# ==============================================================================
# Scene:      TransactionFeeExample
# Source:     videos/_2017/crypto.py (lines 4753-4815)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TransactionFeeExample.py TransactionFeeExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TransactionFeeExample(PiCreatureScene):
    def construct(self):
        alice = self.pi_creature
        payment = OldTexText(
            "Alice", "pays", "Bob", "0.42 BTC",
        )
        payment.set_color_by_tex("Alice", BLUE_C)
        payment.set_color_by_tex("Bob", MAROON)
        payment.set_color_by_tex("BTC", YELLOW)
        payment.move_to(2.5*UP)

        fee = OldTexText("And leaves", "0.001 BTC", "to the miner")
        fee.set_color_by_tex("BTC", YELLOW)
        fee.next_to(payment, DOWN)

        signature = OldTexText(
            "$\\langle$Alice's digital signature$\\rangle$"
        )
        signature.set_color(BLUE_C)
        signature.next_to(fee, DOWN)

        group = VGroup(payment, fee, signature)
        rect = SurroundingRectangle(group, color = BLUE_B)

        incentive_words = OldTexText(
            "Incentivizes miner \\\\ to include"
        )
        incentive_words.next_to(rect, DOWN, buff = 1.5)
        incentive_words.shift(2*RIGHT)
        arrow = Arrow(
            incentive_words.get_top(),
            rect.get_bottom(),
            buff = MED_LARGE_BUFF
        )

        fee.save_state()
        fee.shift(DOWN)
        fee.set_fill(opacity = 0)

        self.play(Write(payment))
        self.wait()
        self.play(
            alice.change, "raise_right_hand", payment,
            fee.restore,
        )
        self.play(Write(signature))
        self.play(
            ShowCreation(rect),
            alice.change_mode, "happy"
        )
        self.wait()
        self.play(
            Write(incentive_words),
            ShowCreation(arrow),
            alice.change, "pondering"
        )
        self.wait(2)

    def create_pi_creature(self):
        alice = PiCreature(color = BLUE_C)
        alice.to_edge(DOWN)
        alice.shift(FRAME_X_RADIUS*LEFT/2)
        return alice
