# ==============================================================================
# Scene:      TreeOfThreeFlips
# Source:     videos/_2020/chess.py (lines 1936-2078)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TreeOfThreeFlips.py TreeOfThreeFlips -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
# ==============================================================================

from manim_imports_ext import *

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


class TreeOfThreeFlips(ThreeDScene):
    def construct(self):
        # Setup sums
        csum = Group(
            OldTex("0 \\cdot"),
            Coin(numeric_labels=True),
            OldTex("+\\,1 \\cdot"),
            Coin(numeric_labels=True),
            OldTex("+\\,2 \\cdot"),
            Coin(numeric_labels=True),
            OldTex("="),
            Integer(0)
        )
        csum.coins = csum[1:7:2]
        csum.coins.set_height(1.5 * csum[0].get_height())
        csum.coins.flip(RIGHT)
        csum.coins[1].flip(RIGHT)
        csum.arrange(RIGHT, buff=0.1)
        csum[-1].align_to(csum[0], DOWN)
        csum[-1].shift(SMALL_BUFF * RIGHT)
        csum.to_edge(LEFT)

        csum_rect = SurroundingRectangle(csum, buff=SMALL_BUFF)
        csum_rect.set_stroke(WHITE, 1)

        # Set rhs values
        def set_rhs_target(cs, colors=[RED, GREEN, BLUE]):
            bools = [c.is_heads() for c in cs.coins]
            value = sum([n * b for n, b in enumerate(bools)]) % 3
            cs[-1].generate_target()
            cs[-1].target.set_value(value)
            cs[-1].target.set_color(colors[value])
            return cs[-1]

        rhs = set_rhs_target(csum)
        rhs.become(rhs.target)

        # Create copies
        new_csums = Group()
        for i in range(3):
            new_csum = csum.deepcopy()
            new_csum.coins = new_csum[1:7:2]
            new_csums.add(new_csum)
        new_csums.arrange(DOWN, buff=1.5)
        new_csums.next_to(csum, RIGHT, buff=3)

        # Arrows
        arrows = VGroup()
        for i, ncs in enumerate(new_csums):
            arrow = Arrow(csum_rect.get_right(), ncs.get_left())
            label = OldTexText(f"Flip coin {i}")
            label.set_height(0.3)
            label.set_fill(GREY_A)
            label.set_stroke(BLACK, 3, background=True)
            label.next_to(ORIGIN, UP, buff=0)
            label.rotate(arrow.get_angle(), about_point=ORIGIN)
            label.shift(arrow.get_center())
            arrow.label = label
            arrows.add(arrow)
        arrows.set_color(GREY)

        # Initial state label
        is_label = OldTexText(
            "Initial state: 010",
            tex_to_color_map={"0": RED_D, "1": GOLD_D}
        )
        is_label.set_height(0.4)
        is_label.next_to(csum_rect, UP, aligned_edge=LEFT)

        # Show three flips
        self.add(csum)
        self.add(csum_rect)
        self.add(is_label)
        self.wait()

        anims = []
        for i, arrow, ncs in zip(it.count(), arrows, new_csums):
            anims += [
                GrowArrow(arrow),
                FadeIn(arrow.label, lag_ratio=0.2),
            ]
        self.play(LaggedStart(*anims))
        for indices in [[0], [1, 2]]:
            self.play(*[
                TransformFromCopy(csum, new_csums[i], path_arc=30 * DEGREES, run_time=2)
                for i in indices
            ])
            self.wait()
            for i in indices:
                ncs = new_csums[i]
                ncs.coins[i].flip()
                rhs = set_rhs_target(ncs)
                ncs.coins[i].flip()
                self.play(
                    FlipCoin(ncs.coins[i]),
                    MoveToTarget(rhs)
                )

        # Put key in square 2
        board = Chessboard(shape=(1, 3), square_resolution=(5, 5))
        board.set_gloss(0.5)
        board.set_width(3)
        board.set_depth(0.25, stretch=True)
        board.space_out_submobjects(factor=1.001)
        board.next_to(ORIGIN, LEFT)
        board.to_edge(UP)
        board.shift(IN)
        board.rotate(60 * DEGREES, LEFT)
        opening_square = board[2][0]
        opening_square_top = opening_square.get_corner(UP + IN)

        key = Key()
        key.to_corner(UL, buff=LARGE_BUFF)
        key.shift(OUT)
        key.generate_target()
        key.target.scale(0.3)
        key.target.rotate(60 * DEGREES, LEFT)
        key.target.move_to(board[2][0])

        self.play(
            FadeIn(board, DOWN),
            FadeIn(key)
        )
        self.play(
            MoveToTarget(key, path_arc=30 * DEGREES),
            Rotate(opening_square, 90 * DEGREES, LEFT, about_point=opening_square_top),
        )
        self.play(
            Rotate(opening_square, 90 * DEGREES, RIGHT, about_point=opening_square_top),
            key.next_to, board[1], RIGHT, buff=0.01,
        )
        self.wait()
        self.remove(key)
        self.play(Rotate(board, 0 * DEGREES, RIGHT, run_time=0))
        self.play(Rotate(board, 60 * DEGREES, RIGHT))

        # Put coins on
        coins = csum.coins.copy()
        for coin, cube in zip(coins, board):
            coin.generate_target()
            coin.target.next_to(cube, OUT, buff=0)
        self.play(LaggedStartMap(MoveToTarget, coins, run_time=2))
        self.wait()
