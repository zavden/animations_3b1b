# ==============================================================================
# Scene:      DiagramOfProgression
# Source:     videos/_2020/chess.py (lines 499-653)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DiagramOfProgression.py DiagramOfProgression -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
#   - Arrow no longer has .tip (it is a single filled shape): removing the stroke from the tip is omitted
# ==============================================================================

from manim_imports_ext import *

def string_to_bools(message):
    # For easter eggs on the board
    as_int = int.from_bytes(message.encode(), 'big')
    bits = "{0:b}".format(as_int)
    bits = (len(message) * 8 - len(bits)) * '0' + bits
    return [bool(int(b)) for b in bits]


class Chessboard(Group):
    CONFIG = {
        "shape": (8, 8),
        "height": 7,
        "depth": 0.25,
        "colors": [GREY_B, GREY_E],
        "gloss": 0.2,
        "square_resolution": (3, 3),
        "top_square_resolution": (5, 5),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        nr, nc = self.shape
        cube = Cube(square_resolution=self.square_resolution)
        # Replace top square with something slightly higher res
        top_square = Square3D(resolution=self.top_square_resolution)
        top_square.replace(cube[0])
        cube.replace_submobject(0, top_square)
        self.add(*[cube.copy() for x in range(nc * nr)])
        self.arrange_in_grid(nr, nc, buff=0)
        self.set_height(self.height)
        self.set_depth(self.depth, stretch=True)
        for i, j in it.product(range(nr), range(nc)):
            color = self.colors[(i + j) % 2]
            self[i * nc + j].set_color(color)
        self.center()
        self.set_gloss(self.gloss)


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


class CoinsOnBoard(Group):
    CONFIG = {
        "proportion_of_square_height": 0.7,
        "coin_config": {},
    }

    def __init__(self, chessboard, **kwargs):
        super().__init__(**kwargs)
        prop = self.proportion_of_square_height
        for cube in chessboard:
            coin = Coin(**self.coin_config)
            coin.set_height(prop * cube.get_height())
            coin.next_to(cube, OUT, buff=0)
            self.add(coin)

    def flip_at_random(self, p=0.5):
        bools = np.random.random(len(self)) < p
        self.flip_by_bools(bools)
        return self

    def flip_by_message(self, message):
        self.flip_by_bools(string_to_bools(message))
        return self

    def flip_by_bools(self, bools):
        for coin, head in zip(self, bools):
            if coin.is_heads() ^ head:
                coin.flip()
        return self

    def get_bools(self):
        return [coin.is_heads() for coin in self]


class Key(SVGMobject):
    CONFIG = {
        "file_name": "key",
        "fill_color": YELLOW_D,
        "fill_opacity": 1,
        "stroke_color": YELLOW_D,
        "stroke_width": 0,
        "gloss": 0.5,
        "depth_test": True,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rotate(PI / 2, OUT)


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


class DiagramOfProgression(ThreeDScene):
    def construct(self):
        # Setup panels
        P1_COLOR = BLUE_C
        P2_COLOR = RED

        rect = Rectangle(4, 2)
        rect.set_fill(GREY_E, 1)
        panels = Group()
        for x in range(4):
            panels.add(Group(rect.copy()))
        panels.arrange_in_grid(buff=1)
        panels[::2].shift(0.5 * LEFT)
        panels.set_width(FRAME_WIDTH - 2)
        panels.center().to_edge(DOWN)
        p1_shift = panels[1].get_center() - panels[0].get_center()
        panels[1].move_to(panels[0])

        chessboard = Chessboard()
        chessboard.set_height(0.9 * panels[0].get_height())
        coins = CoinsOnBoard(
            chessboard,
            coin_config={
                "disk_resolution": (2, 25),
            }
        )
        coins.flip_by_message("Tau > Pi")

        for panel in panels[1:]:
            cb = chessboard.copy()
            co = coins.copy()
            cb.next_to(panel.get_right(), LEFT)
            co.next_to(cb, OUT, 0)
            panel.chessboard = cb
            panel.coins = co
            panel.add(cb, co)

        kw = {
            "tex_to_color_map": {
                "Prisoner 1": P1_COLOR,
                "Prisoner 2": P2_COLOR,
            }
        }
        titles = VGroup(
            OldTexText("Prisoners conspire", **kw),
            OldTexText("Prisoner 1 sees key", **kw),
            OldTexText("Prisoner 1 flips coin", **kw),
            OldTexText("Prisoner 2 guesses key square", **kw),
        )

        for panel, title in zip(panels, titles):
            title.next_to(panel, UP)
            panel.title = title
            panel.add(title)

        # Darken first chessboard
        for coin in panels[1].coins:
            coin.remove(coin.edge)
            if coin.is_heads():
                coin.remove(coin.bottom)
                coin.remove(coin.labels[1])
            else:
                coin.remove(coin.top)
                coin.remove(coin.labels[0])
            coin.set_opacity(0.25)

        # Add characters
        prisoner1 = PiCreature(color=P1_COLOR)
        prisoner2 = PiCreature(color=P2_COLOR)
        pis = VGroup(prisoner1, prisoner2)
        pis.arrange(RIGHT, buff=1)
        pis.set_height(1.5)

        p0_pis = pis.copy()
        p0_pis.set_height(2.0, about_edge=DOWN)
        p0_pis[1].flip()
        p0_pis.next_to(panels[0].get_bottom(), UP, SMALL_BUFF)
        p0_pis[0].change("pondering", p0_pis[1].eyes)
        p0_pis[1].change("speaking", p0_pis[0].eyes)
        panels[0].add(p0_pis)

        p1_pi = pis[0].copy()
        p1_pi.next_to(panels[1].get_corner(DL), UR, SMALL_BUFF)
        p1_pi.change("happy")
        key = Key()
        key.set_height(0.5)
        key.next_to(p1_pi, UP)
        key.set_color(YELLOW)
        key_cube = panels[1].chessboard[18]
        key_square = Square()
        key_square.replace(key_cube)
        key_square.set_stroke(width=3)
        key_square.match_color(key)
        p1_pi.look_at(key_square)
        key_arrow = Arrow(
            key.get_right() + SMALL_BUFF * UP,
            key_square.get_corner(UL),
            path_arc=-45 * DEGREES,
            buff=SMALL_BUFF
        )
        # CHANGE: Arrow no longer has .tip (it is a single filled shape): removing the stroke from the tip is omitted
        pass  # manimgl's arrow is a single filled shape, without .tip
        key_arrow.match_color(key)
        panels[1].add(p1_pi, key)

        p2_pi = pis[0].copy()
        p2_pi.next_to(panels[2].get_corner(DL), UR, SMALL_BUFF)
        p2_pi.change("tease")
        flip_coin = panels[2].coins[38]
        panels[3].coins[38].flip()
        flip_square = Square()
        flip_square.replace(panels[2].chessboard[38])
        flip_square.set_stroke(BLUE, 5)
        for coin in panels[2].coins:
            if coin is not flip_coin:
                coin.remove(coin.edge)
                if coin.is_heads():
                    coin.remove(coin.bottom)
                    coin.remove(coin.labels[1])
                else:
                    coin.remove(coin.top)
                    coin.remove(coin.labels[0])
                coin.set_opacity(0.25)
        panels[2].add(p2_pi)

        p3_pi = pis[1].copy()
        p3_pi.next_to(panels[3].get_corner(DL), UR, SMALL_BUFF)
        p3_pi.shift(MED_LARGE_BUFF * RIGHT)
        p3_pi.change("confused")
        panels[3].add(p3_pi)

        # Animate each panel in
        self.play(FadeIn(panels[1], DOWN))
        self.play(
            ShowCreation(key_arrow),
            FadeInFromLarge(key_square),
        )
        panels[1].add(key_arrow, key_square)
        self.wait()

        self.play(FadeIn(panels[2], UP))
        self.play(
            ShowCreation(flip_square),
            FlipCoin(flip_coin),
            p2_pi.look_at, flip_coin,
        )
        self.wait()

        self.play(FadeIn(panels[3], LEFT))
        self.wait()

        self.play(
            FadeIn(panels[0], LEFT),
            panels[1].shift, p1_shift,
        )
        self.wait()
