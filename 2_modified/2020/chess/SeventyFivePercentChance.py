# ==============================================================================
# Scene:      SeventyFivePercentChance
# Source:     videos/_2020/chess.py (lines 2081-2166)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SeventyFivePercentChance.py SeventyFivePercentChance -w -m --fps 15
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


class SeventyFivePercentChance(Scene):
    def construct(self):
        # Setup column
        rows = []
        n_shown = 5
        coins = Group()
        nums = VGroup()
        for n in it.chain(range(n_shown), range(64 - n_shown, 64)):
            coin = Coin(numeric_labels=True)
            coin.set_height(0.7)
            if (random.random() < 0.5 or (n == 2)) and (n != 62):
                coin.flip()
            num = Integer(n)
            row = Group(
                coin,
                OldTex("\\cdot"),
                num,
                OldTex("+"),
            )
            VGroup(*row[1:]).set_stroke(BLACK, 3, background=True)
            row.arrange(RIGHT, buff=MED_SMALL_BUFF)
            rows.append(row)
            coins.add(coin)
            nums.add(num)

        vdots = OldTex("\\vdots")
        rows = Group(*rows[:n_shown], vdots, *rows[n_shown:])
        rows.arrange(DOWN, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
        vdots.match_x(rows[0][2])
        rows.set_height(7)
        rows.to_edge(RIGHT)
        rows[-1][-1].set_opacity(0)

        nums = VGroup(*nums[:n_shown], vdots, *nums[n_shown:])
        self.play(Write(nums))
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, rows, lag_ratio=0.1, run_time=3),
            Animation(nums.copy(), remover=True),
        )
        self.wait()

        # Show desired sums
        brace = Brace(rows, LEFT)
        b_label = brace.get_text("Sum mod 64")
        sum_label = OldTexText("=\\, 53 (say)")
        sum_label.next_to(b_label, DOWN)
        want_label = OldTexText("Need to encode 55 (say)")
        want_label.next_to(sum_label, DOWN, buff=0.25, aligned_edge=RIGHT)
        want_label.set_color(YELLOW)
        need_label = OldTexText("Must add 2")
        need_label.next_to(want_label, DOWN, buff=0.25)
        need_label.set_color(BLUE)

        for label in b_label, sum_label, want_label, need_label:
            label.set_stroke(BLACK, 7, background=True)

        self.play(
            GrowFromCenter(brace),
            FadeIn(b_label, RIGHT)
        )
        self.wait(2)
        self.play(FadeIn(sum_label, 0.25 * UP))
        self.wait(2)
        self.play(LaggedStart(
            FadeIn(want_label, UP),
            FadeIn(need_label, UP),
            lag_ratio=0.3
        ))
        self.wait()

        # Show attempts
        s_rect = SurroundingRectangle(rows[2])

        self.play(ShowCreation(s_rect))
        self.wait()
        self.play(FlipCoin(rows[2][0]))
        self.wait(2)

        self.play(
            s_rect.move_to, rows[-2],
            s_rect.stretch, 1.1, 0,
        )
        self.wait()
        self.play(FlipCoin(rows[-2][0]))
        self.wait()
