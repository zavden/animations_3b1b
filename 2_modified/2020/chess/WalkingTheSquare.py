# ==============================================================================
# Scene:      WalkingTheSquare
# Source:     videos/_2020/chess.py (lines 1476-1618)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WalkingTheSquare.py WalkingTheSquare -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
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


class WalkingTheSquare(ThreeDScene):
    def construct(self):
        # Setup objects
        plane = NumberPlane(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            height=15,
            width=15,
            faded_line_ratio=3,
            axis_config={"include_tip": False}
        )
        plane.move_to(1.5 * DOWN)
        plane.add_coordinate_labels()
        plane.x_axis.add_numbers([0])

        board = Chessboard(shape=(1, 2))
        board.set_height(1.5)
        board.move_to(plane.c2p(-0.75, 0.75))
        coins = CoinsOnBoard(
            board,
            coin_config={"numeric_labels": True}
        )
        coins.flip(RIGHT)

        coords = [(0, 0), (0, 1), (1, 0), (1, 1)]
        coord_labels = VGroup()
        dots = VGroup()
        for x, y in coords:
            label = OldTex(f"({x}, {y})")
            point = plane.c2p(x, y)
            label.next_to(point, UR, buff=0.25)
            dot = Dot(point, radius=0.075)
            dot.set_color(GREY)
            dots.add(dot)
            coord_labels.add(label)

        active_dot = Dot(radius=0.15, color=YELLOW)
        active_dot.move_to(plane.c2p(0, 0))

        # Walk around square
        self.play(Write(plane))
        self.play(
            FadeIn(board),
            FadeIn(coins),
            FadeIn(active_dot),
            FadeIn(coord_labels[0]),
        )
        edges = VGroup()
        for i, j, c in [(0, 1, 1), (1, 3, 0), (3, 2, 1), (2, 0, 0)]:
            edge = Line(plane.c2p(*coords[i]), plane.c2p(*coords[j]))
            edge.set_stroke(PINK, 3)
            edges.add(edge)

            anims = [
                FlipCoin(coins[c]),
                ShowCreation(edge),
                ApplyMethod(active_dot.move_to, dots[j])
            ]
            if j != 0:
                anims += [
                    FadeInFromPoint(coord_labels[j], coord_labels[i].get_center()),
                ]
            self.add(edge, dots[i], active_dot)
            self.play(*anims)
        self.add(edges, dots, active_dot)
        self.wait()

        # Show a few more flips
        self.play(
            FlipCoin(coins[0]),
            active_dot.move_to, dots[2],
        )
        self.play(
            FlipCoin(coins[1]),
            active_dot.move_to, dots[3],
        )
        self.play(
            FlipCoin(coins[1]),
            active_dot.move_to, dots[2],
        )
        self.wait()

        # Circles illustrating scheme
        low_rect = SurroundingRectangle(
            VGroup(edges[3], coord_labels[0], coord_labels[2], plane.x_axis.numbers[-1]),
            buff=0.25,
        )
        low_rect.round_corners()
        low_rect.insert_n_curves(30)
        low_rect.set_stroke(YELLOW, 3)
        high_rect = low_rect.copy()
        high_rect.shift(dots[1].get_center() - dots[0].get_center())

        key = Key()
        key.set_color(YELLOW)
        key.set_gloss(0)
        key.match_width(board[0])
        key.next_to(board[0], UP, SMALL_BUFF)

        s_labels = VGroup(
            OldTex("\\text{Key} = 0").next_to(low_rect, UP, SMALL_BUFF),
            OldTex("\\text{Key} = 1").next_to(high_rect, UP, SMALL_BUFF),
        )

        self.play(
            ShowCreation(low_rect),
        )
        self.play(
            FadeIn(key, DOWN),
            FadeIn(s_labels[0], DOWN),
        )
        self.play(
            FlipCoin(coins[0]),
            active_dot.move_to, dots[0],
        )
        self.wait(0.5)
        self.play(
            FlipCoin(coins[0]),
            active_dot.move_to, dots[2],
        )
        self.wait()
        self.play(
            TransformFromCopy(low_rect, high_rect),
            FadeIn(s_labels[1], DOWN),
            low_rect.set_stroke, GREY, 1,
            FlipCoin(coins[1]),
            active_dot.move_to, dots[3],
            key.match_x, board[1],
        )
        self.wait()
        self.play(
            FlipCoin(coins[0]),
            active_dot.move_to, dots[1],
        )
        self.wait()
        self.play(
            FlipCoin(coins[1]),
            active_dot.move_to, dots[0],
            key.match_x, board[0],
            high_rect.match_style, low_rect,
            low_rect.match_style, high_rect,
        )
        self.wait()
