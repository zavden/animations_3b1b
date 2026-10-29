# ==============================================================================
# Scene:      RandomNoiseMeaning
# Source:     videos/_2026/cross_entropy/robot.py (lines 7781-7818)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomNoiseMeaning.py RandomNoiseMeaning -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import random

class RandomNoiseMeaning(InteractiveScene):
    def construct(self):
        # Demonstrate that "random noise" means a bunch of independent coin tosses for each bit
        message = VGroup(*[
            Integer(0).set_color(YELLOW)
            for _ in range(37)
        ]).arrange(
            buff=0.08
        ).set_width(
            FRAME_WIDTH * 0.9
        )
        self.add(message)

        coins = Group(*[
            Coin(
                color=BLUE_E, tails_color=LIGHT_BROWN, numeric_labels=True
            )
            for b in message
        ]).arrange(buff=0.2).match_width(message).next_to(message, DOWN)
        for coin in coins:
            if random.random() > 0.5:
                coin.flip()
        self.add(coins)

        for bit, coin in zip(message, coins):
            def update_bit(m, coin=coin):
                m.set_value(1 if coin.is_heads() else 0)
            bit.add_updater(update_bit)

        coin_list = list(coins)
        for _ in range(45):
            random.shuffle(coin_list)
            self.play(
                AnimationGroup(*[
                    coin.animate.flip() if random.random() > 0.5 else Rotate(coin, axis=RIGHT, angle=random.choice([-1, 1]) * 2 * PI)
                    for coin in coin_list
                ], lag_ratio=0.01)
            )


class Coin(Group):
    def __init__(
        self,
        disk_resolution=(150, 50),
        height=1,
        depth=0.1,
        color=GOLD_D,
        tails_color=RED,
        include_labels=True,
        numeric_labels=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        res = disk_resolution
        self.top = Disk3D(resolution=res)
        self.bottom = self.top.copy()
        self.top.shift(OUT)
        self.bottom.shift(IN)
        self.edge = Cylinder(height=2, resolution=(res[1], 2))
        self.add(self.top, self.bottom, self.edge)
        self.rotate(90 * DEGREES, OUT)
        self.set_color(color)
        self.bottom.set_color(tails_color)

        if include_labels:
            chars = "10" if numeric_labels else "HT"
            labels = VGroup(*[TexText(c, depth_test=True) for c in chars])
            for label, vect in zip(labels, [OUT, IN]):
                label.shift(1.02 * vect)
                label.set_height(1.2)
            labels[1].rotate(PI, RIGHT)
            # labels.apply_depth_test()
            labels.set_stroke(width=0)
            self.add(*labels)
            self.labels = labels

        self.set_height(height)
        self.set_depth(depth, stretch=True)

        def update_label_opacities(m):
            if m.is_heads():
                m.labels[0].set_opacity(1)
                m.labels[1].set_opacity(0)
            else:
                m.labels[0].set_opacity(0)
                m.labels[1].set_opacity(1)
        self.add_updater(update_label_opacities)

    def is_heads(self):
        return self.top.get_center()[2] > self.bottom.get_center()[2]

    def flip(self, axis=RIGHT):
        super().flip(axis)
        return self
