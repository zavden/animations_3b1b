# ==============================================================================
# Scene:      AttemptAColoring
# Source:     videos/_2020/chess.py (lines 3012-3490)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AttemptAColoring.py AttemptAColoring -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() returns a hex string, not a Color
# ==============================================================================

from manim_imports_ext import *

def int_to_bit_coords(n, min_dim=3):
    bits = "{0:b}".format(n)
    bits = (min_dim - len(bits)) * '0' + bits
    return np.array(list(map(int, bits)))


class AttemptAColoring(ThreeDScene):
    def construct(self):
        # Setup cube
        short_vert_height = 0.3
        tall_vert_height = 0.4

        vert_coords = np.array(list(map(int_to_bit_coords, range(8))))
        vert_coords = vert_coords - 0.5
        vert_coords = vert_coords * 4
        vert_coords[:, 2] *= 1.25  # Stretch in the z
        cube = Group()
        cube.verts = Group()
        cube.edges = VGroup()
        cube.add(cube.verts, cube.edges)
        for n, coords in enumerate(vert_coords):
            vert = Sphere(resolution=(21, 21))
            vert.set_height(short_vert_height)
            vert.rotate(90 * DEGREES, RIGHT)
            vert.move_to(coords)
            cube.verts.add(vert)
            vert.edges = VGroup()
            for m, coords2 in enumerate(vert_coords):
                if sum(int_to_bit_coords(n ^ m)) == 1:
                    edge = Line(coords, coords2)
                    cube.edges.add(edge)
                    vert.edges.add(edge)
            vert.edges.apply_depth_test()

        cube.edges.set_color(GREY)
        cube.edges.apply_depth_test()

        cube.rotate(30 * DEGREES, DOWN)
        cube.to_edge(RIGHT)
        cube.set_height(4)

        self.play(
            ShowCreation(cube.edges, lag_ratio=0.1),
            LaggedStartMap(FadeInFromLarge, cube.verts, lambda m: (m, 0.2)),
            run_time=2,
        )

        # Setup cube color
        def get_colored_vertices(values, verts=cube.verts):
            color_choices = [RED, GREEN, BLUE_D]
            color_label_choices = ["R", "G", "B"]
            vert_targets = Group()
            labels = VGroup()
            for n, vert in zip(values, verts):
                color = color_choices[n]
                v_target = vert.copy()
                if n == -1:
                    v_target.set_height(short_vert_height)
                    v_target.set_color(GREY)
                    label = VectorizedPoint()
                else:
                    v_target.set_color(color)
                    v_target.set_height(tall_vert_height)
                    label = OldTex(color_label_choices[n])
                    label.set_color(color)
                    label.set_stroke(BLACK, 3, background=True)
                label.next_to(vert, UR, buff=0)
                vert_targets.add(v_target)
                labels.add(label)
            return vert_targets, labels

        new_verts, color_labels = get_colored_vertices(np.arange(0, 8) % 3)
        for vert, label in zip(cube.verts, color_labels):
            vert.label = label

        self.play(
            Transform(cube.verts, new_verts),
            Write(color_labels),
            run_time=2,
        )
        self.wait()

        def get_color_change_animations(values, verts=cube.verts, labels=color_labels, gcv=get_colored_vertices):
            new_verts, new_labels = gcv(values)
            old_labels = labels.copy()
            labels.become(new_labels)
            return [
                Transform(verts, new_verts),
                LaggedStartMap(FadeOut, old_labels, lambda m: (m, 0.5 * UP), lag_ratio=0.03),
                LaggedStartMap(FadeIn, labels, lambda m: (m, 0.5 * DOWN), lag_ratio=0.03),
            ]

        # Prepare a few colorings
        mod3_strategy = [
            np.dot(int_to_bit_coords(n), [0, 1, 2]) % 3
            for n in range(8)
        ]
        sum_bits = [sum(int_to_bit_coords(n)) % 3 for n in range(8)]

        self.play(*get_color_change_animations(sum_bits))
        self.wait()
        self.play(*get_color_change_animations(mod3_strategy))
        self.wait()

        # Pull out vertices with their neighbors
        # first just one, then all of them.
        trees = Group()
        tree_targets = Group()
        for n, vert in enumerate(cube.verts):
            tree = Group()
            tree.root = vert.copy()
            tree.root.origin = tree.root.get_center()
            tree.edges = VGroup()
            tree.leafs = Group()
            tree.labels = Group()
            for mask in [1, 2, 4]:
                leaf = cube.verts[n ^ mask]
                leaf.origin = leaf.get_center()
                label = leaf.label.copy()
                label.original = leaf.label
                tree.edges.add(Line(vert.get_center(), leaf.get_center()))
                tree.leafs.add(leaf.copy())
                tree.labels.add(label)
            tree.edges.apply_depth_test()
            tree.edges.match_style(vert.edges)
            tree.edges.save_state()
            tree.add(tree.root, tree.edges, tree.leafs, tree.labels)
            trees.add(tree)

            tree.generate_target(use_deepcopy=True)
            for edge, leaf, label, y in zip(tree.target.edges, tree.target.leafs, tree.target.labels, [0.4, 0, -0.4]):
                start = vert.get_center()
                end = start + RIGHT + y * UP
                edge.set_points_as_corners([start, end])
                leaf.move_to(edge.get_end())
                label.next_to(leaf, RIGHT, buff=SMALL_BUFF)
                label.scale(0.7)
            tree_targets.add(tree.target)
        tree_targets.arrange_in_grid(4, 2, buff=LARGE_BUFF)
        tree_targets[1::2].shift(0.5 * RIGHT)
        tree_targets.set_height(6)
        tree_targets.center()
        tree_targets.to_corner(DL)

        self.play(
            MoveToTarget(trees[0]),
            run_time=3,
        )
        self.wait()
        self.play(
            LaggedStartMap(
                MoveToTarget, trees[1:],
                lag_ratio=0.3,
            ),
            run_time=6,
        )
        self.add(trees)
        self.wait()

        # Show what we want
        want_rect = SurroundingRectangle(trees, buff=MED_SMALL_BUFF)
        want_rect.set_stroke(WHITE, 1)
        want_label = OldTexText("What we want")
        want_label.next_to(want_rect, UP)

        trees.save_state()
        anims = []
        for tree in trees:
            anims.append(ApplyMethod(tree.root.set_color, GREY))
            colors = [RED, GREEN, BLUE_D]
            letters = ["R", "G", "B"]
            for color, letter, leaf, label in zip(colors, letters, tree.leafs, tree.labels):
                new_label = OldTexText(letter)
                new_label.set_fill(color)
                new_label.replace(label, dim_to_match=1)
                old_label = label.copy()
                label.become(new_label)
                anims += [
                    FadeIn(label, 0.1 * LEFT),
                    FadeOut(old_label, 0.1 * RIGHT),
                    ApplyMethod(leaf.set_color, color),
                ]

        cube.verts.generate_target()
        cube.verts.save_state()
        cube.verts.target.set_color(GREY)
        for vert in cube.verts.target:
            vert.scale(0.75)
        self.play(
            ShowCreation(want_rect),
            Write(want_label),
            LaggedStart(*anims, lag_ratio=0.001, run_time=3),
            FadeOut(color_labels),
            MoveToTarget(cube.verts),
        )
        self.add(trees)
        self.wait()

        # Try to fit these back onto the cube
        # First attempt
        def restore_tree(tree, **kwargs):
            anims = []
            for mob in [tree.root, *tree.leafs]:
                anims.append(ApplyMethod(mob.move_to, mob.origin))
            for label in tree.labels:
                label.generate_target()
                label.target.replace(label.original, dim_to_match=1)
                anims.append(MoveToTarget(label))
            anims.append(Restore(tree.edges))
            return AnimationGroup(*anims, **kwargs)

        tree_copies = trees.deepcopy()
        self.play(restore_tree(tree_copies[0], run_time=2))
        self.wait()
        self.play(restore_tree(tree_copies[1], run_time=2))
        self.wait()

        frame = self.camera.frame
        self.play(
            UpdateFromAlphaFunc(
                frame,
                lambda m, a: m.move_to(0.1 * wiggle(a, 6) * RIGHT),
            ),
            FadeOut(tree_copies[0]),
            FadeOut(tree_copies[1]),
        )

        # Second attempt
        def restore_vertex(n, verts=cube.verts, labels=color_labels):
            return AnimationGroup(
                Transform(verts[n], verts.saved_state[n]),
                FadeIn(labels[n], DOWN)
            )

        for i in [0, 4, 2, 1]:
            self.play(restore_vertex(i))
        self.wait()
        self.play(ShowCreationThenFadeAround(cube.verts[4]))
        for i in [6, 5]:
            self.play(restore_vertex(i))
        self.wait()

        q_marks = VGroup(*[Tex("???") for x in range(2)])
        q_marks[0].next_to(cube.verts[7], UP, SMALL_BUFF)
        q_marks[1].next_to(cube.verts[3], UP, SMALL_BUFF)
        self.play(Write(q_marks))
        self.wait()

        # Mention it'll never work
        nv_label = OldTexText("It'll never work!")
        nv_label.set_height(0.5)
        nv_label.next_to(cube, UP, buff=0.75)

        cube_copy = cube.deepcopy()
        self.remove(cube)
        self.add(cube_copy)
        new_verts, new_labels = get_colored_vertices([-1] * 8)
        self.play(
            Transform(cube_copy.verts, new_verts),
            FadeOut(q_marks),
            FadeOut(color_labels[:3]),
            FadeOut(color_labels[4:7]),
        )
        self.add(cube_copy)
        self.play(FadeIn(nv_label, DOWN))
        for vert in cube_copy.verts:
            vert.generate_target()
            vert.target.scale(0.01)
            vert.target.set_opacity(0)
        self.play(
            LaggedStartMap(Uncreate, cube_copy.edges),
            LaggedStartMap(MoveToTarget, cube_copy.verts),
        )

        # Highlight symmetry
        rects = VGroup()
        for tree in trees:
            t_rect = SurroundingRectangle(
                Group(tree.leafs, tree.labels),
                buff=SMALL_BUFF
            )
            t_rect.set_stroke(YELLOW, 2)
            rects.add(t_rect)

        self.play(LaggedStartMap(ShowCreationThenFadeOut, rects, lag_ratio=0.025, run_time=3))
        self.wait()

        # Show implication
        implies = OldTex("\\Rightarrow")
        implies.set_height(0.7)
        implies.next_to(want_rect, RIGHT)
        number_labels = VGroup(*[
            OldTexText("Number of ", f"{color} vertices")
            for color in ["red", "green", "blue"]
        ])
        for color, label in zip(colors, number_labels):
            label[1].set_color(color)
        number_labels.set_height(0.5)
        number_labels.arrange(DOWN, buff=1.5, aligned_edge=LEFT)
        number_labels.next_to(implies, RIGHT, MED_LARGE_BUFF)

        vert_eqs = VGroup(*[Tex("=") for x in range(2)])
        vert_eqs.scale(1.5)
        vert_eqs.rotate(90 * DEGREES)
        vert_eqs[0].move_to(number_labels[0:2])
        vert_eqs[1].move_to(number_labels[1:3])

        rhss = VGroup()
        for label in number_labels:
            rhs = OldTex("= \\frac{8}{3}")
            rhs.scale(1.25)
            rhs.next_to(label, RIGHT)
            rhss.add(rhs)

        self.play(
            Write(implies),
            FadeOut(nv_label),
        )
        self.play(
            GrowFromCenter(vert_eqs),
            FadeIn(number_labels[0], DOWN),
            FadeIn(number_labels[1]),
            FadeIn(number_labels[2], UP),
        )
        self.wait()
        self.play(Write(rhss))
        self.wait(2)
        self.play(
            LaggedStartMap(
                FadeOut, VGroup(*number_labels, *vert_eqs, *rhss, *implies),
            ),
            ShowCreation(cube.edges, lag_ratio=0.1),
            LaggedStartMap(FadeInFromLarge, cube.verts, lambda m: (m, 0.2)),
        )
        self.add(cube)
        new_verts, color_labels = get_colored_vertices(mod3_strategy)
        true_trees = trees.saved_state
        self.play(
            Transform(cube.verts, new_verts),
            FadeIn(color_labels),
            FadeOut(trees),
            FadeOut(want_label)
        )
        self.play(FadeIn(true_trees))
        self.wait()

        # Count colors
        for edge in cube.edges:
            edge.insert_n_curves(10)

        red_total = Integer(height=0.6)
        red_total.next_to(want_rect, UP)
        red_total.set_color(RED)
        self.play(FadeIn(red_total))

        all_label_rects = VGroup()
        for n in range(8):
            tree = true_trees[n]
            vert = cube.verts[n]
            neighbor_highlights = VGroup()
            new_edges = VGroup()
            label_rects = VGroup()
            for mask, label in zip([1, 2, 4], tree.labels):
                neighbor = cube.verts[n ^ mask]
                edge = Line(vert, neighbor, buff=0)
                edge.set_stroke(YELLOW, 5)
                edge.insert_n_curves(10)
                new_edges.add(edge)
                # CHANGE: get_color() returns a hex string, not a Color
                if Color(neighbor.get_color()) == Color(RED):
                    circ = Circle()
                    circ.set_stroke(YELLOW, 3)
                    circ.replace(neighbor)
                    neighbor_highlights.add(circ)
                    rect = SurroundingRectangle(label, buff=0.025)
                    rect.set_stroke(YELLOW, 2)
                    label_rects.add(rect)
            new_edges.apply_depth_test()
            new_edges.shift(0.01 * OUT)
            new_tree_edges = tree.edges.copy()
            new_tree_edges.set_stroke(YELLOW, 3)
            new_tree_edges.shift(0.01 * OUT)

            self.play(
                *map(ShowCreation, [*new_edges, *new_tree_edges]),
            )
            for highlight, rect in zip(neighbor_highlights, label_rects):
                self.play(
                    FadeInFromLarge(highlight, 1.2),
                    FadeInFromLarge(rect, 1.2),
                    run_time=0.25
                )
                red_total.increment_value()
                self.wait(0.25)

            self.play(
                FadeOut(neighbor_highlights),
                FadeOut(new_edges),
                FadeOut(new_tree_edges),
            )
            all_label_rects.add(*label_rects)
        self.wait()

        # Show count to 8
        new_verts = get_colored_vertices([-1] * 8)[0]
        self.play(
            FadeOut(true_trees),
            FadeOut(all_label_rects),
            FadeOut(red_total),
            FadeOut(color_labels),
            Transform(cube.verts, new_verts),
        )
        self.play(FadeIn(trees))
        label_rects = VGroup()
        for tree in trees:
            rect = SurroundingRectangle(tree.labels[0], buff=0.025)
            rect.match_style(all_label_rects[0])
            label_rects.add(rect)

        self.play(
            ShowIncreasingSubsets(label_rects, rate_func=linear),
            UpdateFromFunc(
                red_total, lambda m, lr=label_rects: m.set_value(len(lr))
            )
        )
        self.wait()

        # Show red corners
        r_verts = Group(cube.verts[3], cube.verts[4]).copy()
        r_labels = VGroup()
        r_edge_groups = VGroup()
        for r_vert in r_verts:
            r_label = OldTex("R")
            r_label.set_color(RED)
            r_label.next_to(r_vert, UR, buff=0)
            r_labels.add(r_label)
            r_vert.set_height(tall_vert_height)
            r_vert.set_color(RED)
            edges = VGroup()
            for edge in r_vert.edges:
                to_r_edge = edge.copy()
                to_r_edge.reverse_points()
                to_r_edge.set_stroke(YELLOW, 3)
                to_r_edge.shift(0.01 * OUT)
                edges.add(to_r_edge)
            edges.apply_depth_test()
            r_edge_groups.add(edges)

        self.play(
            LaggedStartMap(FadeInFromLarge, r_verts),
            LaggedStartMap(FadeInFromLarge, r_labels),
            run_time=1,
        )
        self.wait()
        for edges in r_edge_groups:
            self.play(ShowCreationThenDestruction(edges, lag_ratio=0.1))
        self.wait()

        rhs = OldTex("=", "3", "\\, (\\text{\\# Red corners})")
        rhs[2].set_color(RED)
        rhs.match_height(red_total)
        rhs[:2].match_height(red_total, about_edge=RIGHT)
        rhs.next_to(red_total, RIGHT)

        self.play(Write(rhs))
        self.wait()

        three = rhs[1]
        three.generate_target()
        three.target.move_to(red_total, RIGHT)
        over = OldTex("/")
        over.match_height(three)
        over.next_to(three.target, LEFT, MED_SMALL_BUFF)
        self.play(
            MoveToTarget(three, path_arc=90 * DEGREES),
            red_total.next_to, over, LEFT, MED_SMALL_BUFF,
            FadeIn(over, UR),
            rhs[2].move_to, three, LEFT,
        )
        self.wait()

        np_label = OldTexText("Not possible!")
        np_label.set_height(0.6)
        np_label.next_to(rhs, RIGHT, LARGE_BUFF)
        self.play(Write(np_label))
        self.wait()
