# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2020/chess.py (lines 4791-4865)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() now returns a hex string, not a Color object
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


class FourDCubeColoringFromTrees(ThreeDScene):
    def construct(self):
        # Camera stuffs
        frame = self.camera.frame
        light = self.camera.light_source
        light.move_to([-25, -20, 20])

        # Setup cube
        colors = [RED, GREEN, BLUE_D, YELLOW]
        cube = self.get_hypercube()
        for n, vert in enumerate(cube.verts):
            code = boolian_linear_combo(int_to_bit_coords(n, 4))
            cube.verts[n].set_color(colors[code])

        # Create trees
        trees = Group()
        original_trees = Group()
        for vert in cube.verts:
            tree = Group(
                vert,
                vert.edges,
                vert.neighbors,
            ).copy()
            original = tree.copy()
            original[0].set_color(GREY)
            original[0].scale(0)
            original_trees.add(original)
            trees.add(tree)
        for tree in trees:
            tree[0].set_color(GREY)
            tree[0].rotate(90 * DEGREES, LEFT)
            sorted_verts = Group(*tree[2])
            # CHANGE: get_color() now returns a hex string, not a Color object
            sorted_verts.submobjects.sort(key=lambda m: m.get_color())
            sorted_verts.arrange(DOWN, buff=SMALL_BUFF)
            sorted_verts.next_to(tree[0], RIGHT, buff=0.75)
            for edge, neighbor in zip(tree[1], tree[2]):
                edge.become(Line3D(
                    tree[0].get_center(),
                    neighbor.get_center(),
                    resolution=edge.resolution,
                ))
                neighbor.rotate(90 * DEGREES, LEFT)

        trees.arrange_in_grid(4, 4, buff=MED_LARGE_BUFF)
        for i in range(4):
            trees[i::4].shift(0.5 * i * RIGHT)
        trees.center()
        trees.set_height(6)
        trees.rotate(PI / 2, RIGHT)
        trees.move_to(10 * LEFT, LEFT)

        frame.set_phi(90 * DEGREES)
        frame.move_to(5 * LEFT)
        self.add(trees)
        self.wait()

        # Show transition
        anims = []
        for tree, original in zip(trees, original_trees):
            anims.append(Transform(tree, original))
        self.play(
            frame.set_euler_angles, 20 * DEGREES, 70 * DEGREES,
            frame.move_to, ORIGIN,
            LaggedStart(*anims, lag_ratio=0.2),
            run_time=8,
        )
        self.remove(trees)
        self.add(cube)
        frame.add_updater(lambda m, dt: m.increment_theta(2 * dt * DEGREES))
        self.wait(30)

    def get_hypercube(self, dim=4, width=4):
        hc_points = self.get_hypercube_points(dim, width)
        cube = Group()
        cube.verts = Group()
        cube.edges = Group()
        cube.add(cube.verts, cube.edges)
        for point in hc_points:
            vert = get_vertex_sphere(resolution=(25, 13))
            vert.rotate(PI / 2, UP)
            vert.move_to(point)
            cube.verts.add(vert)
            vert.edges = Group()
            vert.neighbors = Group()
        for n in range(2**dim):
            for power in range(dim):
                k = n ^ (1 << power)
                edge = Line3D(
                    hc_points[n],
                    hc_points[k],
                    width=0.05,
                    resolution=(31, 31)
                )
                cube.edges.add(edge)
                cube.verts[n].edges.add(edge)
                cube.verts[n].neighbors.add(cube.verts[k])
        return cube

    def get_hypercube_points(self, dim=4, width=4):
        all_coords = [
            int_to_bit_coords(n, dim).astype(float)
            for n in range(2**dim)
        ]
        vertex_holder = Mobject()
        vertex_holder.set_points([
            sum([c * v for c, v in zip(reversed(coords), [RIGHT, UP, OUT])])
            for coords in all_coords
        ])
        vertex_holder.center()
        if dim == 4:
            vertex_holder.get_points()[8:] *= 2
        vertex_holder.set_width(width)
        return vertex_holder.get_points()


class Thumbnail(FourDCubeColoringFromTrees):
    def construct(self):
        # Board
        board = Chessboard(
            shape=(8, 8),
            # shape=(6, 6),
            square_resolution=(5, 5),
            top_square_resolution=(7, 7),
        )
        board.set_gloss(0.3)
        k = 16
        board[k].set_color(YELLOW)
        board.set_height(7)

        coins = CoinsOnBoard(
            board,
            coin_config={
                # "disk_resolution": (80, 51),
                "disk_resolution": (2, 12),
            }
        )
        coins.flip_by_message("A colab!")

        board_group = Group(board, coins)
        board_group.set_width(FRAME_WIDTH / 2 - 2)
        board_group.set_x(-FRAME_WIDTH / 4)
        self.add(board_group)

        # Hypercube
        cube = self.get_hypercube(width=2)
        colors = [BLUE_D, TEAL, GREEN, YELLOW]
        for n, vert in enumerate(cube.verts):
            code = boolian_linear_combo(int_to_bit_coords(n, 4))
            cube.verts[n].set_color(colors[code])

        cube.set_width(FRAME_WIDTH / 2 - 2)
        cube.set_x(FRAME_WIDTH / 4)
        cube.set_z(0, OUT)
        cube.rotate(7 * DEGREES, UP)
        self.add(cube)

        Group(cube, board_group).to_edge(UP, LARGE_BUFF)

        v_line = Line(UP, DOWN)
        v_line.set_height(FRAME_HEIGHT)
        v_line.set_stroke(GREY_A, 3)
        self.add(v_line)

        titles = VGroup(Text("From chessboards"), Text("to hypercubes"))
        titles.match_width(board_group)
        for title, mob in zip(titles, [board_group, cube]):
            title.match_x(mob)
        titles.to_edge(DOWN)
        self.add(titles)
        return

        # Instructions
        message = OldTexText(
            "Flip one coin\\\\to describe a\\\\",
            "unique square",
            alignment="",
        )
        message[1].set_color(YELLOW)
        message.scale(1.25)
        message.to_edge(LEFT)
        message.shift(1.25 * DOWN)
        message.fix_in_frame()
        arrow = Arrow(
            message.get_corner(UR),
            message.get_corner(UR) + 3 * RIGHT + UP,
            path_arc=-70 * DEGREES,
        )
        arrow.fix_in_frame()
        arrow.shift(1.5 * LEFT)
        arrow.set_color(YELLOW)
