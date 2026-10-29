# ==============================================================================
# Scene:      ShowCube
# Source:     videos/_2020/chess.py (lines 2331-2741)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowCube.py ShowCube -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
#   - get_color() returns a hex string, not a Color
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


class ShowCube(ThreeDScene):
    def construct(self):
        # Camera stuffs
        frame = self.camera.frame
        light = self.camera.light_source
        light.move_to([-10, -10, 20])

        # Plane and axes
        plane = NumberPlane(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            height=15,
            width=15,
            faded_line_ratio=3,
            axis_config={"include_tip": False}
        )
        plane.add_coordinate_labels()
        plane.coordinate_labels.set_stroke(width=0)
        axes = ThreeDAxes(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            z_range=(-2, 2, 1),
            height=15,
            width=15,
            depth=15,
        )
        axes.apply_depth_test()

        # Vertices and edges
        vert_coords = [
            (n % 2, (n // 2) % 2, (n // 4) % 2)
            for n in range(8)
        ]
        verts = []
        coord_labels = VGroup()
        coord_labels_2d = VGroup()
        for coords in vert_coords:
            vert = axes.c2p(*coords)
            verts.append(vert)
            x, y, z = coords
            label = OldTex(f"({x}, {y}, {z})")
            label.set_height(0.3)
            label.next_to(vert, UR, SMALL_BUFF)
            label.rotate(89 * DEGREES, RIGHT, about_point=vert)
            coord_labels.add(label)
            if z == 0:
                label_2d = OldTex(f"({x}, {y})")
                label_2d.set_height(0.3)
                label_2d.next_to(vert, UR, SMALL_BUFF)
                coord_labels_2d.add(label_2d)

        edge_indices = [
            (0, 1), (0, 2), (1, 3), (2, 3),
            (0, 4), (1, 5), (2, 6), (3, 7),
            (4, 5), (4, 6), (5, 7), (6, 7),
        ]

        # Vertex and edge drawings
        spheres = Group()
        for vert in verts:
            sphere = Sphere(
                radius=0.1,
                resolution=(9, 9),
            )
            sphere.set_gloss(0.3)
            sphere.set_color(GREY)
            sphere.move_to(vert)
            spheres.add(sphere)

        edges = Group()
        for i, j in edge_indices:
            edge = Line3D(
                verts[i], verts[j],
                resolution=(5, 51),
                width=0.04,
                gloss=0.5,
            )
            edge.set_color(GREY_BROWN)
            edges.add(edge)

        # Setup highlight animations
        def highlight(n, spheres=spheres, coord_labels=coord_labels):
            anims = []
            for k, sphere, cl in zip(it.count(), spheres, coord_labels):
                if k == n:
                    sphere.save_state()
                    cl.save_state()
                    sphere.generate_target()
                    cl.generate_target()
                    cl.target.set_fill(YELLOW)
                    sphere.target.set_color(YELLOW)
                    Group(cl.target, sphere.target).scale(1.5, about_point=sphere.get_center())
                    anims += [
                        MoveToTarget(sphere),
                        MoveToTarget(cl),
                    ]
                # CHANGE: get_color() returns a hex string, not a Color
                elif Color(sphere.get_color()) == Color(YELLOW):
                    anims += [
                        Restore(sphere),
                        Restore(cl),
                    ]
            return AnimationGroup(*anims)

        # Setup 2d case
        frame.move_to(1.5 * UP)
        self.add(plane)
        self.play(
            LaggedStartMap(FadeIn, coord_labels_2d),
            LaggedStartMap(GrowFromCenter, spheres[:4]),
            LaggedStartMap(GrowFromCenter, edges[:4]),
        )
        self.wait()

        # Transition to 3d case
        frame.generate_target()
        frame.target.set_euler_angles(-25 * DEGREES, 70 * DEGREES)
        frame.target.move_to([1, 2, 0])
        frame.target.set_height(10)
        to_grow = Group(*edges[4:], *spheres[4:], *coord_labels[4:])
        to_grow.save_state()
        to_grow.set_depth(0, about_edge=IN, stretch=True)

        rf = squish_rate_func(smooth, 0.5, 1)
        self.play(
            MoveToTarget(frame),
            ShowCreation(axes.z_axis),
            Restore(to_grow, rate_func=rf),
            FadeOut(coord_labels_2d, rate_func=rf),
            *[
                FadeInFromPoint(cl, cl2.get_center(), rate_func=squish_rate_func(smooth, 0.5, 1))
                for cl, cl2 in zip(coord_labels[:4], coord_labels_2d)
            ],
            run_time=3
        )

        frame.start_time = self.time
        frame.scene = self
        frame.add_updater(lambda m: m.set_theta(
            -25 * DEGREES * math.cos((m.scene.time - m.start_time) * PI / 60)
        ))

        self.add(axes.z_axis)
        self.add(edges)
        self.add(spheres)

        self.play(
            LaggedStart(*[Indicate(s, color=GREEN) for s in spheres], run_time=2, lag_ratio=0.1),
            LaggedStart(*[Indicate(c, color=GREEN) for c in coord_labels], run_time=2, lag_ratio=0.1),
        )

        # Add chessboard
        board = Chessboard(
            shape=(1, 3), height=1,
            square_resolution=(5, 5),
        )
        board.move_to(plane.c2p(-1, 0), DOWN + IN)
        coins = CoinsOnBoard(board, coin_config={"numeric_labels": True})

        self.play(
            FadeIn(board),
            FadeIn(coins),
            highlight(7)
        )

        # Walk along a few edges
        for ci in [1, 2, 0, 1, 2, 1, 0, 1]:
            coin = coins[ci]
            curr_n = sum([(2**k) * c.is_heads() for k, c in enumerate(coins)])
            coin.flip()
            new_n = sum([(2**k) * c.is_heads() for k, c in enumerate(coins)])
            coin.flip()
            line = Line(verts[curr_n], verts[new_n])
            line.set_stroke(YELLOW, 3)
            self.play(
                FlipCoin(coin),
                highlight(new_n),
                ShowCreationThenDestruction(line)
            )
            self.wait()

        # Color the corners
        self.play(
            highlight(-1),
            edges.set_color, GREY, 0.5,
        )

        colors = [RED, GREEN, BLUE_D]
        title = OldTexText("Strategy", "\\, $\\Leftrightarrow$ \\,", "Coloring")
        title[2].set_submobject_colors_by_gradient(*colors)
        title.set_stroke(BLACK, 5, background=True)
        title.set_height(0.7)
        title.to_edge(UP)
        title.shift(LEFT)
        title.fix_in_frame()

        color_label_templates = [
            OldTex(char, color=color).rotate(PI / 2, RIGHT).match_depth(coord_labels[0])
            for char, color in zip("RGB", colors)
        ]
        coord_labels.color_labels = VGroup(*[VMobject() for cl in coord_labels])

        def get_coloring_animation(ns,
                                   spheres=spheres,
                                   coord_labels=coord_labels,
                                   colors=colors,
                                   color_label_templates=color_label_templates,
                                   ):
            anims = []
            new_color_labels = VGroup()
            for n, sphere, coord_label, old_color_label in zip(ns, spheres, coord_labels, coord_labels.color_labels):
                color = colors[int(n)]
                sphere.generate_target()
                coord_label.generate_target()
                sphere.target.set_color(color)
                coord_label.target.set_fill(color)
                color_label = color_label_templates[n].copy()
                color_label.next_to(coord_label, RIGHT, SMALL_BUFF)
                anims += [
                    MoveToTarget(sphere),
                    MoveToTarget(coord_label),
                    FadeIn(color_label, 0.25 * IN),
                    FadeOut(old_color_label, 0.25 * OUT),
                ]
                new_color_labels.add(color_label)
            coord_labels.color_labels = new_color_labels
            return LaggedStart(*anims, run_time=2)

        self.play(
            FadeIn(title, DOWN),
            get_coloring_animation(np.random.randint(0, 3, 8)),
        )
        self.wait()
        for x in range(4):
            self.play(get_coloring_animation(np.random.randint(0, 3, 8)))
            self.wait()

        # Some specific color examples
        S0 = OldTex("\\text{Key} = 0")
        S0.to_edge(LEFT)
        S0.shift(UP)
        S0.fix_in_frame()
        self.play(
            FadeIn(S0, DOWN),
            get_coloring_animation([0] * 8)
        )
        self.wait(5)

        bit_sum = OldTex("\\text{Key} = \\,&c_0 + c_1")
        bit_sum.scale(0.8)
        bit_sum.to_edge(LEFT)
        bit_sum.shift(UP)
        bit_sum.fix_in_frame()
        self.play(
            FadeIn(bit_sum, DOWN),
            FadeOut(S0, UP),
            get_coloring_animation([sum(coords[:2]) for coords in vert_coords])
        )
        self.wait(6)

        bit_sum_with_coefs = OldTex(
            "\\text{Key} = \\,&(0\\cdot c_0 + 1\\cdot c_1 + 2\\cdot c_2) \\\\ &\\quad \\mod 3"
        )
        bit_sum_with_coefs.scale(0.8)
        bit_sum_with_coefs.move_to(bit_sum, LEFT)
        bit_sum_with_coefs.fix_in_frame()
        self.play(
            FadeIn(bit_sum_with_coefs, DOWN),
            FadeOut(bit_sum, UP),
            get_coloring_animation([np.dot(coords, [0, 1, 2]) % 3 for coords in vert_coords])
        )
        self.wait(4)

        # Focus on (0, 0, 0)
        self.play(
            FlipCoin(coins),
            coord_labels[1:].set_opacity, 0.2,
            coord_labels.color_labels[1:].set_opacity, 0.2,
            spheres[1:].set_opacity, 0.2,
        )
        self.wait(2)

        lines = VGroup()
        for n in [1, 2, 4]:
            line = Line(verts[0], verts[n], buff=0.1)
            line.set_stroke(YELLOW, 3)
            coin = coins[int(np.log2(n))]
            self.play(
                ShowCreationThenDestruction(line),
                spheres[n].set_opacity, 1,
                coord_labels[n].set_opacity, 1,
                coord_labels.color_labels[n].set_opacity, 1,
                FlipCoin(coin)
            )
            line.reverse_points()
            self.add(line, coord_labels)
            self.play(
                FlipCoin(coin),
                ShowCreation(line)
            )
            lines.add(line)
        self.wait(10)

        # Focus on (0, 1, 0)
        self.play(
            FlipCoin(coins[1]),
            Uncreate(lines[1]),
            FadeOut(lines[::2]),
            Group(
                spheres[0], coord_labels[0], coord_labels.color_labels[0],
                spheres[1], coord_labels[1], coord_labels.color_labels[1],
                spheres[4], coord_labels[4], coord_labels.color_labels[4],
            ).set_opacity, 0.2,
        )
        self.wait(3)

        lines = VGroup()
        curr_n = 2
        for n in [1, 2, 4]:
            new_n = n ^ curr_n
            line = Line(verts[curr_n], verts[new_n], buff=0.1)
            line.set_stroke(YELLOW, 3)
            coin = coins[int(np.log2(n))]
            self.play(
                ShowCreationThenDestruction(line),
                spheres[new_n].set_opacity, 1,
                coord_labels[new_n].set_opacity, 1,
                coord_labels.color_labels[new_n].set_opacity, 1,
                FlipCoin(coin)
            )
            line.reverse_points()
            self.add(line, coord_labels)
            self.play(
                FlipCoin(coin),
                ShowCreation(line)
            )
            lines.add(line)
        self.wait(10)
        self.play(
            LaggedStartMap(Uncreate, lines),
            spheres.set_opacity, 1,
            coord_labels.set_opacity, 1,
            coord_labels.color_labels.set_opacity, 1,
            FadeOut(bit_sum_with_coefs),
        )
        self.wait()
        for x in range(8):
            self.play(get_coloring_animation(np.random.randint(0, 3, 8)))
            self.wait()

        # Count all strategies
        count = OldTexText("$3^8$ total strategies")
        count64 = OldTexText("$64^{(2^{64})}$ total strategies")
        for words in count, count64:
            words.to_edge(LEFT, buff=MED_SMALL_BUFF)
            words.shift(UP)
            words.fix_in_frame()

        full_board = Chessboard()
        full_board.set_height(6)
        full_board.next_to(axes.c2p(0, 0, 0), np.array([-1, 1, 1]), buff=0)
        full_board.shift(SMALL_BUFF * UP + LEFT)

        full_coins = CoinsOnBoard(full_board, coin_config={"numeric_labels": True})
        full_coins.flip_by_message("64^ 2^64")

        self.play(FadeIn(count, DOWN))
        self.wait(4)
        self.remove(board, coins)
        frame.clear_updaters()
        frame.generate_target()
        frame.target.set_euler_angles(0, 45 * DEGREES)
        frame.target.shift(2 * UP)
        self.play(
            count.shift, UP,
            count.set_opacity, 0.5,
            ShowIncreasingSubsets(full_board, run_time=4),
            ShowIncreasingSubsets(full_coins, run_time=4),
            FadeIn(count64, DOWN),
            MoveToTarget(frame, run_time=5)
        )

        messages = [
            "Or, use ",
            "Burnside",
            "to count",
            "modulo  ",
            "symmetry",
        ]
        for message in messages:
            bools = string_to_bools(message)
            to_flip = Group()
            for head, coin in zip(bools, full_coins):
                if head ^ coin.is_heads():
                    to_flip.add(coin)
            self.play(
                LaggedStartMap(FlipCoin, to_flip, run_time=1)
            )
            self.wait(0.5)

        frame.generate_target()
        frame.target.shift(2 * DOWN)
        frame.target.set_euler_angles(-15 * DEGREES, 70 * DEGREES)
        self.play(
            MoveToTarget(frame, run_time=3),
            LaggedStartMap(FadeOut, full_board),
            LaggedStartMap(FadeOut, full_coins),
            FadeOut(count),
            FadeOut(count64),
        )
        frame.add_updater(lambda m, dt: m.increment_theta(0.01 * dt))
        self.wait(30)
