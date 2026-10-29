# ==============================================================================
# Scene:      ThreeSquareCase
# Source:     videos/_2020/chess.py (lines 1621-1896)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThreeSquareCase.py ThreeSquareCase -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
#   - Tex no longer accepts integers: str(n) is passed
#   - Error in the original: Chessboard has no flip_by_bools; the coins are in board.coins
#   - In 2020 a leaf mobject with points was its own [0] (split included self); here square[0] fails: square is used
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


class ThreeSquareCase(ThreeDScene):
    CONFIG = {
        "coin_names": ["c_0", "c_1", "c_2"]
    }

    def construct(self):
        # Show sequence of boards
        boards = Group(
            Chessboard(shape=(1, 2), height=0.25 * 1),
            Chessboard(shape=(1, 3), height=0.25 * 1),
            Chessboard(shape=(2, 2), height=0.25 * 2),
            Chessboard(shape=(8, 8), height=0.25 * 8),
        )
        dots = OldTex("\\dots")
        group = Group(*boards[:3], dots, boards[3])

        group.arrange(RIGHT)
        group.set_width(FRAME_WIDTH - 1)

        board_groups = Group()
        for board in boards:
            board.coins = CoinsOnBoard(board, coin_config={"numeric_labels": True})
            board_groups.add(Group(board, board.coins))
        boards[0].coins.flip_at_random()
        boards[1].coins.flip_by_bools([False, True, False])
        boards[2].coins.flip_at_random()
        boards[3].coins.flip_by_message("3 Fails!")

        def get_board_transform(i, bgs=board_groups):
            return TransformFromCopy(
                bgs[i], bgs[i + 1],
                path_arc=PI / 2,
                run_time=2,
            )

        frame = self.camera.frame
        frame.save_state()
        frame.scale(0.5)
        frame.move_to(boards[:2])

        self.add(board_groups[0])
        self.play(get_board_transform(0))
        turn_animation_into_updater(Restore(frame, run_time=4))
        self.add(frame)
        self.play(get_board_transform(1))
        self.play(
            Write(dots),
            get_board_transform(2),
        )
        self.wait()

        # Isolate 3 square board
        board_group = board_groups[1]
        board = boards[1]
        coins = board.coins

        title = OldTexText("Three square case")
        title.set_height(0.7)
        title.to_edge(UP)

        board_group.generate_target()
        board_group.target.set_width(4)
        board_group.target.move_to(DOWN, OUT)

        self.save_state()
        self.play(
            MoveToTarget(board_group, rate_func=squish_rate_func(smooth, 0.5, 1)),
            Write(title),
            LaggedStartMap(FadeOut, Group(
                board_groups[0],
                board_groups[2],
                dots,
                board_groups[3],
            ), lambda m: (m, DOWN)),
            run_time=2,
        )
        self.wait()

        # Try 0*c0 + 1*c1 + 2*c2
        s_sum = OldTex(
            "0", "\\cdot", self.coin_names[0], "+",
            "1", "\\cdot", self.coin_names[1], "+",
            "2", "\\cdot", self.coin_names[2],
        )
        s_sum.set_height(0.6)
        c_sum = s_sum.copy()
        s_sum.center().to_edge(UP)
        c_sum.next_to(s_sum, DOWN, LARGE_BUFF)

        coin_copies = Group()
        for i in range(3):
            part = c_sum.get_part_by_tex(self.coin_names[i], substring=False)
            coin_copy = coins[i].copy()
            coin_copy.set_height(1.2 * c_sum[0].get_height())
            coin_copy.move_to(part)
            coin_copy.align_to(c_sum, UP)
            part.set_opacity(0)
            coin_copies.add(coin_copy)

        self.play(
            FadeOut(title),
            FadeIn(s_sum[:3]),
            FadeIn(c_sum[:2]),
        )
        self.play(TransformFromCopy(coins[0], coin_copies[0]))
        self.wait()
        self.play(
            FadeIn(s_sum[3:7]),
            FadeIn(c_sum[3:6]),
        )
        self.play(TransformFromCopy(coins[1], coin_copies[1]))
        self.wait()
        self.play(
            FadeIn(s_sum[7:11]),
            FadeIn(c_sum[7:10]),
        )
        self.play(TransformFromCopy(coins[2], coin_copies[2]))
        self.wait()
        self.add(s_sum, c_sum, coin_copies)

        rhs = VGroup(OldTex("="), Integer(1))
        rhs.arrange(RIGHT)
        rhs[1].set_color(YELLOW)
        rhs.match_height(c_sum[0])
        rhs.next_to(c_sum, RIGHT, aligned_edge=UP)
        braces = VGroup(
            Brace(c_sum[0:3], DOWN),
            Brace(c_sum[0:7], DOWN),
            Brace(c_sum[0:11], DOWN),
        )
        for brace, n in zip(braces, [0, 1, 1]):
            # CHANGE: Tex no longer accepts integers: str(n) is passed
            brace.add(brace.get_tex(str(n)))
        self.play(GrowFromCenter(braces[0]))
        self.wait()
        self.play(ReplacementTransform(braces[0], braces[1]))
        self.wait()
        self.play(ReplacementTransform(braces[1], braces[2]))
        self.play(
            TransformFromCopy(braces[2][-1], rhs[1], path_arc=-PI / 2),
            Write(rhs[0]),
        )
        self.play(FadeOut(braces[2]))
        self.wait()

        # Show values of S
        s_labels = VGroup(*[
            OldTex(f"K = {n}")
            for n in range(3)
        ])
        for label, square in zip(s_labels, board):
            label.next_to(square, UP)
            label.set_width(0.8 * square.get_width())
            label.set_color(YELLOW)

        key = Key(depth_test=False)
        key.set_stroke(BLACK, 3, background=True)
        key.set_width(0.8 * board[0].get_width())
        key.move_to(board[0])

        self.play(
            coins.next_to, board, DOWN,
            coins.match_z, coins,
            board.set_opacity, 0.75,
            FadeIn(key),
            FadeIn(s_labels[0])
        )
        self.wait(0.5)
        for i in (1, 2):
            self.play(
                ApplyMethod(key.move_to, board[i], path_arc=-45 * DEGREES),
                s_labels[i - 1].set_fill, GREY, 0.25,
                FadeIn(s_labels[i]),
            )
            self.wait(0.5)

        # Mod 3 label
        mod3_label = OldTexText("(mod 3)")
        mod3_label.match_height(s_sum)
        mod3_label.set_color(BLUE)
        mod3_label.next_to(s_sum, RIGHT, buff=0.75)

        rhs_rhs = OldTex("\\equiv 0")
        rhs_rhs.match_height(rhs)
        rhs_rhs.next_to(rhs, RIGHT)

        self.play(Write(mod3_label))
        self.wait()
        self.play(
            FlipCoin(coins[2]),
            FlipCoin(coin_copies[2]),
            rhs[1].set_value, 3,
        )
        self.wait()
        self.play(Write(rhs_rhs))
        self.wait()
        self.play(
            rhs[1].set_value, 0,
            FadeOut(rhs_rhs)
        )

        # Show a few flips
        for i in [2, 1, 0, 2, 1, 2, 0]:
            bools = coins.get_bools()
            bools[i] = not bools[i]
            new_sum = sum([n * b for n, b in enumerate(bools)]) % 3
            self.play(
                FlipCoin(coins[i]),
                FlipCoin(coin_copies[i]),
                rhs[1].set_value, new_sum,
            )
            self.wait()

        # Show general sum
        general_sum = OldTex(r"\sum ^{63}_{n=0}n\cdot c_n")
        mod_64 = OldTexText("(mod 64)")
        mod_64.next_to(general_sum, DOWN)
        general_sum.add(mod_64)
        general_sum.to_corner(UL)

        self.play(FadeIn(general_sum))
        self.wait()
        self.play(FadeOut(general_sum))

        # Walk through 010 example
        # CHANGE: Error in the original: Chessboard has no flip_by_bools; the coins are in board.coins
        board.coins.flip_by_bools([False, False, True])
        self.play(
            s_labels[2].set_fill, GREY, 0.25,
            s_labels[0].set_fill, YELLOW, 1,
            ApplyMethod(key.move_to, board[0], path_arc=30 * DEGREES)
        )
        self.wait()
        self.play(
            FlipCoin(coins[1]),
            FlipCoin(coin_copies[1]),
            rhs[1].set_value, 0,
        )
        self.wait()
        square = Square()
        square.set_stroke(YELLOW, 3)
        square.replace(board[0])
        # CHANGE: In 2020 a leaf mobject with points was its own [0] (split included self); here square[0] fails: square is used
        square.move_to(board[0], OUT)
        self.play(ShowCreation(square))
        self.wait()
        self.play(FadeOut(square))

        # Walk through alternate flip on 010 example
        self.play(
            FlipCoin(coins[1]),
            FlipCoin(coin_copies[1]),
            rhs[1].set_value, 1,
        )

        morty = Mortimer(height=1.5, mode="hooray")
        morty.to_corner(DR)
        bubble = SpeechBubble(height=2, width=2)
        bubble.pin_to(morty)
        bubble.write("There's another\\\\way!")

        self.play(
            FadeIn(morty),
            ShowCreation(bubble),
            Write(bubble.content, run_time=1),
        )
        self.play(Blink(morty))
        self.play(
            FadeOut(VGroup(morty, bubble, bubble.content))
        )

        self.play(
            FlipCoin(coins[2]),
            FlipCoin(coin_copies[2]),
            rhs[1].set_value, 3,
        )
        self.wait()
        self.play(rhs[1].set_value, 0)
        self.wait()
