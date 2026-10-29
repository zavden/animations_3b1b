# ==============================================================================
# Scene:      ErrorCorrectionMention
# Source:     videos/_2020/chess.py (lines 784-965)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ErrorCorrectionMention.py ErrorCorrectionMention -w -m --fps 15
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


def int_to_bit_coords(n, min_dim=3):
    bits = "{0:b}".format(n)
    bits = (min_dim - len(bits)) * '0' + bits
    return np.array(list(map(int, bits)))


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


class ErrorCorrectionMention(Scene):
    def construct(self):
        # Setup board
        message = "Do math!"
        error_message = "Do meth!"
        board = Chessboard()
        board.set_width(5)
        board.to_corner(DL)
        coins = CoinsOnBoard(board)
        coins.flip_by_message(message)
        bools = coins.get_bools()

        right_board = board.copy()
        right_board.to_corner(DR)
        right_board.set_opacity(0.5)
        right_board[boolian_linear_combo(bools)].set_color(BLUE, 1)

        arrow = Arrow(board.get_right(), right_board.get_left())

        words = OldTexText("Feels a bit like ", "Error correction codes", "$\\dots$")
        words.scale(1.2)
        words.to_edge(UP)

        self.add(board, coins, right_board)
        self.add(arrow)
        self.add(words)

        # Go from board diagram to bit string
        bits = VGroup()
        for coin in coins:
            bit = Integer(1 if coin.is_heads() else 0)
            bit.replace(coin, dim_to_match=1)
            bits.add(bit)

            coin.generate_target()
            coin.target.rotate(90 * DEGREES, RIGHT)
            coin.target.set_opacity(0)

        bits_rect = SurroundingRectangle(bits, buff=MED_SMALL_BUFF)
        bits_rect.set_stroke(YELLOW, 2)
        data_label = OldTexText("Data")
        data_label.next_to(bits_rect, UP)
        data_label.set_color(YELLOW)

        meaning_label = OldTexText(f"``{message}''")
        error_meaning_label = OldTexText(f"``{error_message}''")
        for label in meaning_label, error_meaning_label:
            label.scale(1.5)
            label.next_to(arrow, RIGHT)
        error_meaning_label[0][5].set_color(RED)

        message_label = OldTexText("Message")
        message_label.set_color(BLUE)
        message_label.next_to(meaning_label, UP, buff=1.5)
        message_label.to_edge(RIGHT, LARGE_BUFF)
        message_arrow = Arrow(
            message_label.get_bottom(),
            meaning_label.get_top(),
        )
        message_arrow = Arrow(
            message_label.get_left(),
            meaning_label.get_top(),
            path_arc=70 * DEGREES,
        )

        self.play(
            LaggedStartMap(MoveToTarget, coins),
            LaggedStartMap(FadeOut, board),
            Write(bits),
            run_time=3
        )
        self.play(
            words[1].set_x, 0,
            FadeOut(words[0], LEFT),
            FadeOut(words[2], LEFT),
        )
        self.play(
            ShowCreation(bits_rect),
            FadeIn(data_label, DOWN)
        )
        self.play(
            FadeOut(right_board),
            FadeIn(message_label, DOWN),
            ShowCreation(message_arrow),
            FadeIn(meaning_label)
        )
        self.wait()

        # Describe ECC
        error_index = 8 * 4 + 5
        error_bit = bits[error_index]
        error_bit_rect = SurroundingRectangle(error_bit)
        error_bit_rect.set_stroke(RED, 2)

        self.play(
            FadeInFromLarge(error_bit_rect),
            error_bit.set_value, 1 - error_bit.get_value(),
            error_bit.set_color, RED,
        )
        meaning_label.save_state()
        self.play(
            Transform(meaning_label, error_meaning_label)
        )
        self.wait()

        # Ask about correction
        question = OldTexText("How can you\\\\detect the error?")
        question.next_to(bits_rect, RIGHT, aligned_edge=UP)
        self.play(Write(question))
        self.wait(2)

        ecc = VGroup()
        for bit in int_to_bit_coords(boolian_linear_combo(bools), 6):
            ecc.add(Integer(bit).match_height(bits[0]))
        ecc.arrange(RIGHT, buff=0.2)
        ecc.set_color(GREEN)
        ecc.next_to(bits, RIGHT, MED_LARGE_BUFF, aligned_edge=DOWN)
        ecc_rect = SurroundingRectangle(ecc, buff=MED_SMALL_BUFF)
        ecc_rect.set_stroke(GREEN, 2)

        ecc_name = words[1]
        ecc_name.generate_target()
        ecc_name.target[-1].set_opacity(0)
        ecc_name.target.scale(0.75)
        ecc_name.target.next_to(ecc_rect)
        ecc_name.target.match_color(ecc)

        frame = self.camera.frame

        self.play(
            MoveToTarget(ecc_name),
            ShowIncreasingSubsets(ecc),
            ShowCreation(ecc_rect),
            ApplyMethod(frame.move_to, DOWN, run_time=2)
        )
        self.wait()

        # Show correction at play
        lines = VGroup()
        for bit in bits:
            line = Line(ecc_rect.get_top(), bit.get_center())
            line.set_stroke(GREEN, 1, opacity=0.7)
            lines.add(line)

        alert = OldTex("!!!")[0]
        alert.arrange(RIGHT, buff=SMALL_BUFF)
        alert.scale(1.5)
        alert.set_color(RED)
        alert.next_to(ecc_rect, UP)

        self.play(LaggedStartMap(
            ShowCreationThenFadeOut, lines,
            lag_ratio=0.02, run_time=3
        ))
        self.play(FadeIn(alert, DOWN, lag_ratio=0.2))
        self.wait()
        self.play(ShowCreation(lines, lag_ratio=0))
        for line in lines:
            line.generate_target()
            line.target.become(lines[error_index])
        self.play(LaggedStartMap(MoveToTarget, lines, lag_ratio=0, run_time=1))
        self.play(
            error_bit.set_value, 0,
            Restore(meaning_label)
        )
        self.play(
            FadeOut(lines),
            FadeOut(alert),
            FadeOut(error_bit_rect),
            error_bit.set_color, WHITE,
        )
        self.wait()

        # Hamming name
        hamming_label = OldTexText("e.g. Hamming codes")
        hamming_label.move_to(ecc_name, LEFT)

        self.play(
            Write(hamming_label),
            FadeOut(ecc_name, DOWN)
        )
        self.wait()
