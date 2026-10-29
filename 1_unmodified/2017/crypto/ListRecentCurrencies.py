# ==============================================================================
# Scene:      ListRecentCurrencies
# Source:     videos/_2017/crypto.py (lines 265-303)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ListRecentCurrencies.py ListRecentCurrencies -w -m --fps 15
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


class ListRecentCurrencies(Scene):
    def construct(self):
        footnote = OldTexText("$^*$Listed by market cap")
        footnote.scale(0.5)
        footnote.to_corner(DOWN+RIGHT)
        self.add(footnote)

        logos = VGroup(
            BitcoinLogo(),
            EthereumLogo(),
            ImageMobject("ripple_logo"),
            LitecoinLogo(),
            EthereumLogo().set_color_by_gradient(GREEN_B, GREEN_D),
        )
        for logo in logos:
            logo.set_height(0.75)
        logos.arrange(DOWN, buff = MED_LARGE_BUFF)
        logos.shift(LEFT)
        logos.to_edge(UP)
        names = list(map(
            TexText, 
            [
                "Bitcoin", "Ethereum", "Ripple", 
                "Litecoin", "Ethereum Classic"
            ],
        ))
        for logo, name in zip(logos, names):
            name.next_to(logo, RIGHT)
            anims = []
            if isinstance(logo, SVGMobject):
                anims.append(DrawBorderThenFill(logo, run_time = 1))
            else:
                anims.append(FadeIn(logo))
            anims.append(Write(name, run_time = 2))
            self.play(*anims)
        dots = OldTex("\\vdots")
        dots.next_to(logos, DOWN)
        self.play(LaggedStartMap(FadeIn, dots, run_time = 1))
        self.wait()
