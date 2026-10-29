# ==============================================================================
# Scene:      BigDifferenceBetweenLDAndCryptocurrencies
# Source:     videos/_2017/crypto.py (lines 2017-2046)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BigDifferenceBetweenLDAndCryptocurrencies.py BigDifferenceBetweenLDAndCryptocurrencies -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EthereumLogo(SVGMobject):
    CONFIG = {
        "file_name" : "ethereum_logo",
        "stroke_width" : 0,
        "fill_opacity" : 1,
        "color_chars" : "8B8B48",
        "height" : 0.5,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        for part, char in zip(self.submobjects, self.color_chars):
            part.set_color("#" + 6*char)


class LitecoinLogo(SVGMobject):
    CONFIG = {
        "file_name" : "litecoin_logo",
        "stroke_width" : 0,
        "fill_opacity" : 1,
        "fill_color" : GREY_B,
        "height" : 0.5,
    }


class BigDifferenceBetweenLDAndCryptocurrencies(Scene):
    def construct(self):
        ld = OldTexText("LD").scale(1.5).set_color(YELLOW)
        btc = BitcoinLogo()
        eth = EthereumLogo()
        ltc = LitecoinLogo()
        logos = VGroup(ltc, eth, ld, btc)
        cryptos = VGroup(btc, eth, ltc)
        for logo in cryptos:
            logo.set_height(1)
        vects = compass_directions(4, DOWN+LEFT)
        for logo, vect in zip(logos, vects):
            logo.move_to(0.75*vect)

        centralized = OldTexText("Centralized")
        decentralized = OldTexText("Decentralized")
        words = VGroup(centralized, decentralized)
        words.scale(1.5)
        words.to_edge(UP)
        for word, vect in zip(words, [RIGHT, LEFT]):
            word.shift(FRAME_X_RADIUS*vect/2)

        self.add(logos)
        self.wait()
        self.play(
            cryptos.next_to, decentralized, DOWN, LARGE_BUFF,
            ld.next_to, centralized, DOWN, LARGE_BUFF,
        )
        self.play(*list(map(Write, words)))
        self.wait(2)
