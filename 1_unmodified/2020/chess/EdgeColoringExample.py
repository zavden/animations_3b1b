# ==============================================================================
# Scene:      EdgeColoringExample
# Source:     videos/_2020/chess.py (lines 2889-2936)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EdgeColoringExample.py EdgeColoringExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EdgeColoringExample(Scene):
    def construct(self):
        words = VGroup(
            OldTexText(
                "Color edges\\\\red or blue",
                tex_to_color_map={"red": RED, "blue": BLUE}
            ),
            OldTexText("Prove there is a\\\\monochromatic triangle", alignment=""),
        )
        words.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        words.to_edge(RIGHT)
        words.to_edge(UP, buff=LARGE_BUFF)

        def get_graph(words=words):
            points = compass_directions(6)
            points *= 3
            verts = VGroup(*[Dot(p, radius=0.1) for p in points])
            verts.set_fill(GREY_B, 1)
            edges = VGroup(*[
                Line(p1, p2, color=random.choice([RED, BLUE]))
                for p1, p2 in it.combinations(points, 2)
            ])
            graph = VGroup(verts, edges)
            graph.set_height(6)
            graph.next_to(words, LEFT, LARGE_BUFF)
            graph.set_y(0)
            graph.set_stroke(background=True)
            return graph

        graph = get_graph()

        self.add(words)
        self.add(graph)
        self.wait()
        for x in range(2):
            new_graph = get_graph()
            self.play(
                ShowCreation(
                    new_graph, lag_ratio=0.1,
                    run_time=3,
                ),
                ApplyMethod(
                    graph[1].set_stroke, None, 0,
                    run_time=2,
                )
            )
            graph = new_graph
        self.wait(4)
