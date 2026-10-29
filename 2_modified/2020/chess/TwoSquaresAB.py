# ==============================================================================
# Scene:      TwoSquaresAB
# Source:     videos/_2020/chess.py (lines 1454-1457)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TwoSquaresAB.py TwoSquaresAB -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
#   - TexSymbol no longer exists: the glyphs of OldTex are VMobjectFromSVGPath
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


class TwoSquareCase(ThreeDScene):
    CONFIG = {
        "coin_names": ["c_0", "c_1"]
    }

    def construct(self):
        frame = self.camera.frame

        # Transition to just two square
        chessboard = Chessboard()
        chessboard.shift(2 * IN + UP)
        coins = CoinsOnBoard(chessboard)
        coins.flip_by_message("To 2 bits")

        to_remove = Group(*it.chain(*zip(chessboard[:1:-1], coins[:1:-1])))
        small_board = chessboard[:2]
        coin_pair = coins[:2]
        small_group = Group(small_board, coin_pair)

        frame.set_phi(45 * DEGREES)

        two_square_words = OldTexText("What about a 2-square board?")
        two_square_words.fix_in_frame()
        two_square_words.set_height(0.5)
        two_square_words.center().to_edge(UP)

        self.add(chessboard, coins)
        self.play(
            Write(two_square_words, run_time=1),
            LaggedStartMap(
                FadeOut, to_remove,
                lambda m: (m, DOWN),
                run_time=2,
                lag_ratio=0.01
            ),
            small_group.center,
            small_group.set_height, 1.5,
            frame.set_phi, 10 * DEGREES,
            run_time=2
        )
        self.wait(3)

        coins = coin_pair

        # Show two locations for the key
        key = Key()
        key.set_width(0.7 * small_board[0].get_width())
        key.move_to(small_board[0])
        key.shift(0.01 * OUT)

        coin_pair.shift(0.04 * OUT)
        s0_top = small_board[0][0].get_top()
        s1_top = small_board[1][0].get_top()

        s0_rot_group = Group(small_board[0][0], coin_pair[0])
        s1_rot_group = Group(small_board[1][0], coin_pair[1])

        self.add(key)
        angle = 170 * DEGREES
        self.play(
            Rotate(s0_rot_group, angle, LEFT, about_point=s0_top),
            Rotate(s1_rot_group, angle, LEFT, about_point=s1_top),
            frame.set_phi, 45 * DEGREES,
        )
        self.wait()
        self.play(
            key.match_x, small_board[1],
            path_arc=PI,
            path_arc_axis=UP,
        )
        self.wait()
        self.play(
            Rotate(s0_rot_group, angle, RIGHT, about_point=s0_top),
            Rotate(s1_rot_group, angle, RIGHT, about_point=s1_top),
            frame.set_phi, 0,
            run_time=2,
        )
        self.wait()

        # Show four states pointing to two message
        states = VGroup(*[
            OldTexText(letters, tex_to_color_map={"H": GOLD, "T": RED_D})
            for letters in ["TT", "HT", "TH", "HH"]
        ])
        states.set_height(0.8)
        states.arrange(DOWN, buff=1)
        states.to_edge(LEFT)

        self.play(
            FadeOut(two_square_words),
            FlipCoin(coins[1]),
            FadeIn(states[0])
        )
        self.play(
            FlipCoin(coins[0]),
            FadeIn(states[1])
        )
        self.play(
            FlipCoin(coins[0]),
            FlipCoin(coins[1]),
            FadeIn(states[2])
        )
        self.play(
            FlipCoin(coins[0]),
            FadeIn(states[3])
        )
        self.wait()

        key_copy = key.copy()
        key_copy.match_x(small_board[0])
        small_board_copy = small_board.copy()
        small_boards = Group(small_board_copy, small_board)
        for board, vect in zip(small_boards, [UP, DOWN]):
            board.generate_target()
            board.target.set_opacity(0.7)
            board.target.shift(2 * vect)
            board.target.set_depth(0.01, stretch=True)
        self.add(key, key_copy, *small_boards)
        self.play(
            FadeOut(coins),
            MoveToTarget(small_board),
            MaintainPositionRelativeTo(key, small_board),
            MoveToTarget(small_board_copy),
            MaintainPositionRelativeTo(key_copy, small_board_copy),
        )
        self.add(*small_boards, key, key_copy)

        arrows = VGroup()
        for i in range(4):
            arrows.add(Arrow(states[i].get_right(), small_boards[i // 2].get_left()))
        arrows.set_opacity(0.75)

        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.3))
        self.wait()

        # Show one flip changing interpretation
        coins.next_to(states, LEFT, buff=1.5)

        def get_state(coins=coins):
            bools = [c.is_heads() for c in coins]
            return sum([b * (2**n) for n, b in enumerate(reversed(bools))])

        n = 3
        state_rect = SurroundingRectangle(states[n])
        board_rects = VGroup()
        for board in small_boards:
            br = SurroundingRectangle(board, buff=0)
            br.move_to(board, OUT)
            br.set_stroke(YELLOW, 3)
            board_rects.add(br)

        self.play(
            ApplyMethod(frame.shift, 4.5 * LEFT, run_time=1),
            FadeIn(coins),
            FadeIn(state_rect),
            FadeIn(board_rects[1]),
            arrows[n].set_color, YELLOW,
            arrows[n].set_opacity, 1,
        )
        self.wait()
        self.play(
            FlipCoin(coins[1]),
            FadeOut(board_rects[1]),
            FadeIn(board_rects[0]),
            state_rect.move_to, states[1],
            arrows[3].match_style, arrows[0],
            arrows[1].match_style, arrows[3],
        )
        self.wait()
        self.play(
            FlipCoin(coins[0]),
            state_rect.move_to, states[0],
            arrows[0].match_style, arrows[1],
            arrows[1].match_style, arrows[3],
        )
        self.wait()
        self.play(
            FlipCoin(coins[0]),
            state_rect.move_to, states[1],
            arrows[0].match_style, arrows[1],
            arrows[1].match_style, arrows[0],
        )
        self.wait()

        # Erase H and T, replace with 1 and 0
        bin_states = VGroup(*[
            OldTexText(letters, tex_to_color_map={"1": GOLD, "0": RED_D})
            for letters in ["00", "10", "01", "11"]
        ])
        for bin_state, state in zip(bin_states, states):
            for bit, letter in zip(bin_state, state):
                bit.replace(letter, dim_to_match=1)
        bin_coins = CoinsOnBoard(small_board, coin_config={"numeric_labels": True})
        bin_coins[1].flip()
        bin_coins.move_to(coins)

        self.play(
            FadeOut(coins, IN),
            FadeIn(bin_coins),
        )
        self.play(
            LaggedStartMap(GrowFromCenter, Group(*bin_states.family_members_with_points())),
            LaggedStartMap(ApplyMethod, Group(*states.family_members_with_points()), lambda m: (m.scale, 0)),
        )
        self.wait()

        # Add labels
        c_labels = VGroup(*[
            OldTex(name)
            for name in self.coin_names
        ])
        arrow_kw = {
            "tip_config": {
                "width": 0.2,
                "length": 0.2,
            },
            "buff": 0.1,
            "color": GREY_B,
        }
        # s_label_arrows = VGroup()
        # for high_square, low_square, label in zip(*small_boards, s_labels):
        #     label.move_to(Group(high_square, low_square))
        #     label.arrows = VGroup(
        #         Arrow(label.get_bottom(), low_square.get_top(), **arrow_kw),
        #         Arrow(label.get_top(), high_square.get_bottom(), **arrow_kw),
        #     )
        #     s_label_arrows.add(*label.arrows)

        #     self.play(
        #         FadeIn(label),
        #         *map(GrowArrow, label.arrows)
        #     )

        c_label_arrows = VGroup()
        for label, coin in zip(c_labels, bin_coins):
            label.next_to(coin, UP, LARGE_BUFF)
            arrow = Arrow(label.get_bottom(), coin.get_top(), **arrow_kw)
            c_label_arrows.add(arrow)

            self.play(
                FadeIn(label),
                GrowArrow(arrow)
            )
        self.wait()

        # Coin 1 communicates location
        bit1_rect = SurroundingRectangle(
            VGroup(
                bin_states[0][1],
                bin_states[-1][1],
            ),
            buff=SMALL_BUFF,
        )
        coin1_rect = SurroundingRectangle(
            Group(c_labels[1], bin_coins[1]),
            buff=SMALL_BUFF,
        )
        for rect in bit1_rect, coin1_rect:
            rect.insert_n_curves(100)
            nd = int(12 * get_norm(rect.get_area_vector()))
            rect.become(DashedVMobject(rect, num_dashes=nd))
            rect.set_stroke(WHITE, 2)

        kw = {
            "stroke_width": 2,
            "stroke_color": YELLOW,
            "buff": 0.05,
        }
        zero_rects, one_rects = [
            VGroup(
                SurroundingRectangle(bin_states[0][1], **kw),
                SurroundingRectangle(bin_states[1][1], **kw),
            ),
            VGroup(
                SurroundingRectangle(bin_states[2][1], **kw),
                SurroundingRectangle(bin_states[3][1], **kw),
            ),
        ]

        self.play(
            ShowCreation(bit1_rect),
            ShowCreation(coin1_rect),
            FadeOut(state_rect),
        )
        self.wait()
        self.play(board_rects[0].stretch, 0.5, 0, {"about_edge": LEFT})
        self.play(ShowCreation(zero_rects))
        self.wait()
        self.play(
            FadeOut(board_rects[0]),
            FadeOut(zero_rects),
            FadeIn(board_rects[1])
        )
        self.play(
            board_rects[1].stretch, 0.5, 0, {"about_edge": RIGHT}
        )
        self.play(
            FlipCoin(bin_coins[1]),
            arrows[1].match_style, arrows[0],
            arrows[3].match_style, arrows[1],
        )
        self.play(ShowCreation(one_rects[1]))
        self.wait()

        # Talk about null bit
        null_word = OldTexText("Null bit")
        null_word.next_to(bin_coins[0], DOWN, buff=1.5, aligned_edge=LEFT)
        null_arrow = Arrow(null_word.get_top(), bin_coins[0].get_bottom())

        self.play(
            Write(null_word),
            GrowArrow(null_arrow)
        )
        self.wait()

        for i in (0, 1, 0):
            self.play(
                FlipCoin(bin_coins[0]),
                arrows[3 - i].match_style, arrows[0],
                arrows[2 + i].match_style, arrows[3 - i],
                FadeOut(one_rects[1 - i]),
                FadeIn(one_rects[i]),
            )
            self.wait()

        # Written mathematically
        frame.generate_target()
        frame.target.set_height(10, about_edge=DOWN)
        rule_words = OldTexText("Rule: Just look at coin 1")
        rule_words.set_height(0.6)
        rule_words.next_to(frame.target.get_corner(UL), DR, buff=0.5)
        rule_arrow = Vector(1.5 * RIGHT)
        rule_arrow.next_to(rule_words, RIGHT)
        rule_arrow.set_color(BLUE)
        rule_equation = OldTex("K", "=", self.coin_names[1])
        rule_equation_long = OldTex(
            "K", "=", "0", "\\cdot",
            self.coin_names[0], "+", "1", "\\cdot",
            self.coin_names[1],
        )

        for equation in rule_equation, rule_equation_long:
            equation.set_color_by_tex("S", YELLOW)
            equation.set_height(0.7)
            equation.next_to(rule_arrow, RIGHT)

        s_labels = VGroup(
            OldTex("K", "= 0"),
            OldTex("K", "= 1"),
        )
        for label, board in zip(s_labels, small_boards):
            label.set_height(0.5)
            label.next_to(board, UP)
            label.set_color_by_tex("S", YELLOW)

        self.play(
            MoveToTarget(frame),
            FadeIn(rule_words, 2 * DOWN)
        )
        self.wait()
        for label in s_labels:
            self.play(Write(label))
        self.wait()
        self.play(
            GrowArrow(rule_arrow),
            FadeIn(rule_equation, LEFT),
        )
        self.wait()
        mid_equation = rule_equation_long[2:-1]
        mid_equation.save_state()
        mid_equation.scale(0, about_edge=LEFT)
        self.play(
            Transform(rule_equation[:2], rule_equation_long[:2]),
            Transform(rule_equation[2], rule_equation_long[-1]),
            Restore(mid_equation),
        )
        self.wait()

        self.remove(bin_coins)
        for mob in self.mobjects:
            for submob in mob.get_family():
                # CHANGE: TexSymbol no longer exists: the glyphs of OldTex are VMobjectFromSVGPath
                if isinstance(submob, VMobjectFromSVGPath):
                    submob.set_stroke(BLACK, 8, background=True)
        self.add(bin_coins)


class TwoSquaresAB(TwoSquareCase):
    CONFIG = {
        "coin_names": ["a", "b"]
    }
