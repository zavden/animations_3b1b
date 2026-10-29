# ==============================================================================
# Scene:      CompareBlockTimes
# Source:     videos/_2017/crypto.py (lines 4629-4672)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareBlockTimes.py CompareBlockTimes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

BITCOIN_COLOR = "#f7931a"


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


class CompareBlockTimes(Scene):
    def construct(self):
        title = OldTexText("Average block time")
        title.scale(1.5)
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_X_RADIUS)
        h_line.next_to(title, DOWN, SMALL_BUFF)

        examples = VGroup(
            OldTexText("BTC: ", "10 minutes"),
            OldTexText("ETH: ", "15 Seconds"),
            OldTexText("XRP: ", "3.5 Seconds"),
            OldTexText("LTC: ", "2.5 Minutes"),
        )
        examples.arrange(
            DOWN, 
            buff = LARGE_BUFF,
            aligned_edge = LEFT,
        )
        examples.next_to(h_line, DOWN)
        logos = VGroup(
            BitcoinLogo(),
            EthereumLogo(),
            ImageMobject("ripple_logo"),
            LitecoinLogo(),
        )
        colors = [BITCOIN_COLOR, GREEN, BLUE_B, GREY_B]
        for logo, example, color in zip(logos, examples, colors):
            logo.set_height(0.5)
            logo.next_to(example, LEFT)
            example[0].set_color(color)

        self.add(title, h_line)
        self.play(
            FadeIn(examples[0]),
            DrawBorderThenFill(logos[0])
        )
        self.wait()
        self.play(*[
            LaggedStartMap(FadeIn, VGroup(*group[1:]))
            for group in (examples, logos)
        ])
        self.wait(2)
