# ==============================================================================
# Scene:      IntroducePuzzle
# Source:     videos/_2020/chess.py (lines 192-335)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroducePuzzle.py IntroducePuzzle -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
#   - get_color() of a Cube (Group) no longer returns the color of its faces: it is read from cube[0]
#   - get_color() of a Cube (Group) fails; the color of its first face is taken
# ==============================================================================

from manim_imports_ext import *

def boolian_linear_combo(bools):
    return reduce(op.xor, [b * n for n, b in enumerate(bools)], 0)


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


# Scenes
class IntroducePuzzle(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        # Setup
        frame = self.camera.frame

        chessboard = Chessboard()
        chessboard.move_to(ORIGIN, OUT)

        grid = NumberPlane(
            x_range=(0, 8), y_range=(0, 8),
            faded_line_ratio=0
        )
        grid.match_height(chessboard)
        grid.next_to(chessboard, OUT, 1e-8)
        low_grid = grid.copy()
        low_grid.next_to(chessboard, IN, 1e-8)
        grid.add(low_grid)
        grid.set_stroke(GREY, width=2)
        grid.set_gloss(0.5)
        grid.prepare_for_nonlinear_transform(0)

        coins = CoinsOnBoard(chessboard)
        coins.set_gloss(0.2)
        coins_to_flip = Group()
        head_bools = string_to_bools('3b1b  :)')
        for coin, heads in zip(coins, head_bools):
            if not heads:
                coins_to_flip.add(coin)
        coins_to_flip.shuffle()

        count_label = VGroup(
            Integer(0, edge_to_fix=RIGHT),
            OldTexText("Coins")
        )
        count_label.arrange(RIGHT, aligned_edge=DOWN)
        count_label.to_corner(UL)
        count_label.fix_in_frame()

        # Draw board and coins
        frame.set_euler_angles(-25 * DEGREES, 70 * DEGREES, 0)
        self.play(
            FadeIn(chessboard),
            ShowCreationThenDestruction(grid, lag_ratio=0.01),
            frame.set_theta, 0,
            frame.set_phi, 45 * DEGREES,
            run_time=3,
        )
        self.wait()

        self.add(count_label)
        self.play(
            ShowIncreasingSubsets(coins),
            UpdateFromFunc(count_label[0], lambda m, c=coins: m.set_value(len(c))),
            rate_func=bezier([0, 0, 1, 1]),
            run_time=2,
        )
        self.wait()
        self.play(LaggedStartMap(FlipCoin, coins_to_flip, run_time=6, lag_ratio=0.1))
        self.add(coins)
        self.wait()

        # Show key
        key = Key()
        key.rotate(PI / 4, RIGHT)
        key.move_to(3 * OUT)
        key.scale(0.8)
        key.to_edge(LEFT, buff=1)

        k = boolian_linear_combo(head_bools) ^ 63  # To make the flip below the actual solution
        key_cube = Cube(square_resolution=(6, 6))
        # CHANGE: get_color() of a Cube (Group) fails; the color of its first face is taken
        key_cube.match_color(chessboard[k][0])
        key_cube.replace(chessboard[k], stretch=True)
        chessboard.replace_submobject(k, key_cube)
        key_square = key_cube[0]
        chessboard.generate_target()
        chessboard.save_state()
        for i, cube in enumerate(chessboard.target):
            if i == k:
                cube[0].set_color(MAROON_E)
            else:
                # CHANGE: get_color() of a Cube (Group) no longer returns the color of its faces: it is read from cube[0]
                cube.set_color(interpolate_color(cube[0].get_color(), BLACK, 0.8))

        key.generate_target()
        key.target.rotate(PI / 4, LEFT)
        key.target.set_width(0.7 * key_square.get_width())
        key.target.next_to(key_square, IN, buff=SMALL_BUFF)

        self.play(FadeIn(key, LEFT))
        self.wait()
        self.play(
            FadeOut(coins, lag_ratio=0.01),
            MoveToTarget(chessboard),
        )
        ks_top = key_square.get_top()
        self.play(
            Rotate(key_square, PI / 2, axis=LEFT, about_point=ks_top),
            MoveToTarget(key),
            frame.set_phi, 60 * DEGREES,
            run_time=2,
        )
        self.play(
            Rotate(key_square, PI / 2, axis=RIGHT, about_point=ks_top),
            run_time=2,
        )
        chessboard.saved_state[k][0].match_color(key_square)
        self.play(
            chessboard.restore,
            FadeIn(coins),
            frame.set_phi, 0 * DEGREES,
            frame.move_to, 2 * LEFT,
            run_time=3
        )

        # State goal
        goal = OldTexText(
            "Communicate where\\\\the key is",
            " by turning\\\\over one coin.",
            alignment=""
        )
        goal.next_to(count_label, DOWN, LARGE_BUFF, LEFT)
        goal.fix_in_frame()
        goal[1].set_color(YELLOW)

        self.play(FadeIn(goal[0]))
        self.wait()
        self.play(FadeIn(goal[1]))
        self.wait()

        coin = coins[63]
        rect = SurroundingRectangle(coin, color=TEAL)
        rect.set_opacity(0.5)
        rect.save_state()
        rect.replace(chessboard)
        rect.set_stroke(width=0)
        rect.set_fill(opacity=0)

        self.play(Restore(rect, run_time=2))
        self.add(coin, rect)
        self.play(FlipCoin(coin), FadeOut(rect))
