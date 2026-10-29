# ==============================================================================
# Scene:      FiveRegionsFourEdgesEachGraph
# Source:     videos/_2017/mug.py (lines 1496-1741)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FiveRegionsFourEdgesEachGraph.py FiveRegionsFourEdgesEachGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FiveRegionsFourEdgesEachGraph(Scene):
    CONFIG = {
        "v_color" : WHITE,
        "e_color" : YELLOW,
        "f_colors" : (BLUE, RED_E, BLUE_E),
        "n_edge_double_count_examples" : 6,
        "random_seed" : 1,
    }
    def construct(self):
        self.draw_squares()
        self.transition_to_graph()
        self.count_edges_per_region()
        self.each_edges_has_two_regions()
        self.ten_total_edges()

    def draw_squares(self):
        words = VGroup(
            OldTexText("5", "regions"),
            OldTexText("4", "edges each"),
        )
        words.arrange(DOWN)
        words.to_edge(UP)
        words[0][0].set_color(self.f_colors[0])
        words[1][0].set_color(self.e_color)

        squares = VGroup(*[Square() for x in range(5)])
        squares.scale(0.5)
        squares.set_stroke(width = 0)
        squares.set_fill(opacity = 1)
        squares.set_color_by_gradient(*self.f_colors)
        squares.arrange(RIGHT, buff = MED_LARGE_BUFF)
        squares.next_to(words, DOWN, LARGE_BUFF)
        all_edges = VGroup()
        all_vertices = VGroup()
        for square in squares:
            corners = square.get_anchors()[:4]
            square.edges = VGroup(*[
                Line(c1, c2, color = self.e_color)
                for c1, c2 in adjacent_pairs(corners)
            ])
            square.vertices = VGroup(*[
                Dot(color = self.v_color).move_to(c)
                for c in corners
            ])
            all_edges.add(*square.edges)
            all_vertices.add(*square.vertices)

        self.play(
            FadeIn(words[0]),
            LaggedStartMap(FadeIn, squares, run_time = 1.5)
        )
        self.play(
            FadeIn(words[1]),
            LaggedStartMap(ShowCreation, all_edges),
            LaggedStartMap(GrowFromCenter, all_vertices),
        )
        self.wait()

        self.add_foreground_mobjects(words)
        self.set_variables_as_attrs(words, squares)

    def transition_to_graph(self):
        squares = self.squares
        words = self.words

        points = np.array([
            UP+LEFT,
            UP+RIGHT,
            DOWN+RIGHT,
            DOWN+LEFT,
            3*(UP+RIGHT),
            3*(DOWN+LEFT),
            3*(DOWN+RIGHT),
        ])
        points *= 0.75

        regions = VGroup(*[
            Square().set_points_as_corners(points[indices])
            for indices in [
                [0, 1, 2, 3],
                [0, 4, 2, 1],
                [5, 0, 3, 2],
                [5, 2, 4, 6],
                [6, 4, 0, 5],
            ]
        ])
        regions.set_stroke(width = 0)
        regions.set_fill(opacity = 1)
        regions.set_color_by_gradient(*self.f_colors)

        all_edges = VGroup()
        all_movers = VGroup()
        for region, square in zip(regions, squares):
            corners = region.get_anchors()[:4]
            region.edges = VGroup(*[
                Line(c1, c2, color = self.e_color)
                for c1, c2 in adjacent_pairs(corners)
            ])
            all_edges.add(*region.edges)
            region.vertices = VGroup(*[
                Dot(color = self.v_color).move_to(c)
                for c in corners
            ])
            mover = VGroup(
                square, square.edges, square.vertices,
            )
            mover.target = VGroup(
                region, region.edges, region.vertices
            )
            all_movers.add(mover)

        back_region = FullScreenFadeRectangle()
        back_region.set_fill(regions[-1].get_color(), 0.5)
        regions[-1].set_fill(opacity = 0)
        back_region.add(regions[-1].copy().set_fill(BLACK, 1))
        back_region.edges = regions[-1].edges

        self.play(
            FadeIn(
                back_region,
                rate_func = squish_rate_func(smooth, 0.7, 1),
                run_time = 3,
            ),
            LaggedStartMap(
                MoveToTarget, all_movers,
                run_time = 3,
                replace_mobject_with_target_in_scene = True,
            ),
        )
        self.wait(2)

        self.set_variables_as_attrs(
            regions, all_edges, back_region,
            graph = VGroup(*[m.target for m in all_movers])
        )

    def count_edges_per_region(self):
        all_edges = self.all_edges
        back_region = self.back_region
        regions = self.regions
        graph = self.graph
        all_vertices = VGroup(*[r.vertices for r in regions])

        ghost_edges = all_edges.copy()
        ghost_edges.set_stroke(GREY_B, 1)

        count = Integer(0)
        count.scale(2)
        count.next_to(graph, RIGHT, buff = 2)
        count.set_fill(YELLOW, opacity = 0)

        last_region = VGroup(back_region, *regions[1:])
        last_region.add(all_edges)

        for region in list(regions[:-1]) + [back_region]:
            self.play(
                FadeIn(region),
                Animation(ghost_edges),
                FadeOut(last_region),
                Animation(count),
                Animation(all_vertices),
            )
            for edge in region.edges:
                new_count = Integer(count.number + 1)
                new_count.replace(count, dim_to_match = 1)
                new_count.set_color(count.get_color())
                self.play(
                    ShowCreation(edge),
                    FadeOut(count),
                    FadeIn(new_count),
                    run_time = 0.5
                )
                count = new_count
            last_region = VGroup(region, region.edges)
        self.wait()
        self.add_foreground_mobjects(count)
        self.play(
            FadeOut(last_region),
            Animation(ghost_edges),
            Animation(all_vertices),
        )

        self.set_variables_as_attrs(count, ghost_edges, all_vertices)

    def each_edges_has_two_regions(self):
        regions = list(self.regions[:-1]) + [self.back_region]
        back_region = self.back_region
        self.add_foreground_mobjects(self.ghost_edges, self.all_vertices)

        edge_region_pair_groups = []
        for r1, r2 in it.combinations(regions, 2):
            for e1 in r1.edges:
                for e2 in r2.edges:
                    diff = e1.get_center()-e2.get_center()
                    if get_norm(diff) < 0.01:
                        edge_region_pair_groups.append(VGroup(
                            e1, r1, r2
                        ))

        for x in range(self.n_edge_double_count_examples):
            edge, r1, r2 = random.choice(edge_region_pair_groups)
            if r2 is back_region:
                #Flip again, maybe you're still unlucky, maybe not
                edge, r1, r2 = random.choice(edge_region_pair_groups)
            self.play(ShowCreation(edge))
            self.add_foreground_mobjects(edge)
            self.play(FadeIn(r1), run_time = 0.5)
            self.play(FadeIn(r2), Animation(r1), run_time = 0.5)
            self.wait(0.5)
            self.play(*list(map(FadeOut, [r2, r1, edge])), run_time = 0.5)
            self.remove_foreground_mobjects(edge)

    def ten_total_edges(self):
        double_count = self.count
        brace = Brace(double_count, UP)
        words = brace.get_text("Double-counts \\\\ edges")
        regions = self.regions

        edges = VGroup(*it.chain(
            regions[0].edges,
            regions[-1].edges,
            [regions[1].edges[1]],
            [regions[2].edges[3]],
        ))

        count = Integer(0)
        count.scale(2)
        count.set_fill(WHITE, 0)
        count.next_to(self.graph, LEFT, LARGE_BUFF)

        self.play(
            GrowFromCenter(brace),
            Write(words)
        )
        self.wait()
        for edge in edges:
            new_count = Integer(count.number + 1)
            new_count.replace(count, dim_to_match = 1)
            self.play(
                ShowCreation(edge),
                FadeOut(count),
                FadeIn(new_count),
                run_time = 0.5
            )
            count = new_count
        self.wait()
