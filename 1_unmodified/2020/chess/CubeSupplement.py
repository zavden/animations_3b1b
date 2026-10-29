# ==============================================================================
# Scene:      CubeSupplement
# Source:     videos/_2020/chess.py (lines 2744-2824)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CubeSupplement.py CubeSupplement -w -m --fps 15
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


class CubeSupplement(ThreeDScene):
    CONFIG = {
        "try_different_strategies": False,
    }

    def construct(self):
        # Map 8 states to square choices
        boards = Group(*[Chessboard(shape=(1, 3)) for x in range(8)])
        boards.arrange(DOWN, buff=0.5 * boards[0].get_height())
        boards.set_height(7)
        boards.to_edge(LEFT)

        coin_sets = Group(*[
            CoinsOnBoard(board, coin_config={"numeric_labels": True})
            for board in boards
        ])
        vert_coords = [[n // 4, (n // 2) % 2, n % 2] for n in range(7, -1, -1)]
        for coords, coins in zip(vert_coords, coin_sets):
            coins.flip_by_bools(coords)

        def get_choice_boards(values, boards):
            choices = VGroup()
            for value, board in zip(values, boards):
                choice = VGroup(*[Square() for x in range(3)])
                choice.arrange(RIGHT, buff=0)
                choice.match_height(board)
                choice.next_to(board, RIGHT, buff=1.25)
                choice.set_fill(GREY_D, 1)
                choice.set_stroke(WHITE, 1)
                choice[value].set_fill(TEAL)
                choices.add(choice)
            return choices

        colors = [RED, GREEN, BLUE_D]
        color_words = ["Red", "Green", "Blue"]
        s_values = [sum([n * v for n, v in enumerate(cs)]) % 3 for cs in vert_coords]
        choice_boards = get_choice_boards(s_values, boards)
        c_labels = VGroup()
        s_arrows = VGroup()
        for value, board, choice_board in zip(s_values, boards, choice_boards):
            arrow = Vector(RIGHT)
            arrow.next_to(board, RIGHT, SMALL_BUFF)
            c_label = OldTexText(color_words[value], color=colors[value])
            c_label.next_to(choice_board, RIGHT)
            c_labels.add(c_label)
            s_arrows.add(arrow)

            choice_board.generate_target()
            choice_board.target[value].set_fill(colors[value])

        self.play(
            LaggedStartMap(FadeIn, boards, lag_ratio=0.25),
            LaggedStartMap(FadeIn, coin_sets, lag_ratio=0.25),
            run_time=3
        )
        self.play(
            LaggedStartMap(GrowArrow, s_arrows, lag_ratio=0.25),
            LaggedStartMap(FadeIn, choice_boards, lambda m: (m, LEFT), lag_ratio=0.25),
        )
        self.wait()

        # Fork
        if self.try_different_strategies:
            for x in range(5):
                values = list(np.arange(8) % 3)
                random.shuffle(values)
                new_cboards = get_choice_boards(values, boards)
                self.play(
                    LaggedStartMap(FadeOut, choice_boards, lambda m: (m, 0.25 * UP)),
                    LaggedStartMap(FadeIn, new_cboards, lambda m: (m, 0.25 * DOWN)),
                )
                choice_boards = new_cboards
                self.wait(2)

        else:
            # Associate choices with colors
            self.play(
                LaggedStartMap(MoveToTarget, choice_boards),
                LaggedStartMap(FadeIn, c_labels),
            )
            self.wait()
