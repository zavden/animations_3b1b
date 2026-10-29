# ==============================================================================
# Scene:      BitcoinIsALedger
# Source:     videos/_2017/crypto.py (lines 1966-2015)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BitcoinIsALedger.py BitcoinIsALedger -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

BITCOIN_COLOR = "#f7931a"


class BitcoinIsALedger(Scene):
    def construct(self):
        self.add_btc_to_ledger()
        self.add_currency_to_tx_history()

    def add_btc_to_ledger(self):
        logo = BitcoinLogo()
        ledger = self.get_ledger()
        arrow = OldTex("\\Leftrightarrow")
        group = VGroup(logo, arrow, ledger)
        group.arrange(RIGHT)

        self.play(DrawBorderThenFill(logo))
        self.wait()
        self.play(
            Write(arrow),
            Write(ledger)
        )
        self.wait()

        self.btc_to_ledger = group

    def add_currency_to_tx_history(self):
        equation = OldTexText(
            "Currency", "=", "Transaction history"
        )
        equation.set_color_by_tex("Currency", BITCOIN_COLOR)
        equation.shift(
            self.btc_to_ledger[1].get_center() - \
            equation[1].get_center() + 2*UP
        )

        for part in reversed(equation):
            self.play(FadeIn(part))
        self.wait()

    def get_ledger(self):
        rect = Rectangle(height = 2, width = 1.5)
        title = OldTexText("Ledger")
        title.set_width(0.8*rect.get_width())
        title.next_to(rect.get_top(), DOWN, SMALL_BUFF)

        lines = VGroup(*[
            Line(LEFT, RIGHT)
            for x in range(8)
        ])
        lines.arrange(DOWN, buff = SMALL_BUFF)
        lines.stretch_to_fit_width(title.get_width())
        lines.next_to(title, DOWN)
        return VGroup(rect, title, lines)
