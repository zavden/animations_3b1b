# ==============================================================================
# Scene:      IntroduceHypercube
# Source:     videos/_2020/chess.py (lines 4026-4156)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceHypercube.py IntroduceHypercube -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() now returns a hex string, not a Color object
# ==============================================================================

from manim_imports_ext import *

def boolian_linear_combo(bools):
    return reduce(op.xor, [b * n for n, b in enumerate(bools)], 0)


def int_to_bit_coords(n, min_dim=3):
    bits = "{0:b}".format(n)
    bits = (min_dim - len(bits)) * '0' + bits
    return np.array(list(map(int, bits)))


def get_vertex_sphere(height=0.4, color=GREY, resolution=(21, 21)):
    sphere = Sphere(resolution=resolution)
    sphere.set_height(height)
    sphere.set_color(color)
    return sphere


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


class IntroduceHypercube(FourDCubeColoringFromTrees):
    def construct(self):
        # Camera stuffs
        frame = self.camera.frame
        light = self.camera.light_source
        light.move_to([-25, -20, 20])

        # Setup cubes
        cubes = [
            self.get_hypercube(dim=d)
            for d in range(5)
        ]

        def reconnect_edges(cube):
            for vert in cube.verts:
                for edge, neighbor in zip(vert.edges, vert.neighbors):
                    edge.become(Line3D(
                        vert.get_center(),
                        neighbor.get_center(),
                        resolution=edge.resolution
                    ))

        # Show increasing dimensions
        label = VGroup(Integer(0), OldTex("D"))
        label.arrange(RIGHT, buff=SMALL_BUFF)
        label.scale(1.5)
        label.to_edge(UP)
        label.fix_in_frame()

        def get_cube_intro_anim(n, cubes=cubes, reconnect_edges=reconnect_edges, label=label):
            if n == 0:
                return GrowFromCenter(cubes[n])
            self.remove(cubes[n - 1])
            cubes[n].save_state()
            for v1, v2 in zip(cubes[n].verts, it.cycle(cubes[n - 1].verts)):
                v1.move_to(v2)
            reconnect_edges(cubes[n])
            if n == 1:
                cubes[n].edges.scale(0)
            return AnimationGroup(
                Restore(cubes[n]),
                ChangeDecimalToValue(label[0], n),
            )

        self.play(
            FadeIn(label, DOWN),
            get_cube_intro_anim(0)
        )
        self.wait()
        for n in [1, 2]:
            self.play(get_cube_intro_anim(n))
            self.wait()
        self.play(
            get_cube_intro_anim(3),
            ApplyMethod(
                frame.set_euler_angles, -20 * DEGREES, 75 * DEGREES,
                run_time=3
            )
        )
        frame.add_updater(lambda m, dt: m.increment_theta(dt * DEGREES))
        self.wait(4)

        # Flatten cube
        flat_cube = self.get_hypercube(3)
        for n, vert in enumerate(flat_cube.verts):
            point = vert.get_center()
            if n < 4:
                point *= 1.5
            else:
                point *= 0.75
            point[2] = 0
            vert.move_to(point)
        reconnect_edges(flat_cube)

        plane = NumberPlane(x_range=(-10, 10), y_range=(-10, 10), faded_line_ratio=0)
        plane.set_opacity(0.25)
        plane.apply_depth_test()
        plane.axes.shift(0.01 * OUT)
        plane.shift(0.02 * IN)

        cubes[3].save_state()
        self.add(cubes[3], plane)
        self.play(
            FadeIn(plane, run_time=2),
            Transform(cubes[3], flat_cube, run_time=2),
        )
        self.wait(7)
        self.play(
            Restore(cubes[3], run_time=2),
            FadeOut(plane)
        )
        self.play(get_cube_intro_anim(4), run_time=3)
        self.wait(10)

        # Highlight some neighbor groups
        colors = [RED, GREEN, BLUE_D, YELLOW]
        for x in range(6):
            vert = random.choice(cubes[4].verts)
            neighbors = vert.neighbors.copy()
            neighbors.save_state()
            neighbors.generate_target()
            new_edges = VGroup()
            for neighbor, color in zip(neighbors.target, colors):
                neighbor.set_color(color)
                edge = Line(
                    vert.get_center(),
                    neighbor.get_center(),
                    buff=vert.get_height() / 2,
                )
                edge.set_stroke(color, 5)
                new_edges.add(edge)
            self.remove(vert.neighbors)
            self.play(
                ShowCreation(new_edges, lag_ratio=0.2),
                MoveToTarget(neighbors),
            )
            self.wait(1)
            self.play(
                FadeOut(new_edges),
                Restore(neighbors),
            )
            self.remove(neighbors)
            self.add(vert.neighbors)

        # Show valid coloring
        cubes[4].generate_target()
        for n, vert in enumerate(cubes[4].target[0]):
            code = boolian_linear_combo(int_to_bit_coords(n, 4))
            vert.set_color(colors[code])
        self.play(MoveToTarget(cubes[4], lag_ratio=0.2, run_time=3))
        self.wait(15)
