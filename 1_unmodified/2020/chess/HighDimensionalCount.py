# ==============================================================================
# Scene:      HighDimensionalCount
# Source:     videos/_2020/chess.py (lines 3515-3843)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HighDimensionalCount.py HighDimensionalCount -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


def get_vertex_sphere(height=0.4, color=GREY, resolution=(21, 21)):
    sphere = Sphere(resolution=resolution)
    sphere.set_height(height)
    sphere.set_color(color)
    return sphere


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


class HighDimensionalCount(ThreeDScene):
    def construct(self):
        # Definitions
        N = 6
        colors = [RED, GREEN, BLUE_D, YELLOW, PINK, TEAL]
        coords = np.array([0, 1, 1, 1, 0, 0])

        # Add chess board
        board = Chessboard(shape=(2, 3))
        board.set_height(2)
        board.to_corner(UL)

        grid = NumberPlane(
            x_range=(0, 3), y_range=(0, 2),
            faded_line_ratio=0
        )
        grid.match_height(board)
        grid.match_width(board, stretch=True)
        grid.next_to(board, OUT, 1e-8)
        grid.set_gloss(0.5)

        coins = CoinsOnBoard(board, coin_config={"numeric_labels": True})
        coins.flip_by_bools(coords)
        coin_labels = VGroup()
        for i, coin in zip(coords, coins):
            coin_labels.add(coin.labels[1 - i])

        self.play(
            ShowCreationThenFadeOut(grid, lag_ratio=0.1),
            FadeIn(board),
            FadeIn(coins, lag_ratio=0.1),
            run_time=2
        )

        # Setup corners
        def get_vert(height=0.4, color=RED):
            return get_vertex_sphere(height, color)

        def get_vert_label(coords):
            args = ["("]
            for coord in coords:
                args.append(str(coord))
                args.append(",")
            args[-1] = ")"
            return OldTex(*args)

        def get_board_with_highlights(n, height=1, N=N, colors=colors):
            board = VGroup(*[Square() for x in range(N)])
            board.arrange_in_grid(2, 3, buff=0)
            board.set_fill(GREY_E, 1)
            board.set_stroke(WHITE, 1)
            board.set_height(height)
            board[n].set_fill(colors[n])
            return board

        vert = get_vert()
        vert_label = get_vert_label(coords)
        vert_board = get_board_with_highlights(0)
        vert_label.next_to(vert, LEFT)
        vert_board.next_to(vert_label, DOWN, MED_LARGE_BUFF)
        neighbors = Group()
        for color in colors:
            neighbors.add(get_vert(color=color))
        neighbors.arrange(DOWN, buff=0.75)
        neighbors.next_to(vert, RIGHT, buff=2)
        neighbor_labels = VGroup()
        edges = VGroup()
        neighbor_boards = VGroup()
        for n, neighbor in enumerate(neighbors):
            edge = Line(
                vert.get_center(),
                neighbor.get_center(),
                buff=vert.get_height() / 2,
            )
            new_coords = list(coords)
            new_coords[n] ^= 1
            label = get_vert_label(new_coords)
            label.next_to(neighbor, RIGHT)
            label.add(SurroundingRectangle(label[2 * n + 1], buff=0.05))
            n_board = get_board_with_highlights(n, height=0.7)
            n_board.next_to(label, RIGHT)

            neighbor_boards.add(n_board)
            edges.add(edge)
            neighbor_labels.add(label)

        vertex_group = Group(
            vert_board, vert_label, vert,
            edges,
            neighbors, neighbor_labels, neighbor_boards
        )
        vertex_group.to_corner(DL)

        # Show coords with states
        cl_mover = coin_labels.copy()
        cl_mover.generate_target()
        for m1, m2 in zip(cl_mover.target, vert_label[1::2]):
            m1.replace(m2)
        self.play(
            MoveToTarget(cl_mover),
        )
        self.play(
            FadeIn(vert_label),
            FadeOut(cl_mover)
        )
        self.play(FadeIn(vert_board))
        self.wait()
        self.play(
            ShowIncreasingSubsets(neighbor_labels),
            ShowCreation(edges),
        )
        self.wait()
        self.play(LaggedStartMap(
            TransformFromCopy, neighbor_boards,
            lambda m, b=vert_board: (b, m)
        ))
        self.wait()

        # Show one vertex
        self.play(FadeInFromLarge(vert))
        self.play(LaggedStartMap(
            TransformFromCopy, neighbors,
            lambda m, v=vert: (v, m)
        ))
        self.wait()

        # Isolate vertex
        edges.apply_depth_test()
        tree = Group(vert, edges, neighbors)
        tree.generate_target()
        tree.target[0].scale(0.5)
        tree.target[2].scale(0.5)
        tree.target[2].arrange(DOWN, buff=0)
        tree.target[2].next_to(vert, RIGHT, MED_LARGE_BUFF)
        for edge, nv in zip(tree.target[1], tree.target[2]):
            new_edge = Line(
                vert.get_center(),
                nv.get_center(),
            )
            edge.become(new_edge)
            edge.set_stroke(WHITE, 2)
        tree.target.rotate(-90 * DEGREES)
        tree.target.center()

        short_label = vert_label[1::2]
        short_label.generate_target()
        short_label.target.arrange(RIGHT, buff=SMALL_BUFF)
        short_label.target.match_width(tree.target)
        short_label.target.next_to(tree.target, UP)
        short_label.target.set_fill(GREY_A)

        self.play(
            MoveToTarget(tree),
            MoveToTarget(short_label),
            LaggedStartMap(FadeOut, Group(
                vert_label[0::2],
                vert_board,
                *neighbor_labels,
                *neighbor_boards,
                *board,
                *coins,
            )),
            run_time=2,
        )
        tree.add(short_label)

        # Show all vertices
        def get_bit_string(n, template=short_label):
            bits = VGroup(*map(Integer, int_to_bit_coords(n, min_dim=6)))
            bits.arrange(RIGHT, buff=0.075)
            bits.match_height(template)
            bits.set_color(GREY_A)
            return bits

        new_trees = Group()
        for n in [0, 1, 62, 63]:
            new_tree = tree.copy()
            bits = get_bit_string(n)
            bits.move_to(new_tree[3])
            new_tree.replace_submobject(3, bits)
            new_trees.add(new_tree)
        for new_tree, color in zip(new_trees, [YELLOW, GREEN, RED, BLUE_D]):
            new_tree[0].set_color(color)
        new_trees.arrange(RIGHT, buff=MED_LARGE_BUFF)
        new_trees.move_to(tree)
        new_trees[:2].to_edge(LEFT)
        new_trees[2:].to_edge(RIGHT)

        dots = VGroup(*[Tex("\\dots") for x in range(2)])
        dots.scale(2)
        dots[0].move_to(Group(new_trees[1], tree))
        dots[1].move_to(Group(new_trees[2], tree))

        top_brace = Brace(new_trees, UP, buff=MED_LARGE_BUFF)
        total_label = top_brace.get_text("$2^n$ total vertices", buff=MED_LARGE_BUFF)

        low_brace = Brace(tree, DOWN)
        neighbors_label = low_brace.get_text("n neighbors")

        self.play(
            GrowFromCenter(low_brace),
            Write(neighbors_label, run_time=1)
        )
        self.wait()
        self.play(
            GrowFromCenter(dots),
            GrowFromCenter(top_brace),
            LaggedStartMap(
                TransformFromCopy, new_trees,
                lambda m, t=tree: (t, m)
            ),
            Write(total_label, run_time=1),
            run_time=2,
        )
        self.wait()

        # Count red neighbors
        middle_tree = tree
        frame = self.camera.frame
        self.play(frame.move_to, UP)

        count = Integer(1)
        count.set_color(RED)
        count.scale(1.5)
        count.next_to(total_label, UP, LARGE_BUFF, aligned_edge=LEFT)
        two_to_n_label = OldTex("2^n")
        two_to_n_label.scale(1.5)
        two_to_n_label.set_color(RED)
        two_to_n_label.move_to(count, LEFT)

        n_arrows = VGroup()
        for tree in [*new_trees[:2], middle_tree, *new_trees[2:]]:
            arrow = Vector(
                [-1, -2, 0],
                tip_config={"width": 0.2, "length": 0.2}
            )
            arrow.match_height(tree[1])
            arrow.next_to(tree[2][0], UR, buff=0)
            arrow.set_color(RED)
            n_arrows.add(arrow)

        self.add(n_arrows[0], count)
        self.wait()
        self.add(n_arrows[1])
        count.increment_value()
        self.wait()
        self.play(
            ChangeDecimalToValue(count, 63, rate_func=rush_into),
            LaggedStartMap(FadeIn, n_arrows[2:], lag_ratio=0.5),
            run_time=3
        )
        self.remove(count)
        self.add(two_to_n_label)
        self.wait()

        rhs = OldTex("=", "n", "\\cdot", "(\\text{\\# Red vertices})")
        rhs.scale(1.5)
        rhs.next_to(two_to_n_label, RIGHT)
        rhs.shift(0.05 * DOWN)
        rhs.set_color_by_tex("Red", RED)
        highlighted_edges = VGroup(*middle_tree[1], new_trees[2][1]).copy()
        highlighted_edges.set_stroke(YELLOW, 3)
        highlighted_edges.shift(0.01 * OUT)
        edge_anim = ShowCreationThenFadeOut(
            highlighted_edges, lag_ratio=0.3
        )

        self.play(edge_anim)
        self.play(Write(rhs), run_time=1)
        self.play(edge_anim)
        self.wait(2)

        # Conclusion
        pairs = VGroup(VGroup(OldTex("n"), OldTex("2^n")))
        pairs.set_color(YELLOW)
        for n in range(1, 10):
            pairs.add(VGroup(Integer(n), Integer(2**n)))
        for pair in pairs:
            pair.arrange(RIGHT, buff=0.75, aligned_edge=DOWN)
            line = Line(LEFT, RIGHT)
            line.set_stroke(WHITE, 1)
            line.set_width(2)
            line.next_to(pair, DOWN, aligned_edge=LEFT)
            line.shift(SMALL_BUFF * LEFT)
            pair.add(line)
            pairs.add(pair)
        pairs.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        pairs.set_height(7)
        pairs.to_edge(LEFT)
        pairs.shift(UP)

        marks = VGroup()
        for n, pair in zip(it.count(1), pairs[1:]):
            if sum(int_to_bit_coords(n)) == 1:
                mark = Checkmark()
            else:
                mark = Exmark()
            mark.move_to(pair[1], LEFT)
            mark.shift(RIGHT)
            marks.add(mark)

        v_line = Line(UP, DOWN)
        v_line.set_height(7)
        v_line.set_stroke(WHITE, 1)
        v_line.set_x((pairs[0][0].get_right() + pairs[0][1].get_left())[0] / 2)
        v_line.match_y(pairs)
        pairs.add(v_line)

        new_trees.generate_target()
        new_trees.target[:2].move_to(middle_tree, RIGHT)
        shift_vect = new_trees.target[0].get_center() - new_trees[0].get_center()

        self.play(
            MoveToTarget(new_trees),
            top_brace.match_width, new_trees.target, {"about_edge": RIGHT},
            total_label.shift, shift_vect * 0.5,
            n_arrows[:2].shift, shift_vect,
            FadeOut(middle_tree, RIGHT),
            FadeOut(n_arrows[2], RIGHT),
            FadeOut(dots[0], 2 * RIGHT),
            Write(pairs)
        )
        self.play(LaggedStartMap(
            FadeIn, marks,
            lambda m: (m, 0.2 * LEFT),
            lag_ratio=0.4,
            run_time=5,
        ))
        self.wait()
