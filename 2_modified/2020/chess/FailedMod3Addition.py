# ==============================================================================
# Scene:      FailedMod3Addition
# Source:     videos/_2020/chess.py (lines 1905-1933)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FailedMod3Addition.py FailedMod3Addition -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
# ==============================================================================

from manim_imports_ext import *

class Coin(Group):
    CONFIG = {
        "disk_resolution": (4, 51),
        "height": 1,
        "depth": 0.1,
        "color": GOLD_D,
        "tails_color": RED,
        "include_labels": True,
        "numeric_labels": False,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        res = self.disk_resolution
        self.top = Disk3D(resolution=res, gloss=0.2)
        self.bottom = self.top.copy()
        self.top.shift(OUT)
        self.bottom.shift(IN)
        self.edge = Cylinder(height=2, resolution=(res[1], 2))
        self.add(self.top, self.bottom, self.edge)
        self.rotate(90 * DEGREES, OUT)
        self.set_color(self.color)
        self.bottom.set_color(RED)

        if self.include_labels:
            chars = "10" if self.numeric_labels else "HT"
            labels = VGroup(*[TexText(c) for c in chars])
            for label, vect in zip(labels, [OUT, IN]):
                label.shift(1.02 * vect)
                label.set_height(0.8)
            labels[1].rotate(PI, RIGHT)
            labels.apply_depth_test()
            labels.set_stroke(width=0)
            self.add(*labels)
            self.labels = labels

        self.set_height(self.height)
        self.set_depth(self.depth, stretch=True)

    def is_heads(self):
        return self.top.get_center()[2] > self.bottom.get_center()[2]

    def flip(self, axis=RIGHT):
        super().flip(axis)
        return self


class FlipCoin(Animation):
    CONFIG = {
        "axis": RIGHT,
        "run_time": 1,
        "shift_dir": OUT,
    }

    # CHANGE: Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
    def __init__(self, coin, axis=RIGHT, shift_dir=OUT, **kwargs):
        self.axis = axis
        self.shift_dir = shift_dir
        super().__init__(coin, **kwargs)
        self.shift_vect = coin.get_height() * self.shift_dir / 2

    def interpolate_mobject(self, alpha):
        coin = self.mobject
        for sm, start_sm in self.families:
            sm.match_points(start_sm)
        coin.rotate(alpha * PI, axis=self.axis)
        coin.shift(4 * alpha * (1 - alpha) * self.shift_vect)
        return coin


class FailedMod3Addition(Scene):
    def construct(self):
        coin = Coin(height=0.5, numeric_labels=True)
        csum = Group(
            OldTex("0 \\cdot"),
            coin.deepcopy().flip(),
            OldTex(" + 1 \\cdot"),
            coin.deepcopy().flip(),
            OldTex("+ 2 \\cdot"),
            coin.deepcopy(),
            OldTex("="),
            Integer(2, color=YELLOW),
        )
        csum.arrange(RIGHT, buff=SMALL_BUFF)
        csum[-1].shift(SMALL_BUFF * RIGHT)
        coins = csum[1:7:2]
        csum[-1].add_updater(lambda m, coins=coins: m.set_value(coins[1].is_heads() + 2 * coins[2].is_heads()))

        self.add(csum)

        for coin in coins[::-1]:
            rect = SurroundingRectangle(coin)
            self.play(ShowCreation(rect))
            self.play(FlipCoin(coin))
            self.wait()
            self.play(FlipCoin(coin), FadeOut(rect))
        self.wait()

        self.embed()
